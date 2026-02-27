#!/usr/bin/env python3
"""
Cheetah GitHub Research Helper
Fetches and formats GitHub API data for a given topic
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Optional

QUERY_MAP = {
    "ai-dm": "ai dungeon master OR ai dm OR rpg ai assistant",
    "vtt": "foundry vtt OR virtual tabletop OR vtt modules",
    "devtools": "ai coding tools OR llm developer tools OR ai dev tools",
    "ai-llm": "local llm OR self-hosted ai OR open source llm"
}

def run_curl(query: str, per_page: int = 15) -> Optional[Dict]:
    """Run GitHub API search via curl."""
    url = f'https://api.github.com/search/repositories?q={query.replace(" ", "+")}&sort=updated&per_page={per_page}'
    
    try:
        result = subprocess.run(
            ['curl', '-sL', '--max-time', '30', '-A', 'Mozilla/5.0', url],
            capture_output=True,
            text=True,
            timeout=35
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching from GitHub: {e}", file=sys.stderr)
    
    return None

def fetch_repo_details(full_name: str) -> Optional[str]:
    """Fetch README content via jina AI."""
    url = f'https://r.jina.ai/http://github.com/{full_name}'
    
    try:
        result = subprocess.run(
            ['curl', '-sL', '--max-time', '15', url],
            capture_output=True,
            text=True,
            timeout=20
        )
        if result.returncode == 0:
            return result.stdout[:2000]  # Limit to 2000 chars
    except:
        pass
    
    return None

def research_topic(topic: str) -> Dict:
    """Research a topic and return structured data."""
    query = QUERY_MAP.get(topic, topic)
    
    # Fetch from GitHub
    data = run_curl(query)
    if not data:
        return {"error": "Failed to fetch from GitHub", "topic": topic, "projects": []}
    
    projects = []
    items = data.get('items', [])
    
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
        
        # Try to fetch README for top 3 only
        if len(projects) < 3:
            project["readme"] = fetch_repo_details(project["name"])
        
        projects.append(project)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "query": query,
        "total_found": data.get('total_count', 0),
        "projects": projects
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 research_github.py <topic>")
        print(f"  Topics: {', '.join(QUERY_MAP.keys())}")
        sys.exit(1)
    
    topic = sys.argv[1]
    results = research_topic(topic)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
