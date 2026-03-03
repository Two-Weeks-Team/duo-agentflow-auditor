# GitLab Duo Agent Platform — Complete Getting Started Guide

> Source: https://about.gitlab.com/blog/gitlab-duo-agent-platform-complete-getting-started-guide/

## Evolution

- **Duo Pro** → 1:1 developer-AI in IDE (code suggestions + chat)
- **Duo Enterprise** → 1:1 AI across entire SDLC
- **Duo Agent Platform** → **Many-to-many** team-agent collaboration, autonomous task handling

## The Complete 8-Part Series

| Part | Title | Key Topics |
|------|-------|------------|
| 1 | Introduction to GitLab Duo Agent Platform | Architecture, 4 ways to use agents, sessions, model selection |
| 2 | Getting Started with Agentic Chat | Accessing chat (Web UI + IDEs), model switching, agent selection |
| 3 | Understanding Agents | Foundational, Custom, External agents; AGENTS.md customization |
| 4 | Understanding Flows | Foundational/custom YAML workflows, multi-agent orchestration |
| 5 | AI Catalog | Discover, create, share agents and flows; visibility management |
| 6 | Monitor & Automate | Automate menu, sessions monitoring, event-driven triggers |
| 7 | MCP Integration | GitLab as MCP client, GitLab as MCP server, configuration |
| 8 | Customization | Custom chat rules, AGENTS.md, system prompts, flow YAML config |

## Core Components

| Component | Description |
|-----------|-------------|
| **Duo Agentic Chat** | Primary interface; Web UI + IDEs; model selection; conversation history |
| **Agents** | Specialized AI assistants: Foundational, Custom, External |
| **Flows** | Multi-step workflows: Foundational (Developer, Fix CI/CD), Custom (YAML) |
| **AI Catalog** | Central repository for discovering/sharing agents and flows |
| **Automate Menu** | Management hub: Sessions, Flows, Agents, Triggers |
| **MCP** | Model Context Protocol: Client (connect to Jira/Slack/AWS) + Server (for Claude Desktop/Cursor) |

## Key Terminology

| Term | Definition |
|------|-----------|
| **Agent** | Specialized AI assistant for specific tasks |
| **Foundational Agent** | Pre-built by GitLab (GitLab Duo, Planner, Security Analyst, Data Analyst) |
| **Custom Agent** | Created by you with custom system prompts and tools |
| **External Agent** | External AI providers (Claude, OpenAI, Gemini) integrated into platform |
| **Flow** | Combination of 1+ agents solving a complex problem |
| **Foundational Flow** | Pre-built (Issue to MR, Fix Pipeline, Convert Jenkins, SW Dev Flow) |
| **Custom Flow** | YAML-defined workflows you create |
| **Trigger** | Event that auto-starts a flow (mention, assignment, review request) |
| **Session** | Record of agent/flow activity with complete logs |
| **System Prompt** | Instructions defining agent behavior, expertise, communication style |
| **Service Account** | Account used by flows to perform GitLab operations |
| **MCP** | Model Context Protocol for external integrations |
| **AGENTS.md** | Industry-standard file for customizing agent behavior |
| **Custom Rules** | Rules customizing GitLab Duo behavior in IDE |
| **Tools** | Capabilities agents use (create issues, MRs, run pipelines, analyze code) |
