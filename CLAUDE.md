# CLAUDE.md

Instructions for AI agents working with this repository.

## Project Overview

This repository contains an academic white paper examining the use of Claude Code (Anthropic's AI-powered CLI tool) to meet government compliance requirements. The paper draws on real-world case studies from the author's projects.

## Author

Bruce Dombrowski (GitHub: brucedombrowski)

## Repository Structure

```
WhitePaper/
├── whitepaper.tex          # Main LaTeX document
├── references.bib          # BibTeX references
├── CLAUDE.md               # This file
├── PROCESS.md              # Executive summary of process
├── CHANGELOG.md            # Semantic versioning changelog
├── agents.json             # Claude Code --agents mode configuration
├── build.sh                # LaTeX-to-PDF build script
├── scan.sh                 # Security scanning wrapper
├── .gitignore              # Git ignore rules
├── .allowlists/            # Security scan false-positive allowlists
└── figures/                # Diagrams and figures (if needed)
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
./build.sh
```

Or manually:

```bash
pdflatex whitepaper.tex && bibtex whitepaper && pdflatex whitepaper.tex && pdflatex whitepaper.tex
```

## Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).

- **MAJOR**: Structural paper changes (new/removed sections)
- **MINOR**: New content (case studies, methodology additions)
- **PATCH**: Fixes (typos, citations, formatting)

Update `CHANGELOG.md` with every commit. Tag releases: `git tag -a vX.Y.Z -m "description"`

## Writing Conventions

- Academic tone throughout
- IEEE conference paper style
- All claims backed by citations or direct code references
- Government standards cited by full designation (e.g., "NIST SP 800-132")
- Code examples drawn directly from the case study repositories
