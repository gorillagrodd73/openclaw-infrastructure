# Phase 2: Cheetah-Analyzer (Option C - Hybrid)

**Role:** Insights extractor and trend analyzer
**Time Limit:** 10 minutes
**Input:** Current knowledge base for today's topic
**Output:** Trends and insights added to knowledge base
**Next:** Spawns Phase 3 (Writer) on completion

## Mission
Analyze accumulated knowledge base data and extract trends, patterns, and insights.

## Steps

1. **Load Knowledge Base** (30 seconds)
   ```bash
   cat /Users/chimpman/.openclaw/workspace-cheetah/knowledge/<TOPIC>.json
   ```
   
   Today's topic from Phase 1 context.

2. **Analyze New Data** (4 minutes)
   Identify:
   - **New projects**: What got added today vs. what already existed
   - **Trending projects**: Which existing projects gained significant stars?
   - **Technology patterns**: What languages/frameworks are dominant?
   - **Feature patterns**: Common features across projects (MCP, voice, memory, etc.)
   - **Activity patterns**: What's hot right now?

3. **Extract Trends** (3 minutes)
   Use semantic analysis:
   ```bash
   # Search memory for related topics
   ./memory/embedding-index/grodd-memory query -q "<TOPIC> trends patterns"
   ```
   
   Or use OpenClaw memory_search tool:
   ```
   memory_search: "<TOPIC> recent developments trends"
   ```

4. **Update Knowledge Base** (2 minutes)
   Add insights as structured data:
   ```json
   {
     "trends": [
       {
         "text": "Trending observation",
         "category": "technical|ux|market",
         "firstSeen": "2026-02-26",
         "evidence": ["project1", "project2"]
       }
     ],
     "recommendations": [
       {
         "text": "Actionable recommendation",
         "category": "for_developers|for_users",
         "priority": "high|medium|low"
       }
     ]
   }
   ```

5. **Save Checkpoint** (30 seconds)
   ```bash
   checkpoints/phase2-<TOPIC>-<DATE>-insights.json
   ```

6. **Generate Quick Summary** (30 seconds)
   Create mini-summary of key findings for Phase 3:
   ```bash
   checkpoints/phase2-summary-<DATE>.md
   ```

7. **Spawn Phase 3** (30 seconds)
   ```
   Task: "You are Cheetah Phase 3 (Writer). Read tasks/phase3-writer.md and generate living report for <TOPIC>."
   Mode: run
   Timeout: 600s
   ```

## Analysis Framework

### Questions to Answer
1. **What new projects emerged?** Are they forks, originals, related to existing ones?
2. **What's gaining traction?** Compare star counts across days.
3. **What's dying?** Projects not updated recently.
4. **Technology trends**: Language shifts, framework adoption.
5. **Feature convergence**: Are projects copying each other? What's the "must-have" feature?

### Trend Categories
- **Technical**: Architecture patterns, language choices, integrations
- **UX**: User experience improvements, workflow optimizations
- **Market**: Competitive landscape, positioning, target audiences

## Success Criteria
- [ ] Knowledge base loaded successfully
- [ ] At least 2 new trends identified and documented
- [ ] At least 1 recommendation generated
- [ ] Insights saved to knowledge base
- [ ] Phase 3 spawned
- [ ] Summary created for Phase 3 reference

## Output Format
Report completion with:
```
✅ Phase 2 Complete: <TOPIC>
- Knowledge base entries: [N]
- New projects today: [N]
- Trends identified: [N]
- Recommendations: [N]
- Phase 3: Spawned [session ID]
```

## Fast Failure Rules
- If knowledge base missing → report error, DO NOT spawn Phase 3
- If analysis time > 8 min → save partial insights, spawn Phase 3 anyway
- No trends found → note "no significant trends detected", still spawn Phase 3

## Notes
- Focus on *actionable* insights, not just observations
- Compare against previous entries to identify what's truly new
- Look for clusters - multiple projects doing the same thing indicates a trend
- Be concise in the knowledge base - structured data wins over prose
