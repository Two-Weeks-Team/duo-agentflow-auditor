# Agent Tools — Available Tools for Custom Agents

> Source: https://docs.gitlab.com/user/duo_agent_platform/agents/tools/

## Full Tool List

### Code & File Operations
| Tool | Description |
|------|-------------|
| Read File | Read the contents of a file |
| Read Files | Read the contents of multiple files |
| Edit File | Edit existing files |
| Create File With Contents | Create a file and write content to it |
| Find Files | Recursively find files in a project |
| List Dir | List files in a directory relative to project root |
| List Repository Tree | List files and directories in a repository |
| Mkdir | Create a directory in the current working tree |
| Grep | Recursively search for text patterns (respects .gitignore) |
| Extract Lines From Text | Extract specific lines from text |
| Run Command | Run bash commands (Git commands NOT supported) |
| Run Git Command | Run Git commands in current working directory |

### Search Tools
| Tool | Description |
|------|-------------|
| Gitlab Blob Search | Search for file contents in a group or project |
| Gitlab Commit Search | Search for commits in a project or group |
| Gitlab Issue Search | Search for issues in a project or group |
| Gitlab Merge Request Search | Search for MRs in a project or group |
| Gitlab Milestone Search | Search for milestones in a project or group |
| Gitlab Note Search | Search for notes in a project |
| Gitlab Group Project Search | Search for projects in a group |
| Gitlab User Search | Search for users in a project or group |
| Gitlab Wiki Blob Search | Search wiki contents in a project or group |
| Gitlab Documentation Search | Search GitLab documentation |

### Issue & Work Item Management
| Tool | Description |
|------|-------------|
| Create Issue | Create issues in a project |
| Get Issue | Get an issue from a project |
| Update Issue | Update an issue in a project |
| List Issues | List all issues in a project |
| Create Issue Note | Add notes to an issue |
| List Issue Notes | List all notes on an issue |
| Get Issue Note | Get a note from an issue |
| Create Work Item | Create a work item in a group or project |
| Get Work Item | Get a work item |
| Update Work Item | Update an existing work item |
| List Work Items | List work items in a project or group |
| Create Work Item Note | Add a note to a work item |
| Get Work Item Notes | Get all notes for a work item |

### Merge Request Management
| Tool | Description |
|------|-------------|
| Create Merge Request | Create MRs in a project |
| Get Merge Request | Get details about a MR |
| Update Merge Request | Update a MR (target branch, title, close) |
| Create Merge Request Note | Add notes to a MR (no quick actions) |
| List All Merge Request Notes | List all notes on a MR |
| List Merge Request Diffs | List diffs of changed files in a MR |
| Build Review Merge Request Context | Build comprehensive MR context for code review |
| Post Duo Code Review | Post a GitLab Duo code review to a MR |

### Git & Commits
| Tool | Description |
|------|-------------|
| Get Commit | Get a commit from a project |
| Get Commit Comments | Get comments of a commit |
| Get Commit Diff | Get diff of a commit |
| List Commits | List commits in a project |
| Create Commit | Create commit with multiple file actions |

### Epics
| Tool | Description |
|------|-------------|
| Create Epic | Create epics in a group |
| Get Epic | Get an epic in a group |
| Update Epic | Update an epic in a group |
| List Epics | List all epics of a group and subgroups |
| Get Epic Note | Get a note from an epic |
| List Epic Notes | List all notes for an epic |

### CI/CD & Pipeline
| Tool | Description |
|------|-------------|
| Ci Linter | Validate CI/CD YAML against syntax rules |
| Get Job Logs | Get the trace for a job |
| Get Pipeline Errors | Get logs for failed jobs from latest pipeline of MR |
| Get Pipeline Failing Jobs | Get IDs for failed jobs in a pipeline |
| Run Tests | Execute test commands for any language/framework |

### Security & Vulnerability
| Tool | Description |
|------|-------------|
| List Vulnerabilities | List security vulnerabilities (filter by severity/report type) |
| Get Vulnerability Details | Get vulnerability info (location, CVE, pipeline, report data) |
| Dismiss Vulnerability | Dismiss a vulnerability with optional comment |
| Confirm Vulnerability | Change state to CONFIRMED |
| Revert To Detected Vulnerability | Revert state to detected |
| Update Vulnerability Severity | Update severity level |
| Create Vulnerability Issue | Create issue linked to vulnerabilities |
| Link Vulnerability To Issue | Link issue to vulnerabilities |
| Link Vulnerability To Merge Request | Link vulnerability to MR |
| Get Security Finding Details | Get potential vulnerability details |
| List Security Findings | List findings from pipeline security scan |
| Post Sast Fp Analysis To Gitlab | Post SAST false positive analysis |

### Task & Planning
| Tool | Description |
|------|-------------|
| Create Plan | Create a list of tasks |
| Get Plan | Get a list of tasks |
| Add New Task | Add a task |
| Remove Task | Remove a task by ID |
| Set Task Status | Set status of a task |
| Update Task Description | Update description of a task |

### Audit & API
| Tool | Description |
|------|-------------|
| List Project Audit Events | List audit events for a project (Owner role required) |
| List Group Audit Events | List audit events for a group |
| List Instance Audit Events | List instance-level audit events (admin required) |
| Gitlab Api Get | Read-only GET requests to any REST API endpoint |
| Gitlab Graphql | Read-only GraphQL queries |

### Other
| Tool | Description |
|------|-------------|
| Get Project | Get details about a project |
| Get Current User | Get username, job title, preferred languages |
| Get Previous Session Context | Get context from a previous session |
| Get Wiki Page | Get a wiki page with all comments |
