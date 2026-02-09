# Git and AI Coding Agents for Government Compliance

A methodology for using git version control and AI coding agents to meet federal information security requirements.

## Paper

**Title**: Git and AI Coding Agents for Government Compliance: A Methodology for Federal Information Security Requirements

**Format**: 22-page academic paper, two-column, IEEE-style

**Key argument**: Git provides the tamper-evident audit trail (NIST SP 800-53 CM-3); AI coding agents draft compliance artifacts under human review (AC-5). Together they shift the engineer's role from author to reviewer while maintaining human-in-the-loop oversight. The methodology is agent-platform agnostic.

**Case Studies**:
- **SendCUIEmail** — CUI email encryption tool (FIPS 197, NIST SP 800-132, 32 CFR Part 2002)
- **Decision Documentation System** — Formal decision memoranda in LaTeX (SF901 CUI coversheets)
- **Security Verification Toolkit** — Automated NIST SP 800-53 control verification (14 controls, 94 version tags)

**Quantitative results** (single engineer, 26 calendar days):
- 642 commits across 7 repositories
- 34,000+ lines of code, 136 release tags
- 14 NIST SP 800-53 controls automated
- 7 decision memoranda, 29 traced requirements, 29 verification mappings

## Build

Requires `pdflatex`, `bibtex`, and optionally `pandoc`:

```bash
./build.sh
```

Produces `whitepaper.pdf`, `whitepaper-review.md`, and `whitepaper-review.html`.

## Repository Structure

```
whitepaper.tex          Main paper (LaTeX)
references.bib          BibTeX references (23 entries)
build.sh                Reproducible build script
agents.json             Multi-agent configuration (5 agents)
PROCESS.md              Session-by-session development log
CHANGELOG.md            Keep a Changelog format
CLAUDE.md               Agent instructions
scan.sh                 Security scanning wrapper
.allowlists/            Documented scan exceptions
visualizations/         10 charts (PNG/PDF/TikZ) + generation scripts
```

## Ecosystem

| Repository | Purpose |
|---|---|
| [systems-engineering](https://github.com/brucedombrowski/systems-engineering) | Five-phase process framework, templates |
| [ai-agents](https://github.com/brucedombrowski/ai-agents) | Model-agnostic agent role templates |
| [Scrum](https://github.com/brucedombrowski/Scrum) | Sprint-based agent orchestration |
| [SendCUIEmail](https://github.com/brucedombrowski/SendCUIEmail) | Case study: CUI email encryption |
| [security-toolkit](https://github.com/brucedombrowski/security-toolkit) | Case study: NIST 800-53 automated verification |

## Process

This paper was written using the methodology it describes. Every human directive and agent action is logged as a [GitHub issue](https://github.com/brucedombrowski/WhitePaper/issues) with structured labels (`human-prompt`, `agent-output`, `decision`). See [PROCESS.md](PROCESS.md) for the session-by-session narrative.

## License

All rights reserved. Academic use with attribution permitted.
