# CLAUDE.md

Instructions for AI agents working with this repository.

## Project Overview

This repository contains an academic white paper presenting a methodology for using git version control and AI coding agents to meet government compliance requirements. The paper is solution-agnostic — it describes the methodology in general terms while using Claude Code (Anthropic) as the implementation in the case studies. The paper draws on real-world case studies from the author's projects.

## Author

Bruce Dombrowski (GitHub: brucedombrowski)

## Repository Structure

```
WhitePaper/
├── whitepaper.tex          # Main LaTeX document
├── references.bib          # BibTeX references
├── metrics.tex             # AUTO-GENERATED — LaTeX \newcommand definitions for all paper metrics
├── CLAUDE.md               # This file
├── PROCESS.md              # Executive summary of process
├── CHANGELOG.md            # Semantic versioning changelog
├── agents.json             # Claude Code --agents mode configuration
├── .gitignore              # Git ignore rules
├── .allowlists/            # Security scan false-positive allowlists
├── scripts/                # Build and automation scripts
│   ├── build.sh            # LaTeX-to-PDF build script (runs metrics + pdflatex + pandoc)
│   ├── generate_metrics.py # Auto-generates metrics.tex from live git/GitHub data
│   └── scan.sh             # Security scanning wrapper
└── visualizations/         # Git data visualizations
    ├── generate_charts.py  # Cross-repo chart generator (6 figures)
    ├── generate_theseus.py # git-of-theseus analysis (4 figures)
    ├── *.png, *.pdf, *.tex # Output charts (PNG, PDF, TikZ)
    ├── ecosystem-gource.mp4 # Animated repo visualization
    └── stats.json          # Machine-readable statistics
```

## Case Study Source Repositories

These repos provide the real-world examples cited in the paper:

1. **SendCUIEmail** - https://github.com/brucedombrowski/SendCUIEmail
   - CUI file encryption tool (PowerShell)
   - Addresses: FIPS 140-2, NIST SP 800-132, 32 CFR Part 2002, NIST SP 800-171
   - Demonstrates: requirements traceability, decision documentation, verification

2. **LaTeX/Decisions** - Decision memoranda system
   - LaTeX template for formal decision documentation
   - Addresses: SF901 CUI coversheet compliance
   - Demonstrates: document generation, template patterns

3. **Security Verification Toolkit** - https://github.com/brucedombrowski/security-toolkit
   - Automated security scanning and compliance documentation (Bash)
   - Addresses: NIST SP 800-53 (14 controls), NIST SP 800-171 (11 controls), NIST SP 800-88, BOD 22-01, FIPS 199
   - Demonstrates: automated control verification, requirements traceability, PDF attestation generation, multi-agent development

## Recommended Claude Code Invocation

### Multi-agent mode (full workflow)

```bash
claude --agents "$(cat agents.json)"
```

> **Note**: `agents.json` in this repo is a snapshot of the canonical source at
> [ai-agents/claude/agents.json](https://github.com/brucedombrowski/ai-agents).
> When updating agent definitions, update the canonical source first, then sync here.

### Single-session development (default)

```bash
claude --model opus
```

### Key CLI switches

| Switch | Purpose | When to use |
|--------|---------|-------------|
| `--agents FILE` | Load multi-agent configuration | Full workflow with role separation |
| `--model opus` | Use Opus model | Regulatory interpretation, review, complex reasoning |
| `--model sonnet` | Use Sonnet model | Implementation, documentation, structured tasks |
| `--allowedTools` | Restrict available tools | Enforce separation of duties (e.g., review agent) |
| `--resume` | Resume previous session | Continue work across sessions |
| `--continue` | Continue most recent session | Pick up where you left off |
| `--verbose` | Show tool calls and reasoning | Debugging agent behavior |

### Recommended session workflow

```bash
# Start a new development session
claude --model opus

# Resume an interrupted session
claude --continue

# Run the full multi-agent pipeline
claude --agents "$(cat agents.json)"
```

## Build Instructions

### Compile the white paper

```bash
./scripts/build.sh
```

Or manually:

```bash
python3 scripts/generate_metrics.py  # Step 0: auto-update metrics.tex
pdflatex whitepaper.tex && bibtex whitepaper && pdflatex whitepaper.tex && pdflatex whitepaper.tex
```

## Auto-Metrics Pipeline

All quantitative claims in the paper are auto-generated. **Never hardcode numbers** in `whitepaper.tex`.

### How it works

1. `scripts/generate_metrics.py` queries all 17 git repos and GitHub API
2. Outputs `metrics.tex` (in repo root) with `\newcommand` definitions (e.g., `\totalcommits`, `\secloc`)
3. `whitepaper.tex` uses `\input{metrics.tex}` and references commands instead of numbers
4. `scripts/build.sh` runs the script as Step 0 before pdflatex

### Adding a new metric

1. Add the computation to `scripts/generate_metrics.py`
2. Add a `\newcommand` to the output
3. Use `\yournewcommand{}` in `whitepaper.tex`
4. The `{}` after the command prevents LaTeX from eating the following space

## Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).

- **MAJOR**: Structural paper changes (new/removed sections)
- **MINOR**: New content (case studies, methodology additions)
- **PATCH**: Fixes (typos, citations, formatting)

Update `CHANGELOG.md` with every commit. Tag releases: `git tag -a vX.Y.Z -m "description"`

## Git Visualization Toolkit

Publication-quality visualizations generated from git data across all ecosystem repos.

### Installed Tools

| Tool | Install | Purpose |
|------|---------|---------|
| `onefetch` | `brew install onefetch` | Repo summary cards (languages, LOC, commits, version) |
| `gource` | `brew install gource` | Animated 3D tree visualization of repo history |
| `git-quick-stats` | `brew install git-quick-stats` | Terminal-based commit statistics |
| `matplotlib` | `pip3 install matplotlib` | Publication-quality chart generation |
| `pandas` | `pip3 install pandas` | Data analysis and aggregation |
| `git-of-theseus` | `pip3 install git-of-theseus` | Code survival analysis (Kaplan-Meier curves, cohort stack plots) |
| `SciencePlots` | `pip3 install SciencePlots` | IEEE/Nature/Science journal-ready matplotlib styles |
| `matplot2tikz` | `pip3 install matplot2tikz` | Export matplotlib figures to PGFPlots/TikZ for LaTeX |

### Generated Outputs (`visualizations/`)

| File | Description |
|------|-------------|
| `cumulative_commits.png/pdf/tex` | Cumulative commit growth per repo over time |
| `daily_activity.png/pdf/tex` | Stacked bar chart of daily commits by repo |
| `code_churn.png/pdf/tex` | Lines added vs deleted per day |
| `repo_comparison.png/pdf/tex` | Triptych: commits, LOC, and version tags per repo |
| `commit_patterns.png/pdf/tex` | Hour-of-day and day-of-week commit distributions |
| `ecosystem_timeline.png/pdf/tex` | Gantt-style active development windows per repo |
| `theseus_cohorts.png/pdf/tex` | Code age cohort stack plot (Security Toolkit) |
| `theseus_extensions.png/pdf/tex` | Code by file extension over time (Security Toolkit) |
| `theseus_directories.png/pdf/tex` | Code by directory over time (Security Toolkit) |
| `ecosystem-gource.mp4` | 40s animated tree visualization of all repos |
| `gource-snapshot.png` | Still frame from gource video (peak activity) |
| `stats.json` | Machine-readable summary statistics |

### Regenerating Charts

```bash
python3 visualizations/generate_charts.py      # Cross-repo charts (6 figures)
python3 visualizations/generate_theseus.py      # git-of-theseus analysis (4 figures)
```

### Pipeline

```
git log --pretty=format (CSV) → pandas → matplotlib + SciencePlots → matplot2tikz → PGFPlots/LaTeX
```

Each chart is exported as PNG (300 DPI), PDF (vector), and TikZ (.tex) for direct `\input{}` into the paper.

## Writing Conventions

- Academic tone throughout
- IEEE conference paper style
- **Solution-agnostic language**: Use "AI coding agent" for methodology-level discussion; name "Claude Code" only when describing the specific implementation used. Do not write product-review language.
- Model references: Use "reasoning-optimized" and "throughput-optimized" rather than vendor-specific model names (Opus, Sonnet) except in implementation-specific context
- All claims backed by citations or direct code references
- Government standards cited by full designation (e.g., "NIST SP 800-132")
- Code examples drawn directly from the case study repositories
