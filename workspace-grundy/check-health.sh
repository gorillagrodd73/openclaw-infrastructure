#!/bin/bash
# Grundy's Health Check Script
# Run this hourly to check all agent health

echo "🧟 Grundy's Legion Health Check"
echo "================================"
echo "Timestamp: $(date)"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

ISSUES=0

# Check 1: Agent Activity (files modified in last 24h)
echo "📊 Agent Activity (last 24h)"
echo "-----------------------------"

AGENTS=("workspace:main" "workspace-cheetah:cheetah" "workspace-riddler:riddler" "workspace-brainiac:brainiac" "workspace-sinestro:sinestro" "workspace-toyman:toyman")

for agent_path in "${AGENTS[@]}"; do
    IFS=':' read -r path name <<< "$agent_path"
    full_path="/Users/chimpman/.openclaw/$path"
    
    # Check for recent memory files
    recent_files=$(find "$full_path" -name "*.md" -mtime -1 2>/dev/null | wc -l)
    
    if [ "$recent_files" -gt 0 ]; then
        echo -e "${GREEN}✓${NC} $name: $recent_files recent files"
    else
        echo -e "${YELLOW}⚠${NC} $name: No recent files (24h)"
        ((ISSUES++))
    fi
done

echo ""

# Check 2: Git Status
echo "🔄 Git Sync Status"
echo "------------------"
cd /Users/chimpman/.openclaw

uncommitted=$(git status --porcelain | wc -l)
if [ "$uncommitted" -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All changes committed"
else
    echo -e "${YELLOW}⚠${NC} $uncommitted uncommitted changes"
    git status --short | head -5
    ((ISSUES++))
fi

echo ""

# Check 3: Memory System
echo "🧠 Memory System Status"
echo "-----------------------"
if [ -f "/Users/chimpman/.openclaw/workspace/memory/embedding-index/lancedb/memories.lance/_versions/18446744073709551614.manifest" ]; then
    echo -e "${GREEN}✓${NC} Semantic memory indexed"
else
    echo -e "${YELLOW}⚠${NC} Memory index not found"
    ((ISSUES++))
fi

echo ""

# Check 4: Disk Space
echo "💾 Disk Space"
echo "-------------"
df -h /Users/chimpman/.openclaw 2>/dev/null | awk 'NR==2 {
    print "Used: "$3" / "$2" ("$5")"
    gsub(/%/,"",$5)
    if ($5 > 90) exit 2
    else if ($5 > 80) exit 1
}'

case $? in
    0) echo -e "${GREEN}✓${NC} Disk space OK" ;;
    1) echo -e "${YELLOW}⚠${NC} Disk space >80%" ; ((ISSUES++)) ;;
    2) echo -e "${RED}✗${NC} Disk space CRITICAL >90%" ; ((ISSUES++)) ;;
esac

echo ""

# Check 5: Recent Cron Jobs
echo "⏰ Recent Cron Activity"
echo "------------------------"
if [ -d "/Users/chimpman/.openclaw/cron/runs" ]; then
    recent=$(ls -lt /Users/chimpman/.openclaw/cron/runs 2>/dev/null | grep "$(date +%Y-%m-%d)" | wc -l)
    echo -e "${GREEN}✓${NC} $recent cron runs today"
else
    echo -e "${YELLOW}⚠${NC} No cron runs directory"
    ((ISSUES++))
fi

echo ""
echo "================================"

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✓ HEARTBEAT_OK${NC} - All systems operational"
    exit 0
else
    echo -e "${YELLOW}⚠ $ISSUES issues detected${NC} - Review recommended"
    exit 1
fi
