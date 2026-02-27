#!/usr/bin/env python3
"""
Cheetah Research Module
Per-topic GitHub research (reused from workspace-cheetah).
"""
import json
import subprocess
from datetime import datetime
from typing import Dict, Optional

QUERY_MAP = {
    "ai-dm-tools": "AI dungeon master OR AI DM OR rpg ai assistant",
    "vtt-modules": "foundry vtt module OR virtual tabletop",
    "devtools": "ai coding tools OR llm developer tools",
    "ai-llm": "local llm OR self-hosted ai OR open source llm"
}

def fetch_repo_details(full_name: str) -> Optional[str]:
    """Fetch README content via jina AI."""
    url = f'https://r.jina.ai/http://github.com/{full_name}'
    try:
        result = subprocess.run(
            ['curl', '-sL', '--max-time', '10', url],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return result.stdout[:2000]
    except:
        pass
    return None

def research_topic(topic_id: str, query: str) -> Dict:
    """Research a topic and return structured data."""
    # Use query map or provided query
    actual_query = query if query else QUERY_MAP.get(topic_id, topic_id)
    
    url = f'https://api.github.com/search/repositories?q={actual_query.replace(" ", "+")}&sort=updated&per_page=15'
    
    try:
        result = subprocess.run(
            ['curl', '-sL', '--max-time', '30', '-A', 'Mozilla/5.0', url],
            capture_output=True, text=True, timeout=35
        )
        
        if result.returncode != 0:
            return {
                "error": "GitHub API request failed",
                "timestamp": datetime.now().isoformat(),
                "projects": []
            }
        
        data = json.loads(result.stdout)
        
    except Exception as e:
        return {
            "error": f"Failed to fetch from GitHub: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "projects": []
        }
    
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
        
        # Fetch README for top 3 only
        if len(projects) < 3:
            project["readme"] = fetch_repo_details(project["name"])
        
        projects.append(project)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "topic": topic_id,
        "query": actual_query,
        "total_found": data.get('total_count', 0),
        "projects": projects
    }
