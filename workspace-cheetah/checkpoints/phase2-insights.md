# Research Insights: AI-DM Tools

## Executive Summary

Analysis of 10 AI-DM repositories reveals a rapidly evolving ecosystem dominated by Python-based solutions focused on privacy-preserving, local LLM deployments. The space shows strong convergence around **RAG architectures** for D&D 5e rule retrieval and **voice-enabled interfaces** for real-time session assistance. Most projects are early-stage (0-1 stars) but show active development with commits as recent as February 2026, indicating fresh momentum in this niche.

---

## Key Findings

### 1. **Python Dominates the Stack**
- **60% of projects** use Python (6/10 repos)
- Enables easy integration with popular AI frameworks (LangChain, Ollama, LlamaIndex)
- TypeScript/JavaScript holds second place (30%) for web-based interfaces

### 2. **RAG is the Killer Architecture**
- **3 projects** explicitly build RAG pipelines for D&D 5e rules
- Pattern: Vector DB (ChromaDB/Qdrant) + Local LLM (Ollama/llama3.1) + Embeddings
- Key differentiator: Privacy-focused, zero-cloud dependency claims
- Evidence: dnd-rag-helper, natural20-rag, DnD-RAG-Chatbot

### 3. **Voice Integration = Emerging Battleground**
- **2 projects** ship with voice capabilities (dm-hud, DND_DM)
- Tech stack: Deepgram (transcription) + TTS (edge-tts, pyttsx3) + Whisper
- dm-hud describes itself as an "always-listening second brain"
- Represents the shift from prep assistants to real-time session tools

### 4. **Most Active Development**
| Project | Last Updated | Notable Feature |
|---------|--------------|-----------------|
| dm-hud | 2026-02-25 | Claude AI + Deepgram transcription |
| ai-dm-assistant | 2026-02-24 | Session preparation focus |
| gary | 2026-02-22 | TypeScript-based DM assistant |

### 5. **Project Maturity: Early Stage**
- No project exceeds 1 star
- Average age: ~1-4 months of active development
- Opportunity: First-mover advantage still available

---

## Notable Projects

| Project | Stars | Language | Category | Insight |
|---------|-------|----------|----------|---------|
| dm-hud | 0 | JavaScript | Real-time Assistant | Claude AI + Deepgram, always-listening architecture |
| dnd-rag-helper | 1 | Python | RAG/Rule Query | LangChain + ChromaDB + Ollama stack |
| natural20-rag | 0 | Python | RAG/Rule Query | LlamaIndex + Qdrant, includes observability |
| DnDbug | 1 | Python | Story/Narrative | Macro (scene chains) + Detail (scene content) layers |
| DND_DM | 0 | Python | Voice Assistant | Cinematic TTS + Whisper STT + Full combat tracking |
| gary | 0 | TypeScript | DM Assistant | Modern web stack, good for UI reference |

---

## Gaps & Opportunities

1. **MCP (Model Context Protocol) Support** - None of the analyzed projects mention MCP integration
2. **Multi-Modal Support** - No image/map understanding capabilities found
3. **Campaign Memory Persistence** - Limited long-term memory across sessions
4. **Dice-Roll Integration** - Only DND_DM mentions dice mechanics; most overlook physical-digital bridge
5. **Export/Sharing Formats** - No standard campaign export formats (JSON/YAML) emerging

---

## Ready for Report Generation

✅ Phase 2 complete. Phase 3 (Writer) can proceed.

**Input for Phase 3:**
- Total repos analyzed: 10
- Key trend: RAG + Voice convergence
- Recommended focus: Privacy-first, local LLM architecture
- Language recommendation: Python (ecosystem maturity)
