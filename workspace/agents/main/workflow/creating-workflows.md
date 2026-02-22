---
name: Creating Workflows
description: Process for creating new workflows for myself or other agents
agent: main
type: meta
---

# Creating Workflows

This document defines the standard process for creating new workflows in our system.

## Purpose

Workflows define an agent's working process — what happens when a cron job runs. They are documentation-first, written in Markdown with YAML frontmatter for self-description.

## File Location

All workflows live at:

```
agents/{agent_name}/workflow/
```

Examples:
- `agents/main/workflow/` — Workflows for me (Grodd)
- `agents/ingestion/workflow/` — Workflows for a hypothetical ingestion agent
- `agents/notifier/workflow/` — Workflows for a notification agent

## File Structure

### 1. Filename

Use kebab-case (lowercase, hyphens between words):
- ✅ `daily-healthcheck.md`
- ✅ `process-incoming-emails.md`
- ❌ `DailyHealthcheck.md`
- ❌ `process_incoming_emails.md`

### 2. Frontmatter

Every workflow file MUST include YAML frontmatter at the top:

```yaml
---
name: Human-Readable Name
description: Brief description of what this workflow does
agent: main              # The agent that runs this workflow
type: cron | event | manual    # How this workflow is triggered
---
```

Required fields:
- **name**: Short, descriptive title
- **description**: One-sentence summary of purpose
- **agent**: The agent name (matches parent folder)

Optional fields:
- **type**: `cron` (scheduled), `event` (triggered), or `manual` (human-initiated)
- **schedule**: Cron expression if type is `cron` (e.g., `"0 9 * * *"`)
- **tags**: Array of relevant tags

### 3. Content

After the frontmatter, write the actual workflow process:

```markdown
# Workflow Title (matches frontmatter name)

## Trigger

When does this run? (e.g., "Daily at 9am PST", "On new email arrival", "When healthcheck fails")

## Steps

1. **Step Name**: Description of what to do
   - Sub-step details
   - Expected output
2. **Next Step**: Description
   - More details

## Dependencies

- List any external systems, files, or APIs this workflow relies on
- Note any required environment variables or credentials

## Error Handling

What to do if things go wrong:
- Retry logic
- Escalation paths
- Fallback actions

## Outputs

What does this workflow produce? (logs, notifications, files, side effects)
```

## Creating a New Workflow

### Step 1: Choose the Agent

Decide which agent will run this workflow. Create the folder if it doesn't exist:

```bash
mkdir -p agents/{agent_name}/workflow
```

### Step 2: Draft the Workflow

1. Create a new `.md` file in the appropriate `workflow/` folder
2. Add frontmatter with all required fields
3. Write the process documentation

### Step 3: Review

Before implementing:
- Does the workflow have a clear trigger?
- Are all dependencies documented?
- Is error handling defined?
- Is the output described?

### Step 4: Implement

Create the cron job or event handler that references this workflow file. The implementation code reads the workflow file and executes the documented steps.

### Step 5: Document

Update `MEMORY.md` or daily notes if this workflow represents a significant process change.

## Example

See this file (`creating-workflows.md`) as a working example of the structure.

---

## Conventions Summary

| Aspect | Convention |
|--------|------------|
| Location | `agents/{agent}/workflow/` |
| Naming | kebab-case.md |
| Format | Markdown with YAML frontmatter |
| Required frontmatter | `name`, `description`, `agent` |
| Optional fields | `type`, `schedule`, `tags` |

---

*Last updated: When Grodd created this* 🦍
