#!/usr/bin/env python3
"""
Grodd's Memory System Prototype
LanceDB-based semantic memory with sentence embeddings
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add virtual environment path
venv_path = Path("/Users/chimpman/.openclaw/.memory-venv/lib/python3.14/site-packages")
sys.path.insert(0, str(venv_path))

import lancedb
from sentence_transformers import SentenceTransformer
import numpy as np

# Configuration
DB_PATH = Path("/Users/chimpman/.openclaw/workspace/memory/embedding-index/lancedb")
WORKSPACE_ROOT = Path("/Users/chimpman/.openclaw/workspace")
MODEL_NAME = "all-MiniLM-L6-v2"  # Fast, good quality, 384 dimensions

def get_workspace_files() -> List[Path]:
    """Find all relevant markdown files to index."""
    files = []
    
    # Memory directory (daily notes)
    memory_dir = WORKSPACE_ROOT / "memory"
    if memory_dir.exists():
        files.extend(memory_dir.glob("*.md"))
    
    # Main workspace MD files
    for md_file in WORKSPACE_ROOT.glob("*.md"):
        if md_file.name not in [".gitignore", "README.md"]:
            files.append(md_file)
    
    # Agent workspaces
    for agent_dir in WORKSPACE_ROOT.parent.glob("workspace-*"):
        for md_file in agent_dir.glob("*.md"):
            files.append(md_file)
        # Agent daily memory
        agent_memory = agent_dir / "memory"
        if agent_memory.exists():
            files.extend(agent_memory.glob("*.md"))
    
    return sorted(files)

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 128) -> List[str]:
    """Split text into overlapping chunks for better retrieval."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def file_hash(filepath: Path) -> str:
    """Generate a hash of file content for change detection."""
    content = filepath.read_bytes()
    return hashlib.md5(content).hexdigest()

class MemorySystem:
    def __init__(self):
        self.db_path = DB_PATH
        self.model = None
        self.db = None
        self.table = None
        
    def initialize(self):
        """Initialize the database and model."""
        print("🧠 Initializing Memory System...")
        
        # Load embedding model
        print(f"   Loading model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)
        
        # Connect to/create database
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(str(DB_PATH))
        
        # Create or open table
        if "memories" in self.db.table_names():
            self.table = self.db.open_table("memories")
            print(f"   ✓ Opened existing table ({self.table.count_rows()} memories)")
        else:
            self.table = None
            print("   ✓ Ready to create new table")
    
    def index_files(self, force: bool = False):
        """Index all workspace files."""
        files = get_workspace_files()
        print(f"\n📚 Found {len(files)} files to index")
        
        # Get existing file hashes if table exists
        existing_hashes = {}
        if self.table:
            data = self.table.to_pandas()
            for _, row in data.iterrows():
                existing_hashes[row['filepath']] = row['content_hash']
        
        memories = []
        processed = 0
        skipped = 0
        
        for filepath in files:
            try:
                content = filepath.read_text(encoding='utf-8')
                content_hash = hashlib.md5(content.encode()).hexdigest()
                
                # Skip if unchanged
                rel_path = str(filepath.relative_to(WORKSPACE_ROOT.parent))
                if not force and rel_path in existing_hashes:
                    if existing_hashes[rel_path] == content_hash:
                        skipped += 1
                        continue
                
                # Chunk and embed
                chunks = chunk_text(content)
                
                for i, chunk in enumerate(chunks):
                    embedding = self.model.encode(chunk, convert_to_numpy=True)
                    
                    memories.append({
                        "id": f"{rel_path}#{i}",
                        "filepath": rel_path,
                        "filename": filepath.name,
                        "content": chunk,
                        "content_hash": content_hash,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "timestamp": datetime.now().isoformat(),
                        "vector": embedding.tolist()
                    })
                
                processed += 1
                if processed % 10 == 0:
                    print(f"   Processed {processed}/{len(files)} files...")
                    
            except Exception as e:
                print(f"   ⚠️  Error processing {filepath}: {e}")
        
        # Create or update table
        if memories:
            if self.table is None:
                self.table = self.db.create_table("memories", data=memories)
            else:
                # Delete old entries for these files and add new
                self.table.add(memories, mode="overwrite")
            
            print(f"\n✅ Indexed {len(memories)} chunks from {processed} files ({skipped} unchanged)")
        else:
            print(f"\n✅ No new content to index ({skipped} files unchanged)")
    
    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search memories by semantic similarity."""
        print(f"\n🔍 Query: '{query_text}'")
        
        if self.table is None:
            print("   ⚠️  No memories indexed yet")
            return []
        
        # Embed query
        query_embedding = self.model.encode(query_text, convert_to_numpy=True)
        
        # Search
        results = self.table.search(query_embedding.tolist()).limit(top_k).to_list()
        
        print(f"   Found {len(results)} relevant memories:\n")
        return results
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format search results for display."""
        output = []
        for i, result in enumerate(results, 1):
            score = result.get('_distance', 0)
            similarity = 1 / (1 + score)  # Convert distance to similarity-like score
            output.append(f"{i}. [{result['filename']}] (score: {similarity:.3f})")
            output.append(f"   Path: {result['filepath']}")
            # Show first 200 chars of content
            preview = result['content'][:200].replace('\n', ' ')
            output.append(f"   Preview: {preview}...")
            output.append("")
        return "\n".join(output)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Grodd's Memory System")
    parser.add_argument("command", choices=["index", "query", "stats"], 
                       help="Action to perform")
    parser.add_argument("--query", "-q", type=str, help="Query text for search")
    parser.add_argument("--force", "-f", action="store_true", 
                       help="Force reindex all files")
    parser.add_argument("--top-k", "-k", type=int, default=5, 
                       help="Number of results to return")
    
    args = parser.parse_args()
    
    memory = MemorySystem()
    memory.initialize()
    
    if args.command == "index":
        memory.index_files(force=args.force)
    
    elif args.command == "query":
        if not args.query:
            print("Error: --query required for search")
            sys.exit(1)
        results = memory.query(args.query, top_k=args.top_k)
        print(memory.format_results(results))
    
    elif args.command == "stats":
        if memory.table:
            count = memory.table.count_rows()
            print(f"\n📊 Memory Statistics:")
            print(f"   Total memories: {count}")
            print(f"   Database: {DB_PATH}")
            
            # Show unique files
            df = memory.table.to_pandas()
            files = df['filepath'].unique()
            print(f"   Unique files: {len(files)}")
        else:
            print("No memories indexed yet")

if __name__ == "__main__":
    main()
