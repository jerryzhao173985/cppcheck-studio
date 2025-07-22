"""
Dashboard generators for CPPCheck Studio
Creates beautiful, interactive HTML dashboards from analysis results
"""

import json
import base64
import html
from pathlib import Path
from datetime import datetime
import hashlib
import os

class UltimateDashboardGenerator:
    """Ultimate dashboard with all features - best for most use cases"""
    
    def __init__(self, issues_file):
        with open(issues_file) as f:
            data = json.load(f)
        self.issues = data.get('issues', [])
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def generate(self, output_file):
        """Generate the ultimate dashboard with all features"""
        
        # Calculate statistics
        stats = self.calculate_stats()
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPPCheck Studio Dashboard</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css" rel="stylesheet">
    
    <style>
        {self.generate_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1><i class="fas fa-code"></i> CPPCheck Studio Dashboard</h1>
                <div class="header-info">
                    <span><i class="fas fa-clock"></i> {self.timestamp}</span>
                    <span><i class="fas fa-bug"></i> {stats['total']} issues</span>
                </div>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card error">
                <i class="fas fa-exclamation-circle"></i>
                <h3>Errors</h3>
                <div class="value">{stats['errors']}</div>
                <div class="percent">{stats['error_percent']:.1f}%</div>
            </div>
            
            <div class="stat-card warning">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Warnings</h3>
                <div class="value">{stats['warnings']}</div>
                <div class="percent">{stats['warning_percent']:.1f}%</div>
            </div>
            
            <div class="stat-card style">
                <i class="fas fa-palette"></i>
                <h3>Style</h3>
                <div class="value">{stats['style']}</div>
                <div class="percent">{stats['style_percent']:.1f}%</div>
            </div>
            
            <div class="stat-card performance">
                <i class="fas fa-tachometer-alt"></i>
                <h3>Performance</h3>
                <div class="value">{stats['performance']}</div>
                <div class="percent">{stats['performance_percent']:.1f}%</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="search-container">
                <i class="fas fa-search"></i>
                <input type="text" id="searchInput" placeholder="Search issues..." onkeyup="filterIssues()">
            </div>
            
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="setFilter('all')">
                    <i class="fas fa-list"></i> All ({stats['total']})
                </button>
                <button class="filter-btn" onclick="setFilter('error')">
                    <i class="fas fa-exclamation-circle"></i> Errors ({stats['errors']})
                </button>
                <button class="filter-btn" onclick="setFilter('warning')">
                    <i class="fas fa-exclamation-triangle"></i> Warnings ({stats['warnings']})
                </button>
                <button class="filter-btn" onclick="setFilter('style')">
                    <i class="fas fa-palette"></i> Style ({stats['style']})
                </button>
                <button class="filter-btn" onclick="setFilter('performance')">
                    <i class="fas fa-tachometer-alt"></i> Performance ({stats['performance']})
                </button>
            </div>
        </div>
        
        <div class="table-container">
            <table id="issuesTable">
                <thead>
                    <tr>
                        <th>File</th>
                        <th>Line</th>
                        <th>Severity</th>
                        <th>Message</th>
                        <th>ID</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="issuesBody">
                    {self.generate_issue_rows()}
                </tbody>
            </table>
        </div>
        
        <div id="codeModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>
                <h2 id="modalTitle">Code Context</h2>
                <pre><code id="codeContent" class="language-cpp"></code></pre>
            </div>
        </div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>
        {self.generate_scripts()}
    </script>
</body>
</html>"""
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"  📊 Dashboard type: Ultimate")
        print(f"  📏 File size: {len(html_content) / 1024:.1f} KB")
    
    def calculate_stats(self):
        """Calculate issue statistics"""
        total = len(self.issues)
        errors = sum(1 for i in self.issues if i.get('severity') == 'error')
        warnings = sum(1 for i in self.issues if i.get('severity') == 'warning')
        style = sum(1 for i in self.issues if i.get('severity') == 'style')
        performance = sum(1 for i in self.issues if i.get('severity') == 'performance')
        
        return {
            'total': total,
            'errors': errors,
            'warnings': warnings,
            'style': style,
            'performance': performance,
            'error_percent': (errors / total * 100) if total > 0 else 0,
            'warning_percent': (warnings / total * 100) if total > 0 else 0,
            'style_percent': (style / total * 100) if total > 0 else 0,
            'performance_percent': (performance / total * 100) if total > 0 else 0
        }
    
    def generate_styles(self):
        """Generate CSS styles"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f8f9fa;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .header-content h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .header-info {
            display: flex;
            gap: 30px;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            text-align: center;
            transition: transform 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        }
        
        .stat-card i {
            font-size: 2.5rem;
            margin-bottom: 15px;
            opacity: 0.8;
        }
        
        .stat-card h3 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: #666;
        }
        
        .stat-card .value {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .stat-card .percent {
            font-size: 1rem;
            opacity: 0.7;
        }
        
        .stat-card.error { border-top: 4px solid #e74c3c; }
        .stat-card.error i, .stat-card.error .value { color: #e74c3c; }
        
        .stat-card.warning { border-top: 4px solid #f39c12; }
        .stat-card.warning i, .stat-card.warning .value { color: #f39c12; }
        
        .stat-card.style { border-top: 4px solid #3498db; }
        .stat-card.style i, .stat-card.style .value { color: #3498db; }
        
        .stat-card.performance { border-top: 4px solid #2ecc71; }
        .stat-card.performance i, .stat-card.performance .value { color: #2ecc71; }
        
        .controls {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .search-container {
            position: relative;
            flex: 1;
            max-width: 400px;
        }
        
        .search-container i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #666;
        }
        
        #searchInput {
            width: 100%;
            padding: 12px 12px 12px 45px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.2s;
        }
        
        #searchInput:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .filter-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 10px 20px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.95rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .filter-btn:hover {
            border-color: #667eea;
            color: #667eea;
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .table-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th {
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #666;
            border-bottom: 2px solid #e0e0e0;
        }
        
        td {
            padding: 15px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .severity-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        
        .severity-error {
            background: #fee;
            color: #c33;
        }
        
        .severity-warning {
            background: #ffeaa7;
            color: #d68910;
        }
        
        .severity-style {
            background: #dfe6e9;
            color: #2d3436;
        }
        
        .severity-performance {
            background: #d1f2eb;
            color: #27ae60;
        }
        
        .code-btn {
            padding: 6px 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: background 0.2s;
        }
        
        .code-btn:hover {
            background: #5a67d8;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            animation: fadeIn 0.3s;
        }
        
        .modal-content {
            background: white;
            margin: 5% auto;
            padding: 30px;
            width: 80%;
            max-width: 900px;
            border-radius: 12px;
            position: relative;
            animation: slideIn 0.3s;
        }
        
        .close {
            position: absolute;
            right: 20px;
            top: 20px;
            font-size: 2rem;
            cursor: pointer;
            color: #999;
        }
        
        .close:hover {
            color: #333;
        }
        
        pre {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            max-height: 600px;
            overflow-y: auto;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        """
    
    def generate_issue_rows(self):
        """Generate HTML for issue rows"""
        rows = []
        for i, issue in enumerate(self.issues):
            file_name = Path(issue.get('file', '')).name
            line = issue.get('line', '0')
            severity = issue.get('severity', 'unknown')
            message = html.escape(issue.get('message', ''))
            issue_id = issue.get('id', f'ISSUE{i}')
            
            has_context = 'code_context' in issue
            
            row = f"""
            <tr data-severity="{severity}">
                <td>{file_name}</td>
                <td>{line}</td>
                <td><span class="severity-badge severity-{severity}">{severity.upper()}</span></td>
                <td>{message}</td>
                <td>{issue_id}</td>
                <td>
                    {"<button class='code-btn' onclick='showCode(" + str(i) + ")'><i class='fas fa-code'></i> View</button>" if has_context else ""}
                </td>
            </tr>
            """
            rows.append(row)
        
        return ''.join(rows)
    
    def generate_scripts(self):
        """Generate JavaScript code"""
        # Encode issues data
        issues_json = json.dumps(self.issues)
        issues_b64 = base64.b64encode(issues_json.encode()).decode()
        
        return f"""
        // Decode issues data
        const issuesData = JSON.parse(atob('{issues_b64}'));
        let currentFilter = 'all';
        
        function filterIssues() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const rows = document.querySelectorAll('#issuesTable tbody tr');
            
            rows.forEach(row => {{
                const severity = row.dataset.severity;
                const text = row.textContent.toLowerCase();
                
                const matchesFilter = currentFilter === 'all' || severity === currentFilter;
                const matchesSearch = searchTerm === '' || text.includes(searchTerm);
                
                row.style.display = matchesFilter && matchesSearch ? '' : 'none';
            }});
        }}
        
        function setFilter(filter) {{
            currentFilter = filter;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.closest('.filter-btn').classList.add('active');
            
            filterIssues();
        }}
        
        function showCode(index) {{
            const issue = issuesData[index];
            if (!issue.code_context) return;
            
            const modal = document.getElementById('codeModal');
            const title = document.getElementById('modalTitle');
            const content = document.getElementById('codeContent');
            
            title.textContent = `${{issue.file}}:${{issue.line}}`;
            
            // Build code content
            let code = '';
            issue.code_context.lines.forEach(line => {{
                const highlight = line.is_target ? 'style="background: #fffbdd;"' : '';
                code += `<div ${{highlight}}>` +
                        `<span style="color: #999; margin-right: 10px;">${{String(line.number).padStart(4)}}</span>` +
                        `${{escapeHtml(line.content)}}` +
                        `</div>`;
            }});
            
            content.innerHTML = code;
            modal.style.display = 'block';
            
            // Syntax highlighting
            hljs.highlightElement(content);
        }}
        
        function closeModal() {{
            document.getElementById('codeModal').style.display = 'none';
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        // Close modal on outside click
        window.onclick = function(event) {{
            const modal = document.getElementById('codeModal');
            if (event.target == modal) {{
                closeModal();
            }}
        }}
        """


class VirtualDashboardGenerator:
    """Virtual scrolling dashboard for large datasets"""
    
    def __init__(self, issues_file):
        with open(issues_file) as f:
            data = json.load(f)
        self.issues = data.get('issues', [])
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Generate unique IDs for each issue
        for i, issue in enumerate(self.issues):
            if 'id' not in issue:
                id_str = f"{issue.get('file', '')}:{issue.get('line', '')}:{issue.get('message', '')}"
                issue['id'] = hashlib.md5(id_str.encode()).hexdigest()[:8].upper()
    
    def generate(self, output_file):
        """Generate virtual scrolling dashboard"""
        
        # Calculate statistics
        stats = self.calculate_stats()
        
        # Generate HTML with embedded JSONL data
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPPCheck Studio - Virtual Scroll Dashboard</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        {self.generate_virtual_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1><i class="fas fa-code"></i> CPPCheck Studio - Virtual Scroll</h1>
                <div class="header-info">
                    <span><i class="fas fa-rocket"></i> Handles {len(self.issues):,} issues smoothly</span>
                    <span><i class="fas fa-clock"></i> {self.timestamp}</span>
                </div>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card error">
                <i class="fas fa-exclamation-circle"></i>
                <h3>Errors</h3>
                <div class="value">{stats['errors']:,}</div>
                <div class="percent">{stats['error_percent']:.1f}%</div>
            </div>
            
            <div class="stat-card warning">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Warnings</h3>
                <div class="value">{stats['warnings']:,}</div>
                <div class="percent">{stats['warning_percent']:.1f}%</div>
            </div>
            
            <div class="stat-card style">
                <i class="fas fa-palette"></i>
                <h3>Style</h3>
                <div class="value">{stats['style']:,}</div>
                <div class="percent">{stats['style_percent']:.1f}%</div>
            </div>
            
            <div class="stat-card performance">
                <i class="fas fa-tachometer-alt"></i>
                <h3>Performance</h3>
                <div class="value">{stats['performance']:,}</div>
                <div class="percent">{stats['performance_percent']:.1f}%</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="search-container">
                <i class="fas fa-search"></i>
                <input type="text" id="searchInput" placeholder="Search {len(self.issues):,} issues...">
                <span class="search-status"></span>
            </div>
            
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">
                    <i class="fas fa-list"></i> All
                </button>
                <button class="filter-btn" data-filter="error">
                    <i class="fas fa-exclamation-circle"></i> Errors
                </button>
                <button class="filter-btn" data-filter="warning">
                    <i class="fas fa-exclamation-triangle"></i> Warnings
                </button>
                <button class="filter-btn" data-filter="style">
                    <i class="fas fa-palette"></i> Style
                </button>
                <button class="filter-btn" data-filter="performance">
                    <i class="fas fa-tachometer-alt"></i> Performance
                </button>
            </div>
        </div>
        
        <div class="virtual-container">
            <div class="table-header">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 25%">File</th>
                            <th style="width: 8%">Line</th>
                            <th style="width: 12%">Severity</th>
                            <th style="width: 40%">Message</th>
                            <th style="width: 10%">ID</th>
                            <th style="width: 5%">View</th>
                        </tr>
                    </thead>
                </table>
            </div>
            
            <div id="virtualScroll" class="virtual-scroll">
                <div id="scrollContent" class="scroll-content"></div>
            </div>
            
            <div class="status-bar">
                <span id="visibleRange">Showing 0-0 of 0</span>
                <span id="performance">0 FPS</span>
            </div>
        </div>
        
        <div id="codeModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 id="modalTitle">Code Context</h2>
                    <span class="close">&times;</span>
                </div>
                <pre id="codeContent"></pre>
            </div>
        </div>
    </div>
    
    <script>
        // Embedded JSONL data
        const issuesJSONL = `{self.generate_jsonl_data()}`;
        
        {self.generate_virtual_scripts()}
    </script>
</body>
</html>"""
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"  📊 Dashboard type: Virtual Scroll")
        print(f"  📏 File size: {len(html_content) / 1024 / 1024:.1f} MB")
        print(f"  🚀 Optimized for {len(self.issues):,} issues")
    
    def calculate_stats(self):
        """Calculate issue statistics"""
        total = len(self.issues)
        errors = sum(1 for i in self.issues if i.get('severity') == 'error')
        warnings = sum(1 for i in self.issues if i.get('severity') == 'warning')
        style = sum(1 for i in self.issues if i.get('severity') == 'style')
        performance = sum(1 for i in self.issues if i.get('severity') == 'performance')
        
        return {
            'total': total,
            'errors': errors,
            'warnings': warnings,
            'style': style,
            'performance': performance,
            'error_percent': (errors / total * 100) if total > 0 else 0,
            'warning_percent': (warnings / total * 100) if total > 0 else 0,
            'style_percent': (style / total * 100) if total > 0 else 0,
            'performance_percent': (performance / total * 100) if total > 0 else 0
        }
    
    def generate_jsonl_data(self):
        """Generate JSONL format data"""
        lines = []
        for issue in self.issues:
            # Create compact version without code context for initial load
            compact = {k: v for k, v in issue.items() if k != 'code_context'}
            lines.append(json.dumps(compact))
        return '\\n'.join(lines)
    
    def generate_virtual_styles(self):
        """Generate CSS for virtual scrolling"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f0f2f5;
            color: #1a1a1a;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .header-content h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .header-info {
            display: flex;
            gap: 30px;
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            text-align: center;
            transition: transform 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        
        .stat-card i {
            font-size: 2rem;
            margin-bottom: 10px;
            opacity: 0.8;
        }
        
        .stat-card h3 {
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: #666;
        }
        
        .stat-card .value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 4px;
        }
        
        .stat-card .percent {
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        .stat-card.error { border-top: 3px solid #e74c3c; }
        .stat-card.error i, .stat-card.error .value { color: #e74c3c; }
        
        .stat-card.warning { border-top: 3px solid #f39c12; }
        .stat-card.warning i, .stat-card.warning .value { color: #f39c12; }
        
        .stat-card.style { border-top: 3px solid #3498db; }
        .stat-card.style i, .stat-card.style .value { color: #3498db; }
        
        .stat-card.performance { border-top: 3px solid #2ecc71; }
        .stat-card.performance i, .stat-card.performance .value { color: #2ecc71; }
        
        .controls {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
        }
        
        .search-container {
            position: relative;
            flex: 1;
            max-width: 500px;
        }
        
        .search-container i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #666;
        }
        
        #searchInput {
            width: 100%;
            padding: 10px 10px 10px 40px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 0.95rem;
        }
        
        #searchInput:focus {
            outline: none;
            border-color: #1e3c72;
        }
        
        .search-status {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.85rem;
            color: #666;
        }
        
        .filter-buttons {
            display: flex;
            gap: 8px;
        }
        
        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .filter-btn:hover {
            border-color: #1e3c72;
            color: #1e3c72;
        }
        
        .filter-btn.active {
            background: #1e3c72;
            color: white;
            border-color: #1e3c72;
        }
        
        .virtual-container {
            flex: 1;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .table-header {
            background: #f8f9fa;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .table-header table {
            width: 100%;
            table-layout: fixed;
        }
        
        .table-header th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #666;
            font-size: 0.9rem;
        }
        
        .virtual-scroll {
            flex: 1;
            overflow-y: auto;
            position: relative;
        }
        
        .scroll-content {
            position: relative;
        }
        
        .virtual-row {
            position: absolute;
            width: 100%;
            display: flex;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #f0f0f0;
            transition: background 0.1s;
        }
        
        .virtual-row:hover {
            background: #f8f9fa;
        }
        
        .virtual-row > div {
            padding: 0 12px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .virtual-row .file { width: 25%; }
        .virtual-row .line { width: 8%; }
        .virtual-row .severity { width: 12%; }
        .virtual-row .message { width: 40%; }
        .virtual-row .id { width: 10%; font-family: monospace; font-size: 0.85rem; }
        .virtual-row .actions { width: 5%; }
        
        .severity-badge {
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-block;
        }
        
        .severity-error {
            background: #fee;
            color: #c33;
        }
        
        .severity-warning {
            background: #fff3cd;
            color: #856404;
        }
        
        .severity-style {
            background: #e7f1ff;
            color: #004085;
        }
        
        .severity-performance {
            background: #d4edda;
            color: #155724;
        }
        
        .code-btn {
            padding: 4px 8px;
            background: transparent;
            color: #1e3c72;
            border: 1px solid #1e3c72;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s;
        }
        
        .code-btn:hover {
            background: #1e3c72;
            color: white;
        }
        
        .status-bar {
            background: #f8f9fa;
            padding: 10px 20px;
            border-top: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: #666;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
        }
        
        .modal-content {
            background: white;
            margin: 5% auto;
            width: 80%;
            max-width: 900px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        .modal-header {
            background: #1e3c72;
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-header h2 {
            font-size: 1.3rem;
            font-weight: 600;
        }
        
        .close {
            font-size: 1.5rem;
            cursor: pointer;
            opacity: 0.8;
        }
        
        .close:hover {
            opacity: 1;
        }
        
        #codeContent {
            padding: 20px;
            max-height: 600px;
            overflow-y: auto;
            background: #f8f9fa;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .code-line {
            display: flex;
            padding: 2px 0;
        }
        
        .code-line.highlight {
            background: #fffbdd;
        }
        
        .line-number {
            color: #999;
            margin-right: 20px;
            min-width: 40px;
            text-align: right;
            user-select: none;
        }
        """
    
    def generate_virtual_scripts(self):
        """Generate JavaScript for virtual scrolling"""
        return """
        // Parse JSONL data
        const issues = issuesJSONL.trim().split('\\n').map(line => JSON.parse(line));
        
        // Virtual scrolling configuration
        const ROW_HEIGHT = 48;
        const BUFFER_ROWS = 5;
        const DEBOUNCE_DELAY = 150;
        
        // State
        let filteredIssues = issues;
        let currentFilter = 'all';
        let searchTerm = '';
        let visibleStart = 0;
        let visibleEnd = 0;
        
        // DOM elements
        const virtualScroll = document.getElementById('virtualScroll');
        const scrollContent = document.getElementById('scrollContent');
        const searchInput = document.getElementById('searchInput');
        const searchStatus = document.querySelector('.search-status');
        const visibleRange = document.getElementById('visibleRange');
        const performanceDisplay = document.getElementById('performance');
        
        // FPS tracking
        let lastFrameTime = performance.now();
        let fps = 60;
        
        function updateFPS() {
            const now = performance.now();
            const delta = now - lastFrameTime;
            fps = Math.round(1000 / delta);
            lastFrameTime = now;
            performanceDisplay.textContent = `${fps} FPS`;
        }
        
        // Debounce function
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
        
        // Filter issues
        function filterIssues() {
            const search = searchTerm.toLowerCase();
            
            filteredIssues = issues.filter(issue => {
                const matchesFilter = currentFilter === 'all' || issue.severity === currentFilter;
                const matchesSearch = !search || 
                    issue.file.toLowerCase().includes(search) ||
                    issue.message.toLowerCase().includes(search) ||
                    issue.id.toLowerCase().includes(search);
                
                return matchesFilter && matchesSearch;
            });
            
            searchStatus.textContent = `${filteredIssues.length.toLocaleString()} results`;
            updateVirtualScroll();
        }
        
        // Update virtual scroll
        function updateVirtualScroll() {
            const scrollTop = virtualScroll.scrollTop;
            const containerHeight = virtualScroll.clientHeight;
            
            // Calculate visible range
            visibleStart = Math.max(0, Math.floor(scrollTop / ROW_HEIGHT) - BUFFER_ROWS);
            visibleEnd = Math.min(
                filteredIssues.length,
                Math.ceil((scrollTop + containerHeight) / ROW_HEIGHT) + BUFFER_ROWS
            );
            
            // Update scroll content height
            scrollContent.style.height = `${filteredIssues.length * ROW_HEIGHT}px`;
            
            // Clear existing rows
            scrollContent.innerHTML = '';
            
            // Render visible rows
            for (let i = visibleStart; i < visibleEnd; i++) {
                const issue = filteredIssues[i];
                const row = createRow(issue, i);
                scrollContent.appendChild(row);
            }
            
            // Update status
            visibleRange.textContent = `Showing ${visibleStart + 1}-${visibleEnd} of ${filteredIssues.length.toLocaleString()}`;
            updateFPS();
        }
        
        // Create row element
        function createRow(issue, index) {
            const row = document.createElement('div');
            row.className = 'virtual-row';
            row.style.top = `${index * ROW_HEIGHT}px`;
            
            const fileName = issue.file.split('/').pop();
            const hasContext = issue.code_context !== undefined;
            
            row.innerHTML = `
                <div class="file" title="${issue.file}">${fileName}</div>
                <div class="line">${issue.line}</div>
                <div class="severity">
                    <span class="severity-badge severity-${issue.severity}">${issue.severity.toUpperCase()}</span>
                </div>
                <div class="message" title="${escapeHtml(issue.message)}">${escapeHtml(issue.message)}</div>
                <div class="id">${issue.id}</div>
                <div class="actions">
                    ${hasContext ? `<button class="code-btn" onclick="showCode('${issue.id}')">View</button>` : ''}
                </div>
            `;
            
            return row;
        }
        
        // Show code modal
        function showCode(issueId) {
            const issue = issues.find(i => i.id === issueId);
            if (!issue || !issue.code_context) return;
            
            const modal = document.getElementById('codeModal');
            const title = document.getElementById('modalTitle');
            const content = document.getElementById('codeContent');
            
            title.textContent = `${issue.file}:${issue.line}`;
            
            // Build code content
            let code = '';
            if (issue.code_context.lines) {
                issue.code_context.lines.forEach(line => {
                    const highlight = line.is_target ? ' highlight' : '';
                    code += `<div class="code-line${highlight}">` +
                            `<span class="line-number">${line.number}</span>` +
                            `<span>${escapeHtml(line.content)}</span>` +
                            `</div>`;
                });
            }
            
            content.innerHTML = code;
            modal.style.display = 'block';
        }
        
        // Escape HTML
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Event listeners
        virtualScroll.addEventListener('scroll', debounce(updateVirtualScroll, 16));
        
        searchInput.addEventListener('input', debounce(function(e) {
            searchTerm = e.target.value;
            filterIssues();
        }, DEBOUNCE_DELAY));
        
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentFilter = this.dataset.filter;
                filterIssues();
            });
        });
        
        // Modal close
        document.querySelector('.close').addEventListener('click', function() {
            document.getElementById('codeModal').style.display = 'none';
        });
        
        window.addEventListener('click', function(event) {
            const modal = document.getElementById('codeModal');
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
        
        // Window resize
        window.addEventListener('resize', debounce(updateVirtualScroll, 100));
        
        // Initialize
        filterIssues();
        """