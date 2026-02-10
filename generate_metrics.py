#!/usr/bin/env python3
"""
Auto-generate metrics.tex from live git and GitHub data.

Queries all ecosystem repos and GitHub API to produce LaTeX \newcommand
definitions. The paper uses \\input{metrics.tex} and these commands instead
of hardcoded numbers, ensuring every build has fresh data.

Standards: NIST SP 800-53 CM-3 (configuration change control)
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).parent

# ============================================================================
# Repository definitions (must match generate_charts.py)
# ============================================================================
MEASURED_REPOS = {
    'WhitePaper':             '/Users/brucedombrowski/WhitePaper',
    'SendCUIEmail':           '/Users/brucedombrowski/Git/SendCUIEmail',
    'Decisions':              '/Users/brucedombrowski/LaTeX',
    'Security Toolkit':       '/Users/brucedombrowski/Security',
    'Scrum':                  '/Users/brucedombrowski/Scrum',
    'ai-agents':              '/Users/brucedombrowski/ai-agents',
    'systems-engineering':    '/Users/brucedombrowski/systems-engineering',
}

EXTRA_REPOS = {
    'Hardware':               '/Users/brucedombrowski/Git/Hardware',
    'WeddingWebsite':         '/Users/brucedombrowski/Git/WeddingWebsite',
    'OpenSourceHouseProject': '/Users/brucedombrowski/OpenSourceHouseProject',
    'PdfSigner':              '/Users/brucedombrowski/PdfSigner',
    'SpeakUp':                '/Users/brucedombrowski/SpeakUp',
    'screen2cam':             '/Users/brucedombrowski/screen2cam',
    'claude-dangerously':     '/Users/brucedombrowski/claude-dangerously',
    'privacy':                '/Users/brucedombrowski/privacy',
    'MusicProduction':        '/Users/brucedombrowski/MusicProduction',
    'homebrew-tap':           '/Users/brucedombrowski/Security/homebrew-tap',
}

ALL_REPOS = {**MEASURED_REPOS, **EXTRA_REPOS}

# Binary extensions to exclude from LOC count
BINARY_EXTS = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mp3', '.wav',
               '.pptx', '.xlsx', '.docx', '.zip', '.tar', '.gz', '.ico', '.svg',
               '.woff', '.woff2', '.ttf', '.eot', '.pyc', '.o', '.a', '.so',
               '.dylib', '.exe', '.dll', '.bin', '.dat', '.db', '.sqlite',
               '.class', '.jar'}

# GitHub repos for issue counting (owner/repo format)
GITHUB_REPOS = {
    'WhitePaper':        'brucedombrowski/WhitePaper',
    'SendCUIEmail':      'brucedombrowski/SendCUIEmail',
    'Security Toolkit':  'brucedombrowski/security-toolkit',
    'ai-agents':         'brucedombrowski/ai-agents',
    'Scrum':             'brucedombrowski/Scrum',
}


def get_commits(repo_path):
    """Count commits in a repo."""
    r = subprocess.run(['git', '-C', repo_path, 'rev-list', '--all', '--count'],
                       capture_output=True, text=True)
    return int(r.stdout.strip()) if r.returncode == 0 else 0


def get_tags(repo_path):
    """Count tags in a repo."""
    r = subprocess.run(['git', '-C', repo_path, 'tag', '-l'],
                       capture_output=True, text=True)
    return len(r.stdout.strip().split('\n')) if r.stdout.strip() else 0


def get_loc(repo_path):
    """Count lines of code, excluding binary files."""
    r = subprocess.run(['git', '-C', repo_path, 'ls-files'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return 0
    files = [f for f in r.stdout.strip().split('\n')
             if f and not any(f.lower().endswith(ext) for ext in BINARY_EXTS)]
    if not files:
        return 0
    abs_files = [f'{repo_path}/{f}' for f in files]
    wc = subprocess.run(['wc', '-l'] + abs_files, capture_output=True, text=True)
    lines = wc.stdout.strip().split('\n')
    total_line = lines[-1] if len(files) > 1 else lines[0]
    return int(total_line.strip().split()[0])


def get_first_last_commit(repo_path):
    """Get first and last commit dates by sorting all commit timestamps."""
    r = subprocess.run(
        ['git', '-C', repo_path, 'log', '--all', '--pretty=format:%aI'],
        capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return '', ''
    dates = sorted(r.stdout.strip().split('\n'))
    return dates[0], dates[-1]


def get_github_issues(gh_repo):
    """Count total issues via gh CLI."""
    r = subprocess.run(
        ['gh', 'issue', 'list', '--repo', gh_repo, '--state', 'all',
         '--limit', '500', '--json', 'number'],
        capture_output=True, text=True)
    if r.returncode == 0:
        return len(json.loads(r.stdout))
    return 0


def count_sessions():
    """Count sessions from PROCESS.md."""
    process_file = SCRIPT_DIR / 'PROCESS.md'
    if not process_file.exists():
        return 0
    count = 0
    for line in process_file.read_text().split('\n'):
        if line.startswith('## Session '):
            count += 1
    return count


def count_languages():
    """Count unique programming languages across all repos using file extensions."""
    lang_map = {
        '.sh': 'Bash', '.bash': 'Bash',
        '.py': 'Python',
        '.ps1': 'PowerShell', '.psm1': 'PowerShell',
        '.c': 'C', '.h': 'C',
        '.swift': 'Swift',
        '.cs': 'C#',
        '.tex': 'LaTeX', '.bib': 'LaTeX',
        '.js': 'JavaScript', '.jsx': 'JavaScript',
        '.ts': 'TypeScript', '.tsx': 'TypeScript',
        '.html': 'HTML', '.css': 'CSS',
        '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML',
        '.md': 'Markdown',
    }
    # Only count "real" programming languages
    programming_langs = {'Bash', 'Python', 'PowerShell', 'C', 'Swift', 'C#',
                         'LaTeX', 'JavaScript', 'TypeScript'}
    found = set()
    for path in ALL_REPOS.values():
        if not Path(path).exists():
            continue
        r = subprocess.run(['git', '-C', path, 'ls-files'],
                           capture_output=True, text=True)
        for f in r.stdout.strip().split('\n'):
            ext = Path(f).suffix.lower()
            lang = lang_map.get(ext)
            if lang and lang in programming_langs:
                found.add(lang)
    return len(found)


def fmt_number(n):
    """Format number with commas for LaTeX."""
    return f'{n:,}'


def fmt_number_approx(n):
    """Format as approximate (round to nearest thousand)."""
    thousands = (n // 1000) * 1000
    return f'{fmt_number(thousands)}+'


# ============================================================================
# Gather all metrics
# ============================================================================
print('Generating metrics.tex from live data...')

# Per-repo data
repo_data = {}
for name, path in ALL_REPOS.items():
    if not Path(path).exists() or not (Path(path) / '.git').exists():
        continue
    commits = get_commits(path)
    tags = get_tags(path)
    loc = get_loc(path)
    first, last = get_first_last_commit(path)
    repo_data[name] = {
        'commits': commits, 'tags': tags, 'loc': loc,
        'first': first, 'last': last,
        'measured': name in MEASURED_REPOS,
    }
    print(f'  {name:25s} {commits:4d} commits  {loc:>8,} LOC  {tags:3d} tags')

# Totals
total_repos = len(repo_data)
total_commits = sum(d['commits'] for d in repo_data.values())
total_loc = sum(d['loc'] for d in repo_data.values())
total_tags = sum(d['tags'] for d in repo_data.values())
total_langs = count_languages()

# Measured set totals
measured_repos = sum(1 for d in repo_data.values() if d['measured'])
measured_commits = sum(d['commits'] for d in repo_data.values() if d['measured'])
measured_loc = sum(d['loc'] for d in repo_data.values() if d['measured'])
measured_tags = sum(d['tags'] for d in repo_data.values() if d['measured'])

# Security Toolkit specifics
sec = repo_data.get('Security Toolkit', {})
sec_commits = sec.get('commits', 0)
sec_tags = sec.get('tags', 0)
sec_loc = sec.get('loc', 0)

# Calendar days
all_firsts = [d['first'] for d in repo_data.values() if d['first']]
all_lasts = [d['last'] for d in repo_data.values() if d['last']]
if all_firsts and all_lasts:
    first_date = min(datetime.fromisoformat(d) for d in all_firsts)
    last_date = max(datetime.fromisoformat(d) for d in all_lasts)
    calendar_days = (last_date - first_date).days + 1
else:
    calendar_days = 0

daily_rate = round(total_commits / calendar_days, 1) if calendar_days > 0 else 0

# WhitePaper repo specifics
wp = repo_data.get('WhitePaper', {})
wp_commits = wp.get('commits', 0)
wp_tags = wp.get('tags', 0)
wp_sessions = count_sessions()

# GitHub issue counts
print('\nQuerying GitHub issues...')
issue_counts = {}
total_issues = 0
for name, gh_repo in GITHUB_REPOS.items():
    count = get_github_issues(gh_repo)
    issue_counts[name] = count
    total_issues += count
    print(f'  {name:25s} {count:4d} issues')

wp_issues = issue_counts.get('WhitePaper', 0)
sec_issues = issue_counts.get('Security Toolkit', 0)

# ============================================================================
# Generate metrics.tex
# ============================================================================
print(f'\nWriting metrics.tex...')

lines = [
    '% AUTO-GENERATED — do not edit manually.',
    f'% Generated by generate_metrics.py on {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}',
    f'% Source: {total_repos} git repos, {len(GITHUB_REPOS)} GitHub repos queried',
    '%',
    '% Ecosystem totals',
    f'\\newcommand{{\\totalrepos}}{{{fmt_number(total_repos)}}}',
    f'\\newcommand{{\\totalcommits}}{{{fmt_number(total_commits)}}}',
    f'\\newcommand{{\\totalloc}}{{{fmt_number_approx(total_loc)}}}',
    f'\\newcommand{{\\totaltags}}{{{fmt_number(total_tags)}}}',
    f'\\newcommand{{\\totallangs}}{{{total_langs}}}',
    f'\\newcommand{{\\calendardays}}{{{calendar_days}}}',
    f'\\newcommand{{\\dailyrate}}{{{daily_rate}}}',
    f'\\newcommand{{\\totalissues}}{{{fmt_number(total_issues)}}}',
    '%',
    '% Measured set (7 core repos)',
    f'\\newcommand{{\\measuredrepos}}{{{measured_repos}}}',
    f'\\newcommand{{\\measuredcommits}}{{{fmt_number(measured_commits)}}}',
    f'\\newcommand{{\\measuredloc}}{{{fmt_number(measured_loc)}}}',
    f'\\newcommand{{\\measuredtags}}{{{fmt_number(measured_tags)}}}',
    '%',
    '% Security Toolkit',
    f'\\newcommand{{\\seccommits}}{{{fmt_number(sec_commits)}}}',
    f'\\newcommand{{\\sectags}}{{{sec_tags}}}',
    f'\\newcommand{{\\secloc}}{{{fmt_number(sec_loc)}}}',
    f'\\newcommand{{\\secissues}}{{{fmt_number(sec_issues)}}}',
    '%',
    '% WhitePaper repo',
    f'\\newcommand{{\\wpcommits}}{{{wp_commits}}}',
    f'\\newcommand{{\\wptags}}{{{wp_tags}}}',
    f'\\newcommand{{\\wpissues}}{{{wp_issues}}}',
    f'\\newcommand{{\\wpsessions}}{{{wp_sessions}}}',
]

metrics_path = SCRIPT_DIR / 'metrics.tex'
metrics_path.write_text('\n'.join(lines) + '\n')
print(f'  Saved: {metrics_path}')

# Summary
print(f'\n=== Metrics Summary ===')
print(f'  Ecosystem: {total_repos} repos, {total_commits} commits, {total_loc:,} LOC, {total_tags} tags')
print(f'  Measured:  {measured_repos} repos, {measured_commits} commits, {measured_loc:,} LOC, {measured_tags} tags')
print(f'  Security:  {sec_commits} commits, {sec_loc:,} LOC, {sec_tags} tags, {sec_issues} issues')
print(f'  WhitePaper: {wp_commits} commits, {wp_tags} tags, {wp_issues} issues, {wp_sessions} sessions')
print(f'  Period:    {calendar_days} days, {daily_rate} commits/day')
print(f'  Issues:    {total_issues} total across {len(GITHUB_REPOS)} repos')
