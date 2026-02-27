# Phase 1: Cheetah-Researcher (Option C - Hybrid)

**Role:** Research data gatherer
**Time Limit:** 10 minutes
**Input:** Today's topic based on day of week
**Output:** Raw findings added to knowledge base JSON
**Next:** Spawns Phase 2 (Analyzer) on completion

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
   Use Python script to gather and process data:
   ```bash
   cd /Users/chimpman/.openclaw/workspace-cheetah
   python3 scripts/research_github.py <TOPIC>
   ```
   
   Or manually with curl/jq:
   ```bash
   curl -sL --max-time 30 \
     "https://api.github.com/search/repositories?q=<QUERY>&sort=updated&per_page=15" \
     | jq '.items[] | {name: .full_name, description: .description, stars: .stargazers_count, language: .language, url: .html_url, updated: .updated_at}'
   ```

3. **Update Knowledge Base** (2 minutes)
   Use knowledge_manager.py to add findings:
   ```bash
   python3 scripts/knowledge_manager.py <TOPIC> < <RESEARCH_JSON>
   ```
   
   This:
   - Deduplicates by project name
   - Updates existing projects' star counts
   - Tracks first/last seen dates
   - Maintains running totals

4. **Save Research Artifacts** (1 minute)
   Save raw results to checkpoint (backup):
   ```bash
   checkpoints/phase1-<TOPIC>-<DATE>.json
   ```

5. **Spawn Phase 2** (30 seconds)
   Trigger Phase 2 with sessions_spawn:
   ```
   Task: "You are Cheetah Phase 2 (Analyzer). Read tasks/phase2-analyzer.md and process today's <TOPIC> findings."
   Mode: run
   Timeout: 600s
   ```

## Success Criteria
- [ ] GitHub API call successful (or error handled)
- [ ] At least 3 repos processed
- [ ] Knowledge base updated via knowledge_manager.py
- [ ] Phase 2 spawned
- [ ] Summary reported

## Output Format
Report completion with:
```
✅ Phase 1 Complete: <TOPIC>
- Repos found: [N]
- New to knowledge base: [N]
- Updated in knowledge base: [N]
- Total tracked: [N]
- Knowledge file: knowledge/<TOPIC>.json
- Phase 2: Spawned [session ID]
```

## Fast Failure Rules
- ⏱️ If GitHub API rate-limited → wait 60s, retry once, then skip
- ⏱️ If curl timeout → skip to next repo
- ⏱️ If knowledge_manager.py fails → save raw JSON manually, still spawn Phase 2
- ⏱️ If total time > 8 min → save what you have, spawn Phase 2

## Notes
- Focus on quality over quantity - better 5 detailed repos than 20 shallow ones
- Look for new/up-and-coming projects, not just most starred
- Note any emerging patterns or repeated keywords
- The knowledge_manager handles deduplication - don't worry about duplicates
