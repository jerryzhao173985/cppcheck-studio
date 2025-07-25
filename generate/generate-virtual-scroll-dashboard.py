#!/usr/bin/env python3
"""
Professional Dashboard with Virtual Scrolling and Lazy Loading
Uses JSONL format for efficient data streaming and on-demand code loading
"""

import json
from pathlib import Path
from datetime import datetime
import hashlib
import os

class VirtualScrollDashboardGenerator:
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
    
    def generate_jsonl_data(self, output_dir):
        """Generate JSONL files for efficient streaming"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Write main issues data (without code context) as JSONL
        issues_jsonl_path = os.path.join(output_dir, 'issues.jsonl')
        with open(issues_jsonl_path, 'w') as f:
            for issue in self.issues:
                # Create a copy without code context
                issue_copy = {k: v for k, v in issue.items() if k != 'code_context'}
                f.write(json.dumps(issue_copy) + '\n')
        
        # Write code context separately for lazy loading
        code_jsonl_path = os.path.join(output_dir, 'code_context.jsonl')
        with open(code_jsonl_path, 'w') as f:
            for issue in self.issues:
                if 'code_context' in issue:
                    context_data = {
                        'id': issue['id'],
                        'code_context': issue['code_context']
                    }
                    f.write(json.dumps(context_data) + '\n')
        
        return issues_jsonl_path, code_jsonl_path
    
    def generate(self, output_file, data_dir='dashboard_data'):
        """Generate professional dashboard with virtual scrolling"""
        
        # Generate JSONL data files
        issues_jsonl, code_jsonl = self.generate_jsonl_data(data_dir)
        
        # Calculate statistics
        stats = self.calculate_stats()
        
        # Count issues with code context
        with_context = sum(1 for i in self.issues if 'code_context' in i)
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPPCheck Studio - Professional Dashboard</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        {self.generate_styles()}
    </style>
</head>
<body>
    <div class="container">
        <!-- Font Size Controls -->
        <div class="font-size-controls" id="fontSizeControls" style="position: fixed; top: 10px; right: 10px; z-index: 1000; background: rgba(255,255,255,0.95); padding: 8px 12px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 8px;">
            <label style="font-size: 0.85em; color: #666;">Font Size:</label>
            <button onclick="adjustFontSize(-1)" title="Decrease font size (Ctrl -)" style="width: 30px; height: 30px; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 4px; font-size: 14px; transition: all 0.2s;">A-</button>
            <button onclick="adjustFontSize(0)" title="Reset font size (Ctrl 0)" style="width: 30px; height: 30px; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 4px; font-size: 14px; transition: all 0.2s;">A</button>
            <button onclick="adjustFontSize(1)" title="Increase font size (Ctrl +)" style="width: 30px; height: 30px; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 4px; font-size: 14px; transition: all 0.2s;">A+</button>
            <span id="fontSizeDisplay" style="font-size: 0.85em; color: #666; min-width: 40px; text-align: right;">100%</span>
        </div>
        
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <h1><i class="fas fa-code"></i> CPPCheck Studio - Professional Dashboard</h1>
                <div class="header-info">
                    <span><i class="fas fa-project-diagram"></i> LPZRobots</span>
                    <span><i class="fas fa-clock"></i> {self.timestamp}</span>
                    <span><i class="fas fa-database"></i> {len(self.issues)} total issues</span>
                    <span><i class="fas fa-file-code"></i> {with_context} with code context</span>
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
                <input type="text" id="searchInput" placeholder="Search by file, message, ID, or line number... (Ctrl+F to focus, Esc to clear)">
            </div>
            
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="setSeverityFilter('all', this)">
                    <i class="fas fa-list"></i> All ({stats['total']})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('error', this)">
                    <i class="fas fa-exclamation-circle"></i> Errors ({stats['errors']})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('warning', this)">
                    <i class="fas fa-exclamation-triangle"></i> Warnings ({stats['warnings']})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('style', this)">
                    <i class="fas fa-palette"></i> Style ({stats['style']})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('performance', this)">
                    <i class="fas fa-tachometer-alt"></i> Performance ({stats['performance']})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('information', this)">
                    <i class="fas fa-info-circle"></i> Info
                </button>
            </div>
        </div>
        
        <!-- Issues Count and Loading Status -->
        <div class="status-bar">
            <div class="issues-count">
                <span id="issuesCount" role="status" aria-live="polite">Loading...</span>
            </div>
            <div class="loading-status" id="loadingStatus" style="display: none;">
                <i class="fas fa-spinner fa-spin"></i> <span id="loadingText">Loading...</span>
            </div>
        </div>
        
        <!-- Virtual Scroll Container -->
        <div class="virtual-scroll-container" id="scrollContainer">
            <div class="issues-table-wrapper">
                <table class="issues-table">
                    <thead>
                        <tr>
                            <th class="col-indicator"></th>
                            <th class="col-file">FILE</th>
                            <th class="col-line">LINE</th>
                            <th class="col-severity">SEVERITY</th>
                            <th class="col-message">MESSAGE</th>
                            <th class="col-id">ID</th>
                            <th class="col-actions">ACTIONS</th>
                        </tr>
                    </thead>
                </table>
                <div class="virtual-scroll-viewport" id="viewport">
                    <div class="virtual-scroll-spacer" id="spacerTop"></div>
                    <table class="issues-table">
                        <tbody id="issuesBody">
                            <!-- Virtual rows will be rendered here -->
                        </tbody>
                    </table>
                    <div class="virtual-scroll-spacer" id="spacerBottom"></div>
                </div>
            </div>
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
        // Configuration
        const CONFIG = {{
            ROW_HEIGHT: 50,
            VISIBLE_BUFFER: 5,
            SCROLL_DEBOUNCE: 10,
            SEARCH_DEBOUNCE: 300,
            BATCH_SIZE: 50,
            DATA_DIR: '{data_dir}',
            MAX_CONTEXT_CACHE: 1000,
            CLEANUP_INTERVAL: 60000,
            RENDER_BATCH_SIZE: 100,
            INTERSECTION_THRESHOLD: 0.1
        }};
        
        // Global state
        const state = {{
            allIssues: [],
            filteredIssues: [],
            codeContextMap: new Map(),
            loadedContextIds: new Set(),
            currentFilter: 'all',
            currentSearch: '',
            visibleStart: 0,
            visibleEnd: 0,
            isLoading: false,
            scrollTop: 0,
            containerHeight: 0,
            fontSize: 100, // Font size percentage
            renderPending: false
        }};
        
        // Create debounced filter function with loading indicator
        const debouncedFilter = debounce((e) => {{
            const searchValue = e ? e.target.value : document.getElementById('searchInput').value;
            if (searchValue.length > 0) {{
                showLoadingStatus('Searching...');
            }}
            filterData();
            if (searchValue.length > 0) {{
                setTimeout(hideLoadingStatus, 100);
            }}
        }}, 300);
        
        // Global error handlers
        window.addEventListener('error', (event) => {{
            console.error('Global error:', event.error);
            showErrorNotification('An unexpected error occurred', event.error.message);
        }});
        
        window.addEventListener('unhandledrejection', (event) => {{
            console.error('Unhandled promise rejection:', event.reason);
            showErrorNotification('Failed to load resource', event.reason);
        }});
        
        // Error notification system
        function showErrorNotification(title, message) {{
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #ff4444;
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 10000;
                max-width: 400px;
                animation: slideIn 0.3s ease-out;
            `;
            
            notification.innerHTML = `
                <div style="display: flex; align-items: start; gap: 10px;">
                    <i class="fas fa-exclamation-circle" style="font-size: 20px;"></i>
                    <div>
                        <strong style="display: block; margin-bottom: 5px;">${{title}}</strong>
                        <span style="font-size: 0.9em; opacity: 0.9;">${{message || 'Unknown error'}}</span>
                    </div>
                    <button onclick="this.parentElement.parentElement.remove()" 
                            style="background: none; border: none; color: white; 
                                   font-size: 20px; cursor: pointer; margin-left: auto;">×</button>
                </div>
            `;
            
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 8000);
        }}
        
        // Initialize with comprehensive error handling
        async function initialize() {{
            let initTimeout;
            
            try {{
                showLoadingStatus('Loading issues data...');
                
                // Set initialization timeout
                initTimeout = setTimeout(() => {{
                    throw new Error('Initialization timeout - please check your data files');
                }}, 30000);
                
                // Load issues from JSONL
                await loadIssuesData().catch(error => {{
                    throw new Error(`Data loading failed: ${{error.message}}`);
                }});
                
                clearTimeout(initTimeout);
                
                // Validate data
                if (!state.allIssues || state.allIssues.length === 0) {{
                    throw new Error('No issues found in data file');
                }}
                
                // Set up virtual scrolling
                setupVirtualScroll();
                
                // Start memory monitoring
                startMemoryMonitoring();
                
                // Initial render
                filterData();
                
                // Set up search event listeners with error handling
                const searchInput = document.getElementById('searchInput');
                if (!searchInput) {{
                    throw new Error('Search input element not found');
                }}
                
                searchInput.addEventListener('input', debouncedFilter);
                
                // Clear search on Escape key
                searchInput.addEventListener('keydown', (e) => {{
                    if (e.key === 'Escape') {{
                        e.target.value = '';
                        debouncedFilter.cancel();
                        filterData();
                    }}
                }});
                
                // Focus search on Ctrl+F or Cmd+F
                document.addEventListener('keydown', (e) => {{
                    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {{
                        e.preventDefault();
                        searchInput.focus();
                        searchInput.select();
                    }} else if ((e.ctrlKey || e.metaKey) && (e.key === '+' || e.key === '=')) {{
                        e.preventDefault();
                        adjustFontSize(1);
                    }} else if ((e.ctrlKey || e.metaKey) && e.key === '-') {{
                        e.preventDefault();
                        adjustFontSize(-1);
                    }} else if ((e.ctrlKey || e.metaKey) && e.key === '0') {{
                        e.preventDefault();
                        adjustFontSize(0);
                    }}
                }});
                
                hideLoadingStatus();
                console.log(`Dashboard initialized successfully with ${{state.allIssues.length}} issues`);
                
            }} catch (error) {{
                clearTimeout(initTimeout);
                console.error('Initialization error:', error);
                hideLoadingStatus();
                
                // Show user-friendly error
                showErrorNotification('Dashboard Initialization Failed', error.message);
                
                // Display fallback UI
                displayFallbackUI(error);
            }}
        }}
        
        // Load issues data from JSONL
        // Load issues data with comprehensive error handling
        async function loadIssuesData() {{
            let response;
            
            try {{
                // Fetch with timeout
                const controller = new AbortController();
                const timeout = setTimeout(() => controller.abort(), 15000);
                
                response = await fetch('{data_dir}/issues.jsonl', {{
                    signal: controller.signal
                }}).catch(error => {{
                    if (error.name === 'AbortError') {{
                        throw new Error('Request timeout - data file is taking too long to load');
                    }}
                    throw new Error(`Network error: ${{error.message}}`);
                }});
                
                clearTimeout(timeout);
                
                if (!response.ok) {{
                    throw new Error(`Failed to load data: HTTP ${{response.status}} ${{response.statusText}}`);
                }}
                
                const text = await response.text();
                
                if (!text || text.trim() === '') {{
                    throw new Error('Data file is empty');
                }}
                
                const lines = text.trim().split('\\n');
                let parseErrors = 0;
                const errors = [];
                
                state.allIssues = lines.map((line, index) => {{
                    if (!line || line.trim() === '') return null;
                    
                    try {{
                        const issue = JSON.parse(line);
                        
                        // Basic validation
                        if (!issue || typeof issue !== 'object') {{
                            throw new Error('Invalid issue object');
                        }}
                        
                        // Ensure required fields have defaults
                        return {{
                            id: issue.id || `issue_${{index}}`,
                            file: issue.file || 'Unknown file',
                            line: issue.line || 0,
                            severity: issue.severity || 'style',
                            message: issue.message || 'No message',
                            ...issue
                        }};
                        
                    }} catch (e) {{
                        parseErrors++;
                        if (parseErrors <= 5) {{
                            errors.push(`Line ${{index + 1}}: ${{e.message}}`);
                        }}
                        console.error(`Failed to parse line ${{index + 1}}:`, e);
                        return null;
                    }}
                }}).filter(Boolean);
                
                if (state.allIssues.length === 0) {{
                    throw new Error('No valid issues found in data file');
                }}
                
                // Show warning for parse errors
                if (parseErrors > 0) {{
                    const errorMsg = `Skipped ${{parseErrors}} invalid entries`;
                    console.warn(errorMsg);
                    if (parseErrors > 10) {{
                        showErrorNotification('Data Quality Warning', errorMsg);
                    }}
                }}
                
                console.log(`Successfully loaded ${{state.allIssues.length}} issues`);
                
            }} catch (error) {{
                console.error('Failed to load issues:', error);
                throw error;
            }}
        }}
        
        // Load code context for specific issue IDs
        // Memory-optimized code context loading with streaming
        async function loadCodeContext(issueIds) {{
            const idsToLoad = issueIds.filter(id => !state.loadedContextIds.has(id));
            if (idsToLoad.length === 0) return;
            
            // Memory cleanup if needed
            if (state.codeContextMap.size > CONFIG.MAX_CONTEXT_CACHE) {{
                cleanupOldContextEntries();
            }}
            
            try {{
                const response = await fetch('{data_dir}/code_context.jsonl');
                if (!response.ok) throw new Error('Failed to fetch code context');
                
                // Use streaming to handle large files efficiently
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';
                let processedCount = 0;
                
                while (true) {{
                    const {{ done, value }} = await reader.read();
                    if (done) break;
                    
                    buffer += decoder.decode(value, {{ stream: true }});
                    const lines = buffer.split('\\n');
                    buffer = lines.pop() || '';
                    
                    for (const line of lines) {{
                        if (!line) continue;
                        
                        try {{
                            const data = JSON.parse(line);
                            if (idsToLoad.includes(data.id)) {{
                                state.codeContextMap.set(data.id, data.code_context);
                                state.loadedContextIds.add(data.id);
                                processedCount++;
                                
                                // Break early if we've loaded all needed contexts
                                if (processedCount >= idsToLoad.length) {{
                                    reader.cancel();
                                    return;
                                }}
                            }}
                        }} catch (e) {{
                            console.error('Failed to parse code context line:', e);
                        }}
                    }}
                }}
                
                // Process remaining buffer
                if (buffer && buffer.trim()) {{
                    try {{
                        const data = JSON.parse(buffer);
                        if (idsToLoad.includes(data.id)) {{
                            state.codeContextMap.set(data.id, data.code_context);
                            state.loadedContextIds.add(data.id);
                        }}
                    }} catch (e) {{
                        console.error('Failed to parse final context:', e);
                    }}
                }}
                
                console.log('Loaded code context for', idsToLoad.length, 'issues');
            }} catch (error) {{
                console.error('Failed to load code context:', error);
            }}
        }}
        
        // Set up virtual scrolling
        function setupVirtualScroll() {{
            const viewport = document.getElementById('viewport');
            const scrollContainer = document.getElementById('scrollContainer');
            
            // Update container height on resize
            const updateContainerHeight = () => {{
                state.containerHeight = scrollContainer.clientHeight - 100; // Account for header
                renderVisibleRows();
            }};
            
            updateContainerHeight();
            window.addEventListener('resize', updateContainerHeight);
            
            // Handle scroll events
            scrollContainer.addEventListener('scroll', debounce(() => {{
                state.scrollTop = scrollContainer.scrollTop;
                renderVisibleRows();
            }}, CONFIG.SCROLL_DEBOUNCE));
        }}
        
        // Render visible rows based on scroll position with performance optimization
        async function renderVisibleRows() {{
            // Prevent concurrent renders
            if (state.renderPending) return;
            state.renderPending = true;
            
            const renderStart = performance.now();
            const totalHeight = state.filteredIssues.length * CONFIG.ROW_HEIGHT;
            const visibleStart = Math.floor(state.scrollTop / CONFIG.ROW_HEIGHT) - CONFIG.VISIBLE_BUFFER;
            const visibleEnd = Math.ceil((state.scrollTop + state.containerHeight) / CONFIG.ROW_HEIGHT) + CONFIG.VISIBLE_BUFFER;
            
            state.visibleStart = Math.max(0, visibleStart);
            state.visibleEnd = Math.min(state.filteredIssues.length, visibleEnd);
            
            // Update spacers
            document.getElementById('spacerTop').style.height = (state.visibleStart * CONFIG.ROW_HEIGHT) + 'px';
            document.getElementById('spacerBottom').style.height = 
                ((state.filteredIssues.length - state.visibleEnd) * CONFIG.ROW_HEIGHT) + 'px';
            
            // Get visible issues and their IDs
            const visibleIssues = state.filteredIssues.slice(state.visibleStart, state.visibleEnd);
            const visibleIds = visibleIssues.map(issue => issue.id).filter(Boolean);
            
            // Load code context for visible issues
            await loadCodeContext(visibleIds);
            
            // Render rows
            const tbody = document.getElementById('issuesBody');
            tbody.innerHTML = '';
            
            // Batch DOM updates using DocumentFragment for better performance
            const fragment = document.createDocumentFragment();
            visibleIssues.forEach((issue, index) => {{
                const row = createIssueRow(issue, state.visibleStart + index);
                fragment.appendChild(row);
            }});
            tbody.appendChild(fragment);
            
            // Performance monitoring
            const renderTime = performance.now() - renderStart;
            if (renderTime > 50) {{
                console.warn(`Slow render: ${{renderTime.toFixed(2)}}ms for ${{visibleIssues.length}} rows`);
            }}
            
            state.renderPending = false;
        }}
        
        // Create issue row
        function createIssueRow(issue, globalIndex) {{
            const row = document.createElement('tr');
            row.className = 'issue-row';
            row.dataset.id = issue.id;
            
            const hasCodeContext = state.codeContextMap.has(issue.id);
            
            // Indicator cell (for code context)
            const indicatorCell = document.createElement('td');
            indicatorCell.className = 'indicator-cell';
            if (hasCodeContext) {{
                indicatorCell.innerHTML = '<div class="code-indicator"></div>';
            }}
            
            // File cell
            const fileCell = document.createElement('td');
            fileCell.className = 'file-cell';
            fileCell.title = issue.file || '';
            fileCell.innerHTML = '<i class="fas fa-file-code"></i> ' + escapeHtml(getFileName(issue.file || ''));
            
            // Line cell
            const lineCell = document.createElement('td');
            lineCell.className = 'line-cell';
            lineCell.textContent = issue.line || '-';
            
            // Severity cell
            const severityCell = document.createElement('td');
            const severityBadge = document.createElement('span');
            severityBadge.className = 'severity-badge ' + (issue.severity || 'unknown');
            severityBadge.textContent = (issue.severity || 'UNKNOWN').toUpperCase();
            severityCell.appendChild(severityBadge);
            
            // Message cell
            const messageCell = document.createElement('td');
            messageCell.className = 'message-cell';
            messageCell.title = issue.message || '';
            messageCell.textContent = truncateMessage(issue.message || 'No message');
            
            // ID cell
            const idCell = document.createElement('td');
            idCell.className = 'id-cell';
            idCell.textContent = issue.id || 'N/A';
            
            // Actions cell
            const actionsCell = document.createElement('td');
            actionsCell.className = 'actions-cell';
            const actionBtn = document.createElement('button');
            actionBtn.className = 'action-btn' + (hasCodeContext ? ' has-code' : '');
            actionBtn.innerHTML = '<i class="fas ' + (hasCodeContext ? 'fa-code' : 'fa-eye') + '"></i>';
            actionBtn.onclick = (e) => {{
                e.stopPropagation();
                showIssueDetails(issue, globalIndex);
            }};
            actionsCell.appendChild(actionBtn);
            
            // Add cells to row
            row.appendChild(indicatorCell);
            row.appendChild(fileCell);
            row.appendChild(lineCell);
            row.appendChild(severityCell);
            row.appendChild(messageCell);
            row.appendChild(idCell);
            row.appendChild(actionsCell);
            
            // Row click handler
            row.onclick = () => showIssueDetails(issue, globalIndex);
            
            return row;
        }}
        
        // Filter data based on search and severity
        function filterData() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            state.currentSearch = searchTerm;
            
            state.filteredIssues = state.allIssues.filter(issue => {{
                // Severity filter
                if (state.currentFilter !== 'all' && issue.severity !== state.currentFilter) {{
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
            
            // Update count
            updateIssueCount();
            
            // Reset scroll and render
            document.getElementById('scrollContainer').scrollTop = 0;
            state.scrollTop = 0;
            renderVisibleRows();
        }}
        
        // Update issue count display
        function updateIssueCount() {{
            const countEl = document.getElementById('issuesCount');
            const filtered = state.filteredIssues.length;
            const total = state.allIssues.length;
            
            if (filtered === total) {{
                countEl.textContent = `Showing all ${{total}} issues`;
            }} else {{
                countEl.textContent = `Showing ${{filtered}} of ${{total}} issues`;
            }}
        }}
        
        // Set severity filter
        function setSeverityFilter(severity, button) {{
            state.currentFilter = severity;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            button.classList.add('active');
            
            filterData();
        }}
        
        // Show issue details modal
        async function showIssueDetails(issue, index) {{
            const modal = document.getElementById('codeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.innerHTML = '<i class="fas fa-file-code"></i> ' + 
                escapeHtml(getFileName(issue.file || 'Unknown')) + ':' + (issue.line || '?');
            
            // Ensure code context is loaded
            if (issue.id && !state.codeContextMap.has(issue.id)) {{
                showLoadingStatus('Loading code context...');
                await loadCodeContext([issue.id]);
                hideLoadingStatus();
            }}
            
            const codeContext = state.codeContextMap.get(issue.id);
            
            // Build modal content
            let content = '<div class="issue-details">';
            
            // Issue info
            content += '<div class="info-section">';
            content += '<h4><i class="fas fa-info-circle"></i> Issue Information</h4>';
            content += '<table class="info-table">';
            content += '<tr><td><strong>File:</strong></td><td class="code-text">' + escapeHtml(issue.file || 'Unknown') + '</td></tr>';
            content += '<tr><td><strong>Line:</strong></td><td>' + (issue.line || 'N/A') + '</td></tr>';
            content += '<tr><td><strong>Severity:</strong></td><td><span class="severity-badge ' + (issue.severity || 'unknown') + '">' + (issue.severity || 'UNKNOWN').toUpperCase() + '</span></td></tr>';
            content += '<tr><td><strong>Issue ID:</strong></td><td><code>' + (issue.id || 'N/A') + '</code></td></tr>';
            content += '<tr><td><strong>Position:</strong></td><td>' + (index + 1) + ' of ' + state.filteredIssues.length + '</td></tr>';
            content += '</table></div>';
            
            // Message
            content += '<div class="message-section">';
            content += '<h4><i class="fas fa-comment-alt"></i> Message</h4>';
            content += '<div class="message-box">' + escapeHtml(issue.message || 'No message available') + '</div>';
            content += '</div>';
            
            // Code context
            content += '<div class="code-section">';
            content += '<h4><i class="fas fa-code"></i> Code Context</h4>';
            
            if (codeContext && codeContext.lines && codeContext.lines.length > 0) {{
                content += '<div class="code-preview"><pre><code class="language-cpp">';
                
                codeContext.lines.forEach(line => {{
                    const isTarget = line.is_target === true;
                    const lineNum = String(line.number || 0).padStart(4, ' ');
                    const lineContent = escapeHtml(line.content || '');
                    
                    if (isTarget) {{
                        content += '<span class="highlight-line">' + lineNum + ': ' + lineContent + '</span>\\n';
                    }} else {{
                        content += lineNum + ': ' + lineContent + '\\n';
                    }}
                }});
                
                content += '</code></pre></div>';
            }} else {{
                content += '<div class="no-code-message">';
                content += '<i class="fas fa-info-circle"></i>';
                content += '<p>Code context not available for this issue.</p>';
                content += '</div>';
            }}
            
            content += '</div></div>';
            
            modalBody.innerHTML = content;
            modal.style.display = 'block';
        }}
        
        // Helper functions
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
        
        function truncateMessage(message) {{
            const maxLength = 80;
            if (message && message.length > maxLength) {{
                return message.substring(0, maxLength - 3) + '...';
            }}
            return message || '';
        }}
        
        function debounce(func, wait, immediate = false) {{
            let timeout;
            let cancelled = false;
            
            const debounced = function(...args) {{
                if (cancelled) return;
                
                const callNow = immediate && !timeout;
                const later = () => {{
                    timeout = null;
                    if (!immediate && !cancelled) {{
                        func.apply(this, args);
                    }}
                }};
                
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                
                if (callNow) {{
                    func.apply(this, args);
                }}
            }};
            
            // Add cancel method
            debounced.cancel = function() {{
                clearTimeout(timeout);
                timeout = null;
                cancelled = true;
            }};
            
            // Add reset method
            debounced.reset = function() {{
                cancelled = false;
            }};
            
            return debounced;
        }}
        
        function showLoadingStatus(text) {{
            document.getElementById('loadingStatus').style.display = 'block';
            document.getElementById('loadingText').textContent = text;
        }}
        
        function hideLoadingStatus() {{
            document.getElementById('loadingStatus').style.display = 'none';
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
        }};
        
        // Font size adjustment functions
        function adjustFontSize(delta) {{
            if (delta === 0) {{
                // Reset to default
                state.fontSize = 100;
            }} else {{
                // Adjust by 10% increments
                state.fontSize = Math.max(70, Math.min(150, state.fontSize + (delta * 10)));
            }}
            
            // Apply new font size
            document.documentElement.style.fontSize = state.fontSize + '%';
            
            // Update display
            const display = document.getElementById('fontSizeDisplay');
            if (display) {{
                display.textContent = state.fontSize + '%';
            }}
            
            // Save preference
            try {{
                localStorage.setItem('dashboardFontSize', state.fontSize);
            }} catch (e) {{
                console.warn('Could not save font size preference:', e);
            }}
            
            // Adjust row height proportionally
            const newRowHeight = Math.round(50 * (state.fontSize / 100));
            if (CONFIG.ROW_HEIGHT !== newRowHeight) {{
                CONFIG.ROW_HEIGHT = newRowHeight;
                renderVisibleRows();
            }}
        }}
        
        // Load saved font size preference
        function loadFontSizePreference() {{
            try {{
                const saved = localStorage.getItem('dashboardFontSize');
                if (saved) {{
                    state.fontSize = parseInt(saved, 10);
                    if (!isNaN(state.fontSize) && state.fontSize >= 70 && state.fontSize <= 150) {{
                        document.documentElement.style.fontSize = state.fontSize + '%';
                        CONFIG.ROW_HEIGHT = Math.round(50 * (state.fontSize / 100));
                    }} else {{
                        state.fontSize = 100;
                    }}
                }}
            }} catch (e) {{
                console.warn('Could not load font size preference:', e);
            }}
        }}
        
        // Memory cleanup function
        function cleanupOldContextEntries() {{
            const maxSize = CONFIG.MAX_CONTEXT_CACHE;
            if (state.codeContextMap.size <= maxSize) return;
            
            const entriesToRemove = state.codeContextMap.size - Math.floor(maxSize * 0.8);
            const keysToRemove = Array.from(state.codeContextMap.keys()).slice(0, entriesToRemove);
            
            keysToRemove.forEach(key => {{
                state.codeContextMap.delete(key);
                state.loadedContextIds.delete(key);
            }});
            
            console.log(`Cleaned up ${{entriesToRemove}} old context entries`);
        }}
        
        // Monitor memory usage
        function startMemoryMonitoring() {{
            if (!performance.memory) return;
            
            setInterval(() => {{
                const memInfo = performance.memory;
                const usagePercent = (memInfo.usedJSHeapSize / memInfo.jsHeapSizeLimit) * 100;
                
                if (usagePercent > 80) {{
                    console.warn(`High memory usage: ${{usagePercent.toFixed(1)}}%`);
                    cleanupOldContextEntries();
                    
                    // Force garbage collection if available
                    if (window.gc) {{
                        window.gc();
                    }}
                }}
            }}, 30000); // Check every 30 seconds
        }}
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', () => {{
                loadFontSizePreference();
                initialize();
            }});
        }} else {{
            loadFontSizePreference();
            initialize();
        }}
        
        // Display fallback UI when critical errors occur
        function displayFallbackUI(error) {{
            const container = document.querySelector('.container');
            if (!container) return;
            
            container.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; 
                            justify-content: center; min-height: 100vh; padding: 40px; 
                            text-align: center; background: #f5f7fa;">
                    <div style="background: white; padding: 40px; border-radius: 16px; 
                                box-shadow: 0 4px 20px rgba(0,0,0,0.1); max-width: 600px;">
                        <i class="fas fa-exclamation-triangle" 
                           style="font-size: 64px; color: #ff4444; margin-bottom: 20px;"></i>
                        <h1 style="font-size: 28px; color: #333; margin-bottom: 15px;">
                            Dashboard Loading Error
                        </h1>
                        <p style="font-size: 18px; color: #666; margin-bottom: 30px; line-height: 1.6;">
                            ${{error.message || 'An unexpected error occurred while loading the dashboard.'}}
                        </p>
                        
                        <div style="display: flex; gap: 15px; justify-content: center; margin-bottom: 30px;">
                            <button onclick="location.reload()" 
                                    style="padding: 12px 24px; background: #4CAF50; color: white; 
                                           border: none; border-radius: 8px; cursor: pointer; 
                                           font-size: 16px; font-weight: 500; 
                                           transition: background 0.2s;">
                                <i class="fas fa-redo" style="margin-right: 8px;"></i>
                                Retry Loading
                            </button>
                            <button onclick="window.history.back()" 
                                    style="padding: 12px 24px; background: #666; color: white; 
                                           border: none; border-radius: 8px; cursor: pointer; 
                                           font-size: 16px; font-weight: 500; 
                                           transition: background 0.2s;">
                                <i class="fas fa-arrow-left" style="margin-right: 8px;"></i>
                                Go Back
                            </button>
                        </div>
                        
                        <details style="text-align: left; background: #f8f9fa; padding: 20px; 
                                        border-radius: 8px; margin-top: 20px;">
                            <summary style="cursor: pointer; font-weight: 600; color: #333; 
                                           margin-bottom: 10px;">Troubleshooting Tips</summary>
                            <ul style="margin: 10px 0 0 0; padding-left: 20px; color: #666; 
                                       line-height: 1.8;">
                                <li>Verify that <code>issues.jsonl</code> exists in the data directory</li>
                                <li>Check that the JSON data is properly formatted</li>
                                <li>Ensure you have a stable internet connection</li>
                                <li>Try clearing your browser cache and cookies</li>
                                <li>Check the browser console (F12) for detailed errors</li>
                            </ul>
                            <div style="margin-top: 15px; padding: 10px; background: #fff; 
                                        border-left: 4px solid #ff4444; border-radius: 4px;">
                                <strong>Error Details:</strong>
                                <pre style="margin: 5px 0 0 0; font-family: monospace; 
                                            font-size: 12px; color: #666; 
                                            white-space: pre-wrap;">${{error.stack || error.toString()}}</pre>
                            </div>
                        </details>
                    </div>
                </div>
            `;
        }}
    </script>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Virtual scroll dashboard generated: {output_file}")
        print(f"   Total issues: {len(self.issues)}")
        print(f"   Issues with code context: {with_context}")
        print(f"   Data directory: {data_dir}/")
        print(f"   - issues.jsonl: {os.path.getsize(os.path.join(data_dir, 'issues.jsonl')) / 1024:.1f} KB")
        print(f"   - code_context.jsonl: {os.path.getsize(os.path.join(data_dir, 'code_context.jsonl')) / 1024:.1f} KB")
        
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
                'information': 0,
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
            'performance': sum(1 for i in self.issues if i.get('severity') == 'performance'),
            'information': sum(1 for i in self.issues if i.get('severity') == 'information')
        }
        
        # Calculate percentages
        stats['error_percent'] = (stats['errors'] / total) * 100 if total > 0 else 0
        stats['warning_percent'] = (stats['warnings'] / total) * 100 if total > 0 else 0
        stats['style_percent'] = (stats['style'] / total) * 100 if total > 0 else 0
        stats['performance_percent'] = (stats['performance'] / total) * 100 if total > 0 else 0
            
        return stats
        
    def generate_styles(self):
        """Generate CSS styles with fixed alignment"""
        return """
        /*
         * Virtual Scroll Dashboard CSS System
         * ===================================
         * This dashboard uses a modern CSS approach with:
         * 
         * 1. CSS Variables for theming (var(--name, fallback))
         * 2. Responsive design with mobile-first approach
         * 3. Virtual scrolling for performance with large datasets
         * 4. Accessible color contrast ratios
         * 5. Smooth transitions for better UX
         * 
         * Key Variables:
         * - Colors: Use var() with fallbacks for older browsers
         * - Transitions: Consistent timing (200ms default)
         * - Font sizes: Base 16px, UI elements 0.85em
         * - Mobile: 14px base font below 768px
         */
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f5f7fa;
            color: #2d3748;
            line-height: 1.6;
            overflow: hidden;
            font-size: 16px;
        }
        
        .container {
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            flex-shrink: 0;
        }
        
        .header-content {
            max-width: 1600px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .header h1 {
            font-size: 1.8em;
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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
            width: 100%;
            flex-shrink: 0;
        }
        
        .stat-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
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
            height: 3px;
            background: currentColor;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .stat-card i {
            font-size: 2em;
            margin-bottom: 8px;
            opacity: 0.8;
        }
        
        .stat-card h3 {
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #718096;
            margin-bottom: 8px;
        }
        
        .stat-card .value {
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 4px;
        }
        
        .stat-card .percent {
            font-size: 0.85em;
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
            border-radius: 8px;
            padding: 15px;
            margin: 0 20px;
            max-width: 1560px;
            align-self: center;
            width: calc(100% - 40px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            align-items: center;
            flex-shrink: 0;
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
            border-radius: 6px;
            font-size: 0.85em;
            transition: all 0.2s ease;
            background: var(--bg-primary, #ffffff);
            color: var(--text-primary, #212529);
        }
        
        .search-container input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background: var(--bg-primary, #ffffff);
        }
        
        .search-container input::placeholder {
            color: var(--text-secondary, #6c757d);
            opacity: 0.7;
        }
        
        .search-container input:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .filter-buttons {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 8px 14px;
            border: 1px solid #e2e8f0;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
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
        
        /* Status bar */
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            max-width: 1600px;
            margin: 0 auto;
            width: 100%;
            flex-shrink: 0;
        }
        
        .issues-count {
            font-size: 0.85em;
            color: #718096;
        }
        
        .loading-status {
            font-size: 0.85em;
            color: #667eea;
        }
        
        /* Virtual scroll container */
        .virtual-scroll-container {
            flex: 1;
            overflow-y: auto;
            background: white;
            margin: 0 20px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            max-width: 1560px;
            align-self: center;
            width: calc(100% - 40px);
        }
        
        .issues-table-wrapper {
            position: relative;
        }
        
        /* Issues Table */
        .issues-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
        
        .issues-table thead {
            background: #f7fafc;
            border-bottom: 2px solid #e2e8f0;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .issues-table th {
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #4a5568;
            white-space: nowrap;
        }
        
        /* Column widths - Fixed to prevent shifting */
        .col-indicator { width: 20px; padding: 0 5px; }
        .col-file { width: 25%; }
        .col-line { width: 80px; text-align: center; }
        .col-severity { width: 120px; }
        .col-message { width: calc(100% - 25% - 80px - 120px - 100px - 80px - 20px); }
        .col-id { width: 100px; }
        .col-actions { width: 80px; text-align: center; }
        
        /* Virtual scroll viewport */
        .virtual-scroll-viewport {
            position: relative;
        }
        
        .virtual-scroll-spacer {
            width: 100%;
        }
        
        /* Issue rows */
        .issue-row {
            height: 50px;
            border-bottom: 1px solid #e2e8f0;
            transition: background 0.1s;
            cursor: pointer;
        }
        
        .issue-row:hover {
            background: #f7fafc;
        }
        
        .issue-row td {
            padding: 0 15px;
            font-size: 0.85em;
            height: 50px;
            vertical-align: middle;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        /* Code indicator - Now in separate column */
        .indicator-cell {
            width: 20px;
            padding: 0 5px !important;
        }
        
        .code-indicator {
            width: 4px;
            height: 30px;
            background: #667eea;
            border-radius: 2px;
        }
        
        .file-cell {
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9em;
            color: #4a5568;
        }
        
        .line-cell {
            font-family: 'Monaco', 'Consolas', monospace;
            color: #718096;
            text-align: center;
        }
        
        .message-cell {
            color: #2d3748;
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
        
        .severity-badge.information {
            background: #e0f2fe;
            color: #0369a1;
        }
        
        .severity-badge.unknown {
            background: #e2e8f0;
            color: #4a5568;
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
            backdrop-filter: blur(4px);
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
            font-size: 0.85em;
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
        
        .highlight-line {
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
        
        /* Scrollbar styling */
        .virtual-scroll-container::-webkit-scrollbar {
            width: 10px;
        }
        
        .virtual-scroll-container::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        .virtual-scroll-container::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 5px;
        }
        
        .virtual-scroll-container::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            body {
<<<<<<< HEAD
                font-size: 14px; /* Smaller base font on mobile */
            }
            
            .header h1 {
                font-size: 1.5em; /* Smaller header on mobile */
=======
                font-size: 14px;
>>>>>>> 7b24901 (Complete font size consistency fixes across all HTML generators)
            }
            
            .header-content {
                flex-direction: column;
                text-align: center;
            }
            
            .header-info {
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .stats-grid {
                grid-template-columns: 1fr 1fr;
            }
            
            .stat-card .value {
                font-size: 1.5em;
            }
            
            .issues-table th, .issue-row td {
                font-size: 0.85em;
                padding: 10px;
            }
            
            .filter-buttons {
                justify-content: center;
            }
            
            .col-file { width: 30%; }
            .col-message { width: calc(100% - 30% - 60px - 100px - 80px - 60px - 20px); }
        }
        
        /* Print Styles for Virtual Scroll Dashboard */
        @media print {
            /* Reset for clean printing */
            * {
                background: transparent !important;
                color: #000 !important;
                box-shadow: none !important;
                text-shadow: none !important;
            }
            
            body {
                font-size: 11pt;
                line-height: 1.4;
                font-family: Georgia, serif;
                overflow: visible !important;
            }
            
            /* Hide non-essential elements */
            .controls,
            .search-container,
            .filter-buttons,
            .actions-cell,
            .loading-status,
            #codeModal,
            button {
                display: none !important;
            }
            
            /* Header */
            .header {
                background: none !important;
                color: #000 !important;
                border-bottom: 2px solid #000;
                padding: 0 0 10px 0;
                margin-bottom: 20px;
            }
            
            /* Statistics */
            .stats-grid {
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
                page-break-inside: avoid;
            }
            
            .stat-card {
                border: 1px solid #000;
                padding: 10px;
                text-align: center;
                flex: 1;
                margin: 0 5px;
            }
            
            /* Table layout for print */
            .table-wrapper {
                overflow: visible !important;
                height: auto !important;
            }
            
            #scrollContainer {
                height: auto !important;
                overflow: visible !important;
            }
            
            .issues-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 9pt;
            }
            
            .issues-table th,
            .issues-table td {
                border: 1px solid #000;
                padding: 5px;
                text-align: left;
            }
            
            .issues-table th {
                background-color: #f0f0f0 !important;
                font-weight: bold;
            }
            
            /* Show all issues for print */
            #issuesBody tr {
                display: table-row !important;
                page-break-inside: avoid;
            }
            
            /* Spacers not needed for print */
            #spacerTop,
            #spacerBottom {
                display: none !important;
            }
            
            /* File paths */
            .file-path {
                font-family: monospace;
                font-size: 8pt;
            }
            
            /* Page setup */
            @page {
                size: A4 landscape;
                margin: 0.5in;
            }
        }
        
        /* Accessibility: Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation: none !important;
                transition: none !important;
            }
            
            .fa-spin {
                animation: none !important;
            }
        }
        
        /* Accessibility: High contrast support */
        @media (prefers-contrast: high) {
            .stat-card,
            .issues-table th,
            .issues-table td {
                border-width: 2px;
            }
            
            .severity-error { color: #cc0000; }
            .severity-warning { color: #ff6600; }
            .severity-style { color: #6600cc; }
        }
        """

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: generate-virtual-scroll-dashboard.py <analysis.json> [output.html]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'virtual-scroll-dashboard.html'
    
    generator = VirtualScrollDashboardGenerator(input_file)
    generator.generate(output_file)