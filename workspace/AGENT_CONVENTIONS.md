# Agent Directory Conventions

**Approved:** 2026-02-25  
**Status:** ACTIVE

## Philosophy
- Main is special (workspace root)
- All other agents follow `workspace-{agentName}/` pattern
- Secrets segregated to dedicated `credentials/` folder
- Workflow files MUST be tracked in Git
- Output/Reports are generated artifacts, never tracked

---

## Directory Structure

### Main (Special Case)
```
workspace/                          # Root workspace
├── AGENTS.md                       # Identity files
├── SOUL.md
├── MEMORY.md
├── HEARTBEAT.md
├── USER.md
├── TOOLS.md
├── IDENTITY.md
├── CHANGE_SUMMARY.md
├── CRON_JOBS.md
├── WORKFLOW_AUTO.md
├── AGENT_CONVENTIONS.md            # This file
├── .gitignore
└── memory/                         # Agent memory (optional)
```

### All Other Agents (Standard Pattern)
```
workspace-{agent}/                    # e.g., workspace-riddler
├── AGENTS.md
├── SOUL.md
├── MEMORY.md
├── HEARTBEAT.md
├── USER.md
├── TOOLS.md
├── IDENTITY.md
├── CHANGE_SUMMARY.md
├── workflow/                         # ✅ GIT TRACKED
│   └── {agent}-workflow.md
├── data/                            # ✅ GIT TRACKED (public data)
│   └── known_sources.txt
├── memory/                          # ❌ NOT IN GIT
└── credentials/                     # ❌ NOT IN GIT (secrets here!)
    ├── .gitkeep
    └── README.md
```

### Runtime Data (Never in Git)
```
agents/{agent}/
├── agent/                           # Session state
└── sessions/                        # Session tracking
```

---

## Git Strategy

### Tracked in Git (✅)
- `workspace/*.md` - Main agent identity
- `workspace-{agent}/` EXCEPT excluded folders
- `workspace-{agent}/workflow/` - Critical workflows
- `workspace-{agent}/data/` - Public data
- `workspace-{agent}/credentials/` (empty, via .gitkeep)

### Never in Git (❌)
- `agents/*/agent/` - Session state
- `agents/*/sessions/` - Session tracking
- `workspace-{agent}/credentials/*` - API keys, secrets
- `workspace-{agent}/output/` - Generated reports
- `workspace-{agent}/reports/` - Generated reports
- `workspace-{agent}/digest/` - Processed data
- `workspace-{agent}/memory/` - Personal agent memory
- `workspace-{agent}/.openclaw/` - System files
- `workspace-{agent}/.pi/` - System files
- `*.backup*` - Backup files

---

## .gitignore Rules

```gitignore
# Agent runtime data
agents/*/agent/
agents/*/sessions/

# Agent credentials (secrets)
workspace-*/credentials/*
!workspace-*/credentials/.gitkeep
!workspace-*/credentials/README.md

# Agent private outputs (generated artifacts)
workspace-*/output/
workspace-*/reports/
workspace-*/digest/
workspace-*/memory/
workspace-*/.openclaw/
workspace-*/.pi/

# Backup files
*.backup*
```

---

## Folder Purposes

| Folder | Purpose | In Git? |
|--------|---------|---------|
| `workflow/` | Agent logic, scripts, workflows | ✅ YES |
| `data/` | Public data files, configuration | ✅ YES |
| `credentials/` | API keys, secrets, auth tokens | ❌ NEVER (contents) |
| `output/` | Generated reports, research results | ❌ NEVER |
| `reports/` | Health checks, summaries | ❌ NEVER |
| `memory/` | Agent's personal memory, logs | ❌ NEVER |
| `digest/` | Processed/transformed data | ❌ NEVER |

---

## Secrets Management

Each agent gets a credentials folder:

```bash
workspace-{agent}/credentials/
├── README.md          # Instructions for manual setup
├── .gitkeep           # Keeps directory in git
└── [MANUALLY ADDED]   # Never committed
```

The **parent `credentials/` folder** is in git (via `.gitkeep`), but its **contents are ignored**.

---

## Migration Status

| Agent | Before | After | Status |
|-------|--------|-------|--------|
| Main | workspace/ | workspace/ | ✅ Special case, no change |
| Riddler | workspace-riddler/ | workspace-riddler/ | ✅ Already correct |
| Brainiac | workspace-brainiac/ | workspace-brainiac/ | ✅ Already correct |
| Grundy | workspace-grundy/ | workspace-grundy/ | ✅ Already correct |
| Cheetah | workspace/agents/cheetah/ | workspace-cheetah/ | ⏳ Needs migration |
| Sinestro | workspace/agents/sinestro/ | workspace-sinestro/ | ⏳ Needs migration |

---

*Last updated: 2026-02-25*
