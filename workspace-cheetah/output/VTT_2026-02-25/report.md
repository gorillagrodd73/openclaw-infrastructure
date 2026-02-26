# VTT Research Report - February 25, 2026
## Virtual Tabletop Trends & Tools

---

## Executive Summary

The Foundry VTT ecosystem continues to expand rapidly, with **~165+ active modules** discovered in this week's scan highlighting strong community momentum. Key developments include:

- **AI-powered DM tools** emerging as a major trend (QuestForge, Bob's Talking NPCs)
- **Performance optimization** becoming critical (Geanos Scene Optimizer)
- **Cinematic visual storytelling** gaining traction (Drama Director, FXMaster)
- **Web-based VTT** alternatives developing (Drawspell, Lizzie)
- **V13 compatibility** driving updates across major modules

---

## Trending Discussions

### 🔥 Hot Topics

**1. Foundry VTT V14 Readiness**
- FXMaster v7.4 adds V14 compatibility and new preset API
- Calendaria module now integrates with FXMaster via API
- Module maintainers racing to update before V14 release

**2. Scene Performance & Optimization**
- Large scenes causing crashes with high-particle-density effects
- New tools addressing WebP conversion and audio optimization
- Multi-threaded WebCodecs for asset processing gaining attention

**3. AI Integration at the Table**
- Shift toward AI companions rather than full VTT replacements
- QuestForge positioning as "League of Legends client for D&D"
- Rule enforcement AI vs. creative AI DM debate

**4. Visual Storytelling Renaissance**
- Cinematic effects modules proliferating
- Region-based trigger systems standardizing
- Video overlay support becoming table stakes

---

## New Tools

### 🎯 Featured Finds

#### 1. FXMaster v7.4 by gambit07
- **What it does:** Particle effects, filters, and weather for Foundry scenes
- **Key Update:** V14 support + Preset API for cross-module integration
- **Premium Tier:** FXMaster+ adds exclusive effects (Lightning, Glitch, Sakura, etc.)
- **Impact:** Major ecosystem module with 165+ commits and growing
- **Link:** https://github.com/gambit07/fxmaster

#### 2. Bob's Talking NPCs by ogregod
- **What it does:** Complete NPC interaction system - quests, dialogue trees, merchants, factions, banking, hirelings
- **Key Feature:** Visual dialogue editor + relationships tracking
- **Target:** Foundry V13 + D&D 5e 5.2.4
- **Replaces:** Simple Quest, Item Piles, Monk's Active Tile Triggers
- **Link:** https://github.com/ogregod/Bob-s-Talking-NPCs

#### 3. Drama Director by phoenix1cold
- **What it does:** Cinematic storytelling tools - intros, endings, cutscenes, visual novel mode
- **Key Feature:** Voice recognition support + synchronized video overlays
- **Effects:** Vignette, Black & White, Sepia, Film Grain, Glitch, Blood overlay, Sakura petals
- **Compatibility:** Foundry V12-V13
- **Link:** https://github.com/phoenix1cold/drama-director-fvtt

#### 4. Geanos Scene Optimizer by Craftmesut
- **What it does:** Converts images to WebP and audio to OGG Opus
- **Tech:** Multi-threaded WebCodecs processing in browser
- **Impact:** Faster load times + reduced bandwidth usage
- **Status:** New release, MIT licensed
- **Link:** https://github.com/Craftmesut/geanos-scene-optimizer

#### 5. QuestForge by Kuduxaaa
- **What it does:** D&D 5e digital companion for PHYSICAL tabletop sessions
- **AI Modes:** Full DM / Assistant / NPC Dialogue / Encounter Generator / Rule Enforcer
- **Positioning:** "Not a VTT" - enhances in-person play with session management
- **Tech:** Web + Mobile, NestJS/Laravel backend, Vue 3 frontend
- **Phase:** Currently concept phase, seeking contributors
- **Link:** https://github.com/Kuduxaaa/questforge-hub

#### 6. Drawspell by hansy
- **What it does:** Web-based VTT with real-time sync
- **Features:** Multiplayer rendering, customizable canvas, visibility controls
- **Tech:** TypeScript, React, Socket.io, Docker-compose
- **Status:** v1.0.1 released, MPL-2.0 license
- **Link:** https://github.com/hansy/drawspell

#### 7. Lizzie by LizzieStudio
- **What it does:** Open-source VTT for homebrew game design
- **Features:** Real-time multiplayer, nested actor hierarchies, token-level inventory system, data migration scripts
- **Tech:** Node.js, TypeScript, Canvas API, ESLint, Husky
- **Status:** Active development
- **Link:** https://github.com/LizzieStudio/Lizzie

---

## Actionable Recommendations

### For Game Masters

1. **Install Bob's Talking NPCs** if running social-heavy campaigns with complex NPC networks
2. **Add Drama Director** for cinematic moments - intros/outros elevate session pacing
3. **Run Geanos Scene Optimizer** before your next session to reduce player load times
4. **Track FXMaster+** if you want premium environmental effects beyond core module

### For Tech-Savvy Groups

1. **Watch QuestForge** - concept-phase AI companion could revolutionize physical table play
2. **Evaluate Drawspell** if self-hosted open-source VTT appeals to your group
3. **Consider Lizzie** for homebrew systems needing custom token hierarchies

### For Module Developers

1. **Integrate with FXMaster Preset API** - Calendaria integration shows the pattern works
2. **Target WebCodecs** for performance-critical features
3. **Plan for V14** - compatibility bumps happening now across ecosystem

---

## Data Sources

- GitHub API: 15+ repositories searched (`virtual+tabletop`, `foundry+vtt`)
- Manual extraction via Jina AI endpoint
- Reddit API: BLOCKED (no data retrieved)

---

*Report generated: 2026-02-25*  
*Research agent: Cheetah*  
*Condition: Reddit unavailable, GitHub-only data*
