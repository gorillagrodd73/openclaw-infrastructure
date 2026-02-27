#!/usr/bin/env python3
"""
Riddler Project Digest
Iterates through projects and generates digests from Cheetah outputs.
"""
import json
import os
from datetime import datetime
from pathlib import Path

PROJECTS_ROOT = Path("/Users/chimpman/Projects")

def get_projects():
    """Get all project directories."""
    if not PROJECTS_ROOT.exists():
        return []
    return [d for d in PROJECTS_ROOT.iterdir() if d.is_dir()]

def load_instructions(project_path):
    """Load riddler instructions for a project if they exist."""
    instructions_file = project_path / ".ai" / "riddler" / "instructions.json"
    if instructions_file.exists():
        with open(instructions_file, 'r') as f:
            return json.load(f)
    return None

def load_cheetah_knowledge(project_path):
    """Load Cheetah's knowledge output for this project."""
    kb_file = project_path / ".ai" / "cheetah" / "output" / "knowledge.json"
    if kb_file.exists():
        with open(kb_file, 'r') as f:
            return json.load(f)
    return None

def generate_digest(project_path, cheetah_data, instructions):
    """Generate a digest for a project."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    projects = cheetah_data.get("projects", [])
    
    lines = [
        f"# Riddler Digest - {project_path.name}",
        f"*Generated: {date_str}*",
        "",
        "## Project Research Summary",
        "",
        f"- **Total Findings:** {len(projects)}",
        f"- **Date Range:** {cheetah_data.get('date', date_str)}",
        ""
    ]
    
    # Group by topic (extract from project data if available)
    if projects:
        lines.extend(["## New Discoveries", ""])
        for i, p in enumerate(projects[:5], 1):  # Top 5
            lines.extend([
                f"### {i}. {p.get('display_name', p.get('name', 'Unknown'))}",
                "",
                f"{p.get('description', 'No description')[:150]}...",
                "",
                f"- ⭐ Stars: {p.get('stars', 'N/A')}",
                f"- 🔗 URL: {p.get('url', 'N/A')}",
                ""
            ])
    else:
        lines.append("_No new discoveries today._")
    
    lines.extend([
        "---",
        "",
        f"*Next update scheduled after next Cheetah run*"
    ])
    
    return '\n'.join(lines)

def process_project(project_path):
    """Generate digest for a single project."""
    instructions = load_instructions(project_path)
    cheetah_data = load_cheetah_knowledge(project_path)
    
    if not instructions:
        print(f"  (no Riddler config, skipping)")
        return False
    
    if not cheetah_data:
        print(f"  (no Cheetah data yet, skipping)")
        return False
    
    print(f"\n📁 Project: {project_path.name}")
    
    output_dir = project_path / ".ai" / "riddler" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate digest
    digest = generate_digest(project_path, cheetah_data, instructions)
    
    # Save digest
    date_str = datetime.now().strftime('%Y-%m-%d')
    digest_file = output_dir / f"digest-{date_str}.md"
    with open(digest_file, 'w') as f:
        f.write(digest)
    
    # Also save as "latest.md" for easy access
    latest_file = output_dir / "latest.md"
    with open(latest_file, 'w') as f:
        f.write(digest)
    
    print(f"  ✓ Digest saved to {digest_file}")
    
    return True

def main():
    print("=== Riddler Project Digest ===")
    print(f"Start: {datetime.now().isoformat()}")
    print("")
    
    projects = get_projects()
    print(f"Found {len(projects)} project(s)")
    
    processed = 0
    skipped = 0
    
    for project_path in sorted(projects):
        result = process_project(project_path)
        if result is True:
            processed += 1
        elif result is False:
            skipped += 1
    
    print(f"\n=== Summary ===")
    print(f"Projects digested: {processed}")
    print(f"Projects skipped: {skipped}")
    print(f"End: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
