#!/usr/bin/env python3
"""
Sinestro Web Dashboard
Serves Sinestro output on port 8173
"""
from flask import Flask, render_template_string, jsonify
from pathlib import Path
import json
import re
from datetime import datetime

app = Flask(__name__)
PROJECTS_ROOT = Path("/Users/chimpman/Projects")

def load_project_data(project_name):
    """Load Sinestro data for a project."""
    project_path = PROJECTS_ROOT / project_name
    sinestro_dir = project_path / ".ai" / "sinestro"
    
    data = {
        "project": project_name,
        "kanban": {},
        "dashboard": {},
        "assignments": [],
        "risks": []
    }
    
    # Load kanban
    kanban_file = sinestro_dir / "output" / "kanban.md"
    if kanban_file.exists():
        content = kanban_file.read_text()
        data["kanban"] = parse_kanban(content)
    
    # Load dashboard
    dashboard_file = sinestro_dir / "output" / "executive-dashboard.md"
    if dashboard_file.exists():
        content = dashboard_file.read_text()
        data["dashboard"] = parse_dashboard(content)
    
    # Load assignments
    assignments_file = sinestro_dir / "output" / "ready-for-assignment.md"
    if assignments_file.exists():
        content = assignments_file.read_text()
        data["assignments"] = parse_assignments(content)
    
    # Load risks
    risks_file = sinestro_dir / "output" / "risks-and-blockers.md"
    if risks_file.exists():
        content = risks_file.read_text()
        data["risks"] = parse_risks(content)
    
    return data

def parse_kanban(content):
    """Parse kanban markdown into structured data."""
    columns = {"backlog": [], "ready": [], "active": [], "blocked": [], "completed": []}
    current_column = None
    
    for line in content.split('\n'):
        if '### 📋' in line or 'BACKLOG' in line.upper():
            current_column = "backlog"
        elif '### 🚀' in line or 'READY' in line.upper():
            current_column = "ready"
        elif '### 🏗' in line or 'ACTIVE' in line.upper():
            current_column = "active"
        elif '### 🚧' in line or 'BLOCKED' in line.upper():
            current_column = "blocked"
        elif '### ✅' in line or 'COMPLETED' in line.upper():
            current_column = "completed"
        elif line.strip().startswith('- **') and current_column:
            # Parse item: - **id**: title (size)
            match = re.search(r'- \*\*(.+?)\*\*:\s*(.+?)\s*\((.+?)\)', line)
            if match:
                columns[current_column].append({
                    "id": match.group(1),
                    "title": match.group(2),
                    "size": match.group(3)
                })
    
    return columns

def parse_dashboard(content):
    """Parse dashboard markdown."""
    metrics = {}
    for line in content.split('\n'):
        if '| Milestones |' in line:
            match = re.search(r'(\d+)/(\d+)', line)
            if match:
                metrics["milestones_complete"] = int(match.group(1))
                metrics["milestones_total"] = int(match.group(2))
        elif '| Work Items |' in line:
            match = re.search(r'(\d+)/(\d+)', line)
            if match:
                metrics["work_items_done"] = int(match.group(1))
                metrics["work_items_total"] = int(match.group(2))
        elif '| Velocity |' in line:
            match = re.search(r'(\d+)', line)
            if match:
                metrics["velocity"] = int(match.group(1))
        elif '| Risk Items |' in line:
            match = re.search(r'(\d+)', line)
            if match:
                metrics["risks"] = int(match.group(1))
    
    return metrics

def parse_assignments(content):
    """Parse assignments markdown."""
    items = []
    in_table = False
    
    for line in content.split('\n'):
        if line.startswith('| ID |'):
            in_table = True
            continue
        if in_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6 and parts[1] and parts[1] != 'ID':
                items.append({
                    "id": parts[1],
                    "title": parts[2],
                    "size": parts[3],
                    "hours": parts[4],
                    "priority": parts[5]
                })
    
    return items

def parse_risks(content):
    """Parse risks markdown."""
    risks = []
    current_risk = {}
    
    for line in content.split('\n'):
        if line.startswith('- **') and 'Risk' in content.split('\n')[0]:
            # High risk format
            match = re.search(r'- \*\*(.+?)\*\*:\s*(.+)', line)
            if match:
                risks.append({
                    "milestone": match.group(1),
                    "description": match.group(2)
                })
    
    return risks

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sinestro Dashboard - {{ project }}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            padding: 20px;
        }
        h1 { color: #ffd700; margin-bottom: 10px; }
        .header { margin-bottom: 30px; }
        .timestamp { color: #888; font-size: 14px; }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: #16213e;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-value {
            font-size: 36px;
            font-weight: bold;
            color: #ffd700;
        }
        .metric-label {
            font-size: 14px;
            color: #aaa;
            margin-top: 5px;
        }
        
        .board {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        .column {
            background: #0f3460;
            border-radius: 8px;
            padding: 15px;
            min-height: 200px;
        }
        .column-header {
            font-weight: bold;
            padding-bottom: 10px;
            margin-bottom: 10px;
            border-bottom: 2px solid #e94560;
        }
        .card {
            background: #16213e;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .card:hover { transform: translateY(-2px); }
        .card-id { font-size: 12px; color: #888; }
        .card-title { margin: 5px 0; font-weight: 500; }
        .card-size {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        .size-XS { background: #00d9ff; color: #000; }
        .size-S { background: #00ff88; color: #000; }
        .size-M { background: #ffd700; color: #000; }
        .size-L { background: #ff6b6b; color: #fff; }
        .size-XL { background: #e94560; color: #fff; }
        
        .section {
            background: #16213e;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .section h2 {
            color: #ffd700;
            margin-bottom: 15px;
        }
        
        .assignment-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 10px;
            background: #0f3460;
            border-radius: 6px;
        }
        .assignment-priority {
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 15px;
        }
        .priority-critical { background: #e94560; }
        .priority-high { background: #ff6b6b; }
        .priority-medium { background: #ffd700; color: #000; }
        .priority-low { background: #00ff88; color: #000; }
        
        .risk-item {
            padding: 10px;
            margin-bottom: 8px;
            background: #3d0000;
            border-left: 4px solid #e94560;
            border-radius: 4px;
        }
        
        .refresh-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }
        .refresh-btn:hover { background: #ff6b6b; }
    </style>
</head>
<body>
    <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
    
    <div class="header">
        <h1>🎯 Sinestro Dashboard</h1>
        <div class="timestamp">{{ project }} — Last updated: {{ timestamp }}</div>
    </div>
    
    <div class="metrics">
        <div class="metric-card">
            <div class="metric-value">{{ dashboard.milestones_complete }}/{{ dashboard.milestones_total }}</div>
            <div class="metric-label">Milestones Complete</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ dashboard.work_items_done }}/{{ dashboard.work_items_total }}</div>
            <div class="metric-label">Work Items Done</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ dashboard.velocity }}</div>
            <div class="metric-label">Velocity (hrs/week)</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ dashboard.risks }}</div>
            <div class="metric-label">Risk Items</div>
        </div>
    </div>
    
    <h2 style="margin-bottom: 15px;">📋 Kanban Board</h2>
    <div class="board">
        <div class="column">
            <div class="column-header">📋 Backlog</div>
            {% for item in kanban.backlog %}
            <div class="card">
                <div class="card-id">{{ item.id }}</div>
                <div class="card-title">{{ item.title }}</div>
                <span class="card-size size-{{ item.size }}">{{ item.size }}</span>
            </div>
            {% endfor %}
        </div>
        <div class="column">
            <div class="column-header">🚀 Ready</div>
            {% for item in kanban.ready %}
            <div class="card">
                <div class="card-id">{{ item.id }}</div>
                <div class="card-title">{{ item.title }}</div>
                <span class="card-size size-{{ item.size }}">{{ item.size }}</span>
            </div>
            {% endfor %}
        </div>
        <div class="column">
            <div class="column-header">🏗 Active</div>
            {% for item in kanban.active %}
            <div class="card">
                <div class="card-id">{{ item.id }}</div>
                <div class="card-title">{{ item.title }}</div>
                <span class="card-size size-{{ item.size }}">{{ item.size }}</span>
            </div>
            {% endfor %}
        </div>
        <div class="column">
            <div class="column-header">🚧 Blocked</div>
            {% for item in kanban.blocked %}
            <div class="card">
                <div class="card-id">{{ item.id }}</div>
                <div class="card-title">{{ item.title }}</div>
                <span class="card-size size-{{ item.size }}">{{ item.size }}</span>
            </div>
            {% endfor %}
        </div>
        <div class="column">
            <div class="column-header">✅ Completed</div>
            {% for item in kanban.completed %}
            <div class="card">
                <div class="card-id">{{ item.id }}</div>
                <div class="card-title">{{ item.title }}</div>
                <span class="card-size size-{{ item.size }}">{{ item.size }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <div class="section">
        <h2>🚀 Ready for Assignment</h2>
        {% for item in assignments %}
        <div class="assignment-item">
            <span class="assignment-priority priority-{{ item.priority }}">{{ item.priority.upper() }}</span>
            <div>
                <strong>{{ item.id }}</strong>: {{ item.title }}
                <br><small>{{ item.size }} ({{ item.hours }} hours)</small>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <div class="section">
        <h2>⚠️ Risks & Blockers</h2>
        {% for risk in risks %}
        <div class="risk-item">
            <strong>{{ risk.milestone }}</strong>: {{ risk.description }}
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard view."""
    # Get first project with Sinestro data
    for project_path in PROJECTS_ROOT.iterdir():
        if project_path.is_dir():
            sinestro_dir = project_path / ".ai" / "sinestro"
            if (sinestro_dir / "output" / "kanban.md").exists():
                data = load_project_data(project_path.name)
                return render_template_string(
                    HTML_TEMPLATE,
                    project=project_path.name,
                    timestamp=datetime.now().strftime('%Y-%m-%d %H:%M'),
                    **data
                )
    return "No projects with Sinestro data found", 404

@app.route('/api/projects')
def api_projects():
    """List all projects with Sinestro data."""
    projects = []
    for project_path in PROJECTS_ROOT.iterdir():
        if project_path.is_dir():
            if (project_path / ".ai" / "sinestro" / "output").exists():
                projects.append(project_path.name)
    return jsonify({"projects": projects})

@app.route('/api/project/<project_name>')
def api_project(project_name):
    """Get project data as JSON."""
    try:
        data = load_project_data(project_name)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    print("Starting Sinestro Dashboard on http://localhost:8173")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=8173, debug=False)