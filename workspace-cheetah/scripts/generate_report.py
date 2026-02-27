#!/usr/bin/env python3
"""
Cheetah Living Report Generator
Generates markdown reports from JSON knowledge base
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

KNOWLEDGE_DIR = Path("/Users/chimpman/.openclaw/workspace-cheetah/knowledge")
REPORTS_DIR = Path("/Users/chimpman/.openclaw/workspace-cheetah/reports")

def format_project(project: Dict) -> str:
    """Format a single project entry."""
    lines = [
        f"### {project.get('displayName', project.get('name', 'Unknown'))}",
        "",
        f"**Description:** {project.get('description', 'N/A')}",
        "",
        f"- ⭐ Stars: {project.get('stars', 'N/A')}",
        f"- 🔧 Language: {project.get('language', 'N/A')}",
        f"- 🔗 URL: {project.get('url', 'N/A')}",
        f"- 🏷️ Tags: {', '.join(project.get('tags', []))}",
        f"- 📅 First seen: {project.get('firstSeen', 'N/A')}",
        f"- 👁️ Last seen: {project.get('lastSeen', 'N/A')} (count: {project.get('seenCount', 1)})",
        ""
    ]
    return '\n'.join(lines)

def generate_living_report(topic: str) -> str:
    """Generate a living markdown report from knowledge base."""
    kb_path = KNOWLEDGE_DIR / f"{topic}.json"
    if not kb_path.exists():
        return f"# Error: No knowledge base found for {topic}"

    with open(kb_path, 'r') as f:
        kb = json.load(f)

    # Get meta information
    total = kb.get('totalFindings', 0)
    first_created = kb.get('firstCreated', 'Unknown')
    last_updated = kb.get('lastUpdated', 'Unknown')

    # Get today's findings for changelog section
    today = datetime.now().strftime('%Y-%m-%d')
    projects = kb.get('projects', [])
    new_today = [p for p in projects if p.get('firstSeen') == today]

    # Sort projects by stars (descending)
    sorted_projects = sorted(projects, key=lambda x: x.get('stars', 0), reverse=True)

    # Build report
    report_lines = [
        f"# {topic.upper()} Research - Living Document",
        "",
        f"*Topic: {kb.get('description', topic)}*",
        "",
        "## 📊 Statistics",
        "",
        f"- **Total Projects Tracked:** {total}",
        f"- **Tracking Since:** {first_created}",
        f"- **Last Updated:** {last_updated}",
        f"- **New Today:** {len(new_today)} project(s)",
        "",
        "---",
        "",
        "## 📈 Today's Additions",
        ""
    ]

    # Add today's new projects
    if new_today:
        for proj in new_today:
            report_lines.append(f"- ✅ **{proj.get('displayName', proj['name'])}** - {proj.get('description', 'No description')[:100]}...")
    else:
        report_lines.append("_No new projects added today._")

    report_lines.extend(["", "---", "", "## 📚 All Tracked Projects", ""])

    # Add top projects
    for i, proj in enumerate(sorted_projects[:20], 1):  # Top 20
        report_lines.append(format_project(proj))

    # Add trends section
    report_lines.extend(["---", "", "## 📊 Current Trends", ""])
    trends = kb.get('trends', [])
    if trends:
        for trend in trends[-10:]:  # Last 10 trends
            report_lines.append(f"### {trend.get('category', 'General')}")
            report_lines.append("")
            report_lines.append(f"{trend.get('text', '')}")
            report_lines.append("")
            report_lines.append(f"*First observed: {trend.get('firstSeen', 'Unknown')}*")
            report_lines.append("")
    else:
        report_lines.append("_No trends identified yet._")

    # Add recommendations
    report_lines.extend(["---", "", "## 💡 Recommendations", ""])
    recs = kb.get('recommendations', [])
    if recs:
        for rec in recs[-10:]:  # Last 10 recs
            report_lines.append(f"**{rec.get('audience', 'All')}:** {rec.get('text', '')}")
            report_lines.append("")
    else:
        report_lines.append("_No recommendations yet._")

    report_lines.extend(["---", "", f"*Generated: {datetime.now().isoformat()}*"])

    return '\n'.join(report_lines)

def generate_daily_summary(topic: str) -> str:
    """Generate daily summary report."""
    kb_path = KNOWLEDGE_DIR / f"{topic}.json"
    if not kb_path.exists():
        return f"# No Data for {topic}"

    with open(kb_path, 'r') as f:
        kb = json.load(f)

    today = datetime.now().strftime('%Y-%m-%d')
    projects = kb.get('projects', {})

    new_projects = [p for p in projects.values() if p.get('firstSeen') == today]
    updated = [p for p in projects.values() if p.get('lastSeen') == today and p.get('firstSeen') != today]

    lines = [
        f"# {topic.upper()} Daily Summary - {today}",
        "",
        "## 📊 Today's Activity",
        "",
        f"- **New Projects:** {len(new_projects)}",
        f"- **Updated Projects:** {len(updated)}",
        f"- **Total Tracked:** {len(projects)}",
        ""
    ]

    if new_projects:
        lines.extend(["## 🆕 New Projects", ""])
        for p in new_projects:
            lines.append(f"- **{p.get('displayName', p['name'])}** ({p.get('stars', 0)}⭐)")
            lines.append(f"  {p.get('description', '')[:150]}...")
            lines.append("")

    if updated:
        lines.extend(["## 🔄 Updated Projects", ""])
        for p in updated:
            lines.append(f"- **{p.get('displayName', p['name'])}** - now at {p.get('stars', '?')} stars")
            lines.append("")

    lines.append(f"---\n\n*Next update: next scheduled research day*")

    return '\n'.join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate reports from knowledge base")
    parser.add_argument("topic", choices=["ai-dm", "vtt", "devtools", "ai-llm"])
    parser.add_argument("--type", choices=["living", "summary"], default="living")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()

    if args.type == "living":
        content = generate_living_report(args.topic)
        default_file = REPORTS_DIR / f"{args.topic.upper()}_Living_Report.md"
    else:
        content = generate_daily_summary(args.topic)
        today = datetime.now().strftime('%Y-%m-%d')
        default_file = REPORTS_DIR / "daily_summaries" / f"{args.topic}_{today}.md"

    output_path = Path(args.output) if args.output else default_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(content)

    print(f"Generated: {output_path}")
    print(f"Word count: {len(content.split())}")

if __name__ == "__main__":
    main()
