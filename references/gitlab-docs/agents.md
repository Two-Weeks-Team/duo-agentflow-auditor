# GitLab Duo Agent Platform — Agents

> Source: https://docs.gitlab.com/user/duo_agent_platform/agents/

## Overview

- **Tier**: Premium, Ultimate
- **Offering**: GitLab.com, GitLab Self-Managed
- **GA**: GitLab 18.8
- **Default LLM**: Anthropic Claude Sonnet (via model_selection)

## Three Types of Agents

### 1. Foundational Agents
Pre-built, production-ready agents created by GitLab for common workflows.
- Come with specialized expertise and tools
- Turned on by default
- Available via GitLab Duo Chat
- Examples: GitLab Duo, Planner, Security Analyst, Data Analyst

### 2. Custom Agents
Agents you create and configure for your team's specific needs.
- Define behavior through **system prompts**
- Choose what **tools** they can access
- Ideal for specialized workflows not covered by foundational agents
- Enable in a group or project to use with Chat
- **Create via**: Project → Automate → Agents → New agent, OR AI Catalog

### 3. External Agents
Integrate with AI model providers outside GitLab.
- Allow model providers like Claude to operate in GitLab
- Trigger directly from discussion, issue, or merge request

## Custom Agent Configuration

### Required Fields
1. **Display name**: Name for the agent
2. **Description**: What the agent does
3. **Visibility**: Private or Public
4. **System prompt**: Defines personality, expertise, behavior

### Optional Fields
5. **Tools**: Select from available tools dropdown (see tools.md)

### Visibility Rules
- **Public**: Viewable by anyone, can be enabled in any project
- **Private**: Only members with Developer+ role can view; only managing project can use it
- Cannot make public→private if currently enabled

## Agent Lifecycle
1. **Create** → via Project or AI Catalog
2. **Enable** → in top-level group + project simultaneously
3. **Use** → via GitLab UI Chat, VS Code, or JetBrains IDEs
4. **Edit/Duplicate/Hide/Delete** → manage as needed
