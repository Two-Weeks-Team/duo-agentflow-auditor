# Triggers — Flow Trigger Reference

> Source: https://docs.gitlab.com/user/duo_agent_platform/triggers/

## Overview

- **Tier**: Premium, Ultimate
- **GA**: GitLab 18.8
- A trigger determines **when a flow runs**

## Event Types

| Event | Description |
|-------|-------------|
| **Mention** | When service account user is @mentioned in a comment on an issue or MR |
| **Assign** | When service account user is assigned to an issue or MR |
| **Assign reviewer** | When service account user is assigned as a reviewer to a MR |

## Creating a Trigger

### Prerequisites
- Maintainer or Owner role for the project

### Steps
1. Search or go to → find project
2. Select **Automate** → **Triggers**
3. Select **New flow trigger**
4. Fill in:
   - **Description**: What the trigger does
   - **Event types**: Select one or more (Mention, Assign, Assign reviewer)
   - **Service account**: Select user for composite identity
   - **Configuration source**:
     - **AI Catalog**: Select from configured flows
     - **Configuration path**: Enter path to flow config file (e.g., `.gitlab/duo/flows/claude.yaml`)
       - Requires `ai_catalog_create_third_party_flows` flag
5. Select **Create flow trigger**

## Configuration Path Option

When using **Configuration path**, the flow YAML file lives in your repository:
- Example path: `.gitlab/duo/flows/claude.yaml`
- Requires feature flag: `ai_catalog_create_third_party_flows`
- This enables file-based flow definitions (version-controlled in the repo)

## Trigger Management

- **Edit**: Automate → Triggers → Edit flow trigger (pencil icon)
- **Delete**: Automate → Triggers → Delete flow trigger (remove icon)
