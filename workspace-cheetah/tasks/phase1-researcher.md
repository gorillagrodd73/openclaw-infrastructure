# Phase 1: Cheetah-Researcher

**Role:** Research data gatherer
**Time Limit:** 10 minutes
**Input:** Today's topic (Thu=AI-DM)
**Output:** `/Users/chimpman/.openclaw/workspace-cheetah/checkpoints/phase1-research.json`

## Mission
Gather raw research data on AI Dungeon Master tools from GitHub.

## Steps

1. **Determine Topic** (30 seconds)
   - Today is Thursday → AI-DM topic

2. **GitHub API Search** (2 minutes max)
   ```bash
   curl -sL --max-time 20 \
     "https://api.github.com/search/repositories?q=ai+dungeon+master+OR+ai+dm+OR+rpg+ai+assistant&sort=updated&per_page=10" \
     | jq '{items: [.items[] | {name, full_name, description, html_url, stars: .stargazers_count, updated: .updated_at, language}]}'
   ```

3. **Fetch Top 5 Details** (3 minutes max)
   For each of 5 most interesting repos:
   ```bash
   curl -sL --max-time 15 "https://r.jina.ai/http://github.com/user/repo"
   ```

4. **Save Checkpoint** (30 seconds)
   Save JSON to: `/Users/chimpman/.openclaw/workspace-cheetah/checkpoints/phase1-research.json`

## Success Criteria
- [ ] At least 3 repos with full details
- [ ] JSON file created with structure:
  ```json
  {
    "timestamp": "ISO8601",
    "topic": "AI-DM",
    "repos": [...],
    "sources": ["github"]
  }
  ```

## Fast Failure Rules
- If GitHub API rate-limited: skip, save what you have
- If curl timeout after 2 attempts: skip that repo
- If total time exceeds 8 min: save partial results

## Output Example
```json
{
  "timestamp": "2026-02-26T22:00:00Z",
  "topic": "AI-DM",
  "repos": [
    {"name": "glyphoxa", "stars": 45, "description": "...", "readme": "..."}
  ]
}
```
