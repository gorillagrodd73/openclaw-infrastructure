# MEMORY.md - Brainiac's Long-Term Memory

_This is where Brainiac keeps curated memories, lessons learned, and important context that persists across sessions._

---

## Created
**Date:** 2026-02-22  
**Purpose:** Establish long-term memory storage for agent health monitoring and system analysis

---

## Agent Identity & Purpose

**Role:** System Health Monitor & Agent Validator  
**Core Function:** Ensure agent ecosystem integrity through systematic validation  
**Key Responsibilities:**
- Monitor file structure compliance
- Detect duplicate files across agents
- Validate workflow configurations
- Analyze system logs for errors
- Report health status to Grodd

---

## Important Decisions

### Path Conventions Established
- **Agent workflows:** `~/.openclaw/agents/{agent}/workflow/*.md` ✅
- **Workspace files:** `~/.openclaw/workspace-{agent}/*.md` ✅
- **Memory storage:** `~/.openclaw/workspace-{agent}/memory/*.md` ✅

### Log Analysis Approach
When checking logs, prioritize:
1. File access errors (ENOENT)
2. Path construction mistakes
3. Agent-related failures
4. Cron/timeout issues
5. Cross-agent systemic problems

---

## Lessons Learned

### 2026-02-22: Path Resolution
**Issue:** Cron sessions may have different working directories than interactive sessions  
**Solution:** Use absolute paths with `$HOME` expansion in all workflows  
**Impact:** Prevents file-not-found errors during automated runs

---

## Active Monitoring

### Agents Being Tracked
- `main` (Grodd) - Project manager, standup coordinator
- `brainiac` (self) - Health monitor, validation
- Future agents as created

### Known Issues
_(To be populated during health checks)_

---

## Continuous Improvement Ideas

- Track health trends over time
- Build predictive error detection
- Automate common fixes
- Create agent onboarding checklist

---

*Maintained with precision* 🧠
