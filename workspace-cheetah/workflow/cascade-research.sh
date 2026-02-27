#!/bin/bash
# Cheetah's Cascade Research Workflow
# Orchestrates 3 sub-agents: Researcher → Analyzer → Writer

set -e

OUTPUT_DIR="/Users/chimpman/.openclaw/workspace-cheetah/output/AI_DM_$(date +%Y-%m-%d)"
CHECKPOINT_DIR="/Users/chimpman/.openclaw/workspace-cheetah/checkpoints"
TIMESTAMP=$(date +%s)

mkdir -p "$OUTPUT_DIR" "$CHECKPOINT_DIR"

echo "🐆 Cheetah Cascade Research Starting"
echo "===================================="
echo "Timestamp: $(date)"
echo "Output: $OUTPUT_DIR"
echo ""

# Check for existing checkpoint and resume if needed
if [ -f "$CHECKPOINT_DIR/phase2-insights.md" ]; then
    echo "📋 Resuming from Phase 2 checkpoint"
    START_PHASE=3
elif [ -f "$CHECKPOINT_DIR/phase1-research.json" ]; then
    echo "📋 Resuming from Phase 1 checkpoint"
    START_PHASE=2
else
    echo "🚀 Starting fresh"
    START_PHASE=1
fi

# Phase 1: Researcher
echo ""
echo "🔍 PHASE 1: Researcher"
echo "---------------------"
# Spawn cheetah-researcher via sessions
# This would be triggered by a sessions_spawn call
# For now, document what it does:
# - Search GitHub API for trending AI-DM repos
# - Fetch top 5 with web_fetch
# - Save raw data to phase1-research.json
if [ $START_PHASE -le 1 ]; then
    echo "Status: Ready for researcher sub-agent"
    echo "Task: Search GitHub API for 'ai dungeon master' repos"
    echo "Output: $CHECKPOINT_DIR/phase1-research.json"
    echo ""
    echo "⏳ Waiting for Phase 1 completion..."
    # Wait for checkpoint file
    MAX_WAIT=600
    WAITED=0
    while [ ! -f "$CHECKPOINT_DIR/phase1-research.json" ] && [ $WAITED -lt $MAX_WAIT ]; do
        sleep 5
        WAITED=$((WAITED + 5))
        echo -n "."
    done
    echo ""
    
    if [ ! -f "$CHECKPOINT_DIR/phase1-research.json" ]; then
        echo "❌ Phase 1 timeout - aborting"
        exit 1
    fi
    echo "✅ Phase 1 complete"
fi

# Phase 2: Analyzer
echo ""
echo "🧠 PHASE 2: Analyzer"
echo "--------------------"
if [ $START_PHASE -le 2 ]; then
    echo "Status: Ready for analyzer sub-agent"
    echo "Input: $CHECKPOINT_DIR/phase1-research.json"
    echo "Output: $CHECKPOINT_DIR/phase2-insights.md"
    echo ""
    echo "⏳ Waiting for Phase 2 completion..."
    MAX_WAIT=600
    WAITED=0
    while [ ! -f "$CHECKPOINT_DIR/phase2-insights.md" ] && [ $WAITED -lt $MAX_WAIT ]; do
        sleep 5
        WAITED=$((WAITED + 5))
        echo -n "."
    done
    echo ""
    
    if [ ! -f "$CHECKPOINT_DIR/phase2-insights.md" ]; then
        echo "❌ Phase 2 timeout - aborting"
        exit 1
    fi
    echo "✅ Phase 2 complete"
fi

# Phase 3: Writer
echo ""
echo "✍️  PHASE 3: Writer"
echo "-------------------"
if [ $START_PHASE -le 3 ]; then
    echo "Status: Ready for writer sub-agent"
    echo "Input: $CHECKPOINT_DIR/phase2-insights.md"
    echo "Output: $OUTPUT_DIR/report.md"
    echo ""
    echo "⏳ Waiting for Phase 3 completion..."
    MAX_WAIT=600
    WAITED=0
    while [ ! -f "$OUTPUT_DIR/report.md" ] && [ $WAITED -lt $MAX_WAIT ]; do
        sleep 5
        WAITED=$((WAITED + 5))
        echo -n "."
    done
    echo ""
    
    if [ ! -f "$OUTPUT_DIR/report.md" ]; then
        echo "❌ Phase 3 timeout"
        exit 1
    fi
    echo "✅ Phase 3 complete"
fi

echo ""
echo "===================================="
echo "🎉 CASCADE COMPLETE"
echo "Final report: $OUTPUT_DIR/report.md"
echo "Word count: $(wc -w < $OUTPUT_DIR/report.md)"

# Cleanup checkpoints on success
rm -f "$CHECKPOINT_DIR"/phase1-research.json "$CHECKPOINT_DIR"/phase2-insights.md

exit 0
