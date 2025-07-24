#!/usr/bin/env python3
"""
Final Working Dashboard Generator with Code Context
Fixed version that properly shows code snippets


⚠️ DEPRECATION WARNING: This generator is deprecated and will be removed in April 2025.
Please use generate-standalone-virtual-dashboard.py instead.

See generate/DEPRECATION_NOTICE.md for migration guide.
"""

import sys
import warnings

# Show deprecation warning
warnings.warn(
    "\n⚠️  DEPRECATION: generate-final-working-dashboard.py is deprecated.\n"
    "   Please use generate-standalone-virtual-dashboard.py instead.\n"
    "   See generate/DEPRECATION_NOTICE.md for details.\n",
    DeprecationWarning,
    stacklevel=2
)
print("\n⚠️  This generator is deprecated. Please use generate-standalone-virtual-dashboard.py\n", file=sys.stderr)

import json
from pathlib import Path
from datetime import datetime
import hashlib

class FinalWorkingDashboardGenerator:
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
        """Generate dashboard with working code context"""
        
        # Calculate statistics
        stats = self.calculate_stats()
        
        # Count issues with code context
        with_context = sum(1 for i in self.issues if 'code_context' in i)
        
        # Limit code context to first 1000 issues plus all errors/warnings for size
        issues_with_limited_context = []
        for i, issue in enumerate(self.issues):
            if i < 1000 or issue.get('severity') in ['error', 'warning']:
                issues_with_limited_context.append(issue)
            else:
                # Remove code context for other issues
                issue_copy = issue.copy()
                if 'code_context' in issue_copy:
                    del issue_copy['code_context']
                issues_with_limited_context.append(issue_copy)
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPPCheck Studio Dashboard</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
    
    <style>
        {self.generate_styles()}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <h1><i class="fas fa-code"></i> CPPCheck Studio Dashboard</h1>
                <div class="header-info">
                    <span><i class="fas fa-project-diagram"></i> LPZRobots</span>
                    <span><i class="fas fa-clock"></i> {self.timestamp}</span>
                    <span><i class="fas fa-file-code"></i> {with_context} issues with code preview</span>
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
            <span id="issuesCount">Showing 500 of {len(self.issues)} issues</span>
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
                    <!-- Issues will be populated by JavaScript -->
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
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-cpp.min.js"></script>
    
    <script>
        // Store issues data with code context
        const issuesData = {json.dumps(issues_with_limited_context)};
        const issuesMap = new Map();
        issuesData.forEach((issue, index) => {{
            issuesMap.set(index, issue);
        }});
        
        let currentFilter = 'all';
        let currentSearch = '';
        let filteredIssues = [];
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Loaded', issuesData.length, 'issues');
            const withContext = issuesData.filter(i => i.code_context).length;
            console.log('Issues with code context:', withContext);
            renderIssues();
        }});
        
        // Render issues
        function renderIssues() {{
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
            
            // Update count
            const total = filteredIssues.length;
            const showing = Math.min(total, 500);
            document.getElementById('issuesCount').textContent = 
                total > 500 ? `Showing ${{showing}} of ${{total}} issues` : `${{total}} issues`;
            
            // Limit to first 500 for performance
            const displayIssues = filteredIssues.slice(0, 500);
            
            // Render rows
            displayIssues.forEach((issue, index) => {{
                const originalIndex = issuesData.indexOf(issue);
                const row = document.createElement('tr');
                row.className = 'issue-row';
                if (issue.code_context) {{
                    row.classList.add('has-code');
                }}
                row.onclick = function() {{ showIssueDetails(originalIndex); }};
                
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
                const codeIcon = issue.code_context ? 'fa-code' : 'fa-eye';
                const codeTitle = issue.code_context ? 'View Code' : 'View Details';
                const actionBtn = document.createElement('button');
                actionBtn.className = 'action-btn' + (issue.code_context ? ' has-code' : '');
                actionBtn.title = codeTitle;
                actionBtn.innerHTML = '<i class="fas ' + codeIcon + '"></i>';
                actionBtn.onclick = function(e) {{ 
                    e.stopPropagation(); 
                    showIssueDetails(originalIndex);
                }};
                actionsCell.appendChild(actionBtn);
                
                // Append cells
                row.appendChild(fileCell);
                row.appendChild(lineCell);
                row.appendChild(severityCell);
                row.appendChild(messageCell);
                row.appendChild(idCell);
                row.appendChild(actionsCell);
                
                tbody.appendChild(row);
            }});
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
            renderIssues();
        }}
        
        // Show issue details
        function showIssueDetails(index) {{
            const issue = issuesMap.get(index);
            if (!issue) {{
                console.error('Issue not found at index:', index);
                return;
            }}
            
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
            
            // Code context section
            content += '<div class="code-section">';
            content += '<h4><i class="fas fa-code"></i> Code Context</h4>';
            
            if (issue.code_context && issue.code_context.lines && issue.code_context.lines.length > 0) {{
                console.log('Showing code context for issue:', issue.file, issue.line);
                content += '<div class="code-preview">';
                content += '<pre class="language-cpp line-numbers"><code>';
                
                issue.code_context.lines.forEach(line => {{
                    const isTarget = line.is_target;
                    const lineClass = isTarget ? ' class="highlight-line"' : '';
                    const lineNum = String(line.number).padStart(4, ' ');
                    const escapedContent = escapeHtml(line.content);
                    content += `<span${{lineClass}}>${{lineNum}}: ${{escapedContent}}</span>\\n`;
                }});
                
                content += '</code></pre>';
                content += '</div>';
                
                // Add fix suggestion
                content += '<div class="issue-explanation">';
                content += '<h5><i class="fas fa-lightbulb"></i> Suggested Fix</h5>';
                content += getSuggestedFix(issue);
                content += '</div>';
            }} else {{
                console.log('No code context for issue:', issue.file, issue.line);
                content += `
                    <div class="no-code-message">
                        <i class="fas fa-info-circle"></i>
                        <p>Code preview is available for the first 1000 issues and all errors/warnings.</p>
                        <p class="hint">To see code for all issues, use the full analysis with code extraction.</p>
                    </div>
                `;
            }}
            content += '</div>';
            
            content += '</div>';
            
            modalBody.innerHTML = content;
            
            // Apply syntax highlighting if code is present
            if (issue.code_context) {{
                setTimeout(() => {{
                    Prism.highlightAll();
                }}, 10);
            }}
            
            modal.style.display = 'block';
        }}
        
        // Get suggested fix based on issue type
        function getSuggestedFix(issue) {{
            const message = issue.message || '';
            let suggestion = '<div class="suggestion">';
            
            if (message.includes('not initialized in the constructor')) {{
                suggestion += '<p>Initialize the member variable in the constructor\'s member initializer list:</p>';
                suggestion += '<pre><code class="language-cpp">MyClass() : array{{}} {{ }}</code></pre>';
            }} else if (message.includes('constructor with 1 argument that is not explicit')) {{
                suggestion += '<p>Add the <code>explicit</code> keyword to prevent implicit conversions:</p>';
                suggestion += '<pre><code class="language-cpp">explicit MyClass(int value);</code></pre>';
            }} else if (message.includes('overrides a') && message.includes('but is not marked')) {{
                suggestion += '<p>Add the <code>override</code> specifier to the function declaration:</p>';
                suggestion += '<pre><code class="language-cpp">void myFunction() override;</code></pre>';
            }} else if (message.includes('C-style cast')) {{
                suggestion += '<p>Replace C-style cast with appropriate C++ cast:</p>';
                suggestion += '<pre><code class="language-cpp">// Instead of: (int)value\\n// Use: static_cast<int>(value)</code></pre>';
            }} else {{
                suggestion += '<p>Review the code and apply the appropriate fix based on the issue description.</p>';
            }}
            
            suggestion += '</div>';
            return suggestion;
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
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                closeModal();
            }}
            if (e.key === '/' && !e.ctrlKey && !e.metaKey) {{
                e.preventDefault();
                document.getElementById('searchInput').focus();
            }}
        }});
    </script>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Final working dashboard generated: {output_file}")
        print(f"   Total issues: {len(self.issues)}")
        print(f"   Issues with code context: {with_context}")
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
        """Generate comprehensive CSS styles"""
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
        
        .issues-table tbody tr.has-code {
            position: relative;
        }
        
        .issues-table tbody tr.has-code::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: #667eea;
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
        
        .action-btn.has-code {
            border-color: #667eea;
            color: #667eea;
        }
        
        .action-btn.has-code:hover {
            background: #667eea;
            color: white;
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
            animation: fadeIn 0.2s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .modal-content {
            background: white;
            margin: 50px auto;
            width: 90%;
            max-width: 1000px;
            max-height: 90vh;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            animation: slideIn 0.3s;
        }
        
        @keyframes slideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
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
            max-height: calc(90vh - 80px);
            overflow-y: auto;
        }
        
        /* Issue Details */
        .issue-details {
            padding: 20px;
        }
        
        .info-section, .message-section, .code-section {
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
        
        /* Code Preview */
        .code-preview {
            background: #1e1e1e;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
        }
        
        .code-preview pre {
            margin: 0;
            padding: 20px;
            overflow-x: auto;
            background: #1e1e1e;
        }
        
        .code-preview code {
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9em;
            line-height: 1.6;
            color: #d4d4d4;
            display: block;
        }
        
        .code-preview .highlight-line {
            background: rgba(255, 235, 59, 0.1);
            border-left: 3px solid #ffd600;
            display: block;
            margin: 0 -20px;
            padding: 0 20px;
            padding-left: 17px;
        }
        
        /* Syntax highlighting overrides */
        .token.comment { color: #6a9955; }
        .token.keyword { color: #569cd6; }
        .token.string { color: #ce9178; }
        .token.number { color: #b5cea8; }
        .token.function { color: #dcdcaa; }
        .token.class-name { color: #4ec9b0; }
        .token.operator { color: #d4d4d4; }
        
        /* Issue explanation */
        .issue-explanation {
            margin-top: 20px;
            padding: 20px;
            background: #f0f7ff;
            border-radius: 8px;
            border: 1px solid #bee3f8;
        }
        
        .issue-explanation h5 {
            font-size: 0.95em;
            font-weight: 600;
            color: #2c5282;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .issue-explanation .suggestion {
            color: #2c5282;
            font-size: 0.9em;
        }
        
        .issue-explanation pre {
            background: white;
            border: 1px solid #bee3f8;
            border-radius: 4px;
            padding: 10px;
            margin-top: 10px;
            overflow-x: auto;
        }
        
        .issue-explanation code {
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9em;
            background: white;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        .no-code-message {
            text-align: center;
            padding: 40px;
            color: #718096;
            background: #f7fafc;
            border-radius: 8px;
        }
        
        .no-code-message i {
            font-size: 3em;
            margin-bottom: 15px;
            opacity: 0.5;
        }
        
        .no-code-message p {
            margin: 5px 0;
        }
        
        .no-code-message .hint {
            font-size: 0.9em;
            margin-top: 15px;
        }
        """

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: generate-final-working-dashboard.py <analysis.json> [output.html]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'final-working-dashboard.html'
    
    generator = FinalWorkingDashboardGenerator(input_file)
    generator.generate(output_file)