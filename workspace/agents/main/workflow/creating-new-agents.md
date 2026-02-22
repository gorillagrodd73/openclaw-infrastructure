---
name: Creating New Agents
description: Process for bootstrapping a new autonomous agent in the system
agent: main
type: manual
---

# Creating New Agents

This workflow defines the steps to create and configure a new autonomous agent.

## Trigger

Run this workflow when a human requests creation of a new autonomous agent.

## Prerequisites

- Agent name decided (kebab-case recommended: `data-ingestion`, `notifier`, etc.)
- Purpose of the agent is understood

## Steps

### 1. Create Agent Directory Structure

Create the agent's folder and required subdirectories:

```bash
mkdir -p agents/{agent_name}/agent
mkdir -p agents/{agent_name}/sessions
mkdir -p agents/{agent_name}/workflow
```

**Example:**
```bash
mkdir -p agents/notifier/agent
mkdir -p agents/notifier/sessions
mkdir -p agents/notifier/workflow
```

### 2. Create Agent Workspace

Create the agent's workspace folder in `.openclaw/`:

```bash
mkdir -p ~/.openclaw/workspace-{agent_name}
```

**Example:**
```bash
mkdir -p ~/.openclaw/workspace-notifier
```

### 3. Create Core Agent Files

In the workspace folder, create the standard agent identity files:

| File | Purpose | Required |
|------|---------|----------|
| `IDENTITY.md` | Agent name, creature type, emoji, avatar | ✅ Yes |
| `SOUL.md` | Core personality, behavior, boundaries | ✅ Yes |
| `AGENTS.md` | How this agent relates to other agents | ✅ Yes |
| `USER.md` | Human relationship context (if applicable) | ✅ Yes |
| `TOOLS.md` | Tool-specific notes and preferences | ✅ Yes |
| `MEMORY.md` | Long-term curated memory storage | ✅ **Yes** |

Use existing agents as templates for content structure.

**Also create the memory directory for daily logs:**
```bash
mkdir -p ~/.openclaw/workspace-{agent_name}/memory
```

### 4. Configure Gateway

Edit the OpenClaw configuration to register the new agent:

```bash
# Open config file
openclaw config edit
```

Add the agent to the `agents` list:

```yaml
agents:
  - name: {agent_name}
    description: "Brief description of what this agent does"
    # Add any agent-specific settings
```

If the agent requires specific runtime flags (model, permissions, etc.), document them here.

### 5. Test Agent

Verify the agent loads correctly:

```bash
openclaw agent status {agent_name}
```

Or attempt to spawn the agent:

```bash
openclaw sessions_spawn --agent {agent_name} --task "hello"
```

### 6. Document Creation

Update `MEMORY.md` or daily notes with:
- Agent name and purpose
- Creation date
- Any special configuration notes

## Outputs

- New agent directory: `agents/{agent_name}/`
- New workspace: `~/.openclaw/workspace-{agent_name}/`
- Agent registered in config
- Agent can be spawned and accepts tasks

## Error Handling

If the agent fails to spawn:
1. Check config syntax is valid YAML
2. Verify folder permissions
3. Review agent identity files for required fields
4. Check OpenClaw logs for specific errors

---

*Created when we established agent conventions* 🦍
