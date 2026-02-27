#!/usr/bin/env python3
"""
Cheetah Project Runner
Iterates through /Users/chimpman/Projects/ and runs research per-project.
"""
import json
import os
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
