# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `CHANGELOG.md` following Keep a Changelog format (#10)
- `build.sh` for reproducible LaTeX-to-PDF compilation (#12)
- Semantic versioning requirements in project-setup agent prompt (#10)
- Recommended CLI switches table in paper and CLAUDE.md (#11)
- SemVer paragraph in Phase 5 methodology section
- Session continuity (`--resume`, `--continue`) in Claude Code Architecture
- Retroactive git tags v0.1.0 through v0.5.0
- All human feedback logged as GitHub issues (#13)
- Figure 1: Five-phase methodology workflow diagram (TikZ) (#14)
- Figure 2: Multi-agent architecture diagram (TikZ) (#14)
- Abstract updated to mention five-phase methodology and version control

### Changed
- Introduction "dual burden" broadened to acknowledge safety-critical (DO-178C, IEC 61508) and information-critical (HIPAA, SOX) domains (#15)
- All three case studies now state version numbers and active-development status (#15)
- New limitation: "Case study maturity" noting all projects are pre-production (#15)
- New subsection: Scrum-Based Agent Orchestration (Section 7.4) with Scrum team roles, advantages for compliance, and reference to brucedombrowski/Scrum (#16)
- Scrum Guide (Schwaber & Sutherland, 2020) added to references.bib (#16)
- New subsection: Concurrent Multi-Project Scalability in Discussion — cross-pollination across 5 projects, iterative process refinement (#17)
- Agent instruction ingestion and canonical ai-agents repo reference (#18)
- Created https://github.com/brucedombrowski/ai-agents with model-agnostic templates and Claude implementation (#18)
- Repo scope audit: clean divisions confirmed, upstream reference added to CLAUDE.md (#19)
- Origin story: methodology evolved from CAD/house project and SpeakUp through 16 repos (#21)
- `build.sh` now generates `whitepaper-review.md` via pandoc for human review (#20)
- `whitepaper-review.md` — GitHub-flavored Markdown for selectable-text review (#20)
- Created https://github.com/brucedombrowski/systems-engineering with 5-phase process framework (#22)
- New subsection: Ecosystem Architecture (how/who/when separation across repos) (#22)
- Base `.gitignore` template in systems-engineering, derived from security-toolkit (#25)
- Filed `.gitignore` adoption issues on 6 repos (#26)
- GitHub avatar (SVG/PNG) for brucedombrowski profile (#24)
- Git visualization toolkit: onefetch, gource, git-of-theseus, matplotlib, SciencePlots, matplot2tikz (#27)
- 10 publication-quality charts: cumulative commits, daily activity, code churn, repo comparison, commit patterns, ecosystem timeline, code cohorts, extension evolution, directory evolution, gource snapshot (#27)
- `visualizations/generate_charts.py` — cross-repo chart generator (6 figures)
- `visualizations/generate_theseus.py` — git-of-theseus analysis (4 figures)
- `ecosystem-gource.mp4` — 40s animated tree visualization of all repos (#27)
- TikZ export pipeline: matplotlib → matplot2tikz → PGFPlots for LaTeX inclusion (#27)
- New subsection: Stakeholder Accessibility — bridging CLI-browser gap, Excel/CSV pattern, branch protection (#28, #29)
- New subsection: Git Data Visualization — pipeline description, tool inventory, findings (#27)
- Training slide deck: `visualizations/git-workflow-training.pptx` (14 slides) (#30)
- Issue #30: 30-minute training video concept with content outline
- Figure 6: Cumulative commits timeline embedded in Concurrent Multi-Project Scalability discussion
- Figure 7: Security Toolkit directory evolution (git-of-theseus) embedded in Security Toolkit case study
- Introduction contributions list expanded from 4 to 5 items (added traceability framework and standards-based review)
- Abstract now mentions five-phase methodology and version control
- Reproducibility section updated with current metrics (14 issues, 9 commits, v0.5.0)
- Conclusion expanded with version control/audit trail discussion and meta-methodology paragraph

- `README.md` for the WhitePaper repository
- `@misc` bib entries: Claude Code (Anthropic), SendCUIEmail, Security Toolkit — 23 references total
- HTML review output via pandoc (`whitepaper-review.html` with MathJax)
- Formal `Listing~\ref{}` cross-references for Listings 3 and 4
- Quantitative Output Analysis subsection with Table 5 (642 commits, 34K LOC, 136 tags in 26 days)
- Figure 8: Code churn chart (daily additions vs deletions)
- Solution-agnostic refactoring: title, abstract, keywords, throughout (#33)
- Expanded related work: three-tier AI tool comparison (inline → chat → agentic)
- Abstract includes quantitative claims and "agent-platform agnostic" statement
- Future Work: cross-platform validation with alternative AI tools
- README.md updated with new title, key argument, quantitative results

### Fixed
- "The final phase" → "The verification phase" (stale from 4-phase era)
- "2.7 major versions" → "94 version tags" in Security Toolkit Multi-Agent Development subsection
- Misleading `\cite{nist80053}` on Security Toolkit — replaced with proper `\cite{securitytoolkit}`
- Missing AU-2/AU-3 in NIST control enumeration (14 controls, 8 families confirmed)
- Figure 1: added Phase 4 artifact node (VER matrix) — was only phase missing its artifact
- Table 3: documentation agent spans Phases 3–4, review agent is cross-cutting, footnote added
- Commit count 24 → 28+, session count 9 → 10, issue count 30 → 31+
- Ecosystem stats: 636 → 642 commits, "three weeks" → "four weeks" (26 days actual)
- "Four phases" → "five phases" in two locations (Phase 5 intro, Workflow Orchestration)
- Missing listing reference for `lst:agentsmd` in Phase 2 text
- Scrum section vendor-specific model refs: "Opus"/"Sonnet" → reasoning/throughput-optimized (#34)
- Stale reproducibility metrics: 31→33 issues, 28→39 commits, 6→7 tags, 5→6 figures (#34)
- All 4 overfull hbox warnings: TikZ figures resized, equation split, table font reduced (#34)
- CLAUDE.md: added solution-agnostic writing conventions and model reference guidelines (#34)

## [0.5.0] - 2026-02-09

### Added
- Phase 5 (Version Control and Interaction Traceability) in Methodology section
- Git as audit trail discussion (NIST SP 800-53 CM-3)
- GitHub issues as structured interaction log (`human-prompt`, `agent-output`, `decision`)
- Expanded Reproducibility discussion mapping to CM-3 and AU-3

### Changed
- Paper grew from 12 to 13 pages

## [0.4.0] - 2026-02-09

### Added
- Security Verification Toolkit as third case study (Section 6)
- `scan.sh` wrapper script for automated security scanning
- `.allowlists/pii-allowlist` for documented false positives
- Security scan results: PII, secrets, MAC address, host security
- GitHub issues #6, #7, #8 documenting toolkit integration

### Changed
- Paper grew from 11 to 12 pages
- References grew from 16 to 19 (added NIST SP 800-88, BOD 22-01, FIPS 199)

## [0.3.0] - 2026-02-09

### Added
- QA standards framework (IEEE 1028, IEEE 29148, NIST 800-53 AC-5/SA-11, ISO/IEC 25010, MIL-STD-498)
- QA standards table in Discussion section
- Interaction logging requirements for all 5 agents
- GitHub labels: `human-prompt`, `agent-output`, `decision`, `critical`, `minor`
- References for 4 QA standards + RFC 2119

### Fixed
- All 13 review findings from issue #1 (5 critical, 8 minor)
- Requirement count 28 to 29 in two locations
- Decryption one-liner runtime error (SecureString vs plaintext)
- Overfull hbox in equation (split to multline)
- Table overflow in two-column layout (table to table*)

### Changed
- Paper grew from 9 to 11 pages
- References grew from 8 to 16

## [0.2.0] - 2026-02-09

### Added
- GitHub repository: https://github.com/brucedombrowski/WhitePaper
- 4 additional agents in agents.json (requirements, implementation, documentation, review)
- Review agent enforces separation of duties (no Write/Edit tools, NIST SP 800-53 AC-5)

### Changed
- agents.json expanded from 1 to 5 agents matching Section 6 of paper

## [0.1.0] - 2026-02-09

### Added
- `whitepaper.tex` — 9-page academic paper (two-column, article class)
- `references.bib` — 8 citations (6 government standards, 2 academic)
- `agents.json` — 1 agent (project-setup)
- `CLAUDE.md` — agent instructions with project context
- `PROCESS.md` — process documentation
- `.gitignore` — LaTeX artifacts, OS files, editor files

[Unreleased]: https://github.com/brucedombrowski/WhitePaper/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/brucedombrowski/WhitePaper/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/brucedombrowski/WhitePaper/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/brucedombrowski/WhitePaper/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/brucedombrowski/WhitePaper/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/brucedombrowski/WhitePaper/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/brucedombrowski/WhitePaper/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/brucedombrowski/WhitePaper/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/brucedombrowski/WhitePaper/releases/tag/v0.1.0
