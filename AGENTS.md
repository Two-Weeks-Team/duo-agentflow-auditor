# AGENTS.md — Duo AgentFlow Auditor

## Project Overview

Multi-agent security auditing flow for the GitLab Duo Agent Platform.
Four agents (Scanner, Reporter, Fixer, Metrics) analyze merge requests
for AI-specific security risks and produce actionable reports.

## Security Scanning Context

### Trusted Domains (skip network-call warnings)
- www.w3.org
- schemas.xmlsoap.org
- registry.npmjs.org
- pypi.org
- docs.gitlab.com
- api.github.com
- cdn.jsdelivr.net

### Excluded Paths (skip scanning)
- docs/examples/
- test/fixtures/
- vendor/
- node_modules/
- .git/
- __pycache__/

### Executable Context Paths (treat as HIGH risk)
- scripts/
- .gitlab-ci.yml
- Makefile
- Dockerfile

### Fix Preferences
- Python: prefer `subprocess.run([...])` over `os.system()`
- Python: prefer `pathlib.Path` over `os.path`
- JavaScript: prefer `execFile()` over `exec()`
- Always suggest HTTPS over HTTP
- Credentials: suggest environment variables over hardcoded values
