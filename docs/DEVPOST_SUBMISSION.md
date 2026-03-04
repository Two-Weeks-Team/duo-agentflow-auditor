# Devpost Submission Text

> Copy-paste this into the Devpost submission form at gitlab.devpost.com

---

## Project Name

Duo AgentFlow Auditor

## Short Description (one line)

A four-agent security auditing flow that automatically scans merge requests for AI-specific risks, posts actionable reports, generates fix patches, and tracks sustainability metrics — all triggered by a single @mention.

## Full Description

### The Problem: The AI Paradox

AI accelerates code generation, but creates new bottlenecks. GitLab's 2025 DevSecOps Report found that teams lose **7 hours per week** to AI-related inefficiencies, and **70%** say AI makes compliance harder. Security reviews have become the #1 bottleneck — AI-generated code introduces novel risk patterns (prompt injection, credential exfiltration, unsafe shell automation) that traditional SAST tools completely miss.

### The Solution: AgentFlow Auditor

We built a **multi-agent flow** on the GitLab Duo Agent Platform that automates security reviews end-to-end. One @mention triggers four specialized agents:

1. **Scanner Agent** — Reads MR diffs and matches against 34 detection rules (26 regex + 8 Semgrep) across 8 risk categories. Computes per-finding risk scores (0-100) and assigns a SAFE/WARNING/DANGER grade.

2. **Reporter Agent** — Formats findings into a structured MR comment with risk tables, severity badges, and collapsible fix suggestions. Creates issues with `security-risk` labels for DANGER-grade findings.

3. **Fixer Agent** — Generates confidence-scored code patches (HIGH/MEDIUM/LOW) for actionable findings (e.g., `shell=True` → argument lists, `eval()` → `ast.literal_eval()`, HTTP → HTTPS). HIGH-confidence fixes are applied directly; LOW-confidence ones get TODO comments only. Creates a fix branch and opens a merge request.

4. **Metrics Agent** — Tracks risk baselines between scans, computes drift deltas, performs cross-MR learning (detecting persistent risks across scans), generates team security posture reports, and tracks sustainability metrics including token usage, energy consumption, and carbon footprint estimates (Green Agent).

5. **External SAST Scanner** — Runs bandit and semgrep in a CI/CD container, merges results with custom detection rules via a Python script, and posts unified findings as an MR note. Complements the AI-powered Scanner Agent with deterministic static analysis.

### What Makes It Different

- **AI-specific detection**: 8 custom Semgrep rules catch LLM prompt injection, LLM output-to-exec, unsafe ML model deserialization — patterns that standard SAST tools ignore
- **Conditional flow routing**: SAFE scans skip the Fixer agent entirely, saving tokens and time
- **Multi-agent orchestration**: Four agents with distinct roles, chained via GitLab's flow registry v1 with conditional routing
- **Actionable, not noisy**: Risk scoring formula separates real threats from documentation examples
- **Self-improving**: Cross-MR learning detects persistent risks, tracks fix adoption rates, and projects security posture trends
- **Confidence-aware fixes**: Fixer agent scores each patch (HIGH/MEDIUM/LOW) — never blindly applies uncertain changes
- **Production-ready SAST**: Dockerized bandit + semgrep pipeline with 76 pytest tests covering scoring, grading, and parsing
- **Sustainable by design**: Every scan reports its energy footprint with optimization suggestions

### Technology

- **Platform**: GitLab Duo Agent Platform (Flow Registry v1, ambient environment)
- **AI Model**: Anthropic Claude Sonnet (default for GitLab agents)
- **Triggers**: Mention, Assign, Assign Reviewer
- **Tools**: 27+ GitLab built-in tools (List MR Diffs, Grep, Create Issue, Create Commit, etc.)
- **External SAST**: Dockerized bandit + semgrep + 8 custom Semgrep rules + result merger (Python)
- **Testing**: 76 pytest tests covering scoring formula, grade logic, and SAST parsing
- **Demo**: Automated E2E demo script (glab CLI)
- **Configuration**: Custom flow YAML with conditional routing + 4 catalog agents + 1 external agent + AGENTS.md customization

### Impact

- Reduces security review time from hours to minutes
- Catches AI-specific risks before production deployment
- Tracks codebase security health over time
- Reports environmental impact of every scan

---

## Built With

- GitLab Duo Agent Platform
- Anthropic Claude Sonnet
- GitLab CI/CD
- Flow Registry v1 YAML (with conditional routing)
- AGENTS.md Customization
- bandit (Python SAST)
- semgrep (multi-language SAST) + 8 custom rules
- Python (SAST result merger)
- Docker (production SAST container)
- pytest (76 tests)

## Try It Out

[GitLab Project URL — insert after publishing]

## Demo Video

[YouTube URL — insert after recording]
