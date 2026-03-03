# Custom Flows — Detailed Reference

> Source: https://docs.gitlab.com/user/duo_agent_platform/flows/custom/

## Overview

- Status: **Beta** (GitLab 18.8)
- LLM: Anthropic Claude Sonnet 4
- Custom flows are AI-powered workflows you create and configure

## Flow Visibility

- **Public**: Viewable by anyone, can be enabled in any project
- **Private**: Only members with Developer+ role can view
- Cannot change public→private if enabled

## Creating a Custom Flow

### From a Project
1. Search or go to → find project
2. Select **Automate** → **Flows**
3. Select **New flow**
4. Fill in:
   - **Display name**
   - **Description**
   - **Visibility**: Private or Public
5. Under **Configuration**:
   - Select **Flow**
   - Enter flow configuration YAML
   - Reference: [flow registry framework v1](https://gitlab.com/gitlab-org/modelops/applied-ml/code-suggestions/ai-assist/-/blob/main/docs/flow_registry/v1.md)
6. Select **Create flow**

### From AI Catalog
Same as above but through Explore → AI Catalog → Flows tab

## Enabling a Custom Flow

Flow is enabled in **top-level group + project** simultaneously.

### Triggers (selected when enabling)
- **Mention**: When service account user is @mentioned in comment on issue/MR
- **Assign**: When service account user is assigned to issue/MR
- **Assign reviewer**: When service account user is assigned as reviewer to MR

### Service Account
- Created automatically: `ai-<flow>-<group>` naming convention
- Example: `ai-security-scanner-gitlab-duo`
- Uses **composite identity** authentication
- Gets Developer role in projects

## Using a Custom Flow

1. Open issue, merge request, or epic
2. Trigger by: mentioning, assigning, or requesting review from the flow service account
3. Flow completes → confirmation + ready-to-merge change or inline comment

### Access Scope
Service account can access projects that:
- You have access to
- The flow has been added to

## Flow YAML Configuration

The YAML schema is documented in the flow registry framework:
https://gitlab.com/gitlab-org/modelops/applied-ml/code-suggestions/ai-assist/-/blob/main/docs/flow_registry/v1.md

### Key Concepts
- Steps define what the flow does
- Each step can use agents with specific tools
- Steps can be sequential or conditional
- Variables and context can be passed between steps
