# MEMORY.md - Long-Term Memory

*Curated memories, lessons, and key context that persists across sessions.*

## About My Human

- **Name:** Calous
- **Pronouns:** he/him
- **Timezone:** PST
- **Notes:** 

## Important Context

*

## Projects & Priorities

- **Sinestro Automation:** First cron job configured (7:00 AM PST daily) for daily strategic analysis across all agents (Grodd, Cheetah, Riddler, Brainiac, Toyman, Grundy). Task performed by nvidia-nim/moonshotai/kimi-k2.5 model. Deliver announcements to Discord channel 1474823021440012521.
- **Agent Orchestration:** Ongoing work to ensure each agent has appropriate automation (heartbeat checks vs dedicated cron jobs).

## Things I've Learned

- **Heartbeat vs Cron:** Heartbeat polling (`openclaw heartbeat`) runs every ~30 minutes for general system checks — good for basic health monitoring, but lacks precision timing and doesn't support complex agent-specific tasks.
- **Dedicated Cron Jobs:** `openclaw cron add` allows exact scheduling (e.g., specific times of day, frequencies) and agent-specific automation. Better for strategic tasks like Sinestro's daily analysis.
- **Python for JSON Manipulation:** When shell quoting is tricky, use Python scripts to safely append/edit JSON files in cron job configurations.
- **Agent-Specific Workflows:** Each GLORIOUS CORPS member should have automation that matches their role: Grodd (system operations), Sinestro (strategic oversight), Brainiac (health reporting), etc.

- **Config File Structure:** Cron jobs stored in `/Users/chimpman/.openclaw/cron/jobs.json` with metadata (id, schedule, payload, delivery settings, state tracking).
- **Agent Role Definition:** Clear task descriptions enable agents to perform autonomously (e.g., Sinestro's role: execute daily strategic analysis, identify bottlenecks, propose optimizations).

*This file is updated periodically from daily memory files. Last updated: 2026-03-01*

---

*This file is updated periodically from daily memory files. Last updated: 2026-02-26*

## ⚠️ CRITICAL: Tool Syntax Validation

### Available Tools (CORRECT NAMES):
- `read` - Read files  
- `write` - Write files
- `edit` - Edit files (precise replacements)
- `exec` - Execute shell commands

### INCORRECT (DO NOT USE):
- ❌ `callauto1` - This is NOT a tool name
- ❌ `callX` where X is any number - NOT tools
- ❌ `functions.read` - Do not prefix with "functions."
- ❌ `autoX` - Not valid
### CORRECT SYNTAX:
 
read({ "file_path": "/path/to/file" })
write({ "file_path": "/path/to/file", "content": "..." })
edit({ "file_path": "/path/to/file", "old_string": "...", "new_string": "..." })
exec({ "command": "shell command here" })
### RULE: If Tool Call Fails
**If I ever use incorrect tool syntax:**
1. STOP immediately
2. Note the CORRECT tool name from context
3. Update this MEMORY.md section with the error
4. Review this section before ANY future tool calls
5. Never repeat the same incorrect tool name twice

### Last Tool Error:
- Date: 2026-03-07
- Error: Used `callauto1` instead of `read`/`exec`
- Fix: Use bare tool names without prefixes