---
name: OpenClaw Health Check
description: Audits the .openclaw root directory structure, validates against expected baseline, checks system logs for errors, and identifies unauthorized changes
agent: brainiac
type: manual
tags: [health, audit, maintenance, infrastructure, logs]
---

# OpenClaw Health Check

Systematic validation of the OpenClaw root directory structure integrity.

## Trigger

Run when:
- Daily at 2:00 AM PST (cron schedule)
- After any OpenClaw update or configuration change
- When system behavior appears unexpected
- Before critical operations

## Scope

Audit the root directory: `~/.openclaw/`

## Expected Directory Structure (Baseline)

The canonical .openclaw root structure:

```
~/.openclaw/
├── agents/                    # Agent runtime state
│   └── {agent_id}/
│       ├── agent/
│       └── sessions/
├── canvas/                    # Canvas/screencast resources
├── completions/               # Completion cache
├── credentials/               # Stored credentials
├── cron/                      # Cron job state
├── delivery-queue/           # Message delivery queue
├── devices/                   # Paired device metadata
├── identity/                  # Identity files
├── logs/                      # OpenClaw logs
├── subagents/                 # Subagent session tracking
├── workspace/                 # Main agent workspace (git-tracked)
│   ├── agents/
│   │   └── {agent_id}/
│   │       ├── agent/
│       │       └── sessions/
│   │       └── workflow/
│   ├── memory/
│   ├── AGENTS.md
│   ├── BOOTSTRAP.md
│   ├── HEARTBEAT.md
│   ├── IDENTITY.md
│   ├── MEMORY.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   └── USER.md
├── openclaw.json             # Gateway configuration
├── openclaw.json.bak         # Config backup
└── update-check.json         # Update metadata
```

### Critical Files

These files MUST exist:
| File | Purpose | Criticality |
|------|---------|-------------|
| `openclaw.json` | Gateway configuration | 🔴 CRITICAL |
| `openclaw.json.bak` | Config backup | 🔴 CRITICAL |
| `credentials/` | API keys and tokens | 🔴 CRITICAL |

### Critical Directories

These directories MUST exist:
| Directory | Purpose | Criticality |
|-----------|---------|-------------|
| `logs/` | System logs | 🔴 CRITICAL |
| `workspace/` | Agent code and documents | 🔴 CRITICAL |
| `agents/` | Runtime agent data | 🟡 HIGH |
| `identity/` | Identity configuration | 🟡 HIGH |

## Observability Check

Validate OpenClaw functions perform as expected:

### 1. Gateway Configuration Valid

```bash
# Check config file exists and is valid JSON
jq empty ~/.openclaw/openclaw.json 2>&1 | head -1
```

- Config file is valid JSON
- Required keys present: `agents`, `models`, `gateway`, `channels`
- No orphaned agent references

### 2. Log Rotation Active

```bash
# Check logs are being written
ls -la ~/.openclaw/logs/ | wc -l
```

- Recent log entries exist
- Log files are not excessively large (>100MB)
- Error rates acceptable

### 3. Cron System Functional

```bash
# Verify cron jobs can be read
ls ~/.openclaw/cron/ 2>/dev/null | head -5
```

- Cron state directory accessible
- Job files present if cron jobs configured

### 4. Agent Runtimes Reachable

Test spawning each registered agent:
- Agent responds to health check
- Workspace accessible
- No permission errors

### 5. Workspace Integrity

Validate workspace structure:
- Core files exist (IDENTITY.md, SOUL.md, etc.)
- Git repo is functional
- No uncommitted critical changes

## Audit Steps

### 1. Enumerate Current State

```bash
# Get current directory listing
ls -la ~/.openclaw/
```

Compare against expected baseline.

### 2. Identify Anomalies

Flag any that deviate from expected:
- **Unexpected directories** — new folders not in baseline
- **Missing critical files** — baseline files that disappeared
- **Permission changes** — unexpected mode changes
- **Size anomalies** — files/directories unexpectedly large/small

### 3. Classify Issues

| Severity | Definition | Examples |
|----------|-----------|----------|
| 🔴 **CRITICAL** | System non-functional or data loss risk | Missing openclaw.json, corrupted credentials |
| 🟡 **WARNING** | Degraded functionality or stability risk | New directories (unknown origin), large log files |
| 🟢 **INFO** | Observations or potential improvements | Unused directories, optimization opportunities |

### 4. Analyze System Logs (NEW)

**Check OpenClaw error logs for system-wide issues:**

```bash
# Read the last 1000 lines of error log
cat ~/.openclaw/logs/gateway.err.log | tail -1000
```

**Search for system-level error patterns (non-agent specific):**

```bash
# Gateway/recovery errors
grep -E "(gateway|recovery|restart)" ~/.openclaw/logs/gateway.err.log | tail -20

# Connection/network errors
grep -E "(connection|network|socket|websocket|ws)" ~/.openclaw/logs/gateway.err.log | tail -20

# Rate limiting/errors
grep -E "(rate limit|throttle|queue)" ~/.openclaw/logs/gateway.err.log | tail -20

# Delivery failures
grep -E "(delivery|fail|timeout)" ~/.openclaw/logs/gateway.err.log | tail -30

# Channel/API errors
grep -E "(discord|api|provider)" ~/.openclaw/logs/gateway.err.log | tail -20

# System errors (out of memory, disk, etc.)
grep -E "(OOM|disk|memory|quota|EMFILE|ENOSPC)" ~/.openclaw/logs/gateway.err.log | tail -20
```

**Analyze log entries:**
- **Timestamp**: In last 24 hours? Recurring pattern?
- **Component**: Which subsystem is affected?
- **Severity**: Error, warning, or info?
- **Trend**: Is error frequency increasing?

**Common OpenClaw System Issues:**
| Error Pattern | Meaning | Severity |
|--------------|---------|----------|
| `gateway timeout` | Service unreachable or unresponsive | 🔴 Critical |
| `rate limit` | API throttling | 🟡 Warning |
| `connection refused` | Service down or blocked | 🔴 Critical |
| `delivery failed` | Message sending failed | 🟡 Warning |
| `slow listener` | Performance degradation | 🟡 Warning |
| `LLM request timed out` | Model provider issue | 🟡 Warning |
| `device_token_mismatch` | Authentication issue | 🟡 Warning |

**Log Analysis Summary for Report:**
- Total errors in last 24h
- Critical issues requiring attention
- Trends (same error recurring?)
- Recommendations

### 5. Validate Functionality

- Gateway responds to API calls
- Agents can spawn
- File operations (read/write/check) work
- Memory files accessible
- External integrations (Discord, etc.) functional

## Report Structure

```markdown
# OpenClaw Health Report

**Generated:** YYYY-MM-DD HH:MM PST  
**Agent:** Brainiac  
**Status:** ❌ DEGRADED / ⚠️ WARNING / ✅ HEALTHY

## Summary

- Total items checked: N
- Matches baseline: N
- Deviations found: N
- Status: HEALTHY/DEGRADED

## Deviations from Baseline

### 🔴 / 🟡 / 🟢 Classification

**Issue Type:** [NEW_DIRECTORY / MISSING_FILE / PERMISSION_CHANGE / SIZE_ANOMALY / STRUCTURE_CHANGE]

**Description:** What was found

**Expected:** What should have been there

**Current:** What is actually there

**Impact:** What could break if not addressed

**Recommendation:** Specific action to take

## Anomaly Log

| Item | Expected | Found | Severity |
|------|----------|-------|----------|
| ... | ... | ... | ... |

## Log Analysis Summary

### System Errors Found (Last 24 Hours)
| Timestamp | Error Type | Component | Severity | Frequency |
|-----------|------------|-----------|----------|-----------|
| | | | | |

### Error Patterns Identified
- Pattern 1: (description)
- Pattern 2: (description)

### Log-Based Recommendations
- Recommend action 1
- Recommend action 2

## Functionality Test Results

| Test | Status | Details |
|------|--------|---------|
| Gateway config validation | ✅/❌ | |
| Log accessibility | ✅/❌ | |
| Cron system | ✅/❌ | |
| Agent spawn test | ✅/❌ | |
| Workspace integrity | ✅/❌ | |

## Process Improvement Question

> "What else can I do in order to make sure that the .openclaw folder structure remains healthy, and that standard OpenClaw functions perform as intended and expected?"

Capture insights here:
- Patterns in anomalies that suggest systemic issues
- Additional checks that would be valuable
- Predictive indicators of future problems
- Automated remediation candidates

## Action Items

Priority-ordered list of required actions.
```

## Report Storage

Save reports to:
```
~/.openclaw/workspace-brainiac/reports/
└── openclaw-health-YYYY-MM-DD-HHMM.md
```

## Success Criteria

- ✅ All critical files present with valid contents
- ✅ Root structure matches baseline (or deviations documented)
- ✅ Gateway configuration valid JSON with required keys
- ✅ Logs accessible and not excessive
- ✅ Cron jobs firing (if configured)
- ✅ Agents spawn successfully
- ✅ Workspace git repo healthy
- ✅ Report generated with actionable recommendations

## Error Handling

If unable to access `.openclaw/`:
- Check permissions on home directory
- Verify OpenClaw installation integrity
- Report CRITICAL and escalate to human

If self-corruption detected (workspace-brainiac issues):
- Acknowledge potential bias
- Cross-reference with other agent workspaces
- Document conflict in report

## Historical Trending

Compare current report with previous reports:
- Are the same anomalies recurring?
- Is the structure drifting over time?
- Are new directories accumulating?
- Is log growth accelerating?

Document trends in report under "Historical Analysis."

---

*Auditing the foundation of our operation* 🧠
