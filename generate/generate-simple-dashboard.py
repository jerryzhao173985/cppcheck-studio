#!/usr/bin/env python3
"""
Simple Dashboard Generator - Directly embeds data as JavaScript arrays
No JSONL, no parsing issues, just simple arrays that work

⚠️ DEPRECATION WARNING: This generator is deprecated and will be removed in April 2025.
Please use generate-production-dashboard.py instead, which is simpler and faster.

See generate/DEPRECATION_NOTICE.md for migration guide.
"""

import json
from pathlib import Path
from datetime import datetime
import hashlib
import sys
import warnings

# Show deprecation warning
warnings.warn(
    "\n⚠️  DEPRECATION: generate-simple-dashboard.py is deprecated.\n"
    "   Please use generate-production-dashboard.py instead.\n"
    "   See generate/DEPRECATION_NOTICE.md for details.\n",
    DeprecationWarning,
    stacklevel=2
)
print("\n⚠️  This generator is deprecated. Please use generate-production-dashboard.py\n", file=sys.stderr)

class SimpleDashboardGenerator:
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
        """Generate dashboard with data embedded as JavaScript arrays"""
        
        # Calculate statistics
        stats = self.calculate_stats()
        
        # Separate issues and code context
        issues_data = []
        code_context_data = {}
        
        for issue in self.issues:
            # Store issue without code context
            issue_copy = {k: v for k, v in issue.items() if k != 'code_context'}
            issues_data.append(issue_copy)
            
            # Store code context separately
            if 'code_context' in issue and issue.get('id'):
                code_context_data[issue['id']] = issue['code_context']
        
        # Generate JavaScript data
        issues_js = json.dumps(issues_data, indent=2)
        code_context_js = json.dumps(code_context_data, indent=2)
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPPCheck Dashboard - Simple Version</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        {self.generate_styles()}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <h1><i class="fas fa-code"></i> CPPCheck Dashboard</h1>
                <div class="header-info">
                    <span><i class="fas fa-clock"></i> {self.timestamp}</span>
                    <span><i class="fas fa-database"></i> {len(self.issues)} issues</span>
                </div>
            </div>
        </header>
        
        <!-- Statistics Cards -->
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
            
            <div class="stat-card information">
                <i class="fas fa-info-circle"></i>
                <h3>Information</h3>
                <div class="value">{stats['information']}</div>
                <div class="percent">{stats['information_percent']:.1f}%</div>
            </div>
        </div>
        
        <!-- Controls -->
        <div class="controls">
            <div class="search-box">
                <i class="fas fa-search"></i>
                <input type="text" id="searchInput" placeholder="Search files, messages, or IDs..." onkeyup="filterData()">
            </div>
            
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="setSeverityFilter('all', this)">
                    All ({len(self.issues)})
                </button>
                <button class="filter-btn error" onclick="setSeverityFilter('error', this)">
                    Errors ({stats['errors']})
                </button>
                <button class="filter-btn warning" onclick="setSeverityFilter('warning', this)">
                    Warnings ({stats['warnings']})
                </button>
                <button class="filter-btn style" onclick="setSeverityFilter('style', this)">
                    Style ({stats['style']})
                </button>
                <button class="filter-btn performance" onclick="setSeverityFilter('performance', this)">
                    Performance ({stats['performance']})
                </button>
            </div>
        </div>
        
        <!-- Status Bar -->
        <div class="status-bar">
            <div class="issues-count">
                <span id="issuesCount">Showing all {len(self.issues)} issues</span>
            </div>
        </div>
        
        <!-- Issues Table -->
        <div class="table-container">
            <table class="issues-table">
                <thead>
                    <tr>
                        <th width="30"></th>
                        <th>File</th>
                        <th width="80">Line</th>
                        <th width="100">Severity</th>
                        <th>Message</th>
                        <th width="100">ID</th>
                        <th width="60">Actions</th>
                    </tr>
                </thead>
                <tbody id="issuesBody">
                    <!-- Rows will be rendered here -->
                </tbody>
            </table>
        </div>
        
        <!-- Code Preview Modal -->
        <div id="codeModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 id="modalTitle">Issue Details</h3>
                    <button onclick="closeModal()" class="close-btn">&times;</button>
                </div>
                <div class="modal-body" id="modalBody">
                    <!-- Content will be inserted here -->
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Embed data directly as JavaScript
        const allIssues = {issues_js};
        
        const codeContextMap = {code_context_js};
        
        // Global state
        let filteredIssues = [...allIssues];
        let currentFilter = 'all';
        
        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Dashboard loaded with', allIssues.length, 'issues');
            renderIssues();
        }});
        
        function renderIssues() {{
            const tbody = document.getElementById('issuesBody');
            tbody.innerHTML = '';
            
            filteredIssues.forEach((issue, index) => {{
                const row = createIssueRow(issue, index);
                tbody.appendChild(row);
            }});
            
            updateIssueCount();
        }}
        
        function createIssueRow(issue, index) {{
            const row = document.createElement('tr');
            row.className = 'issue-row';
            
            const hasCodeContext = codeContextMap.hasOwnProperty(issue.id);
            
            // Indicator
            const indicatorCell = document.createElement('td');
            indicatorCell.className = 'indicator-cell';
            if (hasCodeContext) {{
                indicatorCell.innerHTML = '<div class="code-indicator"></div>';
            }}
            
            // File
            const fileCell = document.createElement('td');
            fileCell.className = 'file-cell';
            fileCell.innerHTML = '<i class="fas fa-file-code"></i> ' + escapeHtml(getFileName(issue.file || ''));
            fileCell.title = issue.file || '';
            
            // Line
            const lineCell = document.createElement('td');
            lineCell.className = 'line-cell';
            lineCell.textContent = issue.line || '-';
            
            // Severity
            const severityCell = document.createElement('td');
            const severityBadge = document.createElement('span');
            severityBadge.className = 'severity-badge ' + (issue.severity || 'unknown');
            severityBadge.textContent = (issue.severity || 'UNKNOWN').toUpperCase();
            severityCell.appendChild(severityBadge);
            
            // Message
            const messageCell = document.createElement('td');
            messageCell.className = 'message-cell';
            messageCell.textContent = issue.message || 'No message';
            messageCell.title = issue.message || '';
            
            // ID
            const idCell = document.createElement('td');
            idCell.className = 'id-cell';
            idCell.textContent = issue.id || 'N/A';
            
            // Actions
            const actionsCell = document.createElement('td');
            actionsCell.className = 'actions-cell';
            const actionBtn = document.createElement('button');
            actionBtn.className = 'action-btn' + (hasCodeContext ? ' has-code' : '');
            actionBtn.innerHTML = '<i class="fas ' + (hasCodeContext ? 'fa-code' : 'fa-eye') + '"></i>';
            actionBtn.onclick = () => showIssueDetails(issue, index);
            actionsCell.appendChild(actionBtn);
            
            row.appendChild(indicatorCell);
            row.appendChild(fileCell);
            row.appendChild(lineCell);
            row.appendChild(severityCell);
            row.appendChild(messageCell);
            row.appendChild(idCell);
            row.appendChild(actionsCell);
            
            row.onclick = () => showIssueDetails(issue, index);
            
            return row;
        }}
        
        function filterData() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            filteredIssues = allIssues.filter(issue => {{
                // Severity filter
                if (currentFilter !== 'all' && issue.severity !== currentFilter) {{
                    return false;
                }}
                
                // Search filter
                if (searchTerm) {{
                    const matchFile = (issue.file || '').toLowerCase().includes(searchTerm);
                    const matchMessage = (issue.message || '').toLowerCase().includes(searchTerm);
                    const matchId = (issue.id || '').toLowerCase().includes(searchTerm);
                    return matchFile || matchMessage || matchId;
                }}
                
                return true;
            }});
            
            renderIssues();
        }}
        
        function setSeverityFilter(severity, button) {{
            currentFilter = severity;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            button.classList.add('active');
            
            filterData();
        }}
        
        function updateIssueCount() {{
            const countEl = document.getElementById('issuesCount');
            if (filteredIssues.length === allIssues.length) {{
                countEl.textContent = `Showing all ${{allIssues.length}} issues`;
            }} else {{
                countEl.textContent = `Showing ${{filteredIssues.length}} of ${{allIssues.length}} issues`;
            }}
        }}
        
        function showIssueDetails(issue, index) {{
            const modal = document.getElementById('codeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.innerHTML = '<i class="fas fa-file-code"></i> ' + 
                escapeHtml(getFileName(issue.file || 'Unknown')) + ':' + (issue.line || '?');
            
            const codeContext = codeContextMap[issue.id];
            
            let content = '<div class="issue-details">';
            
            // Issue info
            content += '<div class="info-section">';
            content += '<h4>Issue Information</h4>';
            content += '<table class="info-table">';
            content += '<tr><td><strong>File:</strong></td><td>' + escapeHtml(issue.file || 'Unknown') + '</td></tr>';
            content += '<tr><td><strong>Line:</strong></td><td>' + (issue.line || 'N/A') + '</td></tr>';
            content += '<tr><td><strong>Severity:</strong></td><td><span class="severity-badge ' + (issue.severity || 'unknown') + '">' + (issue.severity || 'UNKNOWN').toUpperCase() + '</span></td></tr>';
            content += '<tr><td><strong>ID:</strong></td><td><code>' + (issue.id || 'N/A') + '</code></td></tr>';
            content += '</table></div>';
            
            // Message
            content += '<div class="message-section">';
            content += '<h4>Message</h4>';
            content += '<div class="message-box">' + escapeHtml(issue.message || 'No message') + '</div>';
            content += '</div>';
            
            // Code context
            if (codeContext && codeContext.lines) {{
                content += '<div class="code-section">';
                content += '<h4>Code Context</h4>';
                content += '<pre class="code-preview"><code>';
                
                codeContext.lines.forEach(line => {{
                    const lineNum = String(line.number || 0).padStart(4, ' ');
                    const lineContent = escapeHtml(line.content || '');
                    if (line.is_target) {{
                        content += '<span class="highlight-line">' + lineNum + ': ' + lineContent + '</span>\\n';
                    }} else {{
                        content += lineNum + ': ' + lineContent + '\\n';
                    }}
                }});
                
                content += '</code></pre></div>';
            }}
            
            content += '</div>';
            
            modalBody.innerHTML = content;
            modal.style.display = 'block';
        }}
        
        function closeModal() {{
            document.getElementById('codeModal').style.display = 'none';
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        function getFileName(path) {{
            if (!path) return 'Unknown';
            const parts = path.split('/');
            return parts[parts.length - 1];
        }}
        
        // Close modal on outside click
        window.onclick = function(event) {{
            const modal = document.getElementById('codeModal');
            if (event.target === modal) {{
                closeModal();
            }}
        }};
    </script>
</body>
</html>"""
        
        # Write the HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Simple dashboard generated: {output_file}")
        print(f"   Total issues: {len(self.issues)}")
        print(f"   File size: {Path(output_file).stat().st_size / 1024 / 1024:.1f} MB")
    
    def calculate_stats(self):
        """Calculate issue statistics"""
        # Initialize counters for severity types
        severity_counts = {
            'error': 0,
            'warning': 0,
            'style': 0,
            'performance': 0,
            'information': 0
        }
        
        # Count issues by severity
        for issue in self.issues:
            severity = issue.get('severity', 'unknown').lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        # Build stats dictionary with both counts and percentages
        stats = {}
        total = len(self.issues)
        
        # For template compatibility, we need both singular and plural forms
        stats['errors'] = severity_counts['error']
        stats['warnings'] = severity_counts['warning']
        stats['style'] = severity_counts['style']
        stats['performance'] = severity_counts['performance']
        stats['information'] = severity_counts['information']
        
        # Calculate percentages
        if total > 0:
            stats['error_percent'] = (severity_counts['error'] / total) * 100
            stats['warning_percent'] = (severity_counts['warning'] / total) * 100
            stats['style_percent'] = (severity_counts['style'] / total) * 100
            stats['performance_percent'] = (severity_counts['performance'] / total) * 100
            stats['information_percent'] = (severity_counts['information'] / total) * 100
        else:
            stats['error_percent'] = 0
            stats['warning_percent'] = 0
            stats['style_percent'] = 0
            stats['performance_percent'] = 0
            stats['information_percent'] = 0
        
        return stats
    
    def generate_styles(self):
        """Generate CSS styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f8f9fa;
            color: #2c3e50;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .header-content h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header-info {
            display: flex;
            gap: 30px;
            font-size: 0.95em;
            opacity: 0.9;
        }
        
        .header-info span {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Statistics */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .stat-card i {
            font-size: 2.5em;
            margin-bottom: 10px;
            opacity: 0.8;
        }
        
        .stat-card h3 {
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            opacity: 0.7;
        }
        
        .stat-card .value {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .stat-card .percent {
            font-size: 0.9em;
            opacity: 0.7;
        }
        
        .stat-card.error { color: #e74c3c; }
        .stat-card.warning { color: #f39c12; }
        .stat-card.style { color: #3498db; }
        .stat-card.performance { color: #2ecc71; }
        .stat-card.information { color: #95a5a6; }
        
        /* Controls */
        .controls {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .search-box {
            flex: 1;
            min-width: 300px;
            position: relative;
        }
        
        .search-box i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #7f8c8d;
        }
        
        .search-box input {
            width: 100%;
            padding: 12px 15px 12px 45px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 0.875em;
            transition: border-color 0.2s;
        }
        
        .search-box input:focus {
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
            border: 1px solid #ddd;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.875em;
            font-weight: 500;
        }
        
        .filter-btn:hover {
            background: #f8f9fa;
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .filter-btn.error { border-color: #e74c3c; color: #e74c3c; }
        .filter-btn.warning { border-color: #f39c12; color: #f39c12; }
        .filter-btn.style { border-color: #3498db; color: #3498db; }
        .filter-btn.performance { border-color: #2ecc71; color: #2ecc71; }
        
        /* Status Bar */
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            margin-bottom: 10px;
            color: #7f8c8d;
            font-size: 0.875em;
        }
        
        /* Table */
        .table-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            overflow: hidden;
        }
        
        .issues-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .issues-table thead {
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }
        
        .issues-table th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
            color: #495057;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .issue-row {
            border-bottom: 1px solid #f1f3f5;
            transition: background-color 0.2s;
            cursor: pointer;
        }
        
        .issue-row:hover {
            background-color: #f8f9fa;
        }
        
        .issue-row td {
            padding: 15px;
            font-size: 0.875em;
        }
        
        .indicator-cell {
            text-align: center;
        }
        
        .code-indicator {
            width: 8px;
            height: 8px;
            background: #2ecc71;
            border-radius: 50%;
            display: inline-block;
        }
        
        .file-cell {
            color: #495057;
            font-weight: 500;
        }
        
        .line-cell {
            text-align: center;
            color: #7f8c8d;
        }
        
        .message-cell {
            max-width: 400px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .severity-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .severity-badge.error {
            background: #fee;
            color: #e74c3c;
        }
        
        .severity-badge.warning {
            background: #fff3cd;
            color: #f39c12;
        }
        
        .severity-badge.style {
            background: #e3f2fd;
            color: #3498db;
        }
        
        .severity-badge.performance {
            background: #e8f8f5;
            color: #2ecc71;
        }
        
        .severity-badge.information {
            background: #f4f6f7;
            color: #95a5a6;
        }
        
        .id-cell {
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.75em;
            color: #7f8c8d;
        }
        
        .action-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.75em;
            transition: background-color 0.2s;
        }
        
        .action-btn:hover {
            background: #5a67d8;
        }
        
        .action-btn.has-code {
            background: #2ecc71;
        }
        
        .action-btn.has-code:hover {
            background: #27ae60;
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
        }
        
        .modal-content {
            background-color: white;
            margin: 5% auto;
            padding: 0;
            width: 80%;
            max-width: 900px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .modal-header {
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-header h3 {
            margin: 0;
            color: #495057;
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 1.5em;
            cursor: pointer;
            color: #adb5bd;
            transition: color 0.2s;
        }
        
        .close-btn:hover {
            color: #495057;
        }
        
        .modal-body {
            padding: 30px;
        }
        
        .issue-details h4 {
            margin-bottom: 15px;
            color: #495057;
            font-size: 1.1em;
        }
        
        .info-table {
            width: 100%;
            margin-bottom: 30px;
        }
        
        .info-table td {
            padding: 8px 0;
        }
        
        .info-table td:first-child {
            width: 120px;
            color: #7f8c8d;
        }
        
        .message-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 30px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.875em;
        }
        
        .code-preview {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 13px;
            line-height: 1.5;
        }
        
        .highlight-line {
            background: #3a3a3a;
            display: block;
            margin: 0 -20px;
            padding: 0 20px;
            border-left: 3px solid #667eea;
        }
        """

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python generate-simple-dashboard.py <input.json> <output.html>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    generator = SimpleDashboardGenerator(input_file)
    generator.generate(output_file)