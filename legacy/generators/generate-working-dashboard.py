#!/usr/bin/env python3
"""
Working CPPCheck Dashboard Generator
Splits data into chunks to avoid memory issues


⚠️ DEPRECATION WARNING: This generator is deprecated and will be removed in April 2025.
Please use generate-standalone-virtual-dashboard.py instead.

See generate/DEPRECATION_NOTICE.md for migration guide.
"""

import sys
import warnings

# Show deprecation warning
warnings.warn(
    "\n⚠️  DEPRECATION: generate-working-dashboard.py is deprecated.\n"
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

class WorkingDashboardGenerator:
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
        """Generate working dashboard with chunked data loading"""
        
        # Calculate statistics
        stats = self.calculate_stats()
        
        # Count issues with code context
        with_context = sum(1 for i in self.issues if 'code_context' in i)
        
        # Split issues into chunks to avoid memory issues
        chunk_size = 100
        chunks = [self.issues[i:i + chunk_size] for i in range(0, len(self.issues), chunk_size)]
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPPCheck Studio Dashboard</title>
    
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
                <h1><i class="fas fa-code"></i> CPPCheck Studio Dashboard</h1>
                <div class="header-info">
                    <span><i class="fas fa-project-diagram"></i> LPZRobots</span>
                    <span><i class="fas fa-clock"></i> {self.timestamp}</span>
                    <span><i class="fas fa-file-code"></i> {with_context}/{len(self.issues)} with code</span>
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
            <span id="issuesCount">Loading issues...</span>
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
        // Initialize data store
        const dataStore = {{
            issues: [],
            loaded: false,
            currentFilter: 'all',
            currentSearch: '',
            filteredIssues: []
        }};
        
        // Load issues data in chunks
        const issueChunks = {json.dumps(chunks)};
        
        // Load all chunks
        function loadIssues() {{
            console.log('Starting to load issue chunks...');
            dataStore.issues = [];
            
            // Combine all chunks
            issueChunks.forEach((chunk, index) => {{
                console.log(`Processing chunk ${{index + 1}}/${{issueChunks.length}}`);
                dataStore.issues = dataStore.issues.concat(chunk);
            }});
            
            dataStore.loaded = true;
            console.log('Loaded', dataStore.issues.length, 'total issues');
            
            // Render issues
            renderIssues();
        }}
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM loaded, loading issues...');
            setTimeout(loadIssues, 100); // Small delay to ensure DOM is ready
        }});
        
        // Render issues
        function renderIssues() {{
            if (!dataStore.loaded) {{
                console.log('Data not loaded yet');
                return;
            }}
            
            console.log('Rendering issues...');
            const tbody = document.getElementById('issuesBody');
            tbody.innerHTML = '';
            
            // Filter issues
            dataStore.filteredIssues = dataStore.issues.filter(issue => {{
                // Apply severity filter
                if (dataStore.currentFilter !== 'all' && issue.severity !== dataStore.currentFilter) {{
                    return false;
                }}
                
                // Apply search filter
                if (dataStore.currentSearch) {{
                    const searchLower = dataStore.currentSearch.toLowerCase();
                    return issue.file.toLowerCase().includes(searchLower) ||
                           (issue.message || '').toLowerCase().includes(searchLower) ||
                           (issue.id || '').toLowerCase().includes(searchLower);
                }}
                
                return true;
            }});
            
            console.log('Filtered to', dataStore.filteredIssues.length, 'issues');
            
            // Update count
            const total = dataStore.filteredIssues.length;
            const showing = Math.min(total, 500);
            document.getElementById('issuesCount').textContent = 
                total > 500 ? `Showing ${{showing}} of ${{total}} issues` : `${{total}} issues`;
            
            // Limit to first 500 for performance
            const displayIssues = dataStore.filteredIssues.slice(0, 500);
            
            // Render rows
            displayIssues.forEach((issue, index) => {{
                const row = document.createElement('tr');
                row.className = 'issue-row';
                if (issue.code_context) {{
                    row.classList.add('has-code');
                }}
                row.onclick = function() {{ showIssueDetails(index); }};
                
                // Build row HTML
                let rowHtml = '<td class="file-cell" title="' + escapeHtml(issue.file) + '">';
                rowHtml += '<i class="fas fa-file-code"></i> ' + escapeHtml(getFileName(issue.file));
                rowHtml += '</td>';
                
                rowHtml += '<td class="line-cell">' + (issue.line || '-') + '</td>';
                
                rowHtml += '<td><span class="severity-badge ' + issue.severity + '">';
                rowHtml += issue.severity.toUpperCase() + '</span></td>';
                
                rowHtml += '<td class="message-cell" title="' + escapeHtml(issue.message || '') + '">';
                rowHtml += escapeHtml(truncateMessage(issue.message || 'No message'));
                rowHtml += '</td>';
                
                rowHtml += '<td class="id-cell">' + (issue.id || 'N/A') + '</td>';
                
                const codeIcon = issue.code_context ? 'fa-code' : 'fa-eye';
                const codeTitle = issue.code_context ? 'View Code' : 'View Details';
                rowHtml += '<td class="actions-cell">';
                rowHtml += '<button class="action-btn ' + (issue.code_context ? 'has-code' : '') + '"';
                rowHtml += ' onclick="showIssueDetails(' + index + '); event.stopPropagation();"';
                rowHtml += ' title="' + codeTitle + '">';
                rowHtml += '<i class="fas ' + codeIcon + '"></i></button></td>';
                
                row.innerHTML = rowHtml;
                tbody.appendChild(row);
            }});
            
            console.log('Rendered', displayIssues.length, 'rows');
        }}
        
        // Helper functions
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text || '';
            return div.innerHTML;
        }}
        
        function getFileName(path) {{
            return path ? path.split('/').pop() : '';
        }}
        
        function truncateMessage(message) {{
            const maxLength = 80;
            if (message && message.length > maxLength) {{
                return message.substring(0, maxLength - 3) + '...';
            }}
            return message || '';
        }}
        
        // Filter functions
        function setFilter(filter, btn) {{
            dataStore.currentFilter = filter;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(b => {{
                b.classList.remove('active');
            }});
            btn.classList.add('active');
            
            renderIssues();
        }}
        
        function filterIssues() {{
            dataStore.currentSearch = document.getElementById('searchInput').value;
            renderIssues();
        }}
        
        // Show issue details
        function showIssueDetails(index) {{
            const issue = dataStore.filteredIssues[index];
            if (!issue) return;
            
            const modal = document.getElementById('codeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.innerHTML = '<i class="fas fa-file-code"></i> ' + escapeHtml(getFileName(issue.file)) + ':' + issue.line;
            
            // Build modal content
            let content = '<div class="issue-details">';
            
            // Issue info section
            content += '<div class="info-section">';
            content += '<h4><i class="fas fa-info-circle"></i> Issue Information</h4>';
            content += '<table class="info-table">';
            content += '<tr><td><strong>File:</strong></td>';
            content += '<td class="code-text">' + escapeHtml(issue.file) + '</td></tr>';
            content += '<tr><td><strong>Line:</strong></td>';
            content += '<td>' + (issue.line || 'N/A') + '</td></tr>';
            content += '<tr><td><strong>Severity:</strong></td>';
            content += '<td><span class="severity-badge ' + issue.severity + '">' + issue.severity.toUpperCase() + '</span></td></tr>';
            content += '<tr><td><strong>Issue ID:</strong></td>';
            content += '<td><code>' + (issue.id || 'N/A') + '</code></td></tr>';
            content += '</table></div>';
            
            content += '<div class="message-section">';
            content += '<h4><i class="fas fa-comment-alt"></i> Message</h4>';
            content += '<div class="message-box">' + escapeHtml(issue.message || 'No message available') + '</div>';
            content += '</div>';
            
            // Code context section
            content += '<div class="code-section">';
            content += '<h4><i class="fas fa-code"></i> Code Context</h4>';
            
            if (issue.code_context && issue.code_context.lines && issue.code_context.lines.length > 0) {{
                content += '<div class="code-preview"><pre><code class="language-cpp">';
                
                issue.code_context.lines.forEach(line => {{
                    const isTarget = line.is_target;
                    const lineClass = isTarget ? ' class="highlight-line"' : '';
                    const lineNum = String(line.number).padStart(4, ' ');
                    const escapedContent = escapeHtml(line.content);
                    content += '<span' + lineClass + '>' + lineNum + ': ' + escapedContent + '</span>\\n';
                }});
                
                content += '</code></pre></div>';
            }} else {{
                content += '<div class="no-code-message">';
                content += '<i class="fas fa-info-circle"></i>';
                content += '<p>Code context not available for this issue.</p>';
                content += '</div>';
            }}
            content += '</div>';
            
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
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                closeModal();
            }}
        }});
    </script>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Working dashboard generated: {output_file}")
        print(f"   Total issues: {len(self.issues)}")
        print(f"   Issues with code context: {with_context}")
        print(f"   Chunks created: {len(chunks)}")
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
        """

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: generate-working-dashboard.py <analysis.json> [output.html]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'working-dashboard.html'
    
    generator = WorkingDashboardGenerator(input_file)
    generator.generate(output_file)