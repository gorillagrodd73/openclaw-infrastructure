# Phase 3: Cheetah-Writer (Option C - Hybrid)

**Role:** Report generator and publisher  
**Time Limit:** 10 minutes  
**Input:** Knowledge base + insights from Phase 2  
**Output:** Living markdown report + daily summary
**Next:** (Optional) Spawn Riddler for digest

## Mission
Generate polished, readable reports from the accumulated knowledge base.

## Steps

1. **Load Knowledge Base** (30 seconds)
   ```bash
   cat /Users/chimpman/.openclaw/workspace-cheetah/knowledge/<TOPIC>.json
   ```

2. **Generate Living Report** (4 minutes)
   Use report generator script:
   ```bash
   cd /Users/chimpman/.openclaw/workspace-cheetah
   python3 scripts/generate_report.py <TOPIC> --type living --output reports/<TOPIC>_Living_Report.md
   ```
   
   This creates:
   - Full project listings with metadata
   - Today's additions highlighted
   - Trend analysis
   - Recommendations
   
   Output: `reports/<TOPIC>_Living_Report.md`

3. **Generate Daily Summary** (2 minutes)
   ```bash
   python3 scripts/generate_report.py <TOPIC> --type summary --output reports/daily_summaries/<TOPIC>_$(date +%Y-%m-%d).md
   ```
   
   This creates:
   - Just today's activity
   - Short digest format
   
   Output: `reports/daily_summaries/<TOPIC>_YYYY-MM-DD.md`

4. **Verify Reports** (2 minutes)
   - Check file exists: `ls -la reports/`
   - Check word counts: `wc -w reports/<TOPIC>_Living_Report.md`
   - Verify >400 words
   - Verify daily summary exists

5. **Update Topic Metadata** (1 minute)
   ```bash
   # Mark when last report was generated
   ```

6. **(Optional) Spawn Riddler** (30 seconds)
   If daily summary is substantial:
   ```
   Task: "You are Riddler. Create digest from Cheetah's daily report: reports/daily_summaries/<TOPIC>_$(date +%Y-%m-%d).md"
   Mode: run
   ```

7. **Cleanup** (30 seconds)
   - Remove checkpoint files: `checkpoints/phase*`

## Report Templates

### Living Report Structure
```markdown
# <TOPIC> Research - Living Document

*Topic: [Description]*

## 📊 Statistics
- Total Projects Tracked: [N]
- Tracking Since: [Date]
- Last Updated: [Date]
- New Today: [N]

---

## 📈 Today's Additions
[List of new projects with stars]

---

## 📚 All Tracked Projects
(List 20 top projects)

---

## 📊 Current Trends
(Analyze patterns)

---

## 💡 Recommendations
(Actionable advice)

---

*Generated: [Timestamp]*
```

### Daily Summary Structure
```markdown
# <TOPIC> Daily Summary - YYYY-MM-DD

## 📊 Today's Activity
- New Projects: [N]
- Updated Projects: [N]
- Total Tracked: [N]

## 🆕 New Projects
(List new ones)

## 🔄 Updated Projects
(List updated ones)

---

*Next update: [Next scheduled day]*
```

## Success Criteria
- [ ] Living Report generated (>400 words)
- [ ] Daily Summary generated
- [ ] Both files verified to exist
- [ ] Checkpoints cleaned up
- [ ] (Optional) Riddler spawned
- [ ] Completion reported

## Output Format
Report completion with:
```
✅ Phase 3 Complete: <TOPIC> Living Report Generated
- Living Report: reports/<TOPIC>_Living_Report.md
  - Word count: [N]
  - Total projects listed: [N]
- Daily Summary: reports/daily_summaries/<TOPIC>_YYYY-MM-DD.md
  - New projects: [N]
- Knowledge base: knowledge/<TOPIC>.json
  - Total tracked: [N]
- Checkpoints: Cleaned up ✅
- Riddler: [Spawned/Skipped]

🐆 CASCADE COMPLETE
```

## Fast Failure Rules
- If knowledge base missing → report error, save partial report if possible
- If report generation fails → try manual markdown creation
- If <400 words → note "insufficient data", but still save report
- Time > 9 min → skip optional Riddler spawn

## Notes
- Living Report is the main artifact - comprehensive reference
- Daily Summary is for quick consumption - what's new today
- Both get committed to git (cron-alerts channel for daily summary)
- Living Report accumulates over time, Daily Summary is ephemeral but archived by date
