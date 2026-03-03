# GitLab Duo Agent Platform — Flows

> Source: https://docs.gitlab.com/user/duo_agent_platform/flows/

## Overview

- **Tier**: Premium, Ultimate
- **Offering**: GitLab.com, GitLab Self-Managed, GitLab Dedicated
- **LLM**: Anthropic Claude Sonnet 4
- **GA**: Foundational flows in GitLab 18.8; Custom flows beta in 18.8

## What is a Flow?

A flow is a **combination of one or more agents** working together to solve a complex problem.

## Two Types

### 1. Foundational Flows
Pre-built, production-ready workflows created by GitLab.
- Issue to MR (software development)
- Fix CI/CD Pipeline
- Convert Jenkins
- Software Development Flow

### 2. Custom Flows
Workflows you create to automate your team's specific processes.
- Define workflow steps and agents in YAML
- Define triggers to control when the flow runs
- Beta status in GitLab 18.8

## Where Flows Run

- **UI**: Directly in GitLab CI/CD (automate without leaving browser)
- **IDEs**: Software development flow available in VS Code, Visual Studio, JetBrains

## Execution

Flows execute in CI/CD. For security, use composite identity.

## AGENTS.md Customization

Use `AGENTS.md` files to provide context and instructions for flows.
See: https://docs.gitlab.com/user/gitlab_duo/customize_duo/agents_md/

## Prerequisites

1. Meet GitLab Duo Agent Platform prerequisites
2. Turn on flows with GitLab Duo settings
3. For code-creating flows: configure push rules to allow service account

## Monitor Running Flows

1. Search or go to → find your project
2. Select **Automate** → **Sessions**

## Flow History in IDEs

On the **Flows** tab → scroll to **Recent agent sessions**
