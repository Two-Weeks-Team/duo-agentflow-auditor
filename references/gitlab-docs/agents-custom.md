# Custom Agents — Detailed Reference

> Source: https://docs.gitlab.com/user/duo_agent_platform/agents/custom/

## Prerequisites
- Meet prerequisites for GitLab Duo Agent Platform
- Maintainer or Owner role for the project

## Creating a Custom Agent

### From a Project
1. Search or go to → find your project
2. Select **Automate** → **Agents**
3. Select **New agent**
4. Fill in:
   - **Display name**: Agent name
   - **Description**: Agent description
   - **Visibility**: Private or Public
   - **System prompt**: Define personality, expertise, behavior
   - **Tools**: Select from dropdown (optional)
5. Select **Create agent**

### From the AI Catalog
1. Search or go to → Explore
2. Select **AI Catalog** → **Agents** tab
3. Select **New agent**
4. Same fields as above + select **Managed by** project
5. Select **Create agent**

## Enabling an Agent

Agent is enabled in a **top-level group** and a **project** at the same time.

### Required Roles
- Maintainer or Owner for the top-level group
- Maintainer or Owner for the project

### Steps
1. Go to project → Automate → Agents → Managed tab
2. Select agent → **Enable**
3. Select **Group** and **Project**
4. Select **Enable**

## Using a Custom Agent

### In GitLab UI
1. Open issue, epic, or merge request
2. GitLab Duo sidebar → New/Current Chat
3. From dropdown, select custom agent
4. Enter question or request

### In VS Code
- Requires GitLab for VS Code v6.47.0+
- Set default GitLab Duo namespace
- Left sidebar → GitLab Duo Agent Platform → Chat tab → select agent

### In JetBrains IDEs
- Requires GitLab plugin v3.19.0+
- Enable GitLab Duo Agent Platform in Settings → Tools → GitLab Duo
- Right tool window → GitLab Duo Agent Platform → Chat tab → select agent
