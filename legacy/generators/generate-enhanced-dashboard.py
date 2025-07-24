#!/usr/bin/env python3
"""
Enhanced Dashboard Generator - Beautiful, modern UI with animations
Direct JavaScript arrays for reliability + stunning visuals for engagement


⚠️ DEPRECATION WARNING: This generator is deprecated and will be removed in April 2025.
Please use generate-standalone-virtual-dashboard.py instead.

See generate/DEPRECATION_NOTICE.md for migration guide.
"""

import sys
import warnings

# Show deprecation warning
warnings.warn(
    "\n⚠️  DEPRECATION: generate-enhanced-dashboard.py is deprecated.\n"
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
import math

class EnhancedDashboardGenerator:
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
        """Generate enhanced dashboard with beautiful UI and animations"""
        
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
    <title>Code Analysis Dashboard - {len(self.issues)} Issues Found</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        {self.generate_enhanced_styles()}
    </style>
</head>
<body>
    <!-- Loading Screen -->
    <div class="loading-screen" id="loadingScreen">
        <div class="loader">
            <div class="loader-inner"></div>
        </div>
        <p class="loading-text">Initializing Dashboard...</p>
    </div>
    
    <!-- Main Container -->
    <div class="container" id="mainContainer">
        <!-- Enhanced Header -->
        <header class="header">
            <div class="header-background">
                <div class="animated-bg"></div>
            </div>
            <div class="header-content">
                <div class="header-left">
                    <div class="logo-container">
                        <div class="logo-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <div class="logo-text">
                            <h1>Code Analysis Dashboard</h1>
                            <p class="subtitle">Comprehensive Static Analysis Report</p>
                        </div>
                    </div>
                </div>
                <div class="header-right">
                    <div class="header-stat">
                        <i class="fas fa-clock"></i>
                        <div>
                            <span class="label">Generated</span>
                            <span class="value">{self.timestamp}</span>
                        </div>
                    </div>
                    <div class="header-stat">
                        <i class="fas fa-bug"></i>
                        <div>
                            <span class="label">Total Issues</span>
                            <span class="value">{len(self.issues)}</span>
                        </div>
                    </div>
                    <div class="header-stat">
                        <i class="fas fa-chart-line"></i>
                        <div>
                            <span class="label">Health Score</span>
                            <span class="value">{self.calculate_health_score(stats)}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>
        
        <!-- Quick Actions Bar -->
        <div class="quick-actions">
            <button class="action-btn" onclick="exportData()">
                <i class="fas fa-download"></i> Export Report
            </button>
            <button class="action-btn" onclick="toggleDarkMode()">
                <i class="fas fa-moon"></i> Dark Mode
            </button>
            <button class="action-btn" onclick="showKeyboardShortcuts()">
                <i class="fas fa-keyboard"></i> Shortcuts
            </button>
        </div>
        
        <!-- Statistics Dashboard -->
        <div class="stats-section">
            <h2 class="section-title">
                <i class="fas fa-chart-pie"></i> Analysis Overview
                <span class="section-subtitle">Click on cards to filter by severity</span>
            </h2>
            
            <div class="stats-grid">
                <div class="stat-card error" onclick="setSeverityFilter('error', this)" data-aos="fade-up">
                    <div class="stat-icon-container">
                        <div class="stat-icon-bg"></div>
                        <i class="fas fa-times-circle"></i>
                    </div>
                    <div class="stat-content">
                        <h3>Critical Errors</h3>
                        <div class="stat-value">
                            <span class="number" data-value="{stats['errors']}">{stats['errors']}</span>
                            <span class="change">{self.get_trend_icon(stats['errors'])}</span>
                        </div>
                        <div class="stat-bar">
                            <div class="stat-bar-fill" style="width: {stats['error_percent']}%"></div>
                        </div>
                        <div class="stat-percent">{stats['error_percent']:.1f}% of total</div>
                    </div>
                </div>
                
                <div class="stat-card warning" onclick="setSeverityFilter('warning', this)" data-aos="fade-up" data-aos-delay="100">
                    <div class="stat-icon-container">
                        <div class="stat-icon-bg"></div>
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div class="stat-content">
                        <h3>Warnings</h3>
                        <div class="stat-value">
                            <span class="number" data-value="{stats['warnings']}">{stats['warnings']}</span>
                            <span class="change">{self.get_trend_icon(stats['warnings'])}</span>
                        </div>
                        <div class="stat-bar">
                            <div class="stat-bar-fill" style="width: {stats['warning_percent']}%"></div>
                        </div>
                        <div class="stat-percent">{stats['warning_percent']:.1f}% of total</div>
                    </div>
                </div>
                
                <div class="stat-card style" onclick="setSeverityFilter('style', this)" data-aos="fade-up" data-aos-delay="200">
                    <div class="stat-icon-container">
                        <div class="stat-icon-bg"></div>
                        <i class="fas fa-palette"></i>
                    </div>
                    <div class="stat-content">
                        <h3>Style Issues</h3>
                        <div class="stat-value">
                            <span class="number" data-value="{stats['style']}">{stats['style']}</span>
                            <span class="change">{self.get_trend_icon(stats['style'])}</span>
                        </div>
                        <div class="stat-bar">
                            <div class="stat-bar-fill" style="width: {stats['style_percent']}%"></div>
                        </div>
                        <div class="stat-percent">{stats['style_percent']:.1f}% of total</div>
                    </div>
                </div>
                
                <div class="stat-card performance" onclick="setSeverityFilter('performance', this)" data-aos="fade-up" data-aos-delay="300">
                    <div class="stat-icon-container">
                        <div class="stat-icon-bg"></div>
                        <i class="fas fa-tachometer-alt"></i>
                    </div>
                    <div class="stat-content">
                        <h3>Performance</h3>
                        <div class="stat-value">
                            <span class="number" data-value="{stats['performance']}">{stats['performance']}</span>
                            <span class="change">{self.get_trend_icon(stats['performance'])}</span>
                        </div>
                        <div class="stat-bar">
                            <div class="stat-bar-fill" style="width: {stats['performance_percent']}%"></div>
                        </div>
                        <div class="stat-percent">{stats['performance_percent']:.1f}% of total</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Enhanced Controls -->
        <div class="controls-section">
            <div class="search-container">
                <i class="fas fa-search search-icon"></i>
                <input type="text" id="searchInput" class="search-input" 
                       placeholder="Search by file, message, or ID..." 
                       onkeyup="handleSearch(event)">
                <div class="search-shortcuts">
                    <span class="shortcut-hint">Press <kbd>/</kbd> to search</span>
                </div>
            </div>
            
            <div class="filter-group">
                <button class="filter-btn active" onclick="setSeverityFilter('all', this)">
                    <i class="fas fa-list"></i> All Issues
                    <span class="badge">{len(self.issues)}</span>
                </button>
                <button class="filter-btn error" onclick="setSeverityFilter('error', this)">
                    <i class="fas fa-times-circle"></i> Errors
                    <span class="badge">{stats['errors']}</span>
                </button>
                <button class="filter-btn warning" onclick="setSeverityFilter('warning', this)">
                    <i class="fas fa-exclamation-triangle"></i> Warnings
                    <span class="badge">{stats['warnings']}</span>
                </button>
                <button class="filter-btn style" onclick="setSeverityFilter('style', this)">
                    <i class="fas fa-palette"></i> Style
                    <span class="badge">{stats['style']}</span>
                </button>
                <button class="filter-btn performance" onclick="setSeverityFilter('performance', this)">
                    <i class="fas fa-tachometer-alt"></i> Performance
                    <span class="badge">{stats['performance']}</span>
                </button>
            </div>
            
            <div class="view-controls">
                <button class="view-btn active" onclick="setViewMode('table', this)" title="Table View">
                    <i class="fas fa-table"></i>
                </button>
                <button class="view-btn" onclick="setViewMode('cards', this)" title="Card View">
                    <i class="fas fa-th"></i>
                </button>
                <button class="view-btn" onclick="setViewMode('compact', this)" title="Compact View">
                    <i class="fas fa-list"></i>
                </button>
            </div>
        </div>
        
        <!-- Status Bar -->
        <div class="status-bar">
            <div class="status-left">
                <i class="fas fa-filter"></i>
                <span id="issuesCount">Showing all {len(self.issues)} issues</span>
            </div>
            <div class="status-right">
                <button class="sort-btn" onclick="showSortMenu(this)">
                    <i class="fas fa-sort"></i> Sort by Severity
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>
        </div>
        
        <!-- Issues Table -->
        <div class="table-container" id="tableView">
            <table class="issues-table">
                <thead>
                    <tr>
                        <th width="40">
                            <input type="checkbox" class="checkbox" id="selectAll" onchange="toggleSelectAll()">
                        </th>
                        <th onclick="sortBy('file')">
                            File <i class="fas fa-sort sort-icon"></i>
                        </th>
                        <th width="80" onclick="sortBy('line')">
                            Line <i class="fas fa-sort sort-icon"></i>
                        </th>
                        <th width="120" onclick="sortBy('severity')">
                            Severity <i class="fas fa-sort sort-icon"></i>
                        </th>
                        <th onclick="sortBy('message')">
                            Message <i class="fas fa-sort sort-icon"></i>
                        </th>
                        <th width="100">ID</th>
                        <th width="100">Actions</th>
                    </tr>
                </thead>
                <tbody id="issuesBody">
                    <!-- Rows will be rendered here -->
                </tbody>
            </table>
        </div>
        
        <!-- Card View Container -->
        <div class="cards-container" id="cardsView" style="display: none;">
            <!-- Cards will be rendered here -->
        </div>
        
        <!-- Compact View Container -->
        <div class="compact-container" id="compactView" style="display: none;">
            <!-- Compact items will be rendered here -->
        </div>
        
        <!-- Pagination -->
        <div class="pagination" id="pagination">
            <!-- Pagination will be rendered here -->
        </div>
        
        <!-- Enhanced Code Preview Modal -->
        <div id="codeModal" class="modal">
            <div class="modal-overlay" onclick="closeModal()"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title">
                        <i class="fas fa-code"></i>
                        <h3 id="modalTitle">Issue Details</h3>
                    </div>
                    <div class="modal-actions">
                        <button class="modal-action-btn" onclick="copyIssueLink()" title="Copy Link">
                            <i class="fas fa-link"></i>
                        </button>
                        <button class="modal-action-btn" onclick="copyCodeSnippet()" title="Copy Code">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="modal-action-btn" onclick="closeModal()" title="Close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div class="modal-body" id="modalBody">
                    <!-- Content will be inserted here -->
                </div>
            </div>
        </div>
        
        <!-- Keyboard Shortcuts Modal -->
        <div id="shortcutsModal" class="modal">
            <div class="modal-overlay" onclick="closeShortcutsModal()"></div>
            <div class="modal-content shortcuts-modal">
                <div class="modal-header">
                    <h3><i class="fas fa-keyboard"></i> Keyboard Shortcuts</h3>
                    <button class="modal-action-btn" onclick="closeShortcutsModal()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="shortcuts-grid">
                    <div class="shortcut-item">
                        <kbd>/</kbd>
                        <span>Focus search</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>Esc</kbd>
                        <span>Clear search / Close modal</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>1-4</kbd>
                        <span>Filter by severity</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>v</kbd>
                        <span>Change view mode</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>d</kbd>
                        <span>Toggle dark mode</span>
                    </div>
                    <div class="shortcut-item">
                        <kbd>e</kbd>
                        <span>Export data</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Toast Notifications -->
        <div class="toast-container" id="toastContainer"></div>
    </div>
    
    <script>
        // Embed data directly as JavaScript
        const allIssues = {issues_js};
        
        const codeContextMap = {code_context_js};
        
        // Global state
        let state = {{
            filteredIssues: [...allIssues],
            currentFilter: 'all',
            currentSort: 'severity',
            currentSortOrder: 'desc',
            currentView: 'table',
            currentPage: 1,
            itemsPerPage: 50,
            selectedIssues: new Set(),
            darkMode: localStorage.getItem('darkMode') === 'true'
        }};
        
        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {{
            // Simulate loading for smooth transition
            setTimeout(() => {{
                document.getElementById('loadingScreen').style.opacity = '0';
                setTimeout(() => {{
                    document.getElementById('loadingScreen').style.display = 'none';
                }}, 300);
            }}, 500);
            
            // Initialize dark mode
            if (state.darkMode) {{
                document.body.classList.add('dark-mode');
            }}
            
            // Initialize tooltips
            initializeTooltips();
            
            // Initialize keyboard shortcuts
            initializeKeyboardShortcuts();
            
            // Animate stat numbers
            animateNumbers();
            
            // Render initial view
            renderIssues();
            
            console.log('✨ Enhanced dashboard loaded with', allIssues.length, 'issues');
        }});
        
        // Core rendering functions
        function renderIssues() {{
            const start = (state.currentPage - 1) * state.itemsPerPage;
            const end = start + state.itemsPerPage;
            const pageIssues = state.filteredIssues.slice(start, end);
            
            if (state.currentView === 'table') {{
                renderTableView(pageIssues);
            }} else if (state.currentView === 'cards') {{
                renderCardsView(pageIssues);
            }} else {{
                renderCompactView(pageIssues);
            }}
            
            renderPagination();
            updateIssueCount();
        }}
        
        function renderTableView(issues) {{
            const tbody = document.getElementById('issuesBody');
            tbody.innerHTML = '';
            
            issues.forEach((issue, index) => {{
                const row = createTableRow(issue, index);
                tbody.appendChild(row);
                
                // Animate row appearance
                setTimeout(() => {{
                    row.classList.add('visible');
                }}, index * 20);
            }});
        }}
        
        function createTableRow(issue, index) {{
            const row = document.createElement('tr');
            row.className = 'issue-row';
            row.dataset.issueId = issue.id;
            
            const hasCodeContext = codeContextMap.hasOwnProperty(issue.id);
            
            row.innerHTML = `
                <td class="checkbox-cell">
                    <input type="checkbox" class="checkbox" onchange="toggleIssueSelection('${{issue.id}}')">
                </td>
                <td class="file-cell">
                    <div class="file-info">
                        <i class="fas fa-file-code file-icon"></i>
                        <span class="file-name" title="${{escapeHtml(issue.file || '')}}">
                            ${{escapeHtml(getFileName(issue.file || ''))}}
                        </span>
                        ${{hasCodeContext ? '<span class="code-indicator" title="Code context available">•</span>' : ''}}
                    </div>
                </td>
                <td class="line-cell">
                    <span class="line-number">${{issue.line || '-'}}</span>
                </td>
                <td class="severity-cell">
                    <span class="severity-badge ${{issue.severity || 'unknown'}}" data-severity="${{issue.severity}}">
                        <span class="severity-icon">${{getSeverityIcon(issue.severity)}}</span>
                        ${{(issue.severity || 'UNKNOWN').toUpperCase()}}
                    </span>
                </td>
                <td class="message-cell">
                    <span class="message-text" title="${{escapeHtml(issue.message || '')}}">
                        ${{escapeHtml(truncateMessage(issue.message || 'No message', 80))}}
                    </span>
                </td>
                <td class="id-cell">
                    <code class="issue-id">${{issue.id || 'N/A'}}</code>
                </td>
                <td class="actions-cell">
                    <button class="action-btn primary" onclick="showIssueDetails('${{issue.id}}', event)" 
                            title="${{hasCodeContext ? 'View code context' : 'View details'}}">
                        <i class="fas ${{hasCodeContext ? 'fa-code' : 'fa-eye'}}"></i>
                    </button>
                    <button class="action-btn" onclick="copyIssueInfo('${{issue.id}}')" title="Copy issue info">
                        <i class="fas fa-copy"></i>
                    </button>
                </td>
            `;
            
            return row;
        }}
        
        function renderCardsView(issues) {{
            const container = document.getElementById('cardsView');
            container.innerHTML = '';
            
            issues.forEach((issue, index) => {{
                const card = createIssueCard(issue);
                container.appendChild(card);
                
                // Animate card appearance
                setTimeout(() => {{
                    card.classList.add('visible');
                }}, index * 30);
            }});
        }}
        
        function createIssueCard(issue) {{
            const card = document.createElement('div');
            card.className = `issue-card ${{issue.severity}}`;
            card.dataset.issueId = issue.id;
            
            const hasCodeContext = codeContextMap.hasOwnProperty(issue.id);
            
            card.innerHTML = `
                <div class="card-header">
                    <span class="severity-badge ${{issue.severity}}">
                        ${{getSeverityIcon(issue.severity)}} ${{(issue.severity || 'UNKNOWN').toUpperCase()}}
                    </span>
                    <code class="issue-id">#${{issue.id}}</code>
                </div>
                <div class="card-body">
                    <div class="file-info">
                        <i class="fas fa-file-code"></i>
                        <span class="file-path">${{escapeHtml(issue.file || 'Unknown')}}</span>
                        <span class="line-info">Line ${{issue.line || '?'}}</span>
                    </div>
                    <p class="message">${{escapeHtml(issue.message || 'No message')}}</p>
                </div>
                <div class="card-footer">
                    <button class="action-btn primary" onclick="showIssueDetails('${{issue.id}}', event)">
                        <i class="fas ${{hasCodeContext ? 'fa-code' : 'fa-eye'}}"></i>
                        ${{hasCodeContext ? 'View Code' : 'View Details'}}
                    </button>
                    <button class="action-btn" onclick="copyIssueInfo('${{issue.id}}')">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
            `;
            
            card.onclick = (e) => {{
                if (!e.target.closest('button')) {{
                    showIssueDetails(issue.id, e);
                }}
            }};
            
            return card;
        }}
        
        // Search and filtering
        function handleSearch(event) {{
            const searchTerm = event.target.value.toLowerCase();
            
            state.filteredIssues = allIssues.filter(issue => {{
                // Apply severity filter first
                if (state.currentFilter !== 'all' && issue.severity !== state.currentFilter) {{
                    return false;
                }}
                
                // Apply search filter
                if (searchTerm) {{
                    const matchFile = (issue.file || '').toLowerCase().includes(searchTerm);
                    const matchMessage = (issue.message || '').toLowerCase().includes(searchTerm);
                    const matchId = (issue.id || '').toLowerCase().includes(searchTerm);
                    return matchFile || matchMessage || matchId;
                }}
                
                return true;
            }});
            
            // Reset to first page
            state.currentPage = 1;
            
            // Apply current sort
            sortIssues();
            renderIssues();
        }}
        
        function setSeverityFilter(severity, button) {{
            state.currentFilter = severity;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            if (button) {{
                button.classList.add('active');
            }}
            
            // Update stat card states
            document.querySelectorAll('.stat-card').forEach(card => {{
                card.classList.remove('active');
                if (card.classList.contains(severity) || severity === 'all') {{
                    card.classList.add('highlight');
                }} else {{
                    card.classList.remove('highlight');
                }}
            }});
            
            // Reapply search
            const searchInput = document.getElementById('searchInput');
            const event = {{ target: searchInput }};
            handleSearch(event);
            
            // Show notification
            showToast(`Filtering by: ${{severity === 'all' ? 'All issues' : severity}}`, 'info');
        }}
        
        // Sorting
        function sortBy(field) {{
            if (state.currentSort === field) {{
                state.currentSortOrder = state.currentSortOrder === 'asc' ? 'desc' : 'asc';
            }} else {{
                state.currentSort = field;
                state.currentSortOrder = 'asc';
            }}
            
            sortIssues();
            renderIssues();
        }}
        
        function sortIssues() {{
            const severityOrder = {{ 'error': 0, 'warning': 1, 'style': 2, 'performance': 3, 'information': 4 }};
            
            state.filteredIssues.sort((a, b) => {{
                let compareValue = 0;
                
                switch (state.currentSort) {{
                    case 'severity':
                        const aOrder = severityOrder[a.severity] ?? 5;
                        const bOrder = severityOrder[b.severity] ?? 5;
                        compareValue = aOrder - bOrder;
                        break;
                    case 'file':
                        compareValue = (a.file || '').localeCompare(b.file || '');
                        break;
                    case 'line':
                        compareValue = (a.line || 0) - (b.line || 0);
                        break;
                    case 'message':
                        compareValue = (a.message || '').localeCompare(b.message || '');
                        break;
                }}
                
                return state.currentSortOrder === 'asc' ? compareValue : -compareValue;
            }});
        }}
        
        // View modes
        function setViewMode(mode, button) {{
            state.currentView = mode;
            
            // Update button states
            document.querySelectorAll('.view-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            button.classList.add('active');
            
            // Hide all views
            document.getElementById('tableView').style.display = 'none';
            document.getElementById('cardsView').style.display = 'none';
            document.getElementById('compactView').style.display = 'none';
            
            // Show selected view
            const viewId = mode + 'View';
            document.getElementById(viewId).style.display = mode === 'cards' ? 'grid' : 'block';
            
            renderIssues();
            showToast(`Switched to ${{mode}} view`, 'info');
        }}
        
        // Modal functions
        function showIssueDetails(issueId, event) {{
            event.stopPropagation();
            
            const issue = allIssues.find(i => i.id === issueId);
            if (!issue) return;
            
            const modal = document.getElementById('codeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.innerHTML = `
                <i class="fas fa-file-code"></i> ${{escapeHtml(getFileName(issue.file || 'Unknown'))}}:${{issue.line || '?'}}
            `;
            
            const codeContext = codeContextMap[issue.id];
            
            let content = `
                <div class="issue-details">
                    <div class="detail-section">
                        <h4><i class="fas fa-info-circle"></i> Issue Information</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <span class="detail-label">File</span>
                                <span class="detail-value">
                                    <code>${{escapeHtml(issue.file || 'Unknown')}}</code>
                                </span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">Line</span>
                                <span class="detail-value">${{issue.line || 'N/A'}}</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">Severity</span>
                                <span class="detail-value">
                                    <span class="severity-badge ${{issue.severity}}">
                                        ${{getSeverityIcon(issue.severity)}} ${{(issue.severity || 'UNKNOWN').toUpperCase()}}
                                    </span>
                                </span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">ID</span>
                                <span class="detail-value">
                                    <code>#${{issue.id || 'N/A'}}</code>
                                </span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="detail-section">
                        <h4><i class="fas fa-comment-dots"></i> Description</h4>
                        <div class="message-box">
                            ${{escapeHtml(issue.message || 'No message')}}
                        </div>
                    </div>
            `;
            
            if (codeContext && codeContext.lines) {{
                content += `
                    <div class="detail-section">
                        <h4><i class="fas fa-code"></i> Code Context</h4>
                        <div class="code-container">
                            <pre class="code-preview"><code>`;
                
                codeContext.lines.forEach(line => {{
                    const lineNum = String(line.number || 0).padStart(4, ' ');
                    const lineContent = escapeHtml(line.content || '');
                    if (line.is_target) {{
                        content += `<span class="highlight-line"><span class="line-number">${{lineNum}}</span>${{lineContent}}</span>\\n`;
                    }} else {{
                        content += `<span class="line-number">${{lineNum}}</span>${{lineContent}}\\n`;
                    }}
                }});
                
                content += `</code></pre>
                        </div>
                    </div>`;
            }}
            
            content += '</div>';
            
            modalBody.innerHTML = content;
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
            
            // Store current issue for actions
            modal.dataset.currentIssueId = issueId;
        }}
        
        function closeModal() {{
            const modal = document.getElementById('codeModal');
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }}
        
        // Utility functions
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
        
        function truncateMessage(message, maxLength) {{
            if (message.length <= maxLength) return message;
            return message.substring(0, maxLength) + '...';
        }}
        
        function getSeverityIcon(severity) {{
            const icons = {{
                'error': '<i class="fas fa-times-circle"></i>',
                'warning': '<i class="fas fa-exclamation-triangle"></i>',
                'style': '<i class="fas fa-palette"></i>',
                'performance': '<i class="fas fa-tachometer-alt"></i>',
                'information': '<i class="fas fa-info-circle"></i>'
            }};
            return icons[severity] || '<i class="fas fa-question-circle"></i>';
        }}
        
        // Pagination
        function renderPagination() {{
            const totalPages = Math.ceil(state.filteredIssues.length / state.itemsPerPage);
            const pagination = document.getElementById('pagination');
            
            if (totalPages <= 1) {{
                pagination.style.display = 'none';
                return;
            }}
            
            pagination.style.display = 'flex';
            let html = '';
            
            // Previous button
            html += `<button class="page-btn" onclick="goToPage(${{state.currentPage - 1}})" 
                     ${{state.currentPage === 1 ? 'disabled' : ''}}>
                     <i class="fas fa-chevron-left"></i>
                     </button>`;
            
            // Page numbers
            const startPage = Math.max(1, state.currentPage - 2);
            const endPage = Math.min(totalPages, startPage + 4);
            
            if (startPage > 1) {{
                html += `<button class="page-btn" onclick="goToPage(1)">1</button>`;
                if (startPage > 2) html += `<span class="page-dots">...</span>`;
            }}
            
            for (let i = startPage; i <= endPage; i++) {{
                html += `<button class="page-btn ${{i === state.currentPage ? 'active' : ''}}" 
                         onclick="goToPage(${{i}})">${{i}}</button>`;
            }}
            
            if (endPage < totalPages) {{
                if (endPage < totalPages - 1) html += `<span class="page-dots">...</span>`;
                html += `<button class="page-btn" onclick="goToPage(${{totalPages}})">${{totalPages}}</button>`;
            }}
            
            // Next button
            html += `<button class="page-btn" onclick="goToPage(${{state.currentPage + 1}})" 
                     ${{state.currentPage === totalPages ? 'disabled' : ''}}>
                     <i class="fas fa-chevron-right"></i>
                     </button>`;
            
            pagination.innerHTML = html;
        }}
        
        function goToPage(page) {{
            const totalPages = Math.ceil(state.filteredIssues.length / state.itemsPerPage);
            if (page < 1 || page > totalPages) return;
            
            state.currentPage = page;
            renderIssues();
            
            // Smooth scroll to top
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
        
        // Update counts
        function updateIssueCount() {{
            const countEl = document.getElementById('issuesCount');
            const showing = Math.min(state.filteredIssues.length, state.currentPage * state.itemsPerPage);
            const from = (state.currentPage - 1) * state.itemsPerPage + 1;
            
            if (state.filteredIssues.length === 0) {{
                countEl.innerHTML = '<i class="fas fa-filter"></i> No issues found';
            }} else if (state.filteredIssues.length === allIssues.length) {{
                countEl.innerHTML = `<i class="fas fa-filter"></i> Showing ${{from}}-${{showing}} of ${{allIssues.length}} issues`;
            }} else {{
                countEl.innerHTML = `<i class="fas fa-filter"></i> Showing ${{from}}-${{showing}} of ${{state.filteredIssues.length}} filtered issues (${{allIssues.length}} total)`;
            }}
        }}
        
        // Dark mode
        function toggleDarkMode() {{
            state.darkMode = !state.darkMode;
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', state.darkMode);
            
            const icon = document.querySelector('.action-btn i.fa-moon, .action-btn i.fa-sun');
            if (icon) {{
                icon.className = state.darkMode ? 'fas fa-sun' : 'fas fa-moon';
            }}
            
            showToast(state.darkMode ? 'Dark mode enabled' : 'Light mode enabled', 'info');
        }}
        
        // Toast notifications
        function showToast(message, type = 'info') {{
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            toast.className = `toast toast-${{type}}`;
            
            const icons = {{
                'info': 'fa-info-circle',
                'success': 'fa-check-circle',
                'warning': 'fa-exclamation-triangle',
                'error': 'fa-times-circle'
            }};
            
            toast.innerHTML = `
                <i class="fas ${{icons[type] || icons.info}}"></i>
                <span>${{message}}</span>
            `;
            
            container.appendChild(toast);
            
            // Trigger animation
            setTimeout(() => toast.classList.add('show'), 10);
            
            // Remove after 3 seconds
            setTimeout(() => {{
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }}, 3000);
        }}
        
        // Export functionality
        function exportData() {{
            const data = {{
                timestamp: new Date().toISOString(),
                totalIssues: allIssues.length,
                filteredIssues: state.filteredIssues.length,
                issues: state.filteredIssues
            }};
            
            const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cppcheck-report-${{new Date().toISOString().split('T')[0]}}.json`;
            a.click();
            URL.revokeObjectURL(url);
            
            showToast('Report exported successfully', 'success');
        }}
        
        // Copy functions
        function copyIssueInfo(issueId) {{
            const issue = allIssues.find(i => i.id === issueId);
            if (!issue) return;
            
            const text = `Issue #${{issue.id}}
File: ${{issue.file}}
Line: ${{issue.line}}
Severity: ${{issue.severity}}
Message: ${{issue.message}}`;
            
            navigator.clipboard.writeText(text).then(() => {{
                showToast('Issue info copied to clipboard', 'success');
            }});
        }}
        
        function copyIssueLink() {{
            const modal = document.getElementById('codeModal');
            const issueId = modal.dataset.currentIssueId;
            const url = window.location.href.split('#')[0] + '#issue-' + issueId;
            
            navigator.clipboard.writeText(url).then(() => {{
                showToast('Link copied to clipboard', 'success');
            }});
        }}
        
        function copyCodeSnippet() {{
            const codeElement = document.querySelector('.code-preview code');
            if (codeElement) {{
                navigator.clipboard.writeText(codeElement.textContent).then(() => {{
                    showToast('Code snippet copied to clipboard', 'success');
                }});
            }}
        }}
        
        // Keyboard shortcuts
        function initializeKeyboardShortcuts() {{
            document.addEventListener('keydown', (e) => {{
                // Don't trigger shortcuts when typing in input
                if (e.target.tagName === 'INPUT') {{
                    if (e.key === 'Escape') {{
                        e.target.blur();
                        e.target.value = '';
                        handleSearch({{ target: e.target }});
                    }}
                    return;
                }}
                
                switch(e.key) {{
                    case '/':
                        e.preventDefault();
                        document.getElementById('searchInput').focus();
                        break;
                    case '1':
                        setSeverityFilter('error', document.querySelector('.filter-btn.error'));
                        break;
                    case '2':
                        setSeverityFilter('warning', document.querySelector('.filter-btn.warning'));
                        break;
                    case '3':
                        setSeverityFilter('style', document.querySelector('.filter-btn.style'));
                        break;
                    case '4':
                        setSeverityFilter('performance', document.querySelector('.filter-btn.performance'));
                        break;
                    case '0':
                        setSeverityFilter('all', document.querySelector('.filter-btn:first-child'));
                        break;
                    case 'v':
                        cycleViewMode();
                        break;
                    case 'd':
                        toggleDarkMode();
                        break;
                    case 'e':
                        exportData();
                        break;
                    case 'Escape':
                        closeModal();
                        closeShortcutsModal();
                        break;
                }}
            }});
        }}
        
        function cycleViewMode() {{
            const modes = ['table', 'cards', 'compact'];
            const currentIndex = modes.indexOf(state.currentView);
            const nextIndex = (currentIndex + 1) % modes.length;
            const nextMode = modes[nextIndex];
            
            const button = document.querySelector(`.view-btn[onclick*="${{nextMode}}"]`);
            setViewMode(nextMode, button);
        }}
        
        // Shortcuts modal
        function showKeyboardShortcuts() {{
            document.getElementById('shortcutsModal').classList.add('show');
        }}
        
        function closeShortcutsModal() {{
            document.getElementById('shortcutsModal').classList.remove('show');
        }}
        
        // Animate numbers on load
        function animateNumbers() {{
            document.querySelectorAll('.stat-card .number').forEach(element => {{
                const target = parseInt(element.dataset.value) || 0;
                const duration = 1000;
                const increment = target / (duration / 16);
                let current = 0;
                
                const timer = setInterval(() => {{
                    current += increment;
                    if (current >= target) {{
                        current = target;
                        clearInterval(timer);
                    }}
                    element.textContent = Math.floor(current);
                }}, 16);
            }});
        }}
        
        // Initialize tooltips (placeholder for future enhancement)
        function initializeTooltips() {{
            // Add tooltip functionality here if needed
        }}
        
        // Handle window resize
        window.addEventListener('resize', () => {{
            // Adjust layout if needed
        }});
        
        // Handle modal outside click
        window.onclick = function(event) {{
            if (event.target.classList.contains('modal-overlay')) {{
                closeModal();
                closeShortcutsModal();
            }}
        }};
    </script>
</body>
</html>"""
        
        # Write the HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Enhanced dashboard generated: {output_file}")
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
    
    def calculate_health_score(self, stats):
        """Calculate overall code health score"""
        # Weight different severity levels
        weights = {
            'errors': -10,
            'warnings': -5,
            'style': -1,
            'performance': -3,
            'information': -0.5
        }
        
        total_issues = len(self.issues)
        if total_issues == 0:
            return 100
        
        # Calculate weighted score
        penalty = 0
        for key, weight in weights.items():
            penalty += stats.get(key, 0) * weight
        
        # Normalize to 0-100 scale
        # Assume -1000 penalty = 0% health
        health = max(0, min(100, 100 + (penalty / 10)))
        return int(health)
    
    def get_trend_icon(self, count):
        """Get trend icon based on count"""
        if count == 0:
            return '<i class="fas fa-check-circle trend-good"></i>'
        elif count < 10:
            return '<i class="fas fa-minus-circle trend-neutral"></i>'
        else:
            return '<i class="fas fa-arrow-up trend-bad"></i>'
    
    def generate_enhanced_styles(self):
        """Generate enhanced CSS with animations and modern design"""
        return """
        /* CSS Variables for theming */
        :root {
            --primary-color: #667eea;
            --primary-dark: #5a67d8;
            --primary-light: #7c8ff7;
            --secondary-color: #48bb78;
            --background: #ffffff;
            --surface: #f7fafc;
            --surface-hover: #edf2f7;
            --text-primary: #1a202c;
            --text-secondary: #4a5568;
            --text-muted: #a0aec0;
            --border-color: #e2e8f0;
            --border-radius: 12px;
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
            --error-color: #f56565;
            --warning-color: #ed8936;
            --style-color: #4299e1;
            --performance-color: #48bb78;
            --info-color: #9f7aea;
            --transition-fast: 150ms ease;
            --transition-normal: 300ms ease;
            --transition-slow: 500ms ease;
        }
        
        /* Dark mode variables */
        body.dark-mode {
            --background: #0f1419;
            --surface: #1a202c;
            --surface-hover: #2d3748;
            --text-primary: #f7fafc;
            --text-secondary: #cbd5e0;
            --text-muted: #718096;
            --border-color: #2d3748;
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.3);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.3);
            --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.3);
        }
        
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--background);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background-color var(--transition-normal), color var(--transition-normal);
        }
        
        /* Loading screen */
        .loading-screen {
            position: fixed;
            inset: 0;
            background: var(--background);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            transition: opacity var(--transition-normal);
        }
        
        .loader {
            width: 60px;
            height: 60px;
            position: relative;
        }
        
        .loader-inner {
            position: absolute;
            inset: 0;
            border: 3px solid var(--border-color);
            border-top-color: var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading-text {
            margin-top: 20px;
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        /* Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Enhanced Header */
        .header {
            position: relative;
            background: var(--surface);
            border-radius: var(--border-radius);
            overflow: hidden;
            margin-bottom: 30px;
            box-shadow: var(--shadow-md);
        }
        
        .header-background {
            position: absolute;
            inset: 0;
            overflow: hidden;
        }
        
        .animated-bg {
            position: absolute;
            inset: -50%;
            background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
            opacity: 0.1;
            animation: gradient-shift 15s ease infinite;
        }
        
        @keyframes gradient-shift {
            0%, 100% { transform: translateX(-50%) translateY(-50%) rotate(0deg); }
            50% { transform: translateX(-30%) translateY(-70%) rotate(180deg); }
        }
        
        .header-content {
            position: relative;
            padding: 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 30px;
            flex-wrap: wrap;
        }
        
        .header-left {
            flex: 1;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .logo-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 28px;
            box-shadow: var(--shadow-lg);
            animation: pulse 2s ease infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .logo-text h1 {
            font-size: 2.5em;
            font-weight: 800;
            color: var(--text-primary);
            margin: 0;
            letter-spacing: -0.02em;
        }
        
        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1em;
            margin-top: 5px;
        }
        
        .header-right {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        
        .header-stat {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 15px 25px;
            background: var(--background);
            border-radius: 10px;
            transition: transform var(--transition-fast);
        }
        
        .header-stat:hover {
            transform: translateY(-2px);
        }
        
        .header-stat i {
            font-size: 24px;
            color: var(--primary-color);
        }
        
        .header-stat .label {
            display: block;
            font-size: 0.85em;
            color: var(--text-muted);
            font-weight: 500;
        }
        
        .header-stat .value {
            display: block;
            font-size: 1.1em;
            font-weight: 700;
            color: var(--text-primary);
        }
        
        /* Quick Actions */
        .quick-actions {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            justify-content: flex-end;
        }
        
        .action-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: var(--surface);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all var(--transition-fast);
        }
        
        .action-btn:hover {
            background: var(--surface-hover);
            transform: translateY(-1px);
            box-shadow: var(--shadow-sm);
        }
        
        /* Statistics Section */
        .stats-section {
            margin-bottom: 40px;
        }
        
        .section-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.8em;
            font-weight: 700;
            margin-bottom: 25px;
            color: var(--text-primary);
        }
        
        .section-subtitle {
            font-size: 0.5em;
            font-weight: 400;
            color: var(--text-muted);
            margin-left: auto;
        }
        
        /* Enhanced Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
        }
        
        .stat-card {
            position: relative;
            background: var(--surface);
            border-radius: var(--border-radius);
            padding: 30px;
            cursor: pointer;
            transition: all var(--transition-normal);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
            border: 2px solid transparent;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.1));
            opacity: 0;
            transition: opacity var(--transition-normal);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
        }
        
        .stat-card:hover::before {
            opacity: 1;
        }
        
        .stat-card.active {
            border-color: var(--primary-color);
        }
        
        .stat-card.highlight {
            animation: highlight 0.5s ease;
        }
        
        @keyframes highlight {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        .stat-icon-container {
            position: relative;
            width: 60px;
            height: 60px;
            margin-bottom: 20px;
        }
        
        .stat-icon-bg {
            position: absolute;
            inset: 0;
            border-radius: 50%;
            opacity: 0.1;
            transition: transform var(--transition-normal);
        }
        
        .stat-card:hover .stat-icon-bg {
            transform: scale(1.2);
        }
        
        .stat-card i {
            position: relative;
            font-size: 30px;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .stat-content h3 {
            font-size: 0.95em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 15px;
            color: var(--text-secondary);
        }
        
        .stat-value {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        .stat-value .number {
            font-size: 2.5em;
            font-weight: 800;
            line-height: 1;
        }
        
        .change {
            font-size: 20px;
        }
        
        .trend-good { color: var(--performance-color); }
        .trend-neutral { color: var(--warning-color); }
        .trend-bad { color: var(--error-color); }
        
        .stat-bar {
            height: 6px;
            background: var(--border-color);
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        
        .stat-bar-fill {
            height: 100%;
            background: currentColor;
            border-radius: 3px;
            transition: width 1s ease;
            animation: fillBar 1s ease;
        }
        
        @keyframes fillBar {
            from { width: 0 !important; }
        }
        
        .stat-percent {
            font-size: 0.9em;
            color: var(--text-muted);
        }
        
        /* Stat card colors */
        .stat-card.error {
            color: var(--error-color);
        }
        
        .stat-card.error .stat-icon-bg {
            background: var(--error-color);
        }
        
        .stat-card.warning {
            color: var(--warning-color);
        }
        
        .stat-card.warning .stat-icon-bg {
            background: var(--warning-color);
        }
        
        .stat-card.style {
            color: var(--style-color);
        }
        
        .stat-card.style .stat-icon-bg {
            background: var(--style-color);
        }
        
        .stat-card.performance {
            color: var(--performance-color);
        }
        
        .stat-card.performance .stat-icon-bg {
            background: var(--performance-color);
        }
        
        .stat-card.information {
            color: var(--info-color);
        }
        
        .stat-card.information .stat-icon-bg {
            background: var(--info-color);
        }
        
        /* Enhanced Controls Section */
        .controls-section {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .search-container {
            flex: 1;
            min-width: 300px;
            position: relative;
        }
        
        .search-icon {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 18px;
            pointer-events: none;
        }
        
        .search-input {
            width: 100%;
            padding: 15px 50px 15px 50px;
            background: var(--surface);
            border: 2px solid var(--border-color);
            border-radius: 10px;
            font-size: 15px;
            color: var(--text-primary);
            transition: all var(--transition-fast);
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        .search-shortcuts {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .shortcut-hint {
            font-size: 12px;
            color: var(--text-muted);
        }
        
        kbd {
            display: inline-block;
            padding: 3px 8px;
            background: var(--background);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            box-shadow: 0 2px 0 rgba(0, 0, 0, 0.1);
        }
        
        /* Filter buttons */
        .filter-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: var(--surface);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all var(--transition-fast);
            position: relative;
            overflow: hidden;
        }
        
        .filter-btn::before {
            content: '';
            position: absolute;
            inset: 0;
            background: currentColor;
            opacity: 0;
            transition: opacity var(--transition-fast);
        }
        
        .filter-btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .filter-btn:hover::before {
            opacity: 0.1;
        }
        
        .filter-btn.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
        
        .filter-btn .badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 24px;
            padding: 2px 6px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            font-size: 12px;
            font-weight: 700;
        }
        
        .filter-btn.error { color: var(--error-color); border-color: var(--error-color); }
        .filter-btn.warning { color: var(--warning-color); border-color: var(--warning-color); }
        .filter-btn.style { color: var(--style-color); border-color: var(--style-color); }
        .filter-btn.performance { color: var(--performance-color); border-color: var(--performance-color); }
        
        /* View controls */
        .view-controls {
            display: flex;
            gap: 5px;
            background: var(--surface);
            padding: 5px;
            border-radius: 8px;
        }
        
        .view-btn {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            border: none;
            border-radius: 6px;
            color: var(--text-muted);
            cursor: pointer;
            transition: all var(--transition-fast);
        }
        
        .view-btn:hover {
            background: var(--surface-hover);
            color: var(--text-primary);
        }
        
        .view-btn.active {
            background: var(--primary-color);
            color: white;
        }
        
        /* Status bar */
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .status-left {
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .sort-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: var(--surface);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 14px;
            cursor: pointer;
            transition: all var(--transition-fast);
        }
        
        .sort-btn:hover {
            background: var(--surface-hover);
        }
        
        /* Table View */
        .table-container {
            background: var(--surface);
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .issues-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .issues-table thead {
            background: var(--background);
            border-bottom: 2px solid var(--border-color);
        }
        
        .issues-table th {
            padding: 20px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: color var(--transition-fast);
            position: relative;
        }
        
        .issues-table th:hover {
            color: var(--text-primary);
        }
        
        .sort-icon {
            margin-left: 5px;
            font-size: 12px;
            opacity: 0.5;
        }
        
        /* Table rows */
        .issue-row {
            border-bottom: 1px solid var(--border-color);
            transition: all var(--transition-fast);
            opacity: 0;
            transform: translateX(-10px);
        }
        
        .issue-row.visible {
            opacity: 1;
            transform: translateX(0);
        }
        
        .issue-row:hover {
            background: var(--surface-hover);
        }
        
        .issue-row td {
            padding: 20px;
            vertical-align: middle;
        }
        
        .checkbox {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        .file-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .file-icon {
            color: var(--primary-color);
            font-size: 18px;
        }
        
        .file-name {
            font-weight: 500;
            color: var(--text-primary);
        }
        
        .code-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: var(--performance-color);
            border-radius: 50%;
            margin-left: 5px;
            animation: pulse 2s ease infinite;
        }
        
        .line-number {
            display: inline-block;
            padding: 4px 12px;
            background: var(--background);
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            color: var(--text-secondary);
        }
        
        /* Severity badges */
        .severity-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all var(--transition-fast);
        }
        
        .severity-badge:hover {
            transform: scale(1.05);
        }
        
        .severity-badge.error {
            background: rgba(245, 101, 101, 0.15);
            color: var(--error-color);
        }
        
        .severity-badge.warning {
            background: rgba(237, 137, 54, 0.15);
            color: var(--warning-color);
        }
        
        .severity-badge.style {
            background: rgba(66, 153, 225, 0.15);
            color: var(--style-color);
        }
        
        .severity-badge.performance {
            background: rgba(72, 187, 120, 0.15);
            color: var(--performance-color);
        }
        
        .severity-badge.information {
            background: rgba(159, 122, 234, 0.15);
            color: var(--info-color);
        }
        
        .message-text {
            color: var(--text-primary);
            line-height: 1.4;
        }
        
        .issue-id {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: var(--text-muted);
            background: var(--background);
            padding: 4px 8px;
            border-radius: 4px;
        }
        
        /* Action buttons */
        .action-btn {
            padding: 8px 12px;
            background: var(--surface);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            cursor: pointer;
            transition: all var(--transition-fast);
            margin-left: 5px;
        }
        
        .action-btn:hover {
            background: var(--surface-hover);
            transform: translateY(-1px);
            box-shadow: var(--shadow-sm);
        }
        
        .action-btn.primary {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
        
        .action-btn.primary:hover {
            background: var(--primary-dark);
        }
        
        /* Card View */
        .cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            animation: slideIn 0.5s ease;
        }
        
        .issue-card {
            background: var(--surface);
            border-radius: var(--border-radius);
            padding: 25px;
            box-shadow: var(--shadow-sm);
            transition: all var(--transition-normal);
            cursor: pointer;
            opacity: 0;
            transform: translateY(20px);
            border: 2px solid transparent;
        }
        
        .issue-card.visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        .issue-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }
        
        .issue-card.error:hover { border-color: var(--error-color); }
        .issue-card.warning:hover { border-color: var(--warning-color); }
        .issue-card.style:hover { border-color: var(--style-color); }
        .issue-card.performance:hover { border-color: var(--performance-color); }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .card-body {
            margin-bottom: 20px;
        }
        
        .card-body .file-info {
            margin-bottom: 10px;
            font-size: 14px;
            color: var(--text-secondary);
        }
        
        .card-body .message {
            font-size: 15px;
            line-height: 1.5;
            color: var(--text-primary);
        }
        
        .card-footer {
            display: flex;
            gap: 10px;
        }
        
        /* Pagination */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 30px;
            padding: 20px;
        }
        
        .page-btn {
            min-width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--surface);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-weight: 500;
            cursor: pointer;
            transition: all var(--transition-fast);
        }
        
        .page-btn:hover:not(:disabled) {
            background: var(--surface-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow-sm);
        }
        
        .page-btn.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
        
        .page-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .page-dots {
            color: var(--text-muted);
            font-size: 14px;
        }
        
        /* Modal */
        .modal {
            position: fixed;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            visibility: hidden;
            opacity: 0;
            transition: all var(--transition-normal);
        }
        
        .modal.show {
            visibility: visible;
            opacity: 1;
        }
        
        .modal-overlay {
            position: absolute;
            inset: 0;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            position: relative;
            background: var(--background);
            border-radius: var(--border-radius);
            width: 90%;
            max-width: 900px;
            max-height: 85vh;
            overflow: hidden;
            box-shadow: var(--shadow-xl);
            transform: scale(0.9) translateY(20px);
            transition: transform var(--transition-normal);
        }
        
        .modal.show .modal-content {
            transform: scale(1) translateY(0);
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 25px 30px;
            background: var(--surface);
            border-bottom: 1px solid var(--border-color);
        }
        
        .modal-title {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .modal-title h3 {
            font-size: 1.3em;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .modal-actions {
            display: flex;
            gap: 10px;
        }
        
        .modal-action-btn {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            border: none;
            border-radius: 8px;
            color: var(--text-muted);
            cursor: pointer;
            transition: all var(--transition-fast);
        }
        
        .modal-action-btn:hover {
            background: var(--surface-hover);
            color: var(--text-primary);
        }
        
        .modal-body {
            padding: 30px;
            overflow-y: auto;
            max-height: calc(85vh - 80px);
        }
        
        /* Issue details */
        .issue-details {
            display: flex;
            flex-direction: column;
            gap: 30px;
        }
        
        .detail-section h4 {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--text-primary);
        }
        
        .detail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .detail-item {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .detail-label {
            font-size: 0.85em;
            font-weight: 500;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .detail-value {
            font-size: 1em;
            color: var(--text-primary);
        }
        
        .message-box {
            background: var(--surface);
            padding: 20px;
            border-radius: 10px;
            font-size: 15px;
            line-height: 1.6;
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }
        
        /* Code preview */
        .code-container {
            background: #1e1e1e;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }
        
        .code-preview {
            margin: 0;
            padding: 20px;
            overflow-x: auto;
        }
        
        .code-preview code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            line-height: 1.6;
            color: #d4d4d4;
        }
        
        .line-number {
            display: inline-block;
            width: 50px;
            color: #858585;
            text-align: right;
            margin-right: 20px;
            user-select: none;
        }
        
        .highlight-line {
            display: block;
            background: rgba(255, 215, 0, 0.1);
            border-left: 3px solid #ffd700;
            margin-left: -20px;
            padding-left: 17px;
        }
        
        /* Shortcuts modal */
        .shortcuts-modal {
            max-width: 600px;
        }
        
        .shortcuts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        
        .shortcut-item {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .shortcut-item kbd {
            min-width: 40px;
            text-align: center;
        }
        
        /* Toast notifications */
        .toast-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 2000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .toast {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 24px;
            background: var(--surface);
            border-radius: 10px;
            box-shadow: var(--shadow-lg);
            color: var(--text-primary);
            font-size: 14px;
            font-weight: 500;
            transform: translateX(400px);
            transition: transform var(--transition-normal);
            border-left: 4px solid;
        }
        
        .toast.show {
            transform: translateX(0);
        }
        
        .toast-info { border-color: var(--info-color); }
        .toast-success { border-color: var(--performance-color); }
        .toast-warning { border-color: var(--warning-color); }
        .toast-error { border-color: var(--error-color); }
        
        .toast i {
            font-size: 20px;
        }
        
        .toast-info i { color: var(--info-color); }
        .toast-success i { color: var(--performance-color); }
        .toast-warning i { color: var(--warning-color); }
        .toast-error i { color: var(--error-color); }
        
        /* Responsive design */
        @media (max-width: 1200px) {
            .header-content {
                flex-direction: column;
                text-align: center;
            }
            
            .header-right {
                justify-content: center;
            }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header-content {
                padding: 20px;
            }
            
            .logo-text h1 {
                font-size: 1.8em;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .controls-section {
                flex-direction: column;
            }
            
            .search-container {
                width: 100%;
            }
            
            .filter-group {
                width: 100%;
                justify-content: center;
            }
            
            .issues-table {
                font-size: 14px;
            }
            
            .issues-table th,
            .issues-table td {
                padding: 12px;
            }
            
            .modal-content {
                width: 95%;
                max-height: 90vh;
            }
        }
        
        /* Animations for AOS (Animate On Scroll) effect */
        [data-aos="fade-up"] {
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.6s ease;
        }
        
        [data-aos="fade-up"].aos-animate {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--surface);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }
        
        /* Print styles */
        @media print {
            .header-background,
            .quick-actions,
            .controls-section,
            .action-btn,
            .modal,
            .toast-container {
                display: none !important;
            }
            
            .container {
                max-width: 100%;
            }
            
            .issue-row {
                page-break-inside: avoid;
            }
        }
        """

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python generate-enhanced-dashboard.py <input.json> <output.html>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    generator = EnhancedDashboardGenerator(input_file)
    generator.generate(output_file)