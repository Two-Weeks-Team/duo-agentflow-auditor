<div align="center">

# Duo AgentFlow Auditor

**AI Code Security — catching what SAST misses in AI-generated code**
**Built on the GitLab Duo Agent Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-GitLab%20Duo%20Agent-E24329?logo=gitlab&logoColor=white)](https://docs.gitlab.com/user/duo_agent_platform/)
[![AI Model](https://img.shields.io/badge/AI-Anthropic%20Claude-191919?logo=anthropic&logoColor=white)](https://www.anthropic.com/)
[![Agents](https://img.shields.io/badge/Agents-4-blue)](#architecture)
[![Detection Rules](https://img.shields.io/badge/Detection%20Rules-34-red)](#detection-categories)
[![Semgrep Rules](https://img.shields.io/badge/Semgrep%20Rules-8-orange)](#semgrep-custom-rules)
[![Tests](https://img.shields.io/badge/Tests-76%20passing-brightgreen)](#testing)
[![Flow Schema](https://img.shields.io/badge/Flow%20Schema-v1-brightgreen)](#technology)
[![Green Agent](https://img.shields.io/badge/Green%20Agent-Sustainability-228B22)](#green-metrics)
[![GitLab AI Hackathon](https://img.shields.io/badge/GitLab%20AI%20Hackathon-2026-FC6D26?logo=gitlab&logoColor=white)](https://gitlab.devpost.com/)

---

> 40-62% of AI-generated code contains security vulnerabilities.
> Traditional SAST catches CVEs. We catch **what SAST misses** — prompt injection, LLM output execution, unsafe ML deserialization.

[Getting Started](#quick-start) · [Architecture](#architecture) · [Detection Rules](#detection-categories) · [Setup Guide](docs/SETUP_GUIDE.md) · [Implementation](IMPLEMENTATION.md)

</div>

---

## The Problem

AI accelerates code generation but creates new security bottlenecks:

| Issue | Impact |
|-------|--------|
| Security reviews block MRs for hours or days | **7 hrs/week** lost per team member |
| AI makes compliance management harder | **70%** of teams report this |
| Compliance issues discovered after deployment | **76%** of organizations |
| Traditional SAST tools miss AI-specific risks | Prompt injection, LLM output-to-exec, unsafe ML deser |
| 40-62% of AI-generated code has vulnerabilities | No existing tool detects AI-specific threat patterns |

<sub>Source: GitLab 2025 Global DevSecOps Report</sub>

## The Solution

**AgentFlow Auditor** — Four AI agents that catch security risks traditional SAST misses in AI-generated code. 34 detection rules including LLM prompt injection, output-to-exec, and unsafe deserialization. Posts scannable reports, generates fix patches, tracks risk drift. One `@mention` triggers everything.

---

## Architecture

```
  Developer opens MR
        │
        ▼
  @duo-agentflow-auditor review this MR
        │
        ▼
┌───────────────────────────────────────────────────────┐
│                                                       │
│   ┌─────────────┐       ┌──────────────────┐         │
│   │   Scanner   │──────▶│    Reporter      │         │
│   │   Agent     │       │    Agent         │         │
│   │             │       │                  │         │
│   │ Read diffs  │       │ Grade risk       │         │
│   │ Match 34    │       │ Risk heatmap     │         │
│   │ rules       │       │ Post MR comment  │         │
│   │ Score risk  │       │ Create issue     │         │
│   └─────────────┘       └────────┬─────────┘         │
│                                  │                   │
│                          ┌───────┴────────┐          │
│                          │  SAFE?         │          │
│                          │  ├─ Yes ──────────────┐   │
│                          │  └─ No ───┐   │       │   │
│                          └───────────┘   │       │   │
│                                  │       │       │   │
│   ┌─────────────┐       ┌────────▼───────┘┐      │   │
│   │   Metrics   │◀──────│    Fixer        │      │   │
│   │   Agent     │       │    Agent        │      │   │
│   │             │◀──────────────────────────────┘   │
│   │ Baseline    │       │ Confidence-scored│         │
│   │ Cross-MR    │       │ patches         │         │
│   │ Green       │       │ Fix branch + MR │         │
│   │ Posture     │       │                 │         │
│   └─────────────┘       └─────────────────┘         │
│                                                       │
│            GitLab Duo Agent Platform (ambient)        │
│                                                       │
│   ┌───────────────────────────────────────────┐       │
│   │  External SAST Agent (CI/CD container)    │       │
│   │  bandit + semgrep + custom rules merge    │       │
│   └───────────────────────────────────────────┘       │
└───────────────────────────────────────────────────────┘
```

### Agent Roster

| Agent | Role | Tools | Key Capability |
|:------|:-----|:------|:---------------|
| **Scanner** | Analyze MR diffs | 10 tools | 34 rules (26 regex + 8 Semgrep), AI-specific threat detection, vulnerability integration |
| **Reporter** | Post audit reports | 7 tools | Scannable in 10s (grade + heatmap + top 5), vulnerability linking, auto issue on DANGER |
| **Fixer** | Generate code fixes | 8 tools | Confidence-scored patches (HIGH/MEDIUM/LOW), auto fix MR creation |
| **Metrics** | Track risk baseline | 6 tools | Cross-MR learning, team posture, baseline drift, energy/carbon tracking |
| **SAST Scanner** | External SAST | CI/CD | Runs bandit + semgrep, merges with custom rules via Python script |

---

## Features

<table>
<tr>
<td width="50%">

### Security Scanning
- **34 Detection Rules** — 26 regex + 8 Semgrep custom rules
- **8 Risk Categories** — From destructive commands to prompt injection
- **AI-Specific Detection** — LLM prompt injection, output-to-exec, unsafe deserialization
- **Risk Scoring** — 0-100 per finding (severity x context x category)
- **Grade System** — SAFE / WARNING / DANGER

</td>
<td width="50%">

### Automation
- **One-trigger activation** — `@mention` or assign reviewer
- **Conditional routing** — SAFE scans skip fixer, saving tokens
- **Structured MR comments** — Risk tables, fix suggestions, collapsible details
- **Auto-fix generation** — Code patches on a new branch
- **Issue creation** — Automatic on DANGER grade

</td>
</tr>
<tr>
<td width="50%">

### Baseline Tracking
- **Risk drift detection** — Compare scans over time
- **Trend analysis** — Improving / degrading / stable
- **Fix adoption rate** — Track how many suggestions were applied
- **History log** — JSONL append per scan

</td>
<td width="50%">

### Green Metrics
- **Token tracking** — Usage per scan
- **Energy estimation** — kWh per scan
- **Carbon footprint** — kg CO2 with real-world analogies
- **Optimization suggestions** — Reduce scan scope, cache baselines

</td>
</tr>
</table>

---

## Detection Categories

### Semgrep Custom Rules

8 production-grade Semgrep rules for AI-specific and Python security:

| Rule | Category | Severity | Detection |
|:-----|:---------|:---------|:----------|
| `llm-prompt-injection` | AI Security | WARNING | User input flowing into LLM API calls |
| `llm-output-code-exec` | AI Security | ERROR | LLM output passed to exec/eval |
| `unsafe-deserialization-ml` | AI Security | WARNING | pickle.load, torch.load on untrusted models |
| `dangerous-eval-exec` | Python | WARNING | eval/exec with dynamic content |
| `subprocess-shell-true` | Python | WARNING | subprocess with shell=True |
| `dangerous-os-system` | Python | WARNING | os.system/popen (deprecated) |
| `hardcoded-credentials` | Secrets | WARNING | Hardcoded passwords, API keys, tokens |
| `insecure-http` | Network | INFO | HTTP URLs (with autofix to HTTPS) |

### Regex Detection Categories

| Category | Severity | Example Patterns |
|:---------|:---------|:-----------------|
| Destructive Commands | 🚨 Danger | `rm -rf /`, `mkfs`, `dd to disk` |
| Credential Exfiltration | 🚨 Danger | `curl` posting secrets to external URLs |
| Prompt Injection (severe) | 🚨 Danger | "Ignore previous instructions", role overrides |
| Obfuscated Execution | 🚨 Danger | `base64 -d \| bash`, remote pipe to shell |
| Shell Execution | ⚠️ Warning | `shell=True`, `eval()`, `exec()`, `os.system()` |
| Network Calls | ⚠️ Warning | `curl`/`wget`/`fetch` to external URLs |
| Insecure Transport | ⚠️ Warning | `http://` where `https://` should be used |
| Hardcoded Credentials | ⚠️ Warning | Passwords, API keys, tokens in source |

### Risk Score Formula

```
score = severity_weight + category_weight + executable_context + actionable + risk_modifier
      = clamp(0, 100)

severity_weight:    danger=50, warning=25
category_weight:    destructive-command=15, credential-exfil=15, prompt-injection=10, ...
executable_context: +20 if file is .sh/.py/.js/.ts
actionable:         +15 if executable AND not in trusted domain allowlist
risk_modifier:      per-rule adjustment (0-15)
```

### Grade Classification

| Grade | Condition | Action |
|:------|:----------|:-------|
| 🚨 **DANGER** | max_risk >= 90 OR high_risk_findings >= 3 | Block merge + create issue |
| ⚠️ **WARNING** | max_risk >= 70 OR high_risk_findings >= 1 | Review before merge |
| ✅ **SAFE** | No meaningful risk signal | Safe to merge |

---

## Quick Start

### Prerequisites

- GitLab project with **Duo Agent Platform** enabled (GitLab 18.8+)
- Access to [GitLab AI Hackathon group](https://gitlab.com/gitlab-ai-hackathon) (for hackathon submission)

### 1. Push to GitLab

```bash
git clone https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git
cd duo-agentflow-auditor

# Add GitLab remote and push
git remote add gitlab https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git
git push gitlab main
```

> 📖 Full mirroring guide (3 methods, CI setup, sync strategies): [`docs/GITLAB_MIRROR_GUIDE.md`](docs/GITLAB_MIRROR_GUIDE.md)

### 2. Agents & Flow Publish Automatically

The hackathon group enforces a [central CI pipeline](https://gitlab.com/gitlab-ai-hackathon/ci) via [security policy](https://gitlab.com/gitlab-ai-hackathon/security-policies). When you push to GitLab, the `catalog-sync` job **automatically** publishes all `agents/*.yml` and `flows/*.yml` to the AI Catalog — no manual setup or git tags needed.

> Your project's `.gitlab-ci.yml` is overridden by the hackathon's central pipeline. The included `.gitlab-ci.yml` serves as reference only.

| # | Agent | Catalog File | Prompt Docs | Tools |
|---|-------|-------------|-------------|-------|
| 1 | Scanner | [`agents/scanner.yml`](agents/scanner.yml) | [`agents/scanner.md`](agents/scanner.md) | 8 tools |
| 2 | Reporter | [`agents/reporter.yml`](agents/reporter.yml) | [`agents/reporter.md`](agents/reporter.md) | 6 tools |
| 3 | Fixer | [`agents/fixer.yml`](agents/fixer.yml) | [`agents/fixer.md`](agents/fixer.md) | 8 tools |
| 4 | Metrics | [`agents/metrics.yml`](agents/metrics.yml) | [`agents/metrics.md`](agents/metrics.md) | 5 tools |

Flow: [`flows/security-audit.yml`](flows/security-audit.yml) — 4-agent pipeline with Scanner → Reporter → Fixer → Metrics routing.

<details>
<summary>Alternative: Manual setup via GitLab UI</summary>

**Agents**: Automate → Agents → New agent → paste system prompt from `.md` files

**Flow**: Automate → Flows → New flow → paste definition from [`flows/security-audit.yml`](flows/security-audit.yml)
</details>

### 3. Enable Triggers

| Trigger | How |
|---------|-----|
| Mention | Comment `@duo-agentflow-auditor` in any MR |
| Assign reviewer | Assign the service account as MR reviewer |

### 4. Try It

```bash
# Create test branch with vulnerable code
git checkout -b test/security-audit
cp examples/vulnerable-mr/* .
git add . && git commit -m "test: add vulnerable code for audit"
git push origin test/security-audit

# Open MR → Comment: @duo-agentflow-auditor please review this MR
```

> **Detailed walkthrough**: See [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md)

---

## Example Output

### MR Comment (DANGER grade)

```markdown
## 🛡️ AgentFlow Auditor — Security Report

Grade: 🚨 DANGER
Recommendation: FAIL — do not merge without fixes

### 🗺️ Risk Heatmap
| Risk          | File                | Findings | Max Score |
|---------------|---------------------|----------|-----------|
| 🟥🟥🟥🟥🟥 | unsafe_script.py    | 5        | 95        |
| 🟥🟥🟥🟧⬜ | risky_config.yaml   | 3        | 78        |
| 🟧🟧⬜⬜⬜ | insecure_fetch.js   | 2        | 62        |

### Top Findings
🚨 unsafe_script.py:55 — rm -rf (95/100)
🚨 unsafe_script.py:13 — shell=True (88/100)
🚨 unsafe_script.py:27 — eval() (85/100)
⚠️ insecure_fetch.js:41 — HTTP (62/100)
```

### Green Metrics

```markdown
### 🌱 Sustainability Report
| Metric              | Value               |
|---------------------|---------------------|
| Tokens Used         | 12,450              |
| Energy              | 0.0037 kWh          |
| CO₂ Footprint       | 0.0014 kg           |
| Efficiency          | 2.4 findings/1K tok |

💡 LED bulb for 13 seconds  |  🚗 Car driving 5.6 meters
```

---

## Project Structure

```
duo-agentflow-auditor/
│
├── agents/
│   ├── scanner.yml                  # Catalog agent — security scanner
│   ├── reporter.yml                 # Catalog agent — report generator
│   ├── fixer.yml                    # Catalog agent — auto-fix patches
│   ├── metrics.yml                  # Catalog agent — green metrics
│   ├── scanner.md                   # Detailed prompt documentation
│   ├── reporter.md                  # Detailed prompt documentation
│   ├── fixer.md                     # Detailed prompt documentation
│   └── metrics.md                   # Detailed prompt documentation
│
├── flows/
│   └── security-audit.yml           # Catalog flow — conditional routing pipeline
│
├── scripts/
│   ├── merge_sast_results.py        # SAST result merger (bandit + semgrep + custom rules)
│   └── demo.sh                      # E2E demo automation (glab CLI)
│
├── tests/
│   └── test_merge_sast_results.py   # 76 pytest tests — scoring, grading, parsing
│
├── .gitlab/
│   └── duo/
│       └── flows/
│           └── sast-scanner.yaml    # External SAST agent (CI/CD container)
│
├── rules/
│   ├── danger_rules.json            # 11 high-severity detection patterns
│   ├── warning_rules.json           # 15 medium-severity detection patterns
│   └── semgrep/                     # 8 Semgrep custom rules
│       ├── ai-security/             # LLM prompt injection, output exec, unsafe deser
│       ├── python-security/         # eval/exec, subprocess, os.system
│       ├── secrets/                 # Hardcoded credentials
│       └── network/                 # Insecure HTTP (with autofix)
│
├── Dockerfile                       # Production SAST container (python:3.11-slim)
├── requirements.txt                 # bandit + semgrep dependencies
│
├── examples/
│   ├── vulnerable-mr/               # Intentionally risky code (demo)
│   │   ├── unsafe_script.py         # shell=True, eval(), rm -rf, cred leak
│   │   ├── risky_config.yaml        # Prompt injection, hardcoded secrets
│   │   └── insecure_fetch.js        # HTTP, exec(), token exposure
│   └── safe-mr/                     # Secure code for contrast (demo)
│       ├── safe_script.py
│       ├── safe_config.yaml
│       └── safe_script.js           # HTTPS, execFile, env vars
│
├── docs/
│   ├── SETUP_GUIDE.md               # Step-by-step setup
│   ├── EXECUTION_PLAN.md            # Implementation plan
│   ├── WOW_MOMENTS.md               # Visual impact & demo choreography
│   ├── DEVPOST_SUBMISSION.md        # Devpost submission draft
│   └── GITLAB_MIRROR_GUIDE.md       # GitHub → GitLab mirroring
│
├── .gitlab-ci.yml                   # CI — catalog-sync + validation
├── AGENTS.md                        # Project-level agent customization
├── IMPLEMENTATION.md                # Architecture & design document
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # MIT License
└── README.md                        # This file
```

---

## Technology

| Component | Technology |
|:----------|:-----------|
| **Platform** | GitLab Duo Agent Platform (GA in GitLab 18.8) |
| **AI Model** | Anthropic Claude Sonnet |
| **Flow Schema** | Flow Registry v1 (`ambient` environment) |
| **Triggers** | Mention, Assign, Assign Reviewer |
| **Agent Tools** | 30+ GitLab built-in tools across 4 agents (incl. vulnerability linking) |
| **Detection** | 34 rules: 26 regex + 8 Semgrep (AI security, secrets, network) |
| **External SAST** | Dockerized bandit + semgrep pipeline with result merger |
| **Testing** | 76 pytest tests covering scoring, grading, and parsing |
| **Output** | Markdown MR comments, GitLab Issues, Fix MRs |

---

## Documentation

| Document | Description |
|:---------|:-----------|
| [`IMPLEMENTATION.md`](IMPLEMENTATION.md) | Architecture, scoring formula, demo script, judging alignment |
| [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md) | 7-step walkthrough with troubleshooting |
| [`docs/EXECUTION_PLAN.md`](docs/EXECUTION_PLAN.md) | 6-phase plan with ~35 granular tasks |
| [`docs/WOW_MOMENTS.md`](docs/WOW_MOMENTS.md) | Visual impact design & demo choreography |
| [`docs/DEVPOST_SUBMISSION.md`](docs/DEVPOST_SUBMISSION.md) | Copy-paste submission form text |
| [`AGENTS.md`](AGENTS.md) | Project-level scanning customization |
| [`docs/GITLAB_MIRROR_GUIDE.md`](docs/GITLAB_MIRROR_GUIDE.md) | GitHub → GitLab mirroring (3 methods) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute |

---

## Testing

```bash
# Run the full test suite (76 tests)
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=scripts --cov-report=term-missing
```

Tests cover: JSON loading, rule parsing, severity/category normalization, risk scoring formula, grade classification, bandit/semgrep output parsing, finding deduplication, and the CLI entry point.

---

## Demo

```bash
# Run the E2E demo (requires glab CLI + GitLab remote)
scripts/demo.sh

# Use a custom remote name
scripts/demo.sh --gitlab-remote origin

# Clean up demo branches and MRs
scripts/demo.sh --cleanup
```

The demo script creates a test MR with vulnerable code, triggers the auditor via `@mention`, and polls for results.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

**Quick summary:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request (GitHub) or Merge Request (GitLab)

---

## The AI Paradox — Why This Matters

<div align="center">

| Without AgentFlow Auditor | With AgentFlow Auditor |
|:--------------------------|:----------------------|
| MR waits 2+ days for review | **45 seconds** to full audit |
| SAST misses AI-specific risks | **34 rules** incl. 3 AI-specific threats |
| No fix suggestions | **Confidence-scored patches** (HIGH/MED/LOW) |
| SAFE scans waste fixer tokens | **Conditional routing** skips fixer |
| No tracking over time | **Cross-MR learning** + team posture |
| No energy awareness | **Green metrics** per scan |

</div>

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**One Trigger. Four Agents. Zero AI Blind Spots.**

Built with the [GitLab Duo Agent Platform](https://docs.gitlab.com/user/duo_agent_platform/) and [Anthropic Claude](https://www.anthropic.com/)

</div>
