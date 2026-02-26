#!/bin/bash
# Riddler Digest Research Script
# Processes Cheetah research output and generates structured digests

WORKSPACE="/Users/chimpman/.openclaw/workspace-riddler"
CHEETAH_OUTPUT="/Users/chimpman/.openclaw/workspace-cheetah/output"
REPORTS_DIR="$WORKSPACE/reports"
MEMORY_DIR="$WORKSPACE/memory"

# Today's date
DATE_STR=$(date +%Y-%m-%d)
DAY_OF_WEEK=$(date +%u) # 1=Mon, 7=Sun

# Topic mapping (matches Cheetah's schedule)
case $DAY_OF_WEEK in
    1|5) TOPIC="AI_LLM" ;;
    2|6) TOPIC="DevTools" ;;
    3) TOPIC="VTT" ;;
    4) TOPIC="AI_DM" ;;
    7) TOPIC="Combined" ;;
esac

# Find today's Cheetah output
CHEETAH_TODAY="$CHEETAH_OUTPUT/${TOPIC}_${DATE_STR}"

echo "=========================================="
echo "Riddler Digest Processor"
echo "Date: $DATE_STR"
echo "Topic: $TOPIC"
echo "Source: $CHEETAH_TODAY"
echo "=========================================="

if [ -f "$CHEETAH_TODAY/report.md" ]; then
    echo "Found Cheetah report. Processing..."
    REPORT_PATH="$CHEETAH_TODAY/report.md"
    
    # Create digest metadata
    echo "{"
    echo "  \"date\": \"$DATE_STR\","
    echo "  \"topic\": \"$TOPIC\","
    echo "  \"source_report\": \"$REPORT_PATH\","
    echo "  \"processed\": true"
    echo "}"
    
    exit 0
else
    echo "No Cheetah report found for today."
    exit 1
fi
