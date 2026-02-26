#!/usr/bin/env python3
"""
Simple memory search for use within Grodd sessions
Usage: python3 search.py "your query here"
"""

import sys
import json
from pathlib import Path

# Setup paths
VENV_PATH = Path("/Users/chimpman/.openclaw/.memory-venv/lib/python3.14/site-packages")
sys.path.insert(0, str(VENV_PATH))

import lancedb
from sentence_transformers import SentenceTransformer

DB_PATH = Path("/Users/chimpman/.openclaw/workspace/memory/embedding-index/lancedb").resolve()
MODEL_NAME = "all-MiniLM-L6-v2"

def search(query: str, top_k: int = 5):
    """Search memories and return JSON results."""
    
    # Load model (cached after first run)
    model = SentenceTransformer(MODEL_NAME)
    
    # Connect to DB
    db = lancedb.connect(str(DB_PATH))
    
    tables = db.list_tables()
    table_names = tables.tables if hasattr(tables, 'tables') else tables
    if "memories" not in table_names:
        return {"error": "No memories indexed. Run: ./grodd-memory index"}
    
    table = db.open_table("memories")
    
    # Embed query
    query_embedding = model.encode(query, convert_to_numpy=True)
    
    # Search
    results = table.search(query_embedding.tolist()).limit(top_k).to_list()
    
    # Format
    output = []
    for result in results:
        output.append({
            "filepath": result.get("filepath", ""),
            "filename": result.get("filename", ""),
            "preview": result.get("content", "")[:300],
            "relevance": round(1 / (1 + result.get("_distance", 0)), 3)
        })
    
    return {"query": query, "results": output}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search.py 'your query here'", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    result = search(query)
    print(json.dumps(result, indent=2))
