# Grodd's Semantic Memory System (LanceDB)

A local, private semantic memory using embeddings and vector search.

## Architecture

| Component | Purpose |
|-----------|---------|
| **LanceDB** | Vector database for fast semantic search |
| **all-MiniLM-L6-v2** | 384-dimensional sentence embeddings (fast, accurate) |
| **Chunking** | Overlapping 512-character chunks for better retrieval |
| **Content Hash** | Change detection to avoid re-indexing unchanged files |

## Files

```
memory/embedding-index/
├── memory_system.py      # Core indexing & search logic
├── grodd-memory          # CLI wrapper script
├── lancedb/              # Vector database (auto-created)
│   └── memories/         # Embedding table
└── README.md             # This file
```

## Usage

### Index All Files
```bash
./grodd-memory index
```

### Semantic Search
```bash
./grodd-memory query -q "what did Calous say about cron jobs" -k 5
```

### Force Reindex (ignore change detection)
```bash
./grodd-memory index --force
```

### Get Stats
```bash
./grodd-memory stats
```

## Integration with Grodd

To use this in sessions, add to `TOOLS.md`:

```bash
# Semantic Memory Search
/path/to/grodd-memory query -q "your query here" -k 3
```

Or create a tool wrapper at `/Users/chimpman/.openclaw/tools/memory_search`.

## Performance

- **Embedding time**: ~100ms per chunk (on M-series Mac)
- **Search time**: ~50ms for top-k
- **Storage**: ~1KB per 512-char chunk (vector + metadata)
- **Memory**: <500MB for model + database

## Security

- All data stays **local** - nothing leaves your machine
- Embeddings are computed locally
- LanceDB is a flat file database (no server)

## Future Enhancements

- [ ] Auto-index via cron job (nightly)
- [ ] Multi-modal (images via CLIP)
- [ ] Re-ranking of results
- [ ] Cross-reference with calendar/email
