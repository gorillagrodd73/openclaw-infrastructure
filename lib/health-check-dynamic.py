#!/usr/bin/env python3
"""
Brainiac Dynamic Project Health Check
Scans all Projects/.ai folders and reports agent activity.
"""
import json
import os
from datetime import datetime
from pathlib import Path

PROJECTS_ROOT = Path("/Users/chimpman/Projects")
AGENT_OUTPUTS = {
    "cheetah": "output/knowledge.json",
    "riddler": "digest-latest.md"
}

def get_projects():
    """Get all project directories."""
    if not PROJECTS_ROOT.exists():
        return []
    return [d for d in PROJECTS_ROOT.iterdir() if d.is_dir()]

def check_agent_output(project_path, agent_name, output_file):
    """Check if agent output exists and is recent."""
    output_path = project_path / ".ai" / agent_name / output_file
    if not output_path.exists():
        return None  # Not found
    
    # Check if recent (within 24h)
    mtime = datetime.fromtimestamp(output_path.stat().st_mtime)
    age_hours = (datetime.now() - mtime).total_seconds() / 3600
    return {
        "exists": True,
        "age_hours": round(age_hours, 2),
        "modified": mtime.strftime('%Y-%m-%d %H:%M:%S')
    }

def generate_report():
    """Generate health report for all projects."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    projects = get_projects()
    report = {
        "timestamp": datetime.now().isoformat(),
        "projects_checked": len(projects),
        "projects_with_ai": 0,
        "agent_activity": {},
        "issues": []
    }
    
    for project_path in sorted(projects):
        project_name = project_path.name
        ai_folder = project_path / ".ai"
        
        if not ai_folder.exists():
            report["issues"].append({
                "project": project_name,
                "issue": "Missing .ai folder",
                "severity": "low"
            })
            continue
        
        report["projects_with_ai"] += 1
        project_activity = {}
        
        for agent_name, output_file in AGENT_OUTPUTS.items():
            status = check_agent_output(project_path, agent_name, output_file)
            if status:
                project_activity[agent_name] = status
        
        if project_activity:
            report["agent_activity"][project_name] = project_activity
    
    return report

def main():
    print("=== Brainiac Project Health Check ===")
    print(f"Start: {datetime.now().isoformat()}")
    print("")
    
    report = generate_report()
    
    print(f"Projects scanned: {report['projects_checked']}")
    print(f"Projects with .ai folders: {report['projects_with_ai']}")
    print("")
    
    # Show agent activity
    if report['agent_activity']:
        print("Agent Activity:")
        print("")
        for project, agents in report['agent_activity'].items():
            print(f"  📁 {project}:")
            for agent, status in agents.items():
                age_status = "✓ Recent" if status['age_hours'] < 24 else "⚠️ Stale"
                print(f"    - {agent}: {age_status} ({status['age_hours']:.1f}h old)")
            print("")
    else:
        print("  No agent activity detected across projects.")
        print("")
    
    # Show issues
    if report['issues']:
        print("Issues Found:")
        print("")
        for issue in report['issues']:
            print(f"  ⚠️ {issue['project']}: {issue['issue']}")
        print("")
    
    print(f"End: {datetime.now().isoformat()}")
    
    # Save report
    output_dir = Path("/Users/chimpman/.openclaw/workspace-brainiac/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir / f"health-{date_str}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to {report_file}")

if __name__ == "__main__":
    main()