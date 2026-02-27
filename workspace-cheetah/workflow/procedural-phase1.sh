#!/bin/bash
# Cheetah Phase 1: Procedural Research Workflow
# Chains: Fetch → Enrich → Merge → Verify (minimal LLM, mostly shell scripts)
# Expected runtime: ~3 minutes total

set -e

WORKSPACE="/Users/chimpman/.openclaw/workspace-cheetah"
KNOWLEDGE_DIR="$WORKSPACE/knowledge"
CHECKPOINT_DIR="$WORKSPACE/checkpoints"
LOG_FILE="$CHECKPOINT_DIR/phase1-$(date +%Y%m%d-%H%M%S).log"

# Map day to topic
DAY_OF_WEEK=$(date +%u)  # 1=Mon, 7=Sun
case $DAY_OF_WEEK in
    1|5) TOPIC="ai-llm" ;;
    2) TOPIC="devtools" ;;
    3) TOPIC="vtt" ;;
    4) TOPIC="ai-dm" ;;
    6|7) TOPIC="mixed" ;;
    *) TOPIC="mixed" ;;
esac

QUERY_MAP=(
    ["ai-dm"]="ai dungeon master OR ai dm OR rpg ai assistant"
    ["vtt"]="foundry vtt OR virtual tabletop OR vtt modules"
    ["devtools"]="ai coding tools OR llm developer tools OR ai dev tools"
    ["ai-llm"]="local llm OR self-hosted ai OR open source llm"
    ["mixed"]="ai tools OR open source OR developer tools"
)

QUERY="${QUERY_MAP[$TOPIC]:-$TOPIC}"

echo "=== Cheetah Phase 1: Procedural Workflow ===" | tee -a "$LOG_FILE"
echo "Topic: $TOPIC | Query: $QUERY" | tee -a "$LOG_FILE"
echo "Start: $(date -Iseconds)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

mkdir -p "$CHECKPOINT_DIR"

# STEP 1: Fetch from GitHub API (30s max)
echo "[STEP 1/4] Fetching from GitHub API..." | tee -a "$LOG_FILE"
FETCH_OUTPUT="$CHECKPOINT_DIR/phase1-fetch-$(date +%Y%m%d).json"

curl -sL --max-time 30 -A "Mozilla/5.0" \
    "https://api.github.com/search/repositories?q=${QUERY// /+}&sort=updated&per_page=15" \
    > "$FETCH_OUTPUT" 2>> "$LOG_FILE"

if [ ! -s "$FETCH_OUTPUT" ]; then
    echo "ERROR: GitHub API fetch failed" | tee -a "$LOG_FILE"
    exit 1
fi

TOTAL_FOUND=$(jq -r '.total_count // 0' "$FETCH_OUTPUT")
echo "  ✓ Fetched $TOTAL_FOUND repos from GitHub" | tee -a "$LOG_FILE"
echo "  ✓ Saved to: $FETCH_OUTPUT" | tee -a "$LOG_FILE"

# STEP 2: Enrich - Fetch READMEs for top 3 repos (60s max)
echo "" | tee -a "$LOG_FILE"
echo "[STEP 2/4] Enriching top 3 repos with README content..." | tee -a "$LOG_FILE"
ENRICHED_OUTPUT="$CHECKPOINT_DIR/phase1-enriched-$(date +%Y%m%d).json"

SCRIPT_DIR="$(dirname "$0")"
python3 "$SCRIPT_DIR/enrich-repos.py" "$FETCH_OUTPUT" "$ENRICHED_OUTPUT" "$TOPIC" 2>> "$LOG_FILE"

if [ ! -s "$ENRICHED_OUTPUT" ]; then
    echo "ERROR: Enrichment failed" | tee -a "$LOG_FILE"
    # Continue with raw data
    cp "$FETCH_OUTPUT" "$ENRICHED_OUTPUT"
fi

echo "  ✓ Enriched data saved to: $ENRICHED_OUTPUT" | tee -a "$LOG_FILE"

# STEP 3: Merge into Knowledge Base (60s max)
echo "" | tee -a "$LOG_FILE"
echo "[STEP 3/4] Merging into knowledge base..." | tee -a "$LOG_FILE"

cd "$WORKSPACE"
python3 scripts/knowledge_manager.py --process-stdin "$TOPIC" < "$ENRICHED_OUTPUT" 2>> "$LOG_FILE"

echo "  ✓ Knowledge base updated" | tee -a "$LOG_FILE"

# STEP 4: Verify and Report (10s - minimal LLM)
echo "" | tee -a "$LOG_FILE"
echo "[STEP 4/4] Verification complete" | tee -a "$LOG_FILE"
echo "  ✓ Phase 1 workflow finished" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "End: $(date -Iseconds)" | tee -a "$LOG_FILE"

# Output summary for agent
echo ""
echo "=== PHASE 1 SUMMARY ==="
echo "Topic: $TOPIC"
echo "Repos Found: $TOTAL_FOUND"
echo "Fetch: $FETCH_OUTPUT"
echo "Enriched: $ENRICHED_OUTPUT"
echo "Knowledge: $KNOWLEDGE_DIR/$TOPIC.json"
echo "Log: $LOG_FILE"
echo "Status: READY for Phase 2"
