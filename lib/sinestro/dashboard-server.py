#!/usr/bin/env python3
"""
Sinestro Dashboard Server
Serves on port 8173
"""
import http.server
import socketserver
import json
import re
from pathlib import Path
from datetime import datetime

PROJECTS_ROOT = Path("/Users/chimpman/Projects")
PORT = 8173

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.generate_dashboard()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def generate_dashboard(self):
        # Find first project with Sinestro data
        for project_path in PROJECTS_ROOT.iterdir():
            if not project_path.is_dir():
                continue
            
            sinestro_dir = project_path / ".ai" / "sinestro"
            if not (sinestro_dir / "output" / "kanban.md").exists():
                continue
            
            # Load data
            kanban_file = sinestro_dir / "output" / "kanban.md"
            dashboard_file = sinestro_dir / "output" / "executive-dashboard.md"
            assignments_file = sinestro_dir / "output" / "ready-for-assignment.md"
            risks_file = sinestro_dir / "output" / "risks-and-blockers.md"
            
            kanban_data = self.parse_kanban(kanban_file.read_text() if kanban_file.exists() else "")
            metrics = self.parse_metrics(dashboard_file.read_text() if dashboard_file.exists() else "")
            assignments = self.parse_assignments(assignments_file.read_text() if assignments_file.exists() else "")
            risks = self.parse_risks(risks_file.read_text() if risks_file.exists() else "")
            
            # Build HTML
            html = open(__file__).read().split("HTML_DASHBOARD = '''")[1].split("'''\ndef parse_markdown")[0]
            
            html = html.replace('{{PROJECT}}', project_path.name)
            html = html.replace('{{TIMESTAMP}}', datetime.now().strftime('%Y-%m-%d %H:%M'))
            html = html.replace('{{M_COMPLETE}}', str(metrics.get('m_complete', 0)))
            html = html.replace('{{M_TOTAL}}', str(metrics.get('m_total', 5)))
            html = html.replace('{{W_DONE}}', str(metrics.get('w_done', 0)))
            html = html.replace('{{W_TOTAL}}', str(metrics.get('w_total', 14)))
            html = html.replace('{{VELOCITY}}', str(metrics.get('velocity', 12)))
            html = html.replace('{{RISKS}}', str(metrics.get('risks', 0)))
            
            html = html.replace('{{KANBAN_BACKLOG}}', kanban_data.get('backlog', '<div class="empty-state">No items</div>'))
            html = html.replace('{{KANBAN_READY}}', kanban_data.get('ready', '<div class="empty-state">No items</div>'))
            html = html.replace('{{KANBAN_ACTIVE}}', kanban_data.get('active', '<div class="empty-state">No items</div>'))
            html = html.replace('{{KANBAN_BLOCKED}}', kanban_data.get('blocked', '<div class="empty-state">No items</div>'))
            html = html.replace('{{KANBAN_COMPLETED}}', kanban_data.get('completed', '<div class="empty-state">No items</div>'))
            
            html = html.replace('{{ASSIGNMENTS}}', assignments or '<div class="empty-state">No items ready</div>')
            html = html.replace('{{RISKS}}', risks or '<div class="empty-state">No active risks</div>')
            
            return html
        
        return "<h1>No projects with Sinestro data found</h1>"
    
    def parse_kanban(self, content):
        """Parse kanban markdown."""
        sections = {"backlog": [], "ready": [], "active": [], "blocked": [], "completed": []}
        current = None
        
        for line in content.split('\n'):
            if 'BACKLOG' in line.upper():
                current = 'backlog'
            elif 'READY' in line.upper():
                current = 'ready'
            elif 'ACTIVE' in line.upper():
                current = 'active'
            elif 'BLOCKED' in line.upper():
                current = 'blocked'
            elif 'COMPLETED' in line.upper():
                current = 'completed'
            elif line.strip().startswith('- **') and current:
                match = re.search(r'- \*\*(.+?)\*\*:\s*(.+?)\s*\((.+?)\)', line)
                if match:
                    sections[current].append({
                        'id': match.group(1),
                        'title': match.group(2),
                        'size': match.group(3)
                    })
        
        result = {}
        for status, items in sections.items():
            if items:
                cards = []
                for item in items[:10]:  # Limit to 10 per column
                    cards.append(f'<div class="card"><div class="card-id">{item["id"]}</div><div class="card-title">{item["title"]}</div><span class="card-size size-{item["size"]}">{item["size"]}</span></div>')
                result[status] = '\n'.join(cards)
            else:
                result[status] = '<div class="empty-state">No items</div>'
        return result
    
    def parse_metrics(self, content):
        """Parse dashboard metrics."""
        metrics = {}
        for line in content.split('\n'):
            if '| Milestones |' in line:
                match = re.search(r'(\d+)/(\d+)', line)
                if match:
                    metrics['m_complete'] = int(match.group(1))
                    metrics['m_total'] = int(match.group(2))
            elif '| Work Items |' in line:
                match = re.search(r'(\d+)/(\d+)', line)
                if match:
                    metrics['w_done'] = int(match.group(1))
                    metrics['w_total'] = int(match.group(2))
            elif '| Velocity |' in line:
                match = re.search(r'(\d+)', line)
                if match:
                    metrics['velocity'] = int(match.group(1))
            elif '| Risk Items |' in line:
                match = re.search(r'(\d+)', line)
                if match:
                    metrics['risks'] = int(match.group(1))
        return metrics
    
    def parse_assignments(self, content):
        """Parse assignments."""
        items = []
        in_table = False
        for line in content.split('\n'):
            if line.startswith('| ID |'):
                in_table = True
                continue
            if in_table and line.startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6 and parts[1] and parts[1] != 'ID':
                    priority = parts[5].lower()
                    items.append(f'<div class="assignment-item"><span class="assignment-priority priority-{priority}">{parts[5]}</span><div><strong>{parts[1]}</strong>: {parts[2]}<br><small>{parts[3]} ({parts[4]} hours)</small></div></div>')
        return '\n'.join(items) if items else ''
    
    def parse_risks(self, content):
        """Parse risks."""
        risks = []
        for line in content.split('\n'):
            if line.strip().startswith('- **') and 'Risk' in content:
                match = re.search(r'- \*\*(.+?)\*\*:\s*(.+)', line)
                if match:
                    risks.append(f'<div class="risk-item"><strong>{match.group(1)}</strong>: {match.group(2)}</div>')
        return '\n'.join(risks) if risks else ''

def main():
    print(f"Starting Sinestro Dashboard on http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    main()
