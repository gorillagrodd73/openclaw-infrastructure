# Cheetah Autonomous 0-COST Web Research Workflow

## Overview
Zero-cost web research using public APIs and Jina AI for content extraction.
No authentication required for any data source.

## Research Topics (Rotate Daily)
1. AI/LLM Developments — Reddit r/LocalLLaMA, GitHub trending
2. Developer Tools — GitHub trending repos, dev subreddits
3. Virtual Tabletop RPG — r/VTTRPG, FoundryVTT, Roll20 communities
4. AI Dungeon Master Tools — r/DMAcademy, AI RPG tools

## Phase 1: Reddit Data (No Auth Required)
Use Reddit JSON endpoints (public, rate-limit friendly):
- `https://www.reddit.com/r/LocalLLaMA/top.json?limit=25&t=week`
- `https://www.reddit.com/r/FoundryVTT/top.json?limit=25&t=week`
- `https://www.reddit.com/r/DMAcademy/top.json?limit=25&t=week`
- `https://www.reddit.com/r/gamedev/top.json?limit=25&t=week`

Use `web_fetch` or `curl` to retrieve JSON, parse for:
- Post titles + scores
- URLs to interesting projects
- Selftext for tool discussions

## Phase 2: GitHub Discovery (No Auth Required)
Use GitHub Search API v3 (public, 60 req/hr unauthenticated):
- `https://api.github.com/search/repositories?q=ai+dungeon+master&sort=updated&order=desc`
- `https://api.github.com/search/repositories?q=foundry+vtt+ai&sort=updated`
- `https://api.github.com/search/repositories?q=llm+local&sort=stars`

Extract:
- Repository name, description, stars
- Primary language
- Last updated
- README content URL

## Phase 3: Deep Content Extraction (Jina AI via web_fetch)
For each interesting URL found:
- Use `web_fetch` with Jina AI extraction (automatic via OpenClaw)
- Alternative: `https://r.jina.ai/http://URL` endpoint (Jina's summary service)

## Phase 4: Synthesis & Report Generation
Generate markdown reports with sections:
- **Executive Summary** (3-5 bullet points)
- **Trending Discussions** (Reddit insights)
- **New Tools & Projects** (GitHub discoveries)
- **Actionable Recommendations** (what to explore/adopt)

## Output Format
Save to: `/Users/chimpman/.openclaw/workspace/agents/cheetah/output/<TOPIC>_<DATE>/`
- `report.md` — Main findings
- `sources.json` — All URLs referenced
- `actionable/` — Specific recommendations with next steps

## Execution Rules
- DO NOT use web_search (Brave API has costs)
- DO use web_fetch for all HTTP requests (uses Jina AI under hood)
- Rotate research topics daily (use date hash: day % 4)
- Respect rate limits: add delays between requests
- Save all raw data before synthesis (reproducible research)

## Today's Research Assignment (Auto-Select)
Based on day of week:
- Mon: AI/LLM Developments
- Tue: Developer Tools
- Wed: Virtual Tabletop RPG
- Thu: AI Dungeon Master Tools
- Fri: AI/LLM Developments
- Sat: Developer Tools (light)
- Sun: VTT + DM Tools combined (weekly digest)

---
*Template created: 2026-02-25*
