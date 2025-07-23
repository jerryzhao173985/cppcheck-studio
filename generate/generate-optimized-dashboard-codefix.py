#!/usr/bin/env python3
"""
Optimized Dashboard Generator for CPPCheck Studio - CODE CONTEXT FIX
This version properly handles the code context structure from add-code-context.py
"""

import json
import sys
import os
from collections import defaultdict
from datetime import datetime
import html
import hashlib

class OptimizedDashboardGenerator:
    def __init__(self, issues_file):
        with open(issues_file, 'r') as f:
            data = json.load(f)
            
        # Handle both direct issues array and nested structure
        if isinstance(data, list):
            self.issues = data
        elif isinstance(data, dict) and 'issues' in data:
            self.issues = data['issues']
        else:
            raise ValueError("Invalid JSON structure")
        
        # Generate unique IDs for each issue
        for i, issue in enumerate(self.issues):
            issue['unique_id'] = hashlib.md5(f"{issue.get('file', '')}:{issue.get('line', '')}:{issue.get('id', '')}:{i}".encode()).hexdigest()[:8]
        
        # Group issues by file
        self.files_map = defaultdict(list)
        for issue in self.issues:
            file_path = issue.get('file', 'Unknown')
            self.files_map[file_path].append(issue)
        
        # Sort files by issue count (most issues first)
        self.sorted_files = sorted(self.files_map.items(), key=lambda x: len(x[1]), reverse=True)
        
        # Calculate statistics
        self.calculate_stats()
        
        # Generate fix patterns
        self.fix_patterns = self.generate_fix_patterns()
    
    def calculate_stats(self):
        self.stats = {
            'total': len(self.issues),
            'error': 0,
            'warning': 0,
            'style': 0,
            'performance': 0,
            'information': 0,
            'portability': 0
        }
        
        for issue in self.issues:
            severity = issue.get('severity', 'style')
            if severity in self.stats:
                self.stats[severity] += 1
    
    def generate_fix_patterns(self):
        """Generate quick fix suggestions based on issue patterns"""
        patterns = {
            'missingOverride': {
                'pattern': 'override',
                'suggestion': 'Add override specifier to virtual function',
                'fix_template': 'void functionName() override'
            },
            'passedByValue': {
                'pattern': 'passed by value',
                'suggestion': 'Pass by const reference instead',
                'fix_template': 'const Type& param'
            },
            'uninitMemberVar': {
                'pattern': 'not initialized',
                'suggestion': 'Initialize member in constructor',
                'fix_template': 'ClassName() : member() {}'
            },
            'cstyleCast': {
                'pattern': 'C-style cast',
                'suggestion': 'Use static_cast instead',
                'fix_template': 'static_cast<Type>(value)'
            },
            'useNullptr': {
                'pattern': 'NULL',
                'suggestion': 'Use nullptr instead of NULL',
                'fix_template': 'nullptr'
            },
            'constParameter': {
                'pattern': 'can be declared with const',
                'suggestion': 'Add const qualifier',
                'fix_template': 'const Type param'
            },
            'explicitConstructor': {
                'pattern': 'should be explicit',
                'suggestion': 'Add explicit keyword',
                'fix_template': 'explicit ClassName(param)'
            }
        }
        return patterns
    
    def get_fix_suggestion(self, issue):
        """Get quick fix suggestion for an issue"""
        message = issue.get('message', '').lower()
        for fix_id, pattern in self.fix_patterns.items():
            if pattern['pattern'] in message:
                return {
                    'id': fix_id,
                    'suggestion': pattern['suggestion'],
                    'template': pattern['fix_template']
                }
        return None
    
    def get_inline_code(self, issue):
        """Get 1-2 lines of code context - FIXED to use correct structure"""
        code_context = issue.get('code_context', {})
        if code_context and 'lines' in code_context:
            lines = code_context['lines']
            target_line = issue.get('line', 0)
            
            # Find the target line in the context
            for i, line_info in enumerate(lines):
                # Check both 'number' field and 'is_target' flag
                if line_info.get('number') == target_line or line_info.get('is_target', False):
                    # Get the line and maybe one before/after
                    result = []
                    if i > 0:
                        result.append(lines[i-1])
                    result.append(line_info)
                    if i < len(lines) - 1 and len(result) < 2:
                        result.append(lines[i+1])
                    return result
        return []
    
    def generate(self, output_file):
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Analysis - Optimized Dashboard</title>
    <style>
        :root {{
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #e9ecef;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --border-color: #dee2e6;
            --error-color: #dc3545;
            --warning-color: #ffc107;
            --info-color: #0dcaf0;
            --success-color: #198754;
            --style-color: #6f42c1;
            --hover-bg: #f8f9fa;
            --shadow: 0 1px 3px rgba(0,0,0,0.12);
            --font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', monospace;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background: var(--bg-secondary);
        }}
        
        /* Header */
        .header {{
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: var(--shadow);
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .header h1 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
        }}
        
        /* Stats Bar */
        .stats-bar {{
            display: flex;
            gap: 2rem;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .stat-value {{
            font-size: 1.25rem;
            font-weight: 600;
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}
        
        /* Filters */
        .filters {{
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 73px;
            z-index: 90;
        }}
        
        .filters-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 200px;
            padding: 0.5rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 0.375rem;
            font-size: 0.875rem;
            transition: border-color 0.2s;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: var(--info-color);
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}
        
        .filter-btn {{
            padding: 0.5rem 1rem;
            border: 1px solid var(--border-color);
            background: var(--bg-primary);
            border-radius: 0.375rem;
            cursor: pointer;
            font-size: 0.875rem;
            transition: all 0.2s;
        }}
        
        .filter-btn:hover {{
            background: var(--bg-secondary);
        }}
        
        .filter-btn.active {{
            background: var(--text-primary);
            color: var(--bg-primary);
            border-color: var(--text-primary);
        }}
        
        /* Main Content */
        .main-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            display: flex;
            gap: 2rem;
        }}
        
        /* Sidebar */
        .sidebar {{
            width: 300px;
            flex-shrink: 0;
        }}
        
        .file-list {{
            background: var(--bg-primary);
            border-radius: 0.5rem;
            box-shadow: var(--shadow);
            overflow: hidden;
        }}
        
        .file-item {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: background-color 0.2s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .file-item:hover {{
            background: var(--hover-bg);
        }}
        
        .file-item.active {{
            background: var(--bg-tertiary);
            font-weight: 500;
        }}
        
        .file-name {{
            font-size: 0.875rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .file-count {{
            background: var(--text-secondary);
            color: var(--bg-primary);
            padding: 0.125rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        
        /* Issues Container */
        .issues-container {{
            flex: 1;
            background: var(--bg-primary);
            border-radius: 0.5rem;
            box-shadow: var(--shadow);
            overflow: hidden;
        }}
        
        .issues-header {{
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .issues-title {{
            font-size: 1.125rem;
            font-weight: 600;
        }}
        
        .issues-actions {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .action-btn {{
            padding: 0.375rem 0.75rem;
            border: 1px solid var(--border-color);
            background: var(--bg-primary);
            border-radius: 0.375rem;
            cursor: pointer;
            font-size: 0.75rem;
            transition: all 0.2s;
        }}
        
        .action-btn:hover {{
            background: var(--bg-secondary);
        }}
        
        /* Issue Items */
        .issues-list {{
            max-height: calc(100vh - 300px);
            overflow-y: auto;
        }}
        
        .issue-item {{
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: background-color 0.2s;
            position: relative;
        }}
        
        .issue-item:hover {{
            background: var(--hover-bg);
        }}
        
        .issue-item.viewed {{
            opacity: 0.7;
        }}
        
        .issue-item.fixed {{
            text-decoration: line-through;
            opacity: 0.5;
        }}
        
        .issue-header {{
            display: flex;
            gap: 0.75rem;
            align-items: flex-start;
            margin-bottom: 0.5rem;
        }}
        
        .issue-severity {{
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
        }}
        
        .issue-content {{
            flex: 1;
        }}
        
        .issue-message {{
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
        }}
        
        .issue-location {{
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-family: var(--font-mono);
        }}
        
        .issue-code {{
            background: var(--bg-secondary);
            padding: 0.5rem;
            border-radius: 0.25rem;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            margin-top: 0.5rem;
            overflow-x: auto;
        }}
        
        .code-line {{
            display: flex;
            gap: 1rem;
        }}
        
        .line-number {{
            color: var(--text-secondary);
            user-select: none;
            min-width: 2rem;
            text-align: right;
        }}
        
        .line-content {{
            flex: 1;
            white-space: pre;
        }}
        
        .code-line.highlighted {{
            background: rgba(220, 53, 69, 0.1);
            margin: 0 -0.5rem;
            padding: 0 0.5rem;
        }}
        
        /* Modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            padding: 2rem;
            overflow-y: auto;
        }}
        
        .modal-content {{
            background: var(--bg-primary);
            border-radius: 0.5rem;
            max-width: 800px;
            margin: 0 auto;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }}
        
        .modal-header {{
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .modal-title {{
            font-size: 1.25rem;
            font-weight: 600;
            font-family: var(--font-mono);
        }}
        
        .close-btn {{
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-secondary);
            padding: 0;
            width: 2rem;
            height: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.25rem;
            transition: all 0.2s;
        }}
        
        .close-btn:hover {{
            background: var(--bg-secondary);
            color: var(--text-primary);
        }}
        
        .modal-body {{
            padding: 1.5rem;
        }}
        
        .detail-section {{
            margin-bottom: 1.5rem;
        }}
        
        .detail-section:last-child {{
            margin-bottom: 0;
        }}
        
        .detail-section h4 {{
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 0.75rem;
        }}
        
        .code-context {{
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 0.375rem;
            font-family: var(--font-mono);
            font-size: 0.875rem;
            overflow-x: auto;
        }}
        
        /* Utility Classes */
        .hidden {{
            display: none;
        }}
        
        /* Progress Tracking */
        .progress-bar {{
            position: fixed;
            bottom: 1rem;
            right: 1rem;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1rem;
            box-shadow: var(--shadow);
            min-width: 200px;
        }}
        
        .progress-stats {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            font-size: 0.875rem;
        }}
        
        .progress-item {{
            display: flex;
            justify-content: space-between;
        }}
        
        /* Responsive */
        @media (max-width: 1024px) {{
            .main-content {{
                flex-direction: column;
            }}
            
            .sidebar {{
                width: 100%;
            }}
            
            .file-list {{
                max-height: 200px;
                overflow-y: auto;
            }}
        }}
        
        @media (max-width: 640px) {{
            .header-content {{
                padding: 1rem;
            }}
            
            .filters-content {{
                padding: 1rem;
            }}
            
            .main-content {{
                padding: 1rem;
            }}
            
            .stats-bar {{
                gap: 1rem;
                font-size: 0.875rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <h1>Code Analysis Dashboard</h1>
            <div class="stats-bar">
                <div class="stat-item">
                    <span class="stat-value" style="color: var(--error-color)">{self.stats['error']}</span>
                    <span class="stat-label">Errors</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" style="color: var(--warning-color)">{self.stats['warning']}</span>
                    <span class="stat-label">Warnings</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" style="color: var(--style-color)">{self.stats['style']}</span>
                    <span class="stat-label">Style</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" style="color: var(--success-color)">{self.stats['performance']}</span>
                    <span class="stat-label">Performance</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{self.stats['total']}</span>
                    <span class="stat-label">Total</span>
                </div>
            </div>
        </div>
    </header>
    
    <div class="filters">
        <div class="filters-content">
            <input type="text" class="search-box" placeholder="Search issues..." id="searchBox">
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="error">Errors</button>
                <button class="filter-btn" data-filter="warning">Warnings</button>
                <button class="filter-btn" data-filter="style">Style</button>
                <button class="filter-btn" data-filter="performance">Performance</button>
            </div>
            <div class="filter-buttons">
                <button class="action-btn" onclick="exportIssues()">Export</button>
                <button class="action-btn" onclick="clearProgress()">Clear Progress</button>
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <aside class="sidebar">
            <div class="file-list" id="fileList">
"""
        
        # Add file list
        for file_path, issues in self.sorted_files:
            display_name = os.path.basename(file_path) if len(file_path) > 30 else file_path
            html_content += f"""
                <div class="file-item" data-file="{html.escape(file_path)}">
                    <span class="file-name" title="{html.escape(file_path)}">{html.escape(display_name)}</span>
                    <span class="file-count">{len(issues)}</span>
                </div>
"""
        
        html_content += """
            </div>
        </aside>
        
        <main class="issues-container">
            <div class="issues-header">
                <h2 class="issues-title">Issues</h2>
                <div class="issues-actions">
                    <span id="issueCount"></span>
                </div>
            </div>
            <div class="issues-list" id="issuesList">
                <!-- Issues will be rendered here -->
            </div>
        </main>
    </div>
    
    <!-- Code Detail Modal -->
    <div class="modal" id="codeModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title" id="modalTitle">Issue Details</h3>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Content will be inserted here -->
            </div>
        </div>
    </div>
    
    <!-- Progress Bar -->
    <div class="progress-bar">
        <div class="progress-stats">
            <div class="progress-item">
                <span>Viewed:</span>
                <span id="viewedCount">0</span>
            </div>
            <div class="progress-item">
                <span>Fixed:</span>
                <span id="fixedCount">0</span>
            </div>
            <div class="progress-item">
                <span>Remaining:</span>
                <span id="remainingCount">{self.stats['total']}</span>
            </div>
        </div>
    </div>
    
    <script>
        // Issues data embedded directly - FIXED to handle code_context properly
        const issuesData = {json.dumps(self.issues, indent=2)};
        
        // Group issues by file
        const fileGroups = {{}};
        issuesData.forEach(issue => {{
            const file = issue.file || 'Unknown';
            if (!fileGroups[file]) fileGroups[file] = [];
            fileGroups[file].push(issue);
        }});
        
        // State management
        let currentFile = null;
        let currentFilter = 'all';
        let searchTerm = '';
        let viewedIssues = new Set(JSON.parse(localStorage.getItem('viewedIssues') || '[]'));
        let fixedIssues = new Set(JSON.parse(localStorage.getItem('fixedIssues') || '[]'));
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            setupEventListeners();
            selectFirstFile();
            updateProgress();
        }});
        
        function setupEventListeners() {{
            // Search
            document.getElementById('searchBox').addEventListener('input', (e) => {{
                searchTerm = e.target.value.toLowerCase();
                renderIssues();
            }});
            
            // Filter buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentFilter = btn.dataset.filter;
                    renderIssues();
                }});
            }});
            
            // File selection
            document.querySelectorAll('.file-item').forEach(item => {{
                item.addEventListener('click', () => {{
                    document.querySelectorAll('.file-item').forEach(i => i.classList.remove('active'));
                    item.classList.add('active');
                    currentFile = item.dataset.file;
                    renderIssues();
                }});
            }});
            
            // Modal close on click outside
            document.getElementById('codeModal').addEventListener('click', (e) => {{
                if (e.target.id === 'codeModal') {{
                    closeModal();
                }}
            }});
        }}
        
        function selectFirstFile() {{
            const firstFile = document.querySelector('.file-item');
            if (firstFile) {{
                firstFile.click();
            }}
        }}
        
        function renderIssues() {{
            const container = document.getElementById('issuesList');
            container.innerHTML = '';
            
            if (!currentFile || !fileGroups[currentFile]) return;
            
            let issues = fileGroups[currentFile];
            
            // Apply filters
            if (currentFilter !== 'all') {{
                issues = issues.filter(issue => issue.severity === currentFilter);
            }}
            
            if (searchTerm) {{
                issues = issues.filter(issue => 
                    issue.message.toLowerCase().includes(searchTerm) ||
                    issue.id.toLowerCase().includes(searchTerm)
                );
            }}
            
            // Update count
            document.getElementById('issueCount').textContent = `${{issues.length}} issue${{issues.length !== 1 ? 's' : ''}}`;
            
            // Render issues
            issues.forEach(issue => {{
                const issueEl = createIssueElement(issue);
                container.appendChild(issueEl);
            }});
        }}
        
        function createIssueElement(issue) {{
            const item = document.createElement('div');
            item.className = 'issue-item';
            
            if (viewedIssues.has(issue.unique_id)) {{
                item.classList.add('viewed');
            }}
            
            if (fixedIssues.has(issue.unique_id)) {{
                item.classList.add('fixed');
            }}
            
            // Click on row shows details modal
            item.onclick = (e) => {{
                if (!e.target.classList.contains('action-btn')) {{
                    showIssueDetails(issue);
                }}
            }};
            
            // Header with severity
            const header = document.createElement('div');
            header.className = 'issue-header';
            
            const severity = document.createElement('div');
            severity.className = `issue-severity ${{issue.severity || 'style'}}`;
            severity.textContent = issue.severity || 'style';
            severity.style.background = getSeverityColor(issue.severity);
            severity.style.color = 'white';
            
            const content = document.createElement('div');
            content.className = 'issue-content';
            
            const message = document.createElement('div');
            message.className = 'issue-message';
            message.textContent = issue.message || 'No message';
            
            const location = document.createElement('div');
            location.className = 'issue-location';
            location.textContent = `Line ${{issue.line || '?'}}${{issue.column ? ', Column ' + issue.column : ''}} • ${{issue.id || 'unknown'}}`;
            
            // Inline code preview (1-2 lines) - FIXED to use correct structure
            const codeLines = getInlineCode(issue);
            if (codeLines.length > 0) {{
                const codePreview = document.createElement('div');
                codePreview.className = 'issue-code';
                
                codeLines.forEach(line => {{
                    const codeLine = document.createElement('div');
                    codeLine.className = 'code-line';
                    if (line.is_target || line.number === issue.line) {{
                        codeLine.classList.add('highlighted');
                    }}
                    
                    const lineNum = document.createElement('span');
                    lineNum.className = 'line-number';
                    lineNum.textContent = line.number;
                    
                    const lineContent = document.createElement('span');
                    lineContent.className = 'line-content';
                    lineContent.textContent = line.content;
                    
                    codeLine.appendChild(lineNum);
                    codeLine.appendChild(lineContent);
                    codePreview.appendChild(codeLine);
                }});
                
                content.appendChild(codePreview);
            }}
            
            // Actions
            const actions = document.createElement('div');
            actions.style.cssText = 'display: flex; gap: 0.5rem; margin-top: 0.5rem;';
            
            const fixBtn = document.createElement('button');
            fixBtn.className = 'action-btn';
            fixBtn.textContent = fixedIssues.has(issue.unique_id) ? 'Unmark Fixed' : 'Mark Fixed';
            fixBtn.onclick = (e) => {{
                e.stopPropagation();
                toggleFixed(issue);
            }};
            
            actions.appendChild(fixBtn);
            
            content.appendChild(message);
            content.appendChild(location);
            content.appendChild(actions);
            
            header.appendChild(severity);
            header.appendChild(content);
            
            item.appendChild(header);
            
            return item;
        }}
        
        // FIXED: Use correct code_context structure
        function getInlineCode(issue) {{
            if (!issue.code_context || !issue.code_context.lines) return [];
            
            const lines = issue.code_context.lines;
            const targetLine = issue.line;
            
            // Find the target line
            for (let i = 0; i < lines.length; i++) {{
                if (lines[i].number === targetLine || lines[i].is_target) {{
                    const result = [];
                    if (i > 0) result.push(lines[i-1]);
                    result.push(lines[i]);
                    if (i < lines.length - 1 && result.length < 2) {{
                        result.push(lines[i+1]);
                    }}
                    return result;
                }}
            }}
            
            return lines.slice(0, 2);
        }}
        
        // Modal functions - FIXED to use correct code_context structure
        function showIssueDetails(issue) {{
            const modal = document.getElementById('codeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.textContent = `${{issue.file || 'Unknown'}}:${{issue.line || '?'}}`;
            
            let content = `
                <div class="issue-details">
                    <div class="detail-section">
                        <h4>Issue Information</h4>
                        <p><strong>Message:</strong> ${{escapeHtml(issue.message || 'No message')}}</p>
                        <p><strong>Severity:</strong> <span class="issue-severity ${{issue.severity || 'style'}}" style="background: ${{getSeverityColor(issue.severity)}}; color: white;">${{issue.severity || 'style'}}</span></p>
                        <p><strong>ID:</strong> ${{issue.id || 'unknown'}}</p>
                        <p><strong>Location:</strong> Line ${{issue.line || '?'}}, Column ${{issue.column || '?'}}</p>
                    </div>
            `;
            
            // Add code context if available - FIXED to use correct structure
            if (issue.code_context && issue.code_context.lines) {{
                content += `
                    <div class="detail-section">
                        <h4>Code Context</h4>
                        <div class="code-context">
                `;
                
                issue.code_context.lines.forEach(line => {{
                    const isHighlighted = line.is_target || line.number == issue.line;
                    content += `
                        <div class="code-line ${{isHighlighted ? 'highlighted' : ''}}">
                            <span class="line-number">${{line.number}}</span>
                            <span class="line-content">${{escapeHtml(line.content)}}</span>
                        </div>
                    `;
                }});
                
                content += `
                        </div>
                    </div>
                `;
            }}
            
            // Add quick fix if available
            const fix = getFixSuggestion(issue);
            if (fix) {{
                content += `
                    <div class="detail-section">
                        <h4>Quick Fix Suggestion</h4>
                        <p>${{fix.suggestion}}</p>
                        <code class="issue-code">${{escapeHtml(fix.template)}}</code>
                    </div>
                `;
            }}
            
            content += '</div>';
            
            modalBody.innerHTML = content;
            modal.style.display = 'block';
            
            // Mark as viewed
            markAsViewed(issue);
        }}
        
        function closeModal() {{
            document.getElementById('codeModal').style.display = 'none';
        }}
        
        function getSeverityColor(severity) {{
            const colors = {{
                'error': 'var(--error-color)',
                'warning': 'var(--warning-color)',
                'style': 'var(--style-color)',
                'performance': 'var(--success-color)',
                'information': 'var(--info-color)',
                'portability': 'var(--text-secondary)'
            }};
            return colors[severity] || 'var(--text-secondary)';
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        function getFixSuggestion(issue) {{
            const patterns = {json.dumps(self.fix_patterns, indent=12)};
            
            const message = (issue.message || '').toLowerCase();
            for (const [fixId, pattern] of Object.entries(patterns)) {{
                if (message.includes(pattern.pattern)) {{
                    return {{
                        id: fixId,
                        suggestion: pattern.suggestion,
                        template: pattern.fix_template
                    }};
                }}
            }}
            return null;
        }}
        
        // Progress tracking
        function markAsViewed(issue) {{
            viewedIssues.add(issue.unique_id);
            localStorage.setItem('viewedIssues', JSON.stringify([...viewedIssues]));
            updateProgress();
            
            // Update UI
            document.querySelectorAll('.issue-item').forEach(el => {{
                if (el.textContent.includes(issue.message)) {{
                    el.classList.add('viewed');
                }}
            }});
        }}
        
        function toggleFixed(issue) {{
            if (fixedIssues.has(issue.unique_id)) {{
                fixedIssues.delete(issue.unique_id);
            }} else {{
                fixedIssues.add(issue.unique_id);
            }}
            localStorage.setItem('fixedIssues', JSON.stringify([...fixedIssues]));
            updateProgress();
            renderIssues();
        }}
        
        function updateProgress() {{
            const total = issuesData.length;
            const viewed = viewedIssues.size;
            const fixed = fixedIssues.size;
            const remaining = total - fixed;
            
            document.getElementById('viewedCount').textContent = viewed;
            document.getElementById('fixedCount').textContent = fixed;
            document.getElementById('remainingCount').textContent = remaining;
        }}
        
        function clearProgress() {{
            if (confirm('Clear all progress? This cannot be undone.')) {{
                viewedIssues.clear();
                fixedIssues.clear();
                localStorage.removeItem('viewedIssues');
                localStorage.removeItem('fixedIssues');
                updateProgress();
                renderIssues();
            }}
        }}
        
        function exportIssues() {{
            const remaining = issuesData.filter(issue => !fixedIssues.has(issue.unique_id));
            const blob = new Blob([JSON.stringify(remaining, null, 2)], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'remaining-issues.json';
            a.click();
            URL.revokeObjectURL(url);
        }}
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                closeModal();
            }} else if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {{
                e.preventDefault();
                document.getElementById('searchBox').focus();
            }}
        }});
    </script>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate-optimized-dashboard-codefix.py <issues.json> <output.html>")
        sys.exit(1)
    
    issues_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(issues_file):
        print(f"Error: Input file '{issues_file}' not found")
        sys.exit(1)
    
    generator = OptimizedDashboardGenerator(issues_file)
    generator.generate(output_file)
    print(f"Dashboard generated successfully: {output_file}")

if __name__ == "__main__":
    main()