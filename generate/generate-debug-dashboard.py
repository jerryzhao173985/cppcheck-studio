#!/usr/bin/env python3
"""
Debug Dashboard Generator - Smaller data size with debug logging
"""

import json
from pathlib import Path
from datetime import datetime
import hashlib

class DebugDashboardGenerator:
    def __init__(self, issues_file, max_issues=500):
        with open(issues_file) as f:
            data = json.load(f)
        # Limit issues for debugging
        self.issues = data.get('issues', [])[:max_issues]
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Generate unique IDs for each issue
        for i, issue in enumerate(self.issues):
            if 'id' not in issue:
                id_str = f"{issue.get('file', '')}:{issue.get('line', '')}:{issue.get('message', '')}"
                issue['id'] = hashlib.md5(id_str.encode()).hexdigest()[:8].upper()
    
    def generate(self, output_file):
        """Generate debug dashboard"""
        
        # Calculate statistics
        stats = self.calculate_stats()
        
        # Count code context
        with_context = sum(1 for i in self.issues if 'code_context' in i)
        
        # Strip code context to reduce size
        issues_no_context = []
        for issue in self.issues:
            issue_copy = {k: v for k, v in issue.items() if k != 'code_context'}
            issues_no_context.append(issue_copy)
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPPCheck Studio Dashboard (Debug)</title>
    
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
                <h1><i class="fas fa-code"></i> CPPCheck Studio Dashboard (Debug Mode)</h1>
                <div class="header-info">
                    <span><i class="fas fa-project-diagram"></i> LPZRobots</span>
                    <span><i class="fas fa-clock"></i> {self.timestamp}</span>
                    <span><i class="fas fa-bug"></i> Debug: {len(self.issues)} issues</span>
                </div>
            </div>
        </header>
        
        <!-- Debug Info -->
        <div class="debug-info">
            <h3>Debug Information</h3>
            <p>Total issues loaded: <strong>{len(self.issues)}</strong></p>
            <p>Issues with code context: <strong>{with_context}</strong></p>
            <p>Check browser console for JavaScript errors</p>
        </div>
        
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
        </div>
        
        <!-- Filter Controls -->
        <div class="controls">
            <div class="search-container">
                <i class="fas fa-search"></i>
                <input type="text" id="searchInput" placeholder="Search issues..." onkeyup="filterIssues()">
            </div>
            
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="setFilter('all', this)">
                    <i class="fas fa-list"></i> All ({stats['total']})
                </button>
                <button class="filter-btn" onclick="setFilter('error', this)">
                    <i class="fas fa-exclamation-circle"></i> Errors ({stats['errors']})
                </button>
                <button class="filter-btn" onclick="setFilter('warning', this)">
                    <i class="fas fa-exclamation-triangle"></i> Warnings ({stats['warnings']})
                </button>
                <button class="filter-btn" onclick="setFilter('style', this)">
                    <i class="fas fa-palette"></i> Style ({stats['style']})
                </button>
                <button class="filter-btn" onclick="setFilter('performance', this)">
                    <i class="fas fa-tachometer-alt"></i> Performance ({stats['performance']})
                </button>
            </div>
        </div>
        
        <!-- Issues Count Display -->
        <div class="issues-count">
            <span id="issuesCount">Loading...</span>
        </div>
        
        <!-- Issues Table -->
        <div class="issues-container">
            <table class="issues-table" id="issuesTable">
                <thead>
                    <tr>
                        <th class="col-file">FILE</th>
                        <th class="col-line">LINE</th>
                        <th class="col-severity">SEVERITY</th>
                        <th class="col-message">MESSAGE</th>
                        <th class="col-id">ID</th>
                        <th class="col-actions">ACTIONS</th>
                    </tr>
                </thead>
                <tbody id="issuesBody">
                    <tr>
                        <td colspan="6" style="text-align: center; padding: 20px;">
                            <i class="fas fa-spinner fa-spin"></i> Loading issues...
                        </td>
                    </tr>
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
        // Debug logging
        console.log('Dashboard loading...');
        
        // Issues data
        const issuesData = {json.dumps(issues_no_context)};
        console.log('Issues loaded:', issuesData.length);
        
        let currentFilter = 'all';
        let currentSearch = '';
        let filteredIssues = [];
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM loaded, initializing...');
            try {{
                renderIssues();
            }} catch (error) {{
                console.error('Error rendering issues:', error);
                document.getElementById('issuesBody').innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align: center; padding: 20px; color: red;">
                            Error: ${{error.message}}
                        </td>
                    </tr>
                `;
            }}
        }});
        
        // Render issues
        function renderIssues() {{
            console.log('Rendering issues...');
            const tbody = document.getElementById('issuesBody');
            tbody.innerHTML = '';
            
            // Filter issues
            filteredIssues = issuesData.filter(issue => {{
                // Apply severity filter
                if (currentFilter !== 'all' && issue.severity !== currentFilter) {{
                    return false;
                }}
                
                // Apply search filter
                if (currentSearch) {{
                    const searchLower = currentSearch.toLowerCase();
                    return issue.file.toLowerCase().includes(searchLower) ||
                           (issue.message || '').toLowerCase().includes(searchLower) ||
                           (issue.id || '').toLowerCase().includes(searchLower);
                }}
                
                return true;
            }});
            
            console.log('Filtered issues:', filteredIssues.length);
            
            // Update count
            const total = filteredIssues.length;
            document.getElementById('issuesCount').textContent = `${{total}} issues`;
            
            // Render all filtered issues (limited data)
            filteredIssues.forEach((issue, index) => {{
                const row = document.createElement('tr');
                row.className = 'issue-row';
                row.onclick = function() {{ showIssueDetails(issue); }};
                
                // Create cells
                const fileCell = document.createElement('td');
                fileCell.className = 'file-cell';
                fileCell.innerHTML = '<i class="fas fa-file-code"></i> ' + escapeHtml(getFileName(issue.file));
                fileCell.title = issue.file;
                
                const lineCell = document.createElement('td');
                lineCell.className = 'line-cell';
                lineCell.textContent = issue.line || '-';
                
                const severityCell = document.createElement('td');
                severityCell.innerHTML = '<span class="severity-badge ' + issue.severity + '">' + issue.severity.toUpperCase() + '</span>';
                
                const messageCell = document.createElement('td');
                messageCell.className = 'message-cell';
                messageCell.textContent = truncateMessage(issue.message || 'No message');
                messageCell.title = issue.message || 'No message';
                
                const idCell = document.createElement('td');
                idCell.className = 'id-cell';
                idCell.textContent = issue.id || 'N/A';
                
                const actionsCell = document.createElement('td');
                actionsCell.className = 'actions-cell';
                actionsCell.innerHTML = `
                    <button class="action-btn" 
                            onclick="showIssueDetails(${{JSON.stringify(issue).replace(/"/g, '&quot;')}}); event.stopPropagation();" 
                            title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                `;
                
                // Append cells
                row.appendChild(fileCell);
                row.appendChild(lineCell);
                row.appendChild(severityCell);
                row.appendChild(messageCell);
                row.appendChild(idCell);
                row.appendChild(actionsCell);
                
                tbody.appendChild(row);
            }});
            
            console.log('Rendering complete');
        }}
        
        // Helper functions
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        function getFileName(path) {{
            return path.split('/').pop();
        }}
        
        function truncateMessage(message) {{
            const maxLength = 80;
            if (message.length > maxLength) {{
                return message.substring(0, maxLength - 3) + '...';
            }}
            return message;
        }}
        
        // Filter functions
        function setFilter(filter, btn) {{
            console.log('Setting filter:', filter);
            currentFilter = filter;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(b => {{
                b.classList.remove('active');
            }});
            btn.classList.add('active');
            
            renderIssues();
        }}
        
        function filterIssues() {{
            currentSearch = document.getElementById('searchInput').value;
            console.log('Search:', currentSearch);
            renderIssues();
        }}
        
        // Show issue details
        function showIssueDetails(issue) {{
            console.log('Showing details for:', issue);
            const modal = document.getElementById('codeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.innerHTML = '<i class="fas fa-file-code"></i> ' + escapeHtml(getFileName(issue.file)) + ':' + issue.line;
            
            // Build modal content
            let content = '<div class="issue-details">';
            
            // Issue info section
            content += `
                <div class="info-section">
                    <h4><i class="fas fa-info-circle"></i> Issue Information</h4>
                    <table class="info-table">
                        <tr>
                            <td><strong>File:</strong></td>
                            <td class="code-text">${{escapeHtml(issue.file)}}</td>
                        </tr>
                        <tr>
                            <td><strong>Line:</strong></td>
                            <td>${{issue.line || 'N/A'}}</td>
                        </tr>
                        <tr>
                            <td><strong>Severity:</strong></td>
                            <td><span class="severity-badge ${{issue.severity}}">${{issue.severity.toUpperCase()}}</span></td>
                        </tr>
                        <tr>
                            <td><strong>Issue ID:</strong></td>
                            <td><code>${{issue.id || 'N/A'}}</code></td>
                        </tr>
                    </table>
                </div>
                
                <div class="message-section">
                    <h4><i class="fas fa-comment-alt"></i> Message</h4>
                    <div class="message-box">${{escapeHtml(issue.message || 'No message available')}}</div>
                </div>
            `;
            
            content += '</div>';
            
            modalBody.innerHTML = content;
            modal.style.display = 'block';
        }}
        
        function closeModal() {{
            document.getElementById('codeModal').style.display = 'none';
        }}
        
        // Close modal on outside click
        window.onclick = function(event) {{
            const modal = document.getElementById('codeModal');
            if (event.target === modal) {{
                closeModal();
            }}
        }}
        
        // Error handling
        window.onerror = function(msg, url, lineNo, columnNo, error) {{
            console.error('JavaScript error:', msg, 'at line', lineNo);
            return false;
        }};
    </script>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Debug dashboard generated: {output_file}")
        print(f"   Total issues: {len(self.issues)}")
        print(f"   File size: {Path(output_file).stat().st_size / 1024:.1f} KB")
        
    def calculate_stats(self):
        """Calculate issue statistics"""
        total = len(self.issues)
        if total == 0:
            return {
                'total': 0,
                'errors': 0,
                'warnings': 0,
                'style': 0,
                'performance': 0,
                'error_percent': 0,
                'warning_percent': 0,
                'style_percent': 0,
                'performance_percent': 0
            }
            
        stats = {
            'total': total,
            'errors': sum(1 for i in self.issues if i.get('severity') == 'error'),
            'warnings': sum(1 for i in self.issues if i.get('severity') == 'warning'),
            'style': sum(1 for i in self.issues if i.get('severity') == 'style'),
            'performance': sum(1 for i in self.issues if i.get('severity') == 'performance')
        }
        
        # Calculate percentages
        stats['error_percent'] = (stats['errors'] / total) * 100 if total > 0 else 0
        stats['warning_percent'] = (stats['warnings'] / total) * 100 if total > 0 else 0
        stats['style_percent'] = (stats['style'] / total) * 100 if total > 0 else 0
        stats['performance_percent'] = (stats['performance'] / total) * 100 if total > 0 else 0
            
        return stats
        
    def generate_styles(self):
        """Generate CSS styles"""
        return """
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f5f7fa;
            color: #2d3748;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Debug Info */
        .debug-info {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .debug-info h3 {
            margin-bottom: 10px;
            color: #856404;
        }
        
        .debug-info p {
            margin: 5px 0;
            color: #856404;
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 0;
            margin: -20px -20px 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .header h1 {
            font-size: 2em;
            font-weight: 700;
        }
        
        .header-info {
            display: flex;
            gap: 20px;
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        /* Statistics Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: currentColor;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .stat-card i {
            font-size: 2.5em;
            margin-bottom: 10px;
            opacity: 0.8;
        }
        
        .stat-card h3 {
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #718096;
            margin-bottom: 10px;
        }
        
        .stat-card .value {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .stat-card .percent {
            font-size: 0.9em;
            color: #718096;
        }
        
        /* Card colors */
        .stat-card.error { color: #e53e3e; }
        .stat-card.warning { color: #dd6b20; }
        .stat-card.style { color: #5a67d8; }
        .stat-card.performance { color: #38a169; }
        
        /* Controls */
        .controls {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .search-container {
            flex: 1;
            min-width: 300px;
            position: relative;
        }
        
        .search-container i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #a0aec0;
        }
        
        .search-container input {
            width: 100%;
            padding: 10px 15px 10px 40px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 0.95em;
            transition: border-color 0.2s;
        }
        
        .search-container input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .filter-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 8px 16px;
            border: 1px solid #e2e8f0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 5px;
            font-family: inherit;
        }
        
        .filter-btn:hover {
            background: #f7fafc;
            transform: translateY(-1px);
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        /* Issues count */
        .issues-count {
            text-align: right;
            padding: 0 10px 10px;
            font-size: 0.85em;
            color: #718096;
        }
        
        /* Issues Table */
        .issues-container {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow-x: auto;
        }
        
        .issues-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .issues-table thead {
            background: #f7fafc;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .issues-table th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #4a5568;
            white-space: nowrap;
        }
        
        /* Column widths */
        .col-file { width: 20%; }
        .col-line { width: 8%; text-align: center; }
        .col-severity { width: 12%; }
        .col-message { width: 42%; }
        .col-id { width: 10%; }
        .col-actions { width: 8%; text-align: center; }
        
        .issues-table tbody tr {
            border-bottom: 1px solid #e2e8f0;
            transition: background 0.1s;
            cursor: pointer;
        }
        
        .issues-table tbody tr:hover {
            background: #f7fafc;
        }
        
        .issues-table td {
            padding: 15px;
            font-size: 0.95em;
        }
        
        .file-cell {
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9em;
            color: #4a5568;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .line-cell {
            font-family: 'Monaco', 'Consolas', monospace;
            color: #718096;
            text-align: center;
        }
        
        .message-cell {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .id-cell {
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.85em;
            color: #718096;
        }
        
        .actions-cell {
            text-align: center;
        }
        
        .severity-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .severity-badge.error {
            background: #fed7d7;
            color: #c53030;
        }
        
        .severity-badge.warning {
            background: #feebc8;
            color: #c05621;
        }
        
        .severity-badge.style {
            background: #e0e7ff;
            color: #3730a3;
        }
        
        .severity-badge.performance {
            background: #d1fae5;
            color: #065f46;
        }
        
        .action-btn {
            padding: 6px 10px;
            border: 1px solid #e2e8f0;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.2s;
            color: #4a5568;
        }
        
        .action-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: scale(1.05);
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
        }
        
        .modal-content {
            background: white;
            margin: 50px auto;
            width: 90%;
            max-width: 800px;
            max-height: 80vh;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        
        .modal-header {
            background: #f7fafc;
            padding: 20px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-header h3 {
            font-size: 1.2em;
            font-weight: 600;
            color: #2d3748;
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 1.5em;
            cursor: pointer;
            color: #718096;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: all 0.2s;
        }
        
        .close-btn:hover {
            background: #e2e8f0;
            color: #2d3748;
        }
        
        .modal-body {
            padding: 0;
            max-height: calc(80vh - 80px);
            overflow-y: auto;
        }
        
        /* Issue Details */
        .issue-details {
            padding: 20px;
        }
        
        .info-section, .message-section {
            margin-bottom: 25px;
        }
        
        .issue-details h4 {
            font-size: 1em;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .info-table {
            width: 100%;
            background: #f7fafc;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .info-table td {
            padding: 10px 15px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .info-table tr:last-child td {
            border-bottom: none;
        }
        
        .info-table strong {
            color: #4a5568;
            font-weight: 500;
            display: inline-block;
            min-width: 100px;
        }
        
        .code-text {
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9em;
        }
        
        .message-box {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            font-size: 0.95em;
            line-height: 1.6;
        }
        """

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: generate-debug-dashboard.py <analysis.json> [output.html]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'debug-dashboard.html'
    
    generator = DebugDashboardGenerator(input_file)
    generator.generate(output_file)