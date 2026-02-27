# Phase 2: Cheetah-Analyzer (Option C - Hybrid)

**Role:** Insights extractor and trend analyzer
**Time Limit:** 10 minutes
**Input:** Current knowledge base for today's topic
**Output:** Trends and insights added to knowledge base

## Mission
Analyze accumulated knowledge base data and extract trends, patterns, and insights.

## Steps

1. **Load Knowledge Base** (30 seconds)
   ```bash
   cat /Users/chimpman/.openclaw/workspace-cheetah/knowledge/<TOPIC>.json
   ```

2. **Analyze Data** (6 minutes)
   - Compare today's findings vs previous days
   - Identify which projects gained stars
   - Extract common technologies/patterns
   - Look for emerging trends

3. **Update Knowledge Base** (2 minutes)
   Add trends as structured data to JSON

4. **Save Summary** (1 minute)
   Save brief analysis to:
   ```
   checkpoints/phase2-<TOPIC>-<DATE>.json
   ```

## Success Criteria
- [ ] Knowledge base loaded
- [ ] At least 2 trends/insights identified
- [ ] Knowledge base updated with trends
- [ ] Summary checkpoint saved

## Output Format
```
✅ Phase 2 Complete: <TOPIC>
- Trends identified: [N]
- Recommendations: [N]
- Knowledge base trends updated
- Checkpoint: checkpoints/phase2-<TOPIC>-<DATE>.json
- Next: Phase 3 at 22:30
```

## Fast Failure Rules
- Missing knowledge base → Report error, wait for tomorrow
- Insufficient data → Note in checkpoint, proceed minimally
