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
