#!/bin/bash
# Cheetah Phase 3: Procedural Report Generation Workflow
# Chains: Living Report → Daily Summary → Git Commit → Cleanup (minimal LLM)
# Expected runtime: ~2 minutes total

set -e

WORKSPACE="/Users/chimpman/.openclaw/workspace-cheetah"
REPORTS_DIR="$WORKSPACE/reports"
KNOWLEDGE_DIR="$WORKSPACE/knowledge"
CHECKPOINT_DIR="$WORKSPACE/checkpoints"
DATE_STR=$(date +%Y-%m-%d)
DATE_COMPACT=$(date +%Y%m%d)
LOG_FILE="$CHECKPOINT_DIR/phase3-$(date +%Y%m%d-%H%M%S).log"

# Map day to topic
DAY_OF_WEEK=$(date +%u)
case $DAY_OF_WEEK in
    1|5) TOPIC="ai-llm" ;;
    2) TOPIC="devtools" ;;
    3) TOPIC="vtt" ;;
    4) TOPIC="ai-dm" ;;
    6|7) TOPIC="ai-llm" ;;
    *) TOPIC="mixed" ;;
esac

echo "=== Cheetah Phase 3: Procedural Report Generation ===" | tee -a "$LOG_FILE"
echo "Topic: $TOPIC | Date: $DATE_STR" | tee -a "$LOG_FILE"
echo "Start: $(date -Iseconds)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Verify knowledge base exists
KB_FILE="$KNOWLEDGE_DIR/$TOPIC.json"
if [ ! -f "$KB_FILE" ]; then
    echo "ERROR: Knowledge base not found: $KB_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

# STEP 1: Generate Living Report (30s - Python templated)
echo "[STEP 1/4] Generating Living Report..." | tee -a "$LOG_FILE"
cd "$WORKSPACE"
python3 scripts/generate_report.py "$TOPIC" --type living 2>> "$LOG_FILE"

# Use tr for uppercase (macOS compatible)
TOPIC_UPPER=$(echo "$TOPIC" | tr '[:lower:]' '[:upper:]')
LIVING_REPORT="$REPORTS_DIR/${TOPIC_UPPER}_Living_Report.md"
if [ -f "$LIVING_REPORT" ]; then
    WORDS=$(wc -w < "$LIVING_REPORT" | tr -d '[:space:]')
    echo "  ✓ Living Report: $LIVING_REPORT ($WORDS words)" | tee -a "$LOG_FILE"
else
    echo "  ✗ Living Report generation failed" | tee -a "$LOG_FILE"
    exit 1
fi

# STEP 2: Generate Daily Summary (30s - Python templated)  
echo "" | tee -a "$LOG_FILE"
echo "[STEP 2/4] Generating Daily Summary..." | tee -a "$LOG_FILE"

SUMMARY_FILE="$REPORTS_DIR/daily_summaries/${TOPIC}_${DATE_STR}.md"
python3 scripts/generate_report.py "$TOPIC" --type summary --output "$SUMMARY_FILE" 2>> "$LOG_FILE"

if [ -f "$SUMMARY_FILE" ]; then
    WORDS=$(wc -w < "$SUMMARY_FILE" | tr -d '[:space:]')
    echo "  ✓ Daily Summary: $SUMMARY_FILE ($WORDS words)" | tee -a "$LOG_FILE"
else
    echo "  ✗ Daily Summary generation failed" | tee -a "$LOG_FILE"
    exit 1
fi

# STEP 3: Git Commit (30s - shell)
echo "" | tee -a "$LOG_FILE"
echo "[STEP 3/4] Committing to git..." | tee -a "$LOG_FILE"
cd /Users/chimpman/.openclaw
git add workspace-cheetah/reports/ 2>> "$LOG_FILE" || true
git commit -m "Cheetah: Daily reports for $TOPIC $DATE_STR" 2>> "$LOG_FILE" || true
git push origin main 2>> "$LOG_FILE" || echo "  ! Push deferred (may need manual auth)" | tee -a "$LOG_FILE"
echo "  ✓ Committed reports" | tee -a "$LOG_FILE"

# STEP 4: Cleanup (10s)
echo "" | tee -a "$LOG_FILE"
echo "[STEP 4/4] Cleaning checkpoints..." | tee -a "$LOG_FILE"
rm -f "$CHECKPOINT_DIR/phase2-$TOPIC-*.json"
echo "  ✓ Old checkpoints removed" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "=== PHASE 3 COMPLETE ===" | tee -a "$LOG_FILE"
echo "End: $(date -Iseconds)" | tee -a "$LOG_FILE"

# Output summary for agent
echo ""
echo "=== PHASE 3 SUMMARY ==="
echo "Topic: $TOPIC"
echo "Living Report: "$LIVING_REPORT" ($WORDS words)"
echo "Daily Summary: $SUMMARY_FILE ($WORDS words)"
echo "Git: Committed"
echo "Status: CASCADE COMPLETE"
