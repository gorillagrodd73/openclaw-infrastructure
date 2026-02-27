#!/usr/bin/env python3
"""
Sinestro Project Architect
Generates roadmap, kanban, dashboards, and tracks milestones.
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

PROJECTS_ROOT = Path("/Users/chimpman/Projects")

def get_projects():
    if not PROJECTS_ROOT.exists():
        return []
    return [d for d in PROJECTS_ROOT.iterdir() if d.is_dir()]

def load_instructions(project_path):
    instructions_file = project_path / ".ai" / "sinestro" / "instructions.json"
    if instructions_file.exists():
        with open(instructions_file, 'r') as f:
            return json.load(f)
    return None

def load_state(project_path):
    state_file = project_path / ".ai" / "sinestro" / ".state.json"
    if state_file.exists():
        with open(state_file, 'r') as f:
            return json.load(f)
    return None

def save_state(project_path, state):
    state_file = project_path / ".ai" / "sinestro" / ".state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now().isoformat()
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def generate_kanban(state):
    lines = ["# Kanban Board", "", f"*Generated: {datetime.now().strftime('%Y-%m-%d')}*", ""]
    
    work_items = {"backlog": [], "ready": [], "active": [], "blocked": [], "completed": []}
    
    for milestone in state.get("milestones", []):
        for wi in milestone.get("work_items", []):
            status = wi.get("status", "backlog")
            item = {"id": wi["id"], "title": wi["title"][:30] + "..." if len(wi["title"]) > 30 else wi["title"], "size": wi.get("size", "?"), "milestone": milestone.get("name", "Unknown")}
            if status in work_items:
                work_items[status].append(item)
    
    for status, items in work_items.items():
        emoji = {"backlog": "📋", "ready": "🚀", "active": "🏗", "blocked": "🚧", "completed": "✅"}.get(status, "❓")
        lines.extend([f"### {emoji} {status.upper()}", ""])
        if items:
            for item in items[:5]:
                lines.append(f"- **{item['id']}**: {item['title']} ({item['size']})")
        else:
            lines.append("_No items_")
        lines.append("")
    
    return "\n".join(lines)

def generate_dashboard(state):
    metrics = state.get("metrics", {})
    milestones = state.get("milestones", [])
    completed = [m for m in milestones if m.get("status") == "completed"]
    at_risk = [m for m in milestones if m.get("status") == "active" and any(r.get("level") == "high" for r in m.get("risks", []))]
    
    lines = [
        f"# Executive Dashboard - {state.get('project', 'Project')}",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "## 📊 Key Metrics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Milestones | {len(completed)}/{len(milestones)} complete |",
        f"| Work Items | {metrics.get('completed_work_items', 0)}/{metrics.get('total_work_items', 0)} done |",
        f"| Velocity | {metrics.get('velocity_avg_hours_per_week', 12)} hrs/week |",
        f"| Risk Items | {len(at_risk)} |",
        ""
    ]
    return "\n".join(lines)

def generate_assignments(state):
    lines = ["# Ready for Assignment", f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*", ""]
    
    ready_items = []
    for milestone in state.get("milestones", []):
        for wi in milestone.get("work_items", []):
            if wi.get("status") == "ready":
                ready_items.append({**wi, "milestone": milestone.get("name")})
    
    if ready_items:
        lines.extend(["## 🚀 Ready Now", "", "| ID | Title | Size | Hours | Priority |", "|----|-------|------|-------|----------|"])
        for item in ready_items[:5]:
            lines.append(f"| {item['id']} | {item['title'][:40]} | {item.get('size', '?')} | {item.get('estimated_hours', '?')} | {item.get('priority', 'medium')} |")
        lines.extend(["", "### Assignment Commands:", "```"])
        for item in ready_items[:3]:
            lines.append(f'Toyman, take {item["id"]}: {item["title"][:50]}')
        lines.append("```")
    else:
        lines.append("_No items ready._")
    
    return "\n".join(lines)

def generate_risks(state):
    lines = ["# Risks and Blockers", f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*", ""]
    
    all_risks = []
    for milestone in state.get("milestones", []):
        for risk in milestone.get("risks", []):
            all_risks.append({**risk, "milestone": milestone.get("name")})
    
    if all_risks:
        high = [r for r in all_risks if r.get("level") == "high"]
        if high:
            lines.extend(["## 🔴 High Risks", ""])
            for r in high:
                lines.append(f"- **{r['milestone']}**: {r.get('description', 'Unknown')}")
        lines.append("")
    
    return "\n".join(lines)

def process_project(project_path):
    instructions = load_instructions(project_path)
    if not instructions:
        print(f"  (no Sinestro config)")
        return False
    
    state = load_state(project_path)
    if not state:
        state = {"project": project_path.name, "milestones": [], "metrics": {}}
    
    print(f"\n📁 {project_path.name}")
    
    output_dir = project_path / ".ai" / "sinestro" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generators = [
        ("kanban.md", generate_kanban),
        ("executive-dashboard.md", generate_dashboard),
        ("ready-for-assignment.md", generate_assignments),
        ("risks-and-blockers.md", generate_risks),
    ]
    
    for filename, generator in generators:
        content = generator(state)
        (output_dir / filename).write_text(content)
        print(f"  ✓ {filename}")
    
    return True

def main():
    print("=== Sinestro Project Architect ===")
    projects = get_projects()
    print(f"Found {len(projects)} projects")
    
    processed = 0
    for project_path in sorted(projects):
        if process_project(project_path):
            processed += 1
    
    print(f"\nProcessed: {processed} projects")
    print(f"End: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
