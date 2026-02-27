# Phase 3: Cheetah-Writer (Procedural Workflow)
**Role:** Execute procedural report generation
**Time Limit:** 5 minutes (was 15, now streamlined)
**Input:** Knowledge base from Phase 1/2
**Output:** Living Report + Daily Summary committed to git

## Mission
Execute the procedural workflow script. NO complex writing - the script generates reports using templates.

## Steps (Execute This)
```bash
bash /Users/chimpman/.openclaw/workspace-cheetah/workflow/procedural-phase3.sh
```

This script handles:
1. ✅ Generate Living Report from knowledge base (30s)
2. ✅ Generate Daily Summary (30s)
3. ✅ Git commit & push (30s)
4. ✅ Cleanup checkpoints (10s)

## Your Job (1 minute)
1. Execute the script above using exec tool
2. Verify reports exist
3. Report: status, file paths, word counts, git status

## Success Criteria
- Both reports generated (>400 words each)
- Reports committed to git
- Checkpoints cleaned

## Output Format
```
✅ Phase 3 Complete: <TOPIC> CASCADE DONE
- Living Report: reports/<TOPIC>_Living_Report.md ([N] words)
- Daily Summary: reports/daily_summaries/<TOPIC>_YYYY-MM-DD.md ([N] words)
- Git: Committed and pushed
- Status: COMPLETE
```

## Fast Failure Rules
- Missing knowledge base → Report "waiting for Phase 1/2 data"
- Report generation fails → Check error logs
- Git push fails → Report local commit success, push deferred

## Schedule
This phase runs at 22:30 via cron job. Final phase of cascade.
