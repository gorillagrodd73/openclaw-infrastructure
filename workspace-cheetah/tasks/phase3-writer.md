# Phase 3: Cheetah-Writer (Option C - Hybrid)

**Role:** Report generator and publisher
**Time Limit:** 10 minutes
**Input:** Knowledge base + Phase 2 checkpoint
**Output:** Living markdown report + daily summary

## Mission
Generate polished reports from the accumulated knowledge base.

## Steps

1. **Load Knowledge Base** (30 seconds)
   ```bash
   cat /Users/chimpman/.openclaw/workspace-cheetah/knowledge/<TOPIC>.json
   ```

2. **Generate Living Report** (4 minutes)
   ```bash
   python3 scripts/generate_report.py <TOPIC> --type living
   ```
   Output: `reports/<TOPIC>_Living_Report.md`

3. **Generate Daily Summary** (2 minutes)
   ```bash
   python3 scripts/generate_report.py <TOPIC> --type summary --output reports/daily_summaries/<TOPIC>_$(date +%Y-%m-%d).md
   ```
   Output: `reports/daily_summaries/<TOPIC>_YYYY-MM-DD.md`

4. **Verify Reports** (2 minutes)
   Check both files exist, verify word counts > 400

5. **Commit Reports** (1 minute)
   ```bash
   cd /Users/chimpman/.openclaw
   git add workspace-cheetah/reports/
   git commit -m "Cheetah: Daily reports for <TOPIC> $(date +%Y-%m-%d)"
   git push origin main
   ```

6. **Cleanup** (30 seconds)
   ```bash
   rm -f workspace-cheetah/checkpoints/phase2-*.json
   ```

## Success Criteria
- [ ] Living Report generated (>400 words)
- [ ] Daily Summary generated
- [ ] Both committed to git
- [ ] Checkpoints cleaned
- [ ] Completion reported

## Output Format
```
✅ Phase 3 Complete: <TOPIC> CASCADE DONE
- Living Report: reports/<TOPIC>_Living_Report.md ([N] words)
- Daily Summary: reports/daily_summaries/<TOPIC>_YYYY-MM-DD.md ([N] words)
- Committed: Yes
- Checkpoints: Cleaned
```

## Fast Failure Rules
- Missing knowledge base → Generate minimal report, note error
- Report < 400 words → Save anyway, note "insufficient data"
- Git push fails → Report error, keep local files

## Schedule
This phase runs at 22:30 via cron job - **standalone, not spawned**.
```