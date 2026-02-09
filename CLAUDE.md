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
├── PROCESS.md              # Process documentation (meta-narrative)
├── agents.json             # Claude Code --agents mode configuration
├── .gitignore              # Git ignore rules
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

## Build Instructions

### Compile the white paper

```bash
pdflatex whitepaper.tex
bibtex whitepaper
pdflatex whitepaper.tex
pdflatex whitepaper.tex
```

Or with latexmk:

```bash
latexmk -pdf whitepaper.tex
```

## Writing Conventions

- Academic tone throughout
- IEEE conference paper style
- All claims backed by citations or direct code references
- Government standards cited by full designation (e.g., "NIST SP 800-132")
- Code examples drawn directly from the case study repositories
