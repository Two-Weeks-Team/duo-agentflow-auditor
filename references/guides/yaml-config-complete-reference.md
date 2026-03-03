# GitLab Duo Agent Platform — Complete YAML Configuration Reference

> Source: Librarian research from official GitLab documentation

## 1. Custom Agents — UI-Based Configuration

Custom agents are created via GitLab UI (not YAML files directly):

```yaml
# Agent configuration structure (conceptual)
name: "Security Scanner"
description: "Scans code for security vulnerabilities"
visibility: private | public
system_prompt: |
  You are a security-focused code reviewer...
tools:
  - Read File
  - Grep
  - Get Merge Request
  - Create Issue
```

## 2. External Agent YAML — `.gitlab/duo/flows/` Directory

External agents run in CI/CD containers and are configured via YAML:

```yaml
# Claude Code Agent Example
injectGatewayToken: true
image: node:22-slim
commands:
  - npm install -g @anthropic-ai/claude-code
  - apt-get update --quiet && apt-get install --yes curl wget gpg git
  - curl --silent --show-error --location "https://raw.githubusercontent.com/upciti/wakemeops/main/assets/install_repository" | bash
  - apt-get install -y glab
  - mkdir -p ~/.config/glab-cli
  - |
    cat > ~/.config/glab-cli/config.yml <<EOF
    hosts:
      $AI_FLOW_GITLAB_HOSTNAME:
        token: $AI_FLOW_GITLAB_TOKEN
        is_oauth2: "true"
        api_host: $AI_FLOW_GITLAB_HOSTNAME
        user: ClaudeCode
    check_update: "false"
    git_protocol: https
    EOF
  - chmod 600 ~/.config/glab-cli/config.yml
  - git config --global user.email "claudecode@gitlab.com"
  - git config --global user.name "Claude Code"
  - git remote set-url origin https://gitlab-ci-token:$AI_FLOW_GITLAB_TOKEN@$AI_FLOW_GITLAB_HOSTNAME/$AI_FLOW_PROJECT_PATH.git
  - export ANTHROPIC_AUTH_TOKEN=$AI_FLOW_AI_GATEWAY_TOKEN
  - export ANTHROPIC_CUSTOM_HEADERS=$AI_FLOW_AI_GATEWAY_HEADERS
  - export ANTHROPIC_BASE_URL="https://cloud.gitlab.com/ai/v1/proxy/anthropic"
  - |
    claude --allowedTools="Bash(glab:*),Bash(git:*)" --permission-mode acceptEdits --verbose --output-format stream-json -p "
    Context: $AI_FLOW_CONTEXT
    Task: $AI_FLOW_INPUT
    Event: $AI_FLOW_EVENT
    "
variables:
  - ADDITIONAL_INSTRUCTIONS
```

## 3. Custom Flow YAML Schema (v1)

```yaml
version: "v1"
environment: ambient
components:
  - name: "security_scanner"
    type: AgentComponent
    prompt_id: "security_prompt"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:inputs.user_rule"
        as: "agents_dot_md"
        optional: true
      - from: "context:mr.diff"
        as: "code_diff"
    outputs:
      - name: "findings"
        as: "security_findings"
    toolset:
      - "get_repository_file"
      - "blob_search"
      - "create_issue"
      - "create_issue_note"
    ui_log_events:
      - "on_agent_final_answer"
      - "on_tool_execution_success"

  - name: "decision_gate"
    type: DecisionComponent
    condition: "len(security_findings) > 0"
    on_true:
      - action: "create_security_issue"
    on_false:
      - action: "post_approval"

routers:
  - from: "security_scanner"
    to: "decision_gate"
  - from: "decision_gate"
    to: "end"

flow:
  entry_point: "security_scanner"
```

## 4. CI/CD Environment Variables for External Agents

| Variable | Description |
|----------|-------------|
| `AI_FLOW_CONTEXT` | JSON-serialized parent object (diff, comments) |
| `AI_FLOW_EVENT` | Trigger event type (mention, assign, assign_reviewer) |
| `AI_FLOW_INPUT` | User prompt from comment |
| `AI_FLOW_GITLAB_TOKEN` | Service account PAT |
| `AI_FLOW_GITLAB_HOSTNAME` | GitLab instance hostname |
| `AI_FLOW_PROJECT_PATH` | Full project path |
| `AI_FLOW_AI_GATEWAY_TOKEN` | AI Gateway auth token |
| `AI_FLOW_AI_GATEWAY_HEADERS` | Formatted API headers |

## 5. Model Selection

| Model | Available |
|-------|-----------|
| Claude Sonnet 4 / 4.5 / 4.6 | Yes |
| Claude Haiku 4.5 | Yes (default for Chat) |
| Claude Opus 4.5 / 4.6 | Yes |
| GPT-5 / 5.2 / 5 Mini / 5 Codex | Yes |

- **Default (Chat)**: Claude Haiku 4.5
- **Default (Agents)**: Claude Sonnet 4.5 Vertex
