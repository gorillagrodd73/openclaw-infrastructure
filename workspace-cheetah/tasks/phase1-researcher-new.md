# Phase 1: Cheetah-Researcher (Procedural Workflow)
**Role:** Execute procedural research workflow
**Time Limit:** 5 minutes (was 15, now streamlined)
**Input:** Today's topic based on day of week
**Output:** Knowledge base updated with new findings

## Today's Topic
| Day | Topic | Knowledge Base |
|-----|-------|----------------|
| Mon/Fri | AI-LLM | `knowledge/ai-llm.json` |
| Tue | DevTools | `knowledge/devtools.json` |
| Wed | VTT | `knowledge/vtt.json` |
| Thu | AI-DM | `knowledge/ai-dm.json` |

## Mission
Execute the procedural workflow script. NO complex analysis - just run the script and report results.

## Steps (Execute This)
```bash
bash /Users/chimpman/.openclaw/workspace-cheetah/workflow/procedural-phase1.sh
```

This script handles:
1. ✅ GitHub API fetch (30s)
2. ✅ README enrichment for top 3 repos (60s)
3. ✅ Knowledge base merge (60s)
4. ✅ Error handling & logging

## Your Job (30 seconds)
1. Execute the script above using exec tool
2. Read the log file it generates
3. Report: status, repos found, knowledge base file

## Success Criteria
- Script exits 0
- Knowledge base file updated
- Log shows completion

## Output Format
```
✅ Phase 1 Complete: <TOPIC>
- Script: procedural-phase1.sh
- Repos found: [N]
- Knowledge file: knowledge/<TOPIC>.json
- Log: checkpoints/phase1-YYYYMMDD-HHMMSS.log
- Status: READY for Phase 2 at 22:15
```

## Fast Failure Rules
- Script fails → Report error log path
- GitHub API rate-limited → Report "rate limited, will retry tomorrow"
- No results → Report "no new projects found"

## Note
Phase 2 runs at 22:15 via separate cron job. Independent execution.
