# Phase 2: Cheetah-Analyzer

**Role:** Insights extractor  
**Time Limit:** 10 minutes  
**Input:** `/Users/chimpman/.openclaw/workspace-cheetah/checkpoints/phase1-research.json`  
**Output:** `/Users/chimpman/.openclaw/workspace-cheetah/checkpoints/phase2-insights.md`  
**Next:** Spawns Phase 3 (Writer) on completion

## Mission
Analyze raw research data and extract actionable insights.

## Steps

1. **Read Input** (30 seconds)
   - Load phase1-research.json
   - Validate structure
   - If missing: report error and exit

2. **Extract Trends** (3 minutes)
   Identify:
   - Top 3 trending patterns
   - Most starred/active projects
   - Emerging technologies mentioned

3. **Compare & Categorize** (3 minutes)
   Group projects by:
   - Purpose (voice, memory, automation, etc.)
   - Tech stack (Python, Go, TS, etc.)
   - Development stage

4. **Generate Insights** (2 minutes)
   Write markdown with:
   - Executive summary (100 words)
   - 3-5 key findings with supporting data
   - Notable projects table
   - Gaps/opportunities identified

5. **Save Checkpoint** (30 seconds)
   Save to: `/Users/chimpman/.openclaw/workspace-cheetah/checkpoints/phase2-insights.md`

6. **Spawn Phase 3** (30 seconds)
   Use sessions_spawn to trigger Phase 3:
   ```
   Task: Read /Users/chimpman/.openclaw/workspace-cheetah/tasks/phase3-writer.md and execute as Cheetah (Phase 3: Writer)
   Mode: run
   Timeout: 600 seconds
   ```

## Output Structure
```markdown
# Research Insights: AI-DM Tools

## Executive Summary
[Brief overview]

## Key Findings
1. **[Finding 1]** - Evidence
2. **[Finding 2]** - Evidence
3. **[Finding 3]** - Evidence

## Notable Projects
| Project | Stars | Category | Insight |
|---------|-------|----------|---------|
| glyphoxa | 45 | Voice NPCs | Go-based, MCP support |

## Gaps & Opportunities
- [Identified gap]

## Ready for Report Generation
[Flag indicating phase 3 can proceed]
```

## Success Criteria
- [ ] Markdown file created
- [ ] At least 3 key findings documented
- [ ] Phase 3 spawned successfully

## Fast Failure Rules
- If input missing: report error, do NOT spawn Phase 3
- If <3 repos in input: note limitation, work with what exists
- If time > 8 min: save partial insights and spawn Phase 3 anyway
