---
name: Git Repository Backup
description: Nightly git commit and push of OpenClaw workspace
agent: main
type: cron
tags: [backup, git, cron]
---

# Git Nightly Backup

**Schedule:** 11:00 PM PST daily
**Purpose:** Ensure all workspace changes are committed and pushed to git

## What Gets Backed Up

### Primary: ~/clawd (main workspace)
- All agent workflows
- Documentation (AGENTS.md, TOOLS.md, SOUL.md, etc.)
- Memory files
- Configuration

### NOT included:
- ~/.openclaw/ root files (configs, credentials)
- Large binary files
- Log files

## Steps

### 1. Check Git Status
```bash
cd ~/clawd
git status --short
```

### 2. Stage Changes
```bash
git add -A
```

### 3. Commit with Timestamp
```bash
git commit -m "Nightly backup: $(date '+%Y-%m-%d %H:%M') - Automated sync"
```

### 4. Push to Remote (if configured)
```bash
git push origin main 2>/dev/null || echo "No remote configured"
```

### 5. Generate Report
```bash
echo "Backup completed: $(date)"
echo "Commit: $(git rev-parse --short HEAD)"
echo "Remote: $(git remote -v 2>/dev/null || echo 'None')"
```

## Success Criteria
- ✅ Changes staged
- ✅ Commit created with timestamp
- ✅ Push attempted (if remote exists)
- ✅ Report generated

## Error Handling
- If no changes: "Nothing to commit"
- If commit fails: Log error and notify
- If push fails: Commit is local (still backed up)

---
*Version control is the best backup* 🦍
