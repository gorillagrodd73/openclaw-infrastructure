# AI Dungeon Master Tools Research Report
*Date: February 26, 2026*

---

## Executive Summary

• **Rapid Innovation in AI-Native TTRPG Assistants**: A surge of new projects combining LLMs with tabletop RPG workflows, particularly focused on persistent memory, voice NPCs, and MCP (Model Context Protocol) integrations for seamless AI assistant interaction.

• **The Rise of Memory-Aware Systems**: Emerging tools like **AI-Dungeon-Master-Persistent-Storytelling** and **Dungeon-Master-** use ChromaDB/RAG to maintain long-term campaign continuity, addressing the key limitation of stateless AI interactions.

• **Voice-First NPC Experience**: New tools like **glyphoxa** are pioneering AI-powered voice NPCs for tabletop, bringing text-to-speech and speech-to-text to character interactions.

• **Server-Authoritative Platforms**: Projects like **fracturing.space** are building infrastructure specifically designed for AI Game Masters, with persistent state and deterministic mechanics.

• **MCP Protocol Adoption**: Multiple projects now integrating MCP (Model Context Protocol) to enable AI assistants to natively interact with campaign data, character sheets, and worldbuilding tools.

---

## Trending Discussions

### 1. Persistent Memory Architecture
- **Key Trend**: The shift from stateless AI DMs to systems with **long-term memory architectures**
- **Discussion Focus**: How to maintain narrative coherence across multi-session campaigns
- **Notable Projects**: 
  - `archmagi` - Claude-based DM with adaptive narrative engine
  - `AI-Dungeon-Master-Persistent-Storytelling` - Built for Inter IIT Tech Meet 14.0
  - `Dungeon-Master-` - Uses Groq (Llama 3) + ChromaDB for infinite storytelling

### 2. Voice NPC Integration
- **Emerging Pattern**: AI-generated voice for NPCs is gaining traction
- **Discussion Focus**: Platform-agnostic frameworks that work with multiple TTS providers
- **Notable Project**: `glyphoxa` - AI-Powered Voice NPCs for Tabletop RPGs (Go-based)

### 3. MCP Protocol for TTRPGs
- **Technical Trend**: Integrating Model Context Protocol into RPG tooling
- **Discussion Focus**: Standardizing how AI assistants access campaign data
- **Notable Projects**:
  - `role-playing-mcp-server` - RPG server for MCP with dynamic storylines
  - `ttrpg-mcp-on-cloudflare` - Cloudflare-hosted MCP for TTRPGs
  - `dungeon-masters-companion` - Proposed MCP-powered AI DM system

---

## New Tools & Projects

### Recently Updated (February 2026)

| Project | Stars | Lang | Description |
|---------|-------|------|-------------|
| **glyphoxa** | New | Go | AI-Powered Voice NPCs for TTRPGs with MCP support |
| **amber** | New | Rust | AI agent scenario generator |
| **fracturing.space** | New | Go | Server-authoritative platform designed for AI Game Master |
| **CampaignMaster** | New | TS | Simple TTRPG campaign manager with AI image generation |
| **dnd-5e-architect** | New | CSS | AI Skill for world/campaign building |
| **libris-maleficarum** | 1⭐ | TS | AI-enhanced campaign manager (React/.NET 8) |

### Established & Notable

| Project | Stars | Lang | Description |
|---------|-------|------|-------------|
| **BOT-MMORPG-AI** | 174⭐ | Jupyter | Personal gaming AI assistant for MMORPG/RPG |
| **archmagi** | 1⭐ | - | Claude-powered DM system with literary-grade storytelling |
| **role-playing-mcp-server** | 10⭐ | JS | RPG server for MCP with dynamic storylines |

### By Category

**Campaign Management:**
- `libris-maleficarum` - .NET 8 + React/TypeScript
- `CampaignManager` - Shared views with AI image capabilities
- `CampaignMaster` - AI-enabled TTRPG app

**Character Tools:**
- `AI-RPG-Character-Sheet-Generator` - TypeScript character generator
- `dnd-5e-architect` - AI Skill for campaign building

**Voice & NPC:**
- `glyphoxa` - Voice AI framework for tabletop (Go)

**Infrastructure:**
- `fracturing.space` - Go-based platform for AI GM
- `dungeon-masters-companion` - MCP-powered AI DM proposal

---

## Actionable Recommendations

### For Players & DMs

1. **Try Memory-First Tools**: Projects like `Dungeon-Master-` with ChromaDB integration offer actual campaign memory—start here for long-term campaigns.

2. **Explore Voice NPCs**: If playing online, `glyphoxa` represents the next evolution in immersion—AI voices for every NPC.

3. **MCP-Ready Workflow**: Adopt tools that support MCP protocol to future-proof your workflow as AI assistants improve.

### For Developers

1. **Focus on Memory**: The biggest pain point is state persistence. Projects solving this (RAG, vector DBs) are seeing the most interest.

2. **MCP Integration**: Build MCP servers for TTRPG tools—this is becoming the standard for AI assistant interoperability.

3. **Voice + Text Hybrid**: Tools combining TTS/STT with LLM narrative generation are underrepresented but high-impact.

### Technology Trends to Watch

- **Groq + Llama 3**: High-speed inference for real-time DM responses
- **ChromaDB/Pinecone**: Vector databases for campaign memory
- **Cloudflare Workers**: Edge-deployed MCP servers
- **TypeScript/React**: Dominant stack for campaign management UIs

---

## Links

- GitHub Topic: `ai+dungeon+master` trending with new MCP integrations
- Key Technologies: Groq, Claude, ChromaDB, MCP Protocol, Cloudflare Workers

---

*Report generated using GitHub API Search on February 26, 2026*
