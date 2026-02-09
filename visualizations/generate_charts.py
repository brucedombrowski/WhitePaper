#!/usr/bin/env python3
"""
Git Visualization Charts for WhitePaper
Generates publication-quality figures from git data across all repos.

Tools: matplotlib, pandas, SciencePlots, matplot2tikz
Standards: NIST SP 800-53 CM-3 (traceability through version control)
"""

import subprocess
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone
from pathlib import Path
import json

# Try SciencePlots for publication-quality styling
try:
    import scienceplots
    plt.style.use(['science', 'ieee', 'no-latex'])
except Exception:
    plt.style.use('seaborn-v0_8-paper')

# Try matplot2tikz for LaTeX export
try:
    import matplot2tikz
    HAS_TIKZ = True
except Exception:
    HAS_TIKZ = False

OUTPUT_DIR = Path(__file__).parent
REPOS = {
    'WhitePaper': '/Users/brucedombrowski/WhitePaper',
    'SendCUIEmail': '/Users/brucedombrowski/Git/SendCUIEmail',
    'Decisions': '/Users/brucedombrowski/LaTeX/Decisions',
    'Security Toolkit': '/Users/brucedombrowski/Security',
}

# Also check for newer repos
EXTRA_REPOS = {
    'Scrum': '/Users/brucedombrowski/Scrum',
    'ai-agents': '/tmp/ai-agents',
    'systems-engineering': '/tmp/systems-engineering',
}
for name, path in EXTRA_REPOS.items():
    if Path(path).exists() and (Path(path) / '.git').exists():
        REPOS[name] = path


def extract_git_log(repo_path, repo_name):
    """Extract commit data from a git repo."""
    cmd = [
        'git', '-C', repo_path, 'log', '--all',
        '--pretty=format:%H|%aI|%an|%s',
        '--no-merges'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    rows = []
    for line in result.stdout.strip().split('\n'):
        if '|' in line:
            parts = line.split('|', 3)
            if len(parts) == 4:
                rows.append({
                    'hash': parts[0],
                    'datetime': parts[1],
                    'author': parts[2],
                    'message': parts[3],
                    'repo': repo_name
                })
    return rows


def extract_file_changes(repo_path, repo_name):
    """Extract per-commit file change stats."""
    cmd = [
        'git', '-C', repo_path, 'log', '--all',
        '--pretty=format:%H|%aI',
        '--numstat', '--no-merges'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    rows = []
    current_hash = None
    current_date = None
    for line in result.stdout.strip().split('\n'):
        if '|' in line and len(line.split('|')) == 2:
            parts = line.split('|')
            current_hash = parts[0]
            current_date = parts[1]
        elif line.strip() and current_hash and '\t' in line:
            parts = line.split('\t')
            if len(parts) == 3:
                try:
                    added = int(parts[0]) if parts[0] != '-' else 0
                    deleted = int(parts[1]) if parts[1] != '-' else 0
                    rows.append({
                        'hash': current_hash,
                        'datetime': current_date,
                        'additions': added,
                        'deletions': deleted,
                        'file': parts[2],
                        'repo': repo_name
                    })
                except ValueError:
                    pass
    return rows


def save_figure(fig, name):
    """Save figure as PNG and optionally as TikZ."""
    png_path = OUTPUT_DIR / f'{name}.png'
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f'  Saved: {png_path}')

    pdf_path = OUTPUT_DIR / f'{name}.pdf'
    fig.savefig(pdf_path, bbox_inches='tight', facecolor='white')
    print(f'  Saved: {pdf_path}')

    if HAS_TIKZ:
        try:
            tikz_path = OUTPUT_DIR / f'{name}.tex'
            matplot2tikz.save(str(tikz_path))
            print(f'  Saved: {tikz_path}')
        except Exception as e:
            print(f'  TikZ export skipped: {e}')


# ============================================================================
# Extract data from all repos
# ============================================================================
print('Extracting git data...')
all_commits = []
all_changes = []
for name, path in REPOS.items():
    commits = extract_git_log(path, name)
    changes = extract_file_changes(path, name)
    all_commits.extend(commits)
    all_changes.extend(changes)
    print(f'  {name}: {len(commits)} commits, {len(changes)} file changes')

df = pd.DataFrame(all_commits)
df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
df['date'] = df['datetime'].dt.date

df_changes = pd.DataFrame(all_changes) if all_changes else pd.DataFrame()
if not df_changes.empty:
    df_changes['datetime'] = pd.to_datetime(df_changes['datetime'], utc=True)
    df_changes['date'] = df_changes['datetime'].dt.date

print(f'\nTotal: {len(df)} commits across {len(REPOS)} repos\n')

# ============================================================================
# Chart 1: Cumulative Commits Over Time (All Repos)
# ============================================================================
print('Chart 1: Cumulative commits over time...')
fig, ax = plt.subplots(figsize=(8, 4))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
for i, (repo_name, group) in enumerate(df.groupby('repo')):
    daily = group.groupby('date').size().sort_index().cumsum()
    ax.step(daily.index, daily.values, where='post',
            label=f'{repo_name} ({daily.values[-1]})',
            color=colors[i % len(colors)], linewidth=1.5)

ax.set_xlabel('Date')
ax.set_ylabel('Cumulative Commits')
ax.set_title('Cumulative Commits Across All Repositories')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)
fig.autofmt_xdate()
save_figure(fig, 'cumulative_commits')
plt.close()

# ============================================================================
# Chart 2: Daily Commit Activity Heatmap-style Bar Chart
# ============================================================================
print('Chart 2: Daily commit activity...')
fig, ax = plt.subplots(figsize=(8, 3.5))

daily_all = df.groupby('date').size()
repo_daily = df.groupby(['date', 'repo']).size().unstack(fill_value=0)

# Stack bars by repo
bottom = None
for i, repo_name in enumerate(repo_daily.columns):
    values = repo_daily[repo_name]
    ax.bar(repo_daily.index, values, bottom=bottom,
           label=repo_name, color=colors[i % len(colors)], alpha=0.85, width=0.8)
    bottom = values if bottom is None else bottom + values

ax.set_xlabel('Date')
ax.set_ylabel('Commits per Day')
ax.set_title('Daily Commit Activity by Repository')
ax.legend(loc='upper left', fontsize=7, ncol=2)
ax.grid(True, alpha=0.3, axis='y')
fig.autofmt_xdate()
save_figure(fig, 'daily_activity')
plt.close()

# ============================================================================
# Chart 3: Lines of Code Changed (Additions vs Deletions)
# ============================================================================
if not df_changes.empty:
    print('Chart 3: Code churn (additions vs deletions)...')
    fig, ax = plt.subplots(figsize=(8, 4))

    churn_daily = df_changes.groupby('date').agg(
        additions=('additions', 'sum'),
        deletions=('deletions', 'sum')
    )

    ax.bar(churn_daily.index, churn_daily['additions'],
           color='#2ca02c', alpha=0.7, label='Additions', width=0.8)
    ax.bar(churn_daily.index, -churn_daily['deletions'],
           color='#d62728', alpha=0.7, label='Deletions', width=0.8)

    ax.set_xlabel('Date')
    ax.set_ylabel('Lines Changed')
    ax.set_title('Code Churn: Lines Added vs Deleted (All Repos)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')
    ax.axhline(y=0, color='black', linewidth=0.5)
    fig.autofmt_xdate()
    save_figure(fig, 'code_churn')
    plt.close()

# ============================================================================
# Chart 4: Repo Size Comparison (Horizontal Bar)
# ============================================================================
print('Chart 4: Repository comparison...')
fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))

repo_stats = df.groupby('repo').agg(
    commits=('hash', 'count'),
).sort_values('commits', ascending=True)

# Commits
axes[0].barh(repo_stats.index, repo_stats['commits'], color=colors[:len(repo_stats)], alpha=0.85)
axes[0].set_xlabel('Commits')
axes[0].set_title('Total Commits')
for i, v in enumerate(repo_stats['commits']):
    axes[0].text(v + 1, i, str(v), va='center', fontsize=8)

# Lines of code (from onefetch data)
loc_data = {
    'WhitePaper': 661,
    'SendCUIEmail': 5026,
    'Decisions': 1699,
    'Security Toolkit': 26630,
}
# Add any extra repos with estimated LOC
for name in REPOS:
    if name not in loc_data:
        loc_data[name] = 0

loc_series = pd.Series(loc_data).sort_values()
loc_series = loc_series[loc_series > 0]
axes[1].barh(loc_series.index, loc_series.values, color='#2ca02c', alpha=0.85)
axes[1].set_xlabel('Lines of Code')
axes[1].set_title('Lines of Code')
for i, v in enumerate(loc_series):
    axes[1].text(v + 100, i, f'{v:,}', va='center', fontsize=8)

# Tags (version releases)
tag_data = {}
for name, path in REPOS.items():
    result = subprocess.run(['git', '-C', path, 'tag', '-l'], capture_output=True, text=True)
    tag_data[name] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

tag_series = pd.Series(tag_data).sort_values()
axes[2].barh(tag_series.index, tag_series.values, color='#ff7f0e', alpha=0.85)
axes[2].set_xlabel('Version Tags')
axes[2].set_title('Releases (Tags)')
for i, v in enumerate(tag_series):
    axes[2].text(v + 0.5, i, str(v), va='center', fontsize=8)

fig.suptitle('Repository Ecosystem Overview', fontsize=12, fontweight='bold')
plt.tight_layout()
save_figure(fig, 'repo_comparison')
plt.close()

# ============================================================================
# Chart 5: Commit Timeline (Hour of Day / Day of Week)
# ============================================================================
print('Chart 5: Commit patterns (hour/day)...')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Hour of day
df['hour'] = df['datetime'].dt.hour
hourly = df.groupby('hour').size()
ax1.bar(hourly.index, hourly.values, color='#1f77b4', alpha=0.85)
ax1.set_xlabel('Hour of Day (UTC)')
ax1.set_ylabel('Commits')
ax1.set_title('Commits by Hour of Day')
ax1.set_xticks(range(0, 24, 3))
ax1.grid(True, alpha=0.3, axis='y')

# Day of week
df['day_of_week'] = df['datetime'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = df['day_of_week'].value_counts().reindex(day_order, fill_value=0)
bar_colors = ['#1f77b4'] * 5 + ['#ff7f0e'] * 2  # weekdays blue, weekends orange
ax2.bar(range(7), day_counts.values, color=bar_colors, alpha=0.85)
ax2.set_xlabel('Day of Week')
ax2.set_ylabel('Commits')
ax2.set_title('Commits by Day of Week')
ax2.set_xticks(range(7))
ax2.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
ax2.grid(True, alpha=0.3, axis='y')

fig.suptitle('Development Patterns', fontsize=12, fontweight='bold')
plt.tight_layout()
save_figure(fig, 'commit_patterns')
plt.close()

# ============================================================================
# Chart 6: Ecosystem Growth Timeline
# ============================================================================
print('Chart 6: Ecosystem growth timeline...')
fig, ax = plt.subplots(figsize=(8, 4))

# Get first commit date per repo
first_commits = df.groupby('repo')['datetime'].min().sort_values()
last_commits = df.groupby('repo')['datetime'].max()
commit_counts = df.groupby('repo').size()

for i, (repo, start) in enumerate(first_commits.items()):
    end = last_commits[repo]
    count = commit_counts[repo]
    start_num = mdates.date2num(start)
    end_num = mdates.date2num(end)
    duration = max(end_num - start_num, 0.3)  # minimum bar width for visibility
    ax.barh(i, duration,
            left=start_num,
            height=0.6, color=colors[i % len(colors)], alpha=0.85)
    ax.text(start_num + duration + 0.15, i,
            f'{count} commits', va='center', fontsize=8)

ax.set_yticks(range(len(first_commits)))
ax.set_yticklabels(first_commits.index)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax.set_xlabel('Date (2026)')
ax.set_title('Repository Lifecycle: Active Development Windows')
ax.grid(True, alpha=0.3, axis='x')
fig.autofmt_xdate()
save_figure(fig, 'ecosystem_timeline')
plt.close()

# ============================================================================
# Summary Statistics JSON (for paper reference)
# ============================================================================
print('\nGenerating summary statistics...')
stats = {
    'generated': datetime.now(timezone.utc).isoformat(),
    'total_repos': len(REPOS),
    'total_commits': len(df),
    'total_loc': sum(loc_data.values()),
    'date_range': {
        'first': str(df['datetime'].min()),
        'last': str(df['datetime'].max()),
    },
    'per_repo': {},
}
for name in REPOS:
    repo_df = df[df['repo'] == name]
    stats['per_repo'][name] = {
        'commits': len(repo_df),
        'loc': loc_data.get(name, 0),
        'tags': tag_data.get(name, 0),
        'first_commit': str(repo_df['datetime'].min()),
        'last_commit': str(repo_df['datetime'].max()),
    }

stats_path = OUTPUT_DIR / 'stats.json'
with open(stats_path, 'w') as f:
    json.dump(stats, f, indent=2)
print(f'  Saved: {stats_path}')

print('\n=== Done! ===')
print(f'Generated {len(list(OUTPUT_DIR.glob("*.png")))} PNG charts')
print(f'Generated {len(list(OUTPUT_DIR.glob("*.pdf")))} PDF charts')
if HAS_TIKZ:
    print(f'Generated {len(list(OUTPUT_DIR.glob("*.tex")))} TikZ files')
