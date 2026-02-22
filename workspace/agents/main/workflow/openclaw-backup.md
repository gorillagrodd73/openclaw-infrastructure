---
name: OpenClaw Backup
description: Nightly backup of OpenClaw configuration, credentials, and workspace files
agent: main
type: cron
tags: [backup, maintenance, cron]
schedule: "0 23 * * *"
timezone: America/Los_Angeles
---

# OpenClaw Nightly Backup

**Schedule:** 11:00 PM PST daily
**Purpose:** Ensure critical OpenClaw data is backed up and recoverable

## Critical Files to Backup

### 1. Configuration Files
- `~/.openclaw/openclaw.json` — Gateway configuration
- `~/.openclaw/openclaw.json.bak` — Config backup
- `~/.openclaw/update-check.json` — Update metadata

### 2. Credentials & Auth
- `~/.openclaw/credentials/` — API keys and tokens
- `~/.openclaw/identity/` — Identity files

### 3. Agent Data
- `~/.openclaw/agents/` — Agent runtime state
- `~/.openclaw/workspace/` — Main agent workspace (git tracked)
- `~/.openclaw/workspace-*/` — All agent workspaces

### 4. State & Logs
- `~/.openclaw/cron/` — Cron job state
- `~/.openclaw/memory/` — Memory files
- `~/.openclaw/logs/` — Recent logs (last 7 days)

## Backup Steps

### Step 1: Create Backup Directory
```bash
mkdir -p ~/.openclaw/backups/$(date +%Y-%m-%d)
```

### Step 2: Export Gateway Config
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/$(date +%Y-%m-%d)/
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/backups/$(date +%Y-%m-%d)/
```

### Step 3: Backup Credentials (Encrypted/Secure)
```bash
tar -czf ~/.openclaw/backups/$(date +%Y-%m-%d)/credentials.tar.gz -C ~/.openclaw credentials/
```

### Step 4: Backup Agent States
```bash
# Backup all workspace directories
for workspace in ~/.openclaw/workspace*; do
  if [ -d "$workspace" ]; then
    name=$(basename "$workspace")
    tar -czf ~/.openclaw/backups/$(date +%Y-%m-%d)/${name}.tar.gz -C ~/.openclaw "$name"
  fi
done
```

### Step 5: Backup Agents Directory
```bash
tar -czf ~/.openclaw/backups/$(date +%Y-%m-%d)/agents.tar.gz -C ~/.openclaw agents/
```

### Step 6: Copy Recent Logs
```bash
# Logs from last 7 days
find ~/.openclaw/logs -name "*.log" -mtime -7 -exec cp {} ~/.openclaw/backups/$(date +%Y-%m-%d)/ \;
```

### Step 7: Create Backup Manifest
```bash
cat > ~/.openclaw/backups/$(date +%Y-%m-%d)/MANIFEST.txt << EOF
OpenClaw Backup Manifest
========================
Date: $(date)
Host: $(hostname)
User: $(whoami)

Contents:
- openclaw.json: Gateway configuration
- credentials.tar.gz: Encrypted credentials
- workspace.tar.gz: Main workspace (git tracked)
- workspace-*.tar.gz: Agent workspaces
- agents.tar.gz: Agent runtime state
- *.log: Recent logs (7 days)

To Restore:
1. Stop OpenClaw gateway
2. Extract backup to ~/.openclaw/
3. Restore credentials: tar -xzf credentials.tar.gz
4. Restart gateway
EOF
```

### Step 8: Cleanup Old Backups
```bash
# Keep last 30 days of backups
find ~/.openclaw/backups -name "20*" -type d -mtime +30 -exec rm -rf {} \; 2>/dev/null
```

### Step 9: Verify Backup
```bash
# Check backup size and file count
BACKUP_DIR="$HOME/.openclaw/backups/$(date +%Y-%m-%d)"
echo "Backup location: $BACKUP_DIR"
echo "Backup size: $(du -sh $BACKUP_DIR | cut -f1)"
echo "Files backed up: $(find $BACKUP_DIR -type f | wc -l)"
```

## Optional: Remote Backup

### Upload to Google Drive
```bash
# After gog is configured:
# gog drive upload ~/.openclaw/backups/$(date +%Y-%m-%d).tar.gz --folder "OpenClaw Backups"
```

## Restore Process

### Full Restore
```bash
# Stop gateway
openclaw gateway stop

# Restore from backup
cd ~/.openclaw/backups/YYYY-MM-DD
tar -xzf credentials.tar.gz -C ~/.openclaw/
tar -xzf agents.tar.gz -C ~/.openclaw/

# Restore workspaces
tar -xzf workspace.tar.gz -C ~/.openclaw/
# Repeat for each agent workspace

cp openclaw.json ~/.openclaw/
cp openclaw.json.bak ~/.openclaw/

# Restart gateway
openclaw gateway start
```

## Success Criteria
- ✅ Backup directory created with date stamp
- ✅ All critical files backed up
- ✅ Backup size > 1MB (sanity check)
- ✅ Manifest file created
- ✅ Old backups cleaned up (>30 days)
- ✅ Disk space check passed (ensure >1GB free)

## Error Handling
- If backup fails, log error and notify
- If disk space < 1GB, skip cleanup and warn
- If credentials backup fails, mark as CRITICAL

---
*Protecting our foundation* 🦍
