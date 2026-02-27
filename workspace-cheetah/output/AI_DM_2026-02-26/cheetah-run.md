# AI-DM Tools Research Report - Feb 26, 2026

## 3 Key Findings

1. **RAG is Essential for Campaign Continuity**: AI-DM tools are increasingly adopting Retrieval-Augmented Generation (RAG) to maintain persistent world state and narrative consistency. Projects like CSCI_4930_Dungeon_Master use LangChain to retrieve campaign history, ensuring NPCs remember player actions and story arcs remain coherent across sessions.

2. **Token Compression Cuts Costs 70-90%**: NeverEndingQuest pioneered a token compression system that dramatically reduces API costs while preserving game fidelity. This innovation makes hosting AI-DMs financially viable for regular play, shifting the economics from expensive per-token pricing to sustainable long-term campaigns.

3. **SRD Compliance is Standard**: Most active projects explicitly target SRD 5.2.1 compatibility, leveraging WOTC's Creative Commons content as a legal foundation. This standardization enables interoperability and reduces legal risk for open-source AI-DM development.

## 2 Notable Projects

### 1. NeverEndingQuest (MoonlightByte)
- **Stars**: 51 | **Lang**: Python/JavaScript
- Standout feature: Revolutionary token compression reducing API costs by 70-90%
- Full SRD 5.2.1 compatibility with memory of player decisions
- Supports local open-source models alongside OpenAI API

### 2. CALYPSO (northern-lights-province)
- **Stars**: 27 | **Research-backed**
- Academic-grade DM assistant with published research paper
- LLM-powered assistant designed for experienced DMs needing quick rule references
- Focuses on augmenting rather than replacing human DMs

## 1 Recommendation

**For Tabletop Groups**: Start with NeverEndingQuest if you want a complete AI-DM experience with cost-effective operation. Its token compression and local model support address the two biggest barriers (cost and API dependency) that kill most AI-DM projects.

**For Existing DMs**: Consider CALYPSO as a rules assistant rather than a full replacement—AI works best as a co-DM for lookups and improvisation prompts.

---

*Research conducted: Feb 26, 2026 | Sources: GitHub API, 5 repos analyzed*
*Word count: ~280*
