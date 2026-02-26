# HEARTBEAT.md - Grundy's Agent Health Monitoring

*Run this every hour to keep the Legion of Doom running smoothly.*

## Hourly Health Checks

### 1. Agent Activity Status
Check each agent's workspace for recent activity (within last 24h):

**Agents to Monitor:**
- ✅ **Grodd** (main) - `/Users/chimpman/.openclaw/workspace/`
- ✅ **Cheetah** - `/Users/chimpman/.openclaw/workspace-cheetah/`
- ✅ **Riddler** - `/Users/chimpman/.openclaw/workspace-riddler/`
- ✅ **Brainiac** - `/Users/chimpman/.openclaw/workspace-brainiac/`
- ✅ **Sinestro** - `/Users/chimpman/.openclaw/workspace-sinestro/`
- ✅ **Toyman** - `/Users/chimpman/.openclaw/workspace-toyman/`

**Check for:**
- Recent memory files (`memory/YYYY-MM-DD.md`)
- Recent output files in `output/` or `reports/`
- Any error logs or stuck processes

### 2. Git Sync Status
Verify all workspaces are committed and pushed:

```bash
cd /Users/chimpman/.openclaw && git status --short | head -20
```

**Alert if:**
- Uncommitted changes exist for >2 hours
- Push failures detected
- Merge conflicts present

### 3. Cron Job Health
Check recent cron runs:

```bash
ls -lt /Users/chimpman/.openclaw/cron/runs/ | head -10
```

**Look for:**
- Failed jobs (non-zero exit codes)
- Timeout errors
- Missing expected output

### 4. Memory System Status
Check semantic memory index:

```bash
./workspace/memory/embedding-index/grodd-memory stats
```

### 5. Disk Space
```bash
df -h /Users/chimpman/.openclaw | tail -1
```

**Alert if:** <10GB free

---

## Response Protocol

### If Everything is Healthy:
Report: `HEARTBEAT_OK - All agents operational. Last checks: [timestamps]`

### If Issues Found:
Report to Discord #general with:
1. **Affected Agent(s)**
2. **Issue Type** (stuck, error, stale, missing)
3. **Recommended Action**
4. **Severity** (LOW/MEDIUM/HIGH)

### Critical Issues (Immediate Alert):
- Agent hasn't produced output in >24h
- Git sync failing
- Disk space critical (<5GB)
- Multiple cron job failures

---

## Quick Reference

**Agent Purposes:**
| Agent | Role | Output Location |
|-------|------|-------------------|
| Grodd (main) | AI PM, coordinator | `workspace/reports/`, `memory/` |
| Cheetah | Research | `workspace-cheetah/output/` |
| Riddler | Digests | `workspace-riddler/digest/` |
| Brainiac | System health | `workspace-brainiac/reports/` |
| Sinestro | Strategy | `workspace-sinestro/outputs/` |
| Toyman | Development | `workspace-toyman/projects/` |

**Healthy Indicators:**
- Daily memory files created
- Git commits every 1-4 hours during active work
- No timeout errors in logs
- All agents have MEMORY.md files

---

*Last updated: 2026-02-26 by Grundy*
