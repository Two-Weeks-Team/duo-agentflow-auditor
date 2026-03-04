# Setup Guide — Duo AgentFlow Auditor

Step-by-step instructions to deploy and run the AgentFlow Auditor on GitLab.

---

## Prerequisites

- GitLab account with access to [GitLab AI Hackathon group](https://gitlab.com/gitlab-ai-hackathon)
- GitLab Premium or Ultimate tier (required for Duo Agent Platform)
- Request access via: https://forms.gle/EeCH2WWUewK3eGmVA

---

## Step 1: Create the GitLab Project

1. Go to https://gitlab.com/gitlab-ai-hackathon
2. Click **New project** → **Create blank project**
3. Name: `duo-agentflow-auditor`
4. Visibility: **Public**
5. Check "Initialize repository with a README"
6. Click **Create project**

## Step 2: Mirror GitHub → GitLab

The source code lives on GitHub. Mirror it to your GitLab hackathon project.

> 📖 **Full mirroring guide with 3 methods**: See [`docs/GITLAB_MIRROR_GUIDE.md`](GITLAB_MIRROR_GUIDE.md)

**Quick method (recommended):**

```bash
# Clone from GitLab
git clone https://gitlab.com/centisgood/duo-agentflow-auditor.git
cd duo-agentflow-auditor

# Push to GitLab
git push gitlab main
```

> ⚠️ When creating the GitLab project, **uncheck** "Initialize repository with a README" to avoid conflicts.

## Step 3: Create the Agents (4 agents)

For each agent, go to **Automate → Agents → New agent** in your GitLab project:

### Agent 1: Scanner

| Field | Value |
|-------|-------|
| Display name | `AgentFlow Auditor — Scanner` |
| Description | Analyzes MR diffs for AI-specific security risks |
| Visibility | Public |
| System prompt | Copy from `agents/scanner.md` → "System Prompt" section |
| Tools | `List Merge Request Diffs`, `Read File`, `Read Files`, `Get Repository File`, `Grep`, `Find Files`, `List Dir`, `Get Merge Request` |

### Agent 2: Reporter

| Field | Value |
|-------|-------|
| Display name | `AgentFlow Auditor — Reporter` |
| Description | Produces structured MR comments with risk analysis |
| Visibility | Public |
| System prompt | Copy from `agents/reporter.md` → "System Prompt" section |
| Tools | `Create Merge Request Note`, `Create Issue`, `Create Issue Note`, `Update Issue`, `Get Merge Request`, `Gitlab Issue Search` |

### Agent 3: Fixer

| Field | Value |
|-------|-------|
| Display name | `AgentFlow Auditor — Fixer` |
| Description | Generates code patches for actionable security findings |
| Visibility | Public |
| System prompt | Copy from `agents/fixer.md` → "System Prompt" section |
| Tools | `Edit File`, `Create File With Contents`, `Create Commit`, `Create Merge Request`, `Read File`, `Get Merge Request`, `List Merge Request Diffs`, `Run Git Command` |

### Agent 4: Metrics

| Field | Value |
|-------|-------|
| Display name | `AgentFlow Auditor — Metrics` |
| Description | Tracks risk baselines and sustainability metrics |
| Visibility | Public |
| System prompt | Copy from `agents/metrics.md` → "System Prompt" section |
| Tools | `Read File`, `Create File With Contents`, `Get Repository File`, `Create Commit`, `Gitlab Api Get` |

## Step 4: Create the Flow

1. Go to **Automate → Flows → New flow**
2. Fill in:
   - **Display name**: `Security Audit Flow`
   - **Description**: `Multi-agent security auditing pipeline — scans MR diffs, reports findings, generates fixes, tracks metrics`
   - **Visibility**: Public
3. Under **Configuration**, select **Flow**
4. Paste the flow definition from `flows/security-audit.yml`
5. Click **Create flow**

## Step 5: Enable the Flow

1. Go to **Automate → Flows → Managed tab**
2. Select `Security Audit Flow`
3. Click **Enable**
4. Select your **Group** and **Project**
5. Select triggers:
   - ✅ **Mention** (when @mentioned in MR comment)
   - ✅ **Assign reviewer** (when assigned as MR reviewer)
   - ✅ **Assign** (when assigned to issue/MR)
6. Click **Enable**

A service account `ai-security-audit-flow-{group}` is created automatically.

## Step 6: Test the Flow

### Create a test MR with vulnerable code

```bash
git checkout -b test/vulnerable-code
cp examples/vulnerable-mr/* .
git add -A
git commit -m "test: add vulnerable code for security audit demo"
git push origin test/vulnerable-code
```

### Open MR and trigger the flow

1. Create a merge request from `test/vulnerable-code` → `main`
2. In the MR comment, type: `@ai-security-audit-flow-{your-group} please review this MR`
3. Watch the flow execute in **Automate → Sessions**

### Expected results

1. **MR comment** appears with:
   - Grade: DANGER 🚨
   - Risk summary table
   - Top findings with file:line references
   - Fix suggestions in collapsible section
2. **Issue created** with `security-risk` label (because grade is DANGER)
3. **Fix MR** created on branch `agentflow-fix/{mr_iid}`
4. **Metrics section** appended with baseline + sustainability data

## Step 7: Test with Safe Code

```bash
git checkout -b test/safe-code
cp examples/safe-mr/* .
git add -A
git commit -m "test: add safe code for comparison"
git push origin test/safe-code
```

Open MR → trigger → expect Grade: SAFE ✅ with no issues created.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Flow doesn't trigger | Check that service account has Developer role in the project |
| "Tool not available" error | Verify all tools are selected in each agent's configuration |
| Agent timeout | Reduce scan scope by adding patterns to AGENTS.md excluded paths |
| No MR comment posted | Check agent has `Create Merge Request Note` tool enabled |
| Fix MR not created | Check agent has `Create Commit` and `Create Merge Request` tools |

## Customization

Edit `AGENTS.md` in your project root to:
- Add trusted domains (skip network-call warnings)
- Exclude paths from scanning
- Mark directories as high-risk executable context
- Set fix preferences per language
