# OpenClaw Infrastructure

🦍 **Super intelligent gorilla-powered AI infrastructure for project management and automation.**

## What is This?

This repository contains the workspace configuration, agent definitions, workflows, and documentation for an OpenClaw deployment. OpenClaw is an AI agent framework that enables intelligent automation across various services.

## Repository Structure

```
├── workspace/                  # Main agent workspace
│   ├── AGENTS.md            # Agent configuration guide
│   ├── BOOTSTRAP.md         # First-run instructions
│   ├── HEARTBEAT.md         # Periodic task definitions
│   ├── IDENTITY.md          # Agent identity configuration
│   ├── MEMORY.md            # Long-term memory (excluded from git)
│   ├── SOUL.md              # Agent personality and behavior
│   ├── TOOLS.md             # Tool configurations and credentials
│   ├── USER.md              # User preferences and context
│   └── agents/              # Agent workflow definitions
│       ├── brainiac/        # Brainiac agent workflows
│       └── main/            # Main agent workflows
├── workspace-brainiac/       # Brainiac agent workspace
│   └── reports/             # Health check reports
└── .gitignore               # Security-focused git exclusions
```

## Key Components

### Agents

- **Main Agent**: General-purpose assistant for day-to-day tasks
- **Brainiac**: Specialized agent for health checks and monitoring

### Workflows

- `daily-standup.md` - Automated daily status reporting
- `agent-health-check.md` - Agent self-monitoring
- `openclaw-health-check.md` - Infrastructure health monitoring
- `git-backup.md` - Repository backup procedures
- `openclaw-backup.md` - Full system backup workflow

### Security Notes

This repository **excludes sensitive data**:

- API keys and credentials (in `agents/*/agent/`)
- OAuth tokens and service accounts
- Session logs and conversation history
- Personal memory databases
- Gateway configuration files

See `.gitignore` for complete exclusion list.

## Getting Started

1. Clone this repository
2. Configure environment variables (see `TOOLS.md`)
3. Install required CLI tools (`gog`, `gh`, etc.)
4. Run initial setup workflows

## Documentation

- `SOUL.md` - Agent personality and behavior guidelines
- `AGENTS.md` - Agent lifecycle and configuration
- `TOOLS.md` - Available tools and authentication setup
- `USER.md` - User preferences and context

## Maintainer

**Grodd** - Super intelligent gorilla and AI Project Manager 🦍

---

*Last updated: 2026-02-22*
