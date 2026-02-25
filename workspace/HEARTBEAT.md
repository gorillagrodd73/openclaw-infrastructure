# HEARTBEAT.md - Agent Health Monitoring

## Agent Health Check Tasks

### 1. Check Recent Agent Activity
List recent cron runs and check for:
- Failed jobs (non-zero exit codes)
- Timeout errors
- Missing expected output files

### 2. Verify Agent Workflows
Check each agent's workspace:
- Cheetah: output/ folder has recent research
- Riddler: digest/ folder processed Cheetah's output
- Brainiac: reports/ folder has health checks

### 3. Report Status
Post summary to Discord #general if:
- Any agent hasn't run in >24h
- Output files are stale (>48h old)
- Errors detected

### 4. Git Repository
Check for uncommitted changes

---

## Daily Checks (Run 4x per day)

### Morning (08:00 PST)
- [ ] Check overnight cron runs
- [ ] Verify Cheetah night run completed
- [ ] Check Riddler digests

### Midday (12:00 PST)
- [ ] Quick status check
- [ ] Verify no stuck sessions

### Evening (18:00 PST)
- [ ] Check Brainiac health report
- [ ] Review any errors

### Night (22:00 PST)
- [ ] Pre-sleep status
- [ ] Verify ready for overnight runs
