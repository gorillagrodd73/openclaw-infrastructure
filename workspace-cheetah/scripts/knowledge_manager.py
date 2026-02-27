#!/usr/bin/env python3
"""
Cheetah Knowledge Base Manager
Handles deduplication, updates, and accumulation of research findings
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

KNOWLEDGE_DIR = Path("/Users/chimpman/.openclaw/workspace-cheetah/knowledge")

def get_topic_for_day(day_of_week: int) -> str:
    """Map day to topic based on schedule."""
    # Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    topics = {
        0: "ai-llm",      # Monday
        1: "devtools",    # Tuesday
        2: "vtt",         # Wednesday
        3: "ai-dm",       # Thursday
        4: "ai-llm",      # Friday (review)
        5: "mixed",       # Saturday (mixed)
        6: "mixed"        # Sunday (mixed)
    }
    return topics.get(day_of_week, "mixed")

def load_knowledge(topic: str) -> Dict:
    """Load or create knowledge base for a topic."""
    filepath = KNOWLEDGE_DIR / f"{topic}.json"
    if filepath.exists():
        with open(filepath, 'r') as f:
            knowledge = json.load(f)
        # Normalize projects to dict format (handles legacy list format)
        projects = knowledge.get('projects', [])
        if isinstance(projects, list):
            knowledge['projects'] = {
                normalize_project_name(p.get('name', '')): p 
                for p in projects 
                if p.get('name')
            }
        return knowledge
    return {
        "topic": topic,
        "description": f"Research findings for {topic}",
        "totalFindings": 0,
        "firstCreated": datetime.now().isoformat(),
        "lastUpdated": datetime.now().isoformat(),
        "projects": {},
        "trends": [],
        "recommendations": [],
        "sources": {"github": [], "reddit": [], "web": []}
    }

def save_knowledge(topic: str, data: Dict):
    """Save knowledge base to disk."""
    filepath = KNOWLEDGE_DIR / f"{topic}.json"
    data["lastUpdated"] = datetime.now().isoformat()
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def normalize_project_name(name: str) -> str:
    """Normalize project name for deduplication."""
    # Remove owner prefix, lowercase, strip
    if '/' in name:
        name = name.split('/')[-1]
    return name.lower().strip()

def add_or_update_project(knowledge: Dict, project: Dict, source: str) -> bool:
    """
    Add new project or update existing.
    Returns True if new, False if updated.
    """
    norm_name = normalize_project_name(project.get('name', ''))
    if not norm_name:
        return False
    
    projects = knowledge.get('projects', {})
    today = datetime.now().strftime('%Y-%m-%d')
    
    if norm_name in projects:
        # Update existing
        existing = projects[norm_name]
        # Update stars if changed
        if project.get('stars') and project['stars'] != existing.get('stars'):
            existing['stars'] = project['stars']
            existing['lastUpdated'] = today
        # Append new description if different
        if project.get('description') and project['description'] != existing.get('description'):
            existing['description_history'] = existing.get('description_history', []) + [
                {'date': today, 'description': project['description']}
            ]
            existing['description'] = project['description']
        # Merge tags
        if project.get('tags'):
            existing['tags'] = list(set(existing.get('tags', []) + project['tags']))
        # Update language
        if project.get('language') and not existing.get('language'):
            existing['language'] = project['language']
        
        existing['lastSeen'] = today
        existing['seenCount'] = existing.get('seenCount', 1) + 1
        
        # Add source if new
        if source not in existing.get('sources', []):
            existing['sources'].append(source)
            
        return False
    else:
        # New project
        project_data = {
            'name': norm_name,
            'displayName': project.get('name', norm_name),
            'description': project.get('description', ''),
            'stars': project.get('stars', 0),
            'language': project.get('language', ''),
            'url': project.get('html_url', project.get('url', '')),
            'tags': project.get('tags', []),
            'firstSeen': today,
            'lastSeen': today,
            'seenCount': 1,
            'sources': [source]
        }
        projects[norm_name] = project_data
        knowledge['totalFindings'] = knowledge.get('totalFindings', 0) + 1
        return True

def add_trend(knowledge: Dict, trend: Dict):
    """Add a trend observation."""
    trends = knowledge.get('trends', [])
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Check if similar trend exists
    trend_text = trend.get('text', '')
    for existing in trends:
        if existing.get('text') == trend_text:
            existing['lastUpdated'] = today
            existing['occurrences'] = existing.get('occurrences', 1) + 1
            return
    
    trends.append({
        'text': trend_text,
        'category': trend.get('category', 'general'),
        'firstSeen': today,
        'lastUpdated': today,
        'occurrences': 1,
        'evidence': trend.get('evidence', [])
    })
    knowledge['trends'] = trends

def add_recommendation(knowledge: Dict, rec: Dict):
    """Add a recommendation."""
    recs = knowledge.get('recommendations', [])
    today = datetime.now().strftime('%Y-%m-%d')
    
    rec_text = rec.get('text', '')
    for existing in recs:
        if existing.get('text') == rec_text:
            existing['lastUpdated'] = today
            return
    
    recs.append({
        'text': rec_text,
        'category': rec.get('category', 'general'),
        'audience': rec.get('audience', 'all'),
        'date': today,
        'priority': rec.get('priority', 'medium')
    })
    knowledge['recommendations'] = recs

def get_new_findings_today(knowledge: Dict) -> Dict:
    """Get findings from today only for daily summary."""
    today = datetime.now().strftime('%Y-%m-%d')
    projects = knowledge.get('projects', {})
    
    new_projects = [
        p for p in projects.values() 
        if p.get('firstSeen') == today
    ]
    
    updated_projects = [
        p for p in projects.values()
        if p.get('lastSeen') == today and p.get('firstSeen') != today
    ]
    
    trends = [t for t in knowledge.get('trends', []) if t.get('firstSeen') == today]
    
    return {
        'newProjects': new_projects,
        'updatedProjects': updated_projects,
        'trends': trends,
        'totalTracked': len(projects)
    }

def process_daily_research(topic: str, research_data: Dict) -> Dict:
    """
    Process a day's research and update knowledge base.
    Returns summary of what was added/updated.
    """
    knowledge = load_knowledge(topic)
    
    # Ensure projects is a dict
    projects = knowledge.get('projects', [])
    if isinstance(projects, list):
        knowledge['projects'] = {}
    
    new_count = 0
    updated_count = 0
    
    # Process projects from GitHub
    for project in research_data.get('projects', []):
        is_new = add_or_update_project(knowledge, project, 'github')
        if is_new:
            new_count += 1
        else:
            updated_count += 1
    
    # Process trends
    for trend in research_data.get('trends', []):
        add_trend(knowledge, trend)
    
    # Process recommendations
    for rec in research_data.get('recommendations', []):
        add_recommendation(knowledge, rec)
    
    # Save updated knowledge
    save_knowledge(topic, knowledge)
    
    return {
        'topic': topic,
        'newProjects': new_count,
        'updatedProjects': updated_count,
        'totalTracked': len(knowledge.get('projects', {})),
        'knowledgeFile': str(KNOWLEDGE_DIR / f"{topic}.json")
    }

def process_stdin(topic: str):
    """Process research JSON from stdin and update knowledge base."""
    try:
        data = json.load(sys.stdin)
        summary = process_daily_research(topic, data)
        print(json.dumps(summary, indent=2))
    except Exception as e:
        print(f"Error processing stdin: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cheetah Knowledge Base Manager")
    parser.add_argument("topic", nargs="?", choices=["ai-dm", "vtt", "devtools", "ai-llm"],
                       help="Topic to process")
    parser.add_argument("--process-stdin", action="store_true",
                       help="Read research JSON from stdin")
    parser.add_argument("--stats", action="store_true",
                       help="Show statistics")
    
    args = parser.parse_args()
    
    if not args.topic:
        parser.print_help()
        sys.exit(1)
    
    if args.process_stdin:
        process_stdin(args.topic)
    elif args.stats:
        knowledge = load_knowledge(args.topic)
        projects = knowledge.get('projects', {})
        print(f"\n📊 {args.topic.upper()} Knowledge Base:")
        print(f"   Total projects: {len(projects)}")
        print(f"   First created: {knowledge.get('firstCreated', 'N/A')}")
        print(f"   Last updated: {knowledge.get('lastUpdated', 'N/A')}")
    else:
        # Default: just load and show status
        knowledge = load_knowledge(args.topic)
        projects = knowledge.get('projects', {})
        print(f"Knowledge base for '{args.topic}': {len(projects)} projects")
        sys.exit(0)
