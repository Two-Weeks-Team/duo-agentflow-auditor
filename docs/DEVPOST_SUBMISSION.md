# Devpost Submission Text

> Copy-paste this into the Devpost submission form at gitlab.devpost.com

---

## Project Name

Duo AgentFlow Auditor

## Short Description (one line)

AI Code Security — four agents that catch what SAST misses in AI-generated code: prompt injection, LLM output-to-exec, unsafe ML deserialization. One @mention, 45 seconds, zero blind spots.

## Full Description

### The Pain: AI Writes Vulnerable Code — and Nobody Catches It

40-62% of AI-generated code contains security vulnerabilities. Your team ships faster with AI copilots, but traditional SAST tools were built for human-written patterns — they miss the new risks AI introduces:

| AI-Specific Risk | Why SAST Misses It | Real Impact |
|------------------|--------------------|-------------|
| **Prompt injection** | No rule for LLM API input flows | Attacker hijacks your AI agent |
| **LLM output → exec** | SAST doesn't trace LLM response to eval() | Remote code execution via AI |
| **Unsafe ML deserialization** | pickle.load isn't flagged in ML context | Arbitrary code execution on model load |
| **AI-suggested anti-patterns** | eval(), shell=True, hardcoded secrets are "valid" code | Known CVE patterns reintroduced by AI |

Meanwhile, security reviews block MRs for hours. GitLab's 2025 DevSecOps Report: teams lose **7 hours/week** to AI-related inefficiencies, **70%** say AI makes compliance harder, **76%** discover issues post-deployment.

### The Solution: AgentFlow Auditor

One `@mention` triggers four specialized agents that scan, report, fix, and track — in 45 seconds:

**Scanner Agent** (10 tools) — Reads MR diffs against 34 detection rules (26 regex + 8 custom Semgrep). Dedicated AI-specific threat patterns: LLM prompt injection, output-to-exec, unsafe ML deserialization. Risk scores 0-100 with SAFE/WARNING/DANGER grading. Integrates with GitLab vulnerability management.

**Reporter Agent** (7 tools) — Posts scannable MR comments: grade + heatmap + top 5 findings, readable in 10 seconds. Collapsible details for deep dives. Links vulnerabilities to MRs. Auto-creates issues on DANGER grade.

**Fixer Agent** (8 tools) — Generates confidence-scored patches (HIGH/MEDIUM/LOW). `shell=True` → argument list, `eval()` → `ast.literal_eval()`, HTTP → HTTPS. Creates fix branch + MR automatically.

**Metrics Agent** (6 tools) — Cross-MR baseline tracking, risk drift detection, fix adoption rates, team security posture. Green metrics: token usage, energy (kWh), carbon footprint with real-world analogies.

**External SAST Scanner** (CI/CD) — Dockerized bandit + semgrep with 8 custom Semgrep rules. Python merger script unifies findings. 76 pytest tests validate scoring, grading, and parsing.

### What Makes It Different

**It's not another chatbot.** AgentFlow Auditor takes action — scans code, posts reports, creates fix MRs, tracks baselines. Every trigger produces tangible artifacts.

| Differentiator | Detail |
|----------------|--------|
| **AI-specific detection** | 3 custom Semgrep rules for LLM prompt injection, output-to-exec, unsafe ML deserialization — patterns no existing SAST tool catches |
| **Conditional flow routing** | SAFE scans skip fixer entirely — saves tokens and time via flow v1 router |
| **Multi-agent orchestration** | 4 agents with 30+ tools, chained via GitLab Flow Registry v1 |
| **Vulnerability linking** | Scanner feeds findings into GitLab vulnerability management; Reporter links them to MRs |
| **Confidence-aware fixes** | Fixer scores each patch HIGH/MEDIUM/LOW — never blindly applies uncertain changes |
| **Cross-MR learning** | Metrics agent detects persistent risks across scans, tracks fix adoption rates |
| **Production-grade validation** | 76 pytest tests, Dockerized SAST pipeline, E2E demo script |
| **Green by design** | Every scan reports energy footprint (kWh, kg CO₂) with optimization suggestions |

### The Numbers

| Metric | Value |
|--------|-------|
| Security review time | **7 hours → 45 seconds** |
| Detection rules | **34** (26 regex + 8 Semgrep) |
| AI-specific threat patterns | **3** (prompt injection, output-to-exec, unsafe ML deser) |
| Agent tools | **30+** across 4 agents |
| Test coverage | **76 pytest tests** passing |
| Flow routing | **Conditional** — SAFE skips fixer |

### Technology

| Component | Technology |
|-----------|-----------|
| **Platform** | GitLab Duo Agent Platform (Flow Registry v1, ambient environment) |
| **AI Model** | Anthropic Claude Sonnet |
| **Triggers** | Mention, Assign, Assign Reviewer |
| **Agent Tools** | 30+ GitLab built-in tools (incl. vulnerability linking) |
| **Detection** | 34 rules: 26 regex + 8 custom Semgrep (AI security, secrets, network) |
| **External SAST** | Dockerized bandit + semgrep + Python result merger |
| **Testing** | 76 pytest tests — scoring, grading, parsing |
| **Demo** | Automated E2E script (glab CLI) |
| **Configuration** | Flow YAML with conditional routing + AGENTS.md project customization |

### Impact

- **Solves the AI Paradox**: AI writes code faster, but also introduces novel security risks. AgentFlow Auditor closes the gap.
- **Catches what others miss**: The only tool detecting AI-specific threat patterns (LLM prompt injection, output-to-exec, unsafe deserialization) in merge request workflows.
- **Saves real time**: From 7-hour manual reviews to 45-second automated audits.
- **Green metrics built in**: Every scan reports its environmental footprint — encouraging efficient scanning practices.
- **Community-ready**: MIT licensed, documented, tested. Install by pushing to GitLab — catalog-sync handles the rest.

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
