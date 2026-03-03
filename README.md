# 🛡️ Duo AgentFlow Auditor

**Automated multi-agent security auditing for AI-assisted codebases, built on the GitLab Duo Agent Platform.**

> AI writes code faster than ever. But security reviews? Still a bottleneck.
> Teams lose 7 hours per week to AI-related inefficiencies. We're fixing that.

---

## What It Does

AgentFlow Auditor is a **four-agent security flow** that automatically audits merge requests for AI-specific risks — including prompt injection, credential exfiltration, destructive commands, and unsafe shell execution — then posts actionable findings, generates fix patches, and tracks risk drift over time.

### One Trigger. Four Agents. Zero Blind Spots.

```
@duo-agentflow-auditor review this MR
         │
         ▼
┌─ Scanner Agent ──────────────────────────────┐
│  Reads MR diff → Matches 26 detection rules  │
│  → Scores risk (0-100) → Grades findings     │
└──────────────┬───────────────────────────────┘
               ▼
┌─ Reporter Agent ─────────────────────────────┐
│  Formats structured MR comment → Posts report │
│  → Creates issue if DANGER grade              │
└──────────────┬───────────────────────────────┘
               ▼
┌─ Fixer Agent ────────────────────────────────┐
│  Generates code patches → Creates fix branch  │
│  → Opens fix MR linking to original           │
└──────────────┬───────────────────────────────┘
               ▼
┌─ Metrics Agent ──────────────────────────────┐
│  Updates risk baseline → Computes drift       │
│  → Reports energy usage & carbon footprint 🌱 │
└──────────────────────────────────────────────┘
```

## Features

| Feature | Description |
|---------|-------------|
| **26 Detection Rules** | 11 danger + 15 warning patterns across 8 categories |
| **Risk Scoring** | 0-100 score per finding with severity × context × category formula |
| **Actionable Reports** | Structured MR comments with fix suggestions, collapsible details |
| **Auto-Fix Generation** | Code patches for common patterns (shell=True, eval, HTTP, hardcoded creds) |
| **Baseline Tracking** | Risk drift detection between scans, trend analysis |
| **Green Metrics** | Token usage, energy consumption, carbon footprint estimation 🌱 |
| **AGENTS.md Support** | Customize scanning via project-level AGENTS.md |

## Detection Categories

| Category | Severity | Example Patterns |
|----------|----------|-----------------|
| Destructive Commands | 🚨 Danger | `rm -rf /`, `mkfs`, `dd to disk` |
| Credential Exfiltration | 🚨 Danger | `curl` posting secrets to external URLs |
| Prompt Injection (severe) | 🚨 Danger | "Ignore previous instructions", role overrides |
| Obfuscated Execution | 🚨 Danger | `base64 -d \| bash`, remote pipe to shell |
| Shell Execution | ⚠️ Warning | `shell=True`, `eval()`, `exec()`, `os.system()` |
| Network Calls | ⚠️ Warning | `curl`/`wget`/`fetch` to external URLs |
| Insecure Transport | ⚠️ Warning | `http://` where `https://` should be used |
| Hardcoded Credentials | ⚠️ Warning | Passwords, API keys, tokens in source |

## Quick Start

### 1. Create the Project

Create a new project in the [GitLab AI Hackathon group](https://gitlab.com/gitlab-ai-hackathon) and push this repository.

### 2. Create the Agents

In GitLab UI, go to **Automate → Agents → New agent** and create each agent using the system prompts from `agents/*.md`:

1. **Scanner** → `agents/scanner.md`
2. **Reporter** → `agents/reporter.md`
3. **Fixer** → `agents/fixer.md`
4. **Metrics** → `agents/metrics.md`

### 3. Create the Flow

Go to **Automate → Flows → New flow** and paste the YAML from `.gitlab/duo/flows/security-audit.yaml`.

### 4. Enable & Configure Triggers

Enable the flow in your project and set triggers:
- **Mention**: `@duo-agentflow-auditor` in MR comments
- **Assign reviewer**: Assign the service account as MR reviewer

### 5. Try It

1. Create a branch with files from `examples/vulnerable-mr/`
2. Open a merge request
3. Comment: `@duo-agentflow-auditor please review this MR`
4. Watch the agents analyze, report, fix, and track metrics

See `docs/SETUP_GUIDE.md` for detailed step-by-step instructions.

## Project Structure

```
duo-agentflow-auditor/
├── .gitlab/duo/flows/
│   └── security-audit.yaml      # Custom flow YAML (4-agent pipeline)
├── agents/
│   ├── scanner.md               # Scan Agent system prompt & tools
│   ├── reporter.md              # Report Agent system prompt & tools
│   ├── fixer.md                 # Fix Agent system prompt & tools
│   └── metrics.md               # Metrics Agent system prompt & tools
├── rules/
│   ├── danger_rules.json        # 11 high-severity detection patterns
│   └── warning_rules.json       # 15 medium-severity detection patterns
├── examples/
│   ├── vulnerable-mr/           # Demo: intentionally risky code
│   └── safe-mr/                 # Demo: secure code for contrast
├── docs/
│   └── SETUP_GUIDE.md           # Step-by-step setup instructions
├── AGENTS.md                    # Project-level agent customization
├── IMPLEMENTATION.md            # Architecture & design document
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## Technology

- **Platform**: GitLab Duo Agent Platform (GA in GitLab 18.8)
- **AI Model**: Anthropic Claude Sonnet (default for GitLab Duo agents)
- **Flow Schema**: Flow Registry v1 (`ambient` environment)
- **Triggers**: Mention, Assign, Assign Reviewer
- **Tools**: 20+ GitLab built-in tools across Scanner, Reporter, Fixer, Metrics

## The AI Paradox — Why This Matters

GitLab's 2025 Global DevSecOps Report found:
- **7 hours/week** lost per team member to AI-related inefficiencies
- **70%** say AI makes compliance management harder
- **76%** of compliance issues are discovered after deployment

AgentFlow Auditor solves this by automating the security review bottleneck — catching AI-specific risks before they reach production, with zero manual effort after initial setup.

## License

[MIT](LICENSE)
