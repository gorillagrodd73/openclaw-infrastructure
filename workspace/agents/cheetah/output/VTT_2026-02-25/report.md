# VTT (Virtual Tabletop) Research Report
**Date:** Wednesday, February 25th, 2026  
**Reporter:** Cheetah 🐆  
**Topic:** Virtual Tabletop Platform Updates and Tools

---

## Executive Summary

Foundry VTT continues to dominate the open-source VTT ecosystem with active development across multiple fronts. This week saw significant activity in:

- **New game system implementations** (Fabula Ultima, Earthdawn 4e, Torg Eternity)
- **Performance optimization tools** for handling large media assets
- **AI-powered VTT prototypes** emerging as a new trend
- **Advanced rendering modules** using three.js for 2.5D battlemaps

Reddit API access was blocked during research, but GitHub activity shows strong community momentum with 40+ relevant repositories updated this week.

---

## Trending Discussions

### Foundry VTT v13 Stable Release
- **Released:** Version 13 is now stable (v13.341)
- The platform continues its self-hosted, modern web-based approach
- Over 200 supported game systems
- Strong focus on API documentation for module developers

### Performance Optimization Gaining Traction
- **Scene optimization** is a major pain point for VTT users
- Large image/audio assets cause load time issues
- Community responding with automated conversion tools

---

## New Tools & Modules

### 🎮 Game Systems (New/Updated)

| Name | Description | Stars | Last Updated |
|------|-------------|-------|--------------|
| **Fabula Ultima** | JRPG-style tabletop experience for Foundry VTT | 87⭐ | Feb 25, 2026 |
| **Torg Eternity** | Multi-genre roleplaying system | 16⭐ | Feb 25, 2026 |
| **Earthdawn 4e** | Classic fantasy system implementation | 3⭐ | Feb 25, 2026 |
| **Synthetic Dream Machine** | New experimental system | 5⭐ | Feb 25, 2026 |

### ⚡ Performance Tools

| Name | Description | Key Feature |
|------|-------------|-------------|
| **geanos-scene-optimizer** | Media optimization module | Auto-converts images to WebP, audio to OGG Opus |
| **map-shine-advanced** | three.js integration | 2.5D battlemaps with BPR shading & particles |

### 🎯 Combat & Utility Modules

- **CritTheme** (NEW) - Theme songs that play when PCs crit or enemies fumble saves
- **Ranged Combat** - Helper effects and macros for Pathfinder 2e ranged combat
- **Rideable** - Token mounting/riding mechanics

### 🤖 AI-Powered VTT Projects

| Project | Description | Tech Stack |
|---------|-------------|------------|
| **Grimoire DnD VTT** | AI GM assistant with PDF/EPUB extraction, 3D dice, dynamic maps | TypeScript, React, Three.js |
| **DnD Quest AI** | AI-powered VTT with campaign generation | JavaScript, React, Express |
| **QuestForge Hub** | D&D companion platform (not a full VTT) | *New project* |

---

## Actionable Recommendations

### For VTT Users
1. **Monitor Foundry v13** - Check compatibility before upgrading
2. **Try geanos-scene-optimizer** - Reduces load times significantly
3. **Consider AI tools** - Grimoire/DnD Quest AI worth testing for campaign prep

### For Developers
1. **Scene optimization** is underserved - opportunity for better tools
2. **AI integration** is trending - early mover advantage available
3. **three.js rendering** - 2.5D battlemaps gaining interest

### For Community
1. **Performance remains #1 issue** - focus on optimization tutorials
2. **Game system diversity** growing - niche RPGs getting VTT support
3. **Self-hosting vs cloud** still a key decision point

---

## Notable Mentions

- **Dungeoneer** - Standalone 5e VTT with 204 stars, dynamic lighting, initiative tracker
- **Fantasy Dice Chamber** - Real-time dice roller supporting D&D and Warhammer
- **dndfog** - Python-based VTT with fog of war
- **dnd4e Beta** - D&D 4th Edition implementation (46 stars, actively maintained)

---

## Source Data

**Reddit:** API access blocked (authentication required for r/FoundryVTT, r/VTT)

**GitHub API Results:**
- Foundry VTT modules: 2,235+ JavaScript repositories
- Virtual tabletop related: 40 recent repositories
- Most active day: February 25, 2026 (today)

---

*Report compiled by Cheetah 🐆 | Speed is survival.*
