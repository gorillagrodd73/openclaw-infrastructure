#!/usr/bin/env python3
"""Enrich GitHub API results with README content - NO LLM calls, pure curl + jina.ai"""
import json
import subprocess
import sys
from datetime import datetime

def fetch_readme_jina(repo_full_name: str) -> str:
    """Fetch README via jina.ai extraction - fast, no API auth needed"""
    url = f'https://r.jina.ai/http://github.com/{repo_full_name}'
    try:
        result = subprocess.run(
            ['curl', '-sL', '--max-time', '10', url],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return result.stdout[:2000]  # Limit to 2k chars
    except Exception:
        pass
    return None

def enrich_repos(input_file: str, output_file: str, topic: str):
    """Process GitHub API output and enrich with READMEs"""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    items = data.get('items', [])
    projects = []
    
    for item in items[:10]:  # Top 10
        project = {
            "name": item.get('full_name', ''),
            "display_name": item.get('name', ''),
            "description": item.get('description', ''),
            "stars": item.get('stargazers_count', 0),
            "language": item.get('language', ''),
            "url": item.get('html_url', ''),
            "updated": item.get('updated_at', ''),
            "created": item.get('created_at', ''),
            "readme": None
        }
        
        # Fetch README for top 3 only
        if len(projects) < 3:
            project["readme"] = fetch_readme_jina(project["name"])
            print(f"Enriched {project['name']}: {'✓' if project['readme'] else '✗'}", file=sys.stderr)
        
        projects.append(project)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "query": topic,  # Simplified
        "total_found": data.get('total_count', 0),
        "projects": projects
    }
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Enriched {len(projects)} projects (3 with READMEs)", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: enrich-repos.py <input.json> <output.json> <topic>", file=sys.stderr)
        sys.exit(1)
    
    enrich_repos(sys.argv[1], sys.argv[2], sys.argv[3])
