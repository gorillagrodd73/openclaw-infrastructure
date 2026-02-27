#!/usr/bin/env python3
"""
Cheetah Project Runner
Iterates through /Users/chimpman/Projects/ and runs research per-project.
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECTS_ROOT = Path("/Users/chimpman/Projects")

def get_projects():
    """Get all project directories."""
    if not PROJECTS_ROOT.exists():
        return []
    return [d for d in PROJECTS_ROOT.iterdir() if d.is_dir()]

def load_instructions(project_path):
    """Load cheetah instructions for a project if they exist."""
    instructions_file = project_path / ".ai" / "cheetah" / "instructions.json"
    if instructions_file.exists():
        with open(instructions_file, 'r') as f:
            return json.load(f)
    return None

def load_expansion_queue(project_path):
    """Load expansion suggestions from Riddler's latest digest."""
    digest_file = project_path / ".ai" / "riddler" / "output" / "latest.md"
    if not digest_file.exists():
        return []
    
    try:
        with open(digest_file, 'r') as f:
            content = f.read()
        
        # Extract EXPANSION JSON from HTML comment
        match = re.search(r'<!-- EXPANSION: (.*?)-->', content, re.DOTALL)
        if match:
            expansion_json = match.group(1).strip()
            return json.loads(expansion_json)
    except Exception as e:
        print(f"   (no expansion queue found: {e})")
    
    return []

def get_expansion_state(project_path):
    """Get state of searched expansions."""
    state_file = project_path / ".ai" / "cheetah" / ".state.json"
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
            return state.get("expansions", {})
    return {}

def save_expansion_searched(project_path, expansion_id, depth):
    """Mark an expansion as searched."""
    state_file = project_path / ".ai" / "cheetah" / ".state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    
    state = {}
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
    
    if "expansions" not in state:
        state["expansions"] = {}
    
    state["expansions"][expansion_id] = {
        "depth": depth,
        "last_searched": datetime.now().isoformat()
    }
    
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def should_run_topic(topic, last_run_str):
    """Check if a topic should run based on frequency."""
    frequency = topic.get("frequency", "daily")
    if not last_run_str:
        return True
    
    last_run = datetime.fromisoformat(last_run_str)
    now = datetime.now()
    delta = now - last_run
    
    if frequency == "daily":
        return delta.days >= 1
    elif frequency == "weekly":
        return delta.days >= 7
    elif frequency == "hourly":
        return delta.total_seconds() >= 3600
    return True

def get_last_run(project_path, topic_id):
    """Get last run timestamp for a topic in a project."""
    state_file = project_path / ".ai" / "cheetah" / ".state.json"
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
            return state.get("last_runs", {}).get(topic_id)
    return None

def save_last_run(project_path, topic_id):
    """Save last run timestamp for a topic."""
    state_file = project_path / ".ai" / "cheetah" / ".state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    
    state = {}
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
    
    if "last_runs" not in state:
        state["last_runs"] = {}
    state["last_runs"][topic_id] = datetime.now().isoformat()
    
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def research_topic_for_project(project_path, topic, output_dir):
    """Research a topic for a specific project."""
    from research import research_topic
    
    print(f"  → Researching '{topic['id']}: {topic['query']}'")
    results = research_topic(topic['id'], topic['query'])
    
    # Save results
    date_str = datetime.now().strftime('%Y-%m-%d')
    results["project"] = str(project_path.name)
    results["topic_id"] = topic['id']
    
    # Save to knowledge base
    kb_file = output_dir / "knowledge.json"
    knowledge = {"projects": [], "date": date_str}
    if kb_file.exists():
        with open(kb_file, 'r') as f:
            knowledge = json.load(f)
    
    # Append new findings
    knowledge["projects"].extend(results.get("projects", []))
    knowledge["last_updated"] = datetime.now().isoformat()
    
    kb_file.parent.mkdir(parents=True, exist_ok=True)
    with open(kb_file, 'w') as f:
        json.dump(knowledge, f, indent=2)
    
    # Archive daily snapshot
    archive_dir = output_dir / "archive" / date_str
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_file = archive_dir / f"{topic['id']}.json"
    with open(archive_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"  ✓ Saved to {archive_file}")
    return results

def run_for_project(project_path):
    """Run Cheetah research for a single project."""
    instructions = load_instructions(project_path)
    if not instructions:
        print(f"  (no instructions, skipping)")
        return None
    
    print(f"\n📁 Project: {project_path.name}")
    
    output_dir = project_path / ".ai" / "cheetah" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    # --- EXPANSION QUEUE (Riddler-guided) ---
    expansion_queue = load_expansion_queue(project_path)
    expansion_state = get_expansion_state(project_path)
    max_depth = 2  # Configurable
    
    if expansion_queue:
        print(f"  🔍 Found {len(expansion_queue)} expansion suggestion(s) from Riddler")
        
        for exp in expansion_queue:
            exp_id = exp.get('id')
            exp_depth = exp.get('depth', 1)
            
            # Skip if already searched at this depth
            if exp_id in expansion_state:
                prev_depth = expansion_state[exp_id].get('depth', 0)
                if prev_depth >= exp_depth:
                    print(f"    ⏸ Skipping '{exp_id}' (already searched at depth {prev_depth})")
                    continue
            
            # Only search if depth is within limit
            if exp_depth <= max_depth:
                print(f"    ↳ Expanding: {exp.get('name')} (depth {exp_depth})")
                
                # Create expansion topic
                expansion_topic = {
                    'id': f"expansion-{exp_id}",
                    'query': exp.get('query'),
                    'frequency': 'daily'  # Expansions can be retried
                }
                
                result = research_topic_for_project(project_path, expansion_topic, output_dir)
                results.append(result)
                
                # Mark as searched
                save_expansion_searched(project_path, exp_id, exp_depth)
            else:
                print(f"    ⏸ Skipping '{exp_id}' (depth {exp_depth} > max {max_depth})")
    
    # --- STANDARD TOPICS ---
    for topic in instructions.get("topics", []):
        last_run = get_last_run(project_path, topic['id'])
        if should_run_topic(topic, last_run):
            result = research_topic_for_project(project_path, topic, output_dir)
            results.append(result)
            save_last_run(project_path, topic['id'])
        else:
            print(f"  ⏸ Skipping '{topic['id']}' (not due yet)")
    
    return results

def main():
    print("=== Cheetah Project Runner ===")
    print(f"Start: {datetime.now().isoformat()}")
    print("")
    
    projects = get_projects()
    print(f"Found {len(projects)} project(s)")
    
    total_projects = 0
    total_topics = 0
    
    for project_path in sorted(projects):
        results = run_for_project(project_path)
        if results is not None:
            total_projects += 1
            total_topics += len(results)
    
    print(f"\n=== Summary ===")
    print(f"Projects configured: {total_projects}")
    print(f"Topics researched: {total_topics}")
    print(f"End: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
