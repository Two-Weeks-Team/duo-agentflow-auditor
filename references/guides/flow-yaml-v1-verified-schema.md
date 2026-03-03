# Flow Registry v1 — Verified YAML Schema

> Source: Librarian research from official GitLab ai-assist repo (verified)

## Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | ✅ | Always `"v1"` |
| `environment` | string | ✅ | `ambient` / `chat` / `chat-partial` |
| `components` | list | ✅ | Array of component definitions |
| `routers` | list | ✅ | Define flow between components (can be `[]`) |
| `flow` | object | ✅ | Contains `entry_point` + optional `inputs` |
| `prompts` | list | ✅ if local | Inline prompt templates |

## Component Types

1. **AgentComponent** — Multi-turn AI agent
2. **OneOffComponent** — Single-round with retry (max_correction_attempts)
3. **DeterministicStepComponent** — Single tool, no AI

## Environment Values

| Value | Use Case |
|-------|----------|
| `ambient` | Background/hands-off (human delegates to agent) |
| `chat` | Full collaborative conversation |
| `chat-partial` | Single-agent chat (only ONE AgentComponent) |

## Tool Names (snake_case)

`read_file`, `read_files`, `edit_file`, `create_file_with_contents`, `find_files`,
`list_dir`, `grep`, `run_command`, `run_git_command`, `get_issue`, `create_issue`,
`create_issue_note`, `update_issue`, `get_merge_request`, `create_merge_request`,
`create_merge_request_note`, `list_merge_request_diffs`, `get_repository_file`,
`list_repository_tree`, `post_duo_code_review`, `build_review_merge_request_context`,
`get_pipeline_failing_jobs`, `create_commit`, `gitlab_api_get`, `gitlab_graphql`

## Input Chaining Between Components

```yaml
# Context variables
- from: "context:goal"                                    # User's input
- from: "context:project_id"                              # Project ID
- from: "context:inputs.user_rule"                        # AGENTS.md content
- from: "context:{component_name}.final_answer"           # Previous agent's answer
- from: "context:{component_name}.tool_responses"         # Previous tool results
- from: "context:{component_name}.execution_result"       # "success" or "failed"
# Literal values
- from: "true"
  as: "flag"
  literal: true
```
