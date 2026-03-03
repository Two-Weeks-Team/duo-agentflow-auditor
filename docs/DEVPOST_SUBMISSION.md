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

1. **Scanner Agent** — Reads MR diffs and matches against 26 detection rules across 8 risk categories. Computes per-finding risk scores (0-100) and assigns a SAFE/WARNING/DANGER grade.

2. **Reporter Agent** — Formats findings into a structured MR comment with risk tables, severity badges, and collapsible fix suggestions. Creates issues with `security-risk` labels for DANGER-grade findings.

3. **Fixer Agent** — Generates concrete code patches for actionable findings (e.g., `shell=True` → argument lists, `eval()` → `ast.literal_eval()`, HTTP → HTTPS). Creates a fix branch and opens a merge request.

4. **Metrics Agent** — Tracks risk baselines between scans, computes drift deltas, and reports sustainability metrics including token usage, energy consumption, and carbon footprint estimates (Green Agent).

### What Makes It Different

- **AI-specific detection**: Catches prompt injection, credential exfiltration, and obfuscated execution — patterns that standard SAST tools ignore
- **Multi-agent orchestration**: Four agents with distinct roles, chained via GitLab's flow registry v1
- **Actionable, not noisy**: Risk scoring formula separates real threats from documentation examples
- **Self-improving**: Baseline tracking shows whether your codebase is getting more or less secure
- **Sustainable by design**: Every scan reports its energy footprint with optimization suggestions

### Technology

- **Platform**: GitLab Duo Agent Platform (Flow Registry v1, ambient environment)
- **AI Model**: Anthropic Claude Sonnet (default for GitLab agents)
- **Triggers**: Mention, Assign, Assign Reviewer
- **Tools**: 20+ GitLab built-in tools (List MR Diffs, Grep, Create Issue, Create Commit, etc.)
- **Configuration**: Custom flow YAML + 4 custom agents + AGENTS.md customization

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
- Flow Registry v1 YAML
- AGENTS.md Customization

## Try It Out

[GitLab Project URL — insert after publishing]

## Demo Video

[YouTube URL — insert after recording]
