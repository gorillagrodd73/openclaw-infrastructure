# Phase 1: Cheetah-Researcher (Option C - Hybrid)

**Role:** Research data gatherer
**Time Limit:** 10 minutes
**Input:** Today's topic based on day of week
**Output:** Knowledge base updated with new findings

## Today's Topic
| Day | Topic | Knowledge Base |
|-----|-------|----------------|
| Mon | AI-LLM | `knowledge/ai-llm.json` |
| Tue | DevTools | `knowledge/devtools.json` |
| Wed | VTT | `knowledge/vtt.json` |
| Thu | AI-DM | `knowledge/ai-dm.json` |
| Fri | AI-LLM | `knowledge/ai-llm.json` |
| Sat/Sun | Mixed | Any pending topics |

## Steps

1. **Get Topic** (10 seconds)
   - Determine today's topic from table above

2. **Research Phase** (6 minutes max)
   Use Python script to gather GitHub data:
   ```bash
   cd /Users/chimpman/.openclaw/workspace-cheetah
   python3 scripts/research_github.py <TOPIC>
   ```
   
   This fetches:
   - 10 repos from GitHub API (30s timeout, single call)
   - README content for top 3 repos only

3. **Update Knowledge Base** (2 minutes)
   Process research JSON and update knowledge base:
   ```bash
   python3 scripts/research_github.py <TOPIC> | python3 scripts/knowledge_manager.py --process-stdin <TOPIC>
   ```
   
   This deduplicates and merges with existing data.

4. **Report** (1 minute)
   Check knowledge base status and report.

## Success Criteria
- [ ] GitHub API call successful (or error handled gracefully)
- [ ] At least 3 repos processed
- [ ] Knowledge base updated
- [ ] Summary reported to Discord

## Output Format
```
✅ Phase 1 Complete: <TOPIC>
- Repos found: [N]
- New to knowledge base: [N]  
- Updated: [N]
- Total tracked: [N]
- Knowledge file: knowledge/<TOPIC>.json
- Next: Phase 2 at 22:15
```

## Fast Failure Rules
- GitHub API rate-limited → Save error, report "rate limited, retry tomorrow"
- No results → Report "no new projects found"
- Knowledge manager fails → Save raw JSON to checkpoints/, report partial success

## Phase 2/3 Note
- Phase 2 runs at 22:15 (cron job), **NOT spawned by Phase 1**
- Phase 3 runs at 22:30 (cron job), **NOT spawned by Phase 2**
- Each phase is independent with checkpoints for resilience
