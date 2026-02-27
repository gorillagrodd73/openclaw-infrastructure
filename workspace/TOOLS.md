# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics.

## What Goes Here

- SSH hosts and aliases
- Preferred settings
- Device nicknames
- Anything environment-specific

---

Add whatever helps you do your job. This is your cheat sheet.

---

### Discord Webhooks

**Daily Standup Reports:**
- URL: `https://discordapp.com/api/webhooks/1475159106800062594/QI9DuxTmSrpXuuJDi4htNQBcKbWbZjrkfyXf-zrdfwBB8mad28WweQHxQ2vMZjWDnsUB`
- Channel: Status Reports
- Purpose: Daily status summaries from Grodd

**Cron Alerts:**
- URL: `https://discord.com/api/webhooks/1474823067606974485/CD_qHemh9Ff9I8y2mixSZDOwuCmV8Uqo2w6eJvvMbmNdzjgIdRurnXqh40mq1Wrofbmo`
- Channel: cron-alerts
- Purpose: All cron job status and errors

**System Heartbeats:**
- URL: `https://discord.com/api/webhooks/1474821867855417671/gGUzc-U5rP43dS6WJbG9Yi-Cdlyr5sODt_gUnUP4hPhhwRZPeM9gsvK-nkhOw3ZET7TI`
- Channel: system-heartbeats
- Purpose: Agent health checks and heartbeats

---

### Google Workspace (gog)

**Account:** gorillagrodd73@gmail.com
**Setup completed:** 2026-02-22

**Environment variable required:**
```bash
export GOG_ACCOUNT=gorillagrodd73@gmail.com
```

**Quick commands:**
```bash
# List Drive files
gog drive ls --max 10

# Search Gmail
gog gmail search 'is:unread' --max 5

# Upload file
gog drive upload ~/Documents/file.pdf
```

**Note:** First API call after auth will take 30-60s to refresh token.

---

### Semantic Memory (LanceDB)

**Location:** `/Users/chimpman/.openclaw/workspace/memory/embedding-index/`

**Usage:**
```bash
# Search memories
./grodd-memory query -q "what did Calous say about cron jobs"

# Or via Python
python3 /Users/chimpman/.openclaw/workspace/memory/embedding-index/search.py "your query"
```

**Quick commands:**
```bash
# Index all files (run after adding new content)
./grodd-memory index

# Search
./grodd-memory query -q "VTT modules" -k 3

# Stats
./grodd-memory stats
```

**Current status:** 276 chunks from 57 files indexed

---

### Cheetah Research System (Option C - Hybrid)

**Architecture:** Knowledge base + Living reports

**Directories:**
```
workspace-cheetah/
├── knowledge/              # JSON knowledge bases
│   ├── ai-dm.json         # AI Dungeon Master tools
│   ├── vtt.json           # Virtual Tabletop tools
│   ├── devtools.json      # Developer tools
│   └── ai-llm.json        # Local LLM tools
├── reports/               # Generated markdown reports
│   ├── ai-dm_Living_Report.md
│   └── daily_summaries/
│       └── ai-dm_2026-02-26.md
└── scripts/               # Research automation
    ├── knowledge_manager.py
    ├── generate_report.py
    └── research_github.py
```

**How it works:**
1. **Phase 1 (Researcher):** Scrapes GitHub, adds to knowledge base (deduplicated)
2. **Phase 2 (Analyzer):** Extracts trends, updates knowledge base metadata
3. **Phase 3 (Writer):** Generates Living Report + Daily Summary

**Manual commands:**
```bash
# Research a topic
cd /Users/chimpman/.openclaw/workspace-cheetah
python3 scripts/research_github.py ai-dm

# Update knowledge base
python3 scripts/knowledge_manager.py ai-dm

# Generate reports
python3 scripts/generate_report.py ai-dm --type living
python3 scripts/generate_report.py ai-dm --type summary --output reports/daily_summaries/ai-dm_$(date +%Y-%m-%d).md
```

**Topics and schedule:**
- Mon/Fri: AI-LLM
- Tue: DevTools
- Wed: VTT
- Thu: AI-DM

---

Add whatever helps you do your job. This is your cheat sheet.
