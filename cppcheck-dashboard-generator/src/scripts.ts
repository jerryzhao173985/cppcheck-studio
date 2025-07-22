/**
 * JavaScript functionality for the virtual scroll dashboard
 */

export function generateScripts(): string {
  return `
    // Configuration
    const CONFIG = {
        ROW_HEIGHT: 50,
        VISIBLE_BUFFER: 5,
        SCROLL_DEBOUNCE: 10,
        SEARCH_DEBOUNCE: 300,
        BATCH_SIZE: 50
    };
    
    // Global state
    const state = {
        allIssues: [],
        filteredIssues: [],
        codeContextMap: new Map(),
        currentFilter: 'all',
        currentSearch: '',
        visibleStart: 0,
        visibleEnd: 0,
        isLoading: false,
        scrollTop: 0,
        containerHeight: 0
    };
    
    // Initialize
    function initialize() {
        try {
            console.log('🚀 Dashboard initializing...');
            showLoadingStatus('Loading issues data...');
            
            // Load issues from embedded JSONL
            loadEmbeddedData();
            console.log('📊 Loaded ' + state.allIssues.length + ' issues');
            
            // Set up virtual scrolling
            setupVirtualScroll();
            
            // Initial render - CRITICAL FOR SCROLLING
            filterData();
            console.log('🎯 Filtered ' + state.filteredIssues.length + ' issues');
            
            // Multiple recovery attempts to ensure rendering
            const attemptRender = (attempt = 1) => {
                renderVisibleRows();
                const tbody = document.getElementById('issuesBody');
                
                if (state.filteredIssues.length > 0 && tbody && tbody.children.length === 0) {
                    console.warn(\`⚠️ Attempt \${attempt}: No rows rendered, retrying...\`);
                    
                    // Force container height recalculation
                    const scrollContainer = document.getElementById('scrollContainer');
                    if (scrollContainer) {
                        const rect = scrollContainer.getBoundingClientRect();
                        state.containerHeight = Math.max(400, rect.height || 600);
                        console.log('Recalculated container height:', state.containerHeight);
                    }
                    
                    if (attempt < 3) {
                        setTimeout(() => attemptRender(attempt + 1), 200 * attempt);
                    } else {
                        console.error('❌ Failed to render after 3 attempts');
                        // Force manual recovery
                        window.recoverDashboard();
                    }
                } else if (tbody && tbody.children.length > 0) {
                    console.log('✅ Successfully rendered ' + tbody.children.length + ' rows');
                }
            };
            
            // Start render attempts after DOM settles
            setTimeout(() => attemptRender(), 100);
            
            hideLoadingStatus();
        } catch (error) {
            console.error('Initialization error:', error);
            alert('Failed to load dashboard: ' + error.message);
        }
    }
    
    // Load embedded JSONL data
    function loadEmbeddedData() {
        try {
            // Parse issues data
            const issuesScript = document.getElementById('issuesData');
            const issuesText = issuesScript.textContent.trim();
            const issuesLines = issuesText.split('__NEWLINE__').filter(line => line.trim());
            
            state.allIssues = issuesLines.map(line => {
                try {
                    return JSON.parse(line);
                } catch (e) {
                    console.error('Failed to parse issue line:', e);
                    return null;
                }
            }).filter(Boolean);
            
            // Successfully loaded issues
            
            // Parse code context data
            const codeScript = document.getElementById('codeContextData');
            const codeText = codeScript.textContent.trim();
            const codeLines = codeText.split('__NEWLINE__').filter(line => line.trim());
            
            codeLines.forEach(line => {
                try {
                    const data = JSON.parse(line);
                    if (data.id && data.code_context) {
                        state.codeContextMap.set(data.id, data.code_context);
                    }
                } catch (e) {
                    console.error('Failed to parse code context:', e);
                }
            });
            
            // Successfully loaded code context
            
        } catch (error) {
            console.error('Failed to load embedded data:', error);
            throw error;
        }
    }
    
    // Set up virtual scrolling
    function setupVirtualScroll() {
        const viewport = document.getElementById('viewport');
        const scrollContainer = document.getElementById('scrollContainer');
        
        if (!scrollContainer) {
            console.error('❌ Scroll container not found!');
            return;
        }
        
        // Update container height on resize
        const updateContainerHeight = () => {
            const rect = scrollContainer.getBoundingClientRect();
            const computedStyle = window.getComputedStyle(scrollContainer);
            const paddingTop = parseFloat(computedStyle.paddingTop) || 0;
            const paddingBottom = parseFloat(computedStyle.paddingBottom) || 0;
            
            // Calculate actual available height
            const availableHeight = rect.height - paddingTop - paddingBottom;
            
            // Ensure minimum height for proper scrolling
            state.containerHeight = Math.max(400, availableHeight || 600);
            
            console.log('📏 Container measurements:', {
                rect: { width: rect.width, height: rect.height },
                padding: { top: paddingTop, bottom: paddingBottom },
                calculated: state.containerHeight,
                scrollHeight: scrollContainer.scrollHeight,
                clientHeight: scrollContainer.clientHeight
            });
            
            renderVisibleRows();
        };
        
        // Initial setup with multiple attempts
        const setupAttempt = (attempt = 1) => {
            updateContainerHeight();
            
            if (state.containerHeight <= 0 && attempt < 3) {
                console.warn(\`⚠️ Container height is \${state.containerHeight}, retrying... (attempt \${attempt})\`);
                setTimeout(() => setupAttempt(attempt + 1), 100 * attempt);
            }
        };
        
        setupAttempt();
        window.addEventListener('resize', updateContainerHeight);
        
        // Handle scroll events
        scrollContainer.addEventListener('scroll', debounce(() => {
            state.scrollTop = scrollContainer.scrollTop;
            renderVisibleRows();
        }, CONFIG.SCROLL_DEBOUNCE));
    }
    
    // Render visible rows based on scroll position
    function renderVisibleRows() {
        // Safety check
        if (!state.filteredIssues || state.filteredIssues.length === 0) {
            console.log('📋 No issues to render');
            return;
        }
        
        // Ensure container height is valid
        if (!state.containerHeight || state.containerHeight <= 0) {
            console.warn('⚠️ Invalid container height:', state.containerHeight);
            const scrollContainer = document.getElementById('scrollContainer');
            if (scrollContainer) {
                state.containerHeight = scrollContainer.clientHeight || 600;
                console.log('📏 Recalculated container height:', state.containerHeight);
            }
        }
        
        const totalHeight = state.filteredIssues.length * CONFIG.ROW_HEIGHT;
        const visibleStart = Math.floor(state.scrollTop / CONFIG.ROW_HEIGHT) - CONFIG.VISIBLE_BUFFER;
        const visibleEnd = Math.ceil((state.scrollTop + state.containerHeight) / CONFIG.ROW_HEIGHT) + CONFIG.VISIBLE_BUFFER;
        
        state.visibleStart = Math.max(0, visibleStart);
        state.visibleEnd = Math.min(state.filteredIssues.length, visibleEnd);
        
        // Debug logging
        if (state.visibleEnd - state.visibleStart > 0) {
            console.log('🎯 Rendering rows:', {
                total: state.filteredIssues.length,
                visible: [state.visibleStart, state.visibleEnd],
                count: state.visibleEnd - state.visibleStart,
                scrollTop: state.scrollTop,
                containerHeight: state.containerHeight
            });
        }
        
        // Update spacers
        const spacerTop = document.getElementById('spacerTop');
        const spacerBottom = document.getElementById('spacerBottom');
        
        if (spacerTop) spacerTop.style.height = (state.visibleStart * CONFIG.ROW_HEIGHT) + 'px';
        if (spacerBottom) spacerBottom.style.height = 
            ((state.filteredIssues.length - state.visibleEnd) * CONFIG.ROW_HEIGHT) + 'px';
        
        // Get visible issues
        const visibleIssues = state.filteredIssues.slice(state.visibleStart, state.visibleEnd);
        
        // Render rows
        const tbody = document.getElementById('issuesBody');
        if (!tbody) {
            console.error('❌ Issues tbody not found!');
            return;
        }
        
        tbody.innerHTML = '';
        
        visibleIssues.forEach((issue, index) => {
            const row = createIssueRow(issue, state.visibleStart + index);
            tbody.appendChild(row);
        });
        
        console.log('✅ Rendered ' + visibleIssues.length + ' rows');
    }
    
    // Create issue row
    function createIssueRow(issue, globalIndex) {
        const row = document.createElement('tr');
        row.className = 'issue-row';
        row.dataset.id = issue.id;
        
        const hasCodeContext = state.codeContextMap.has(issue.id);
        
        // Indicator cell (for code context)
        const indicatorCell = document.createElement('td');
        indicatorCell.className = 'indicator-cell';
        if (hasCodeContext) {
            indicatorCell.innerHTML = '<div class="code-indicator"></div>';
        }
        
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
        actionBtn.onclick = (e) => {
            e.stopPropagation();
            showIssueDetails(issue, globalIndex);
        };
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
    }
    
    // Filter data based on search and severity
    function filterData() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        state.currentSearch = searchTerm;
        
        state.filteredIssues = state.allIssues.filter(issue => {
            // Severity filter
            if (state.currentFilter !== 'all' && issue.severity !== state.currentFilter) {
                return false;
            }
            
            // Search filter
            if (searchTerm) {
                const matchFile = (issue.file || '').toLowerCase().includes(searchTerm);
                const matchMessage = (issue.message || '').toLowerCase().includes(searchTerm);
                const matchId = (issue.id || '').toLowerCase().includes(searchTerm);
                return matchFile || matchMessage || matchId;
            }
            
            return true;
        });
        
        // Update count
        updateIssueCount();
        
        // Reset scroll and render
        document.getElementById('scrollContainer').scrollTop = 0;
        state.scrollTop = 0;
        renderVisibleRows();
    }
    
    // Update issue count display
    function updateIssueCount() {
        const countEl = document.getElementById('issuesCount');
        const filtered = state.filteredIssues.length;
        const total = state.allIssues.length;
        
        if (filtered === total) {
            countEl.textContent = \`Showing all \${total} issues\`;
        } else {
            countEl.textContent = \`Showing \${filtered} of \${total} issues\`;
        }
    }
    
    // Set severity filter
    function setSeverityFilter(severity, button) {
        state.currentFilter = severity;
        
        // Update button states
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');
        
        filterData();
    }
    
    // Show issue details modal
    function showIssueDetails(issue, index) {
        const modal = document.getElementById('codeModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        
        modalTitle.innerHTML = '<i class="fas fa-file-code"></i> ' + 
            escapeHtml(getFileName(issue.file || 'Unknown')) + ':' + (issue.line || '?');
        
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
        
        if (codeContext && codeContext.lines && codeContext.lines.length > 0) {
            content += '<div class="code-preview"><pre><code class="language-cpp">';
            
            codeContext.lines.forEach(line => {
                const isTarget = line.is_target === true;
                const lineNum = String(line.number || 0).padStart(4, ' ');
                const lineContent = escapeHtml(line.content || '');
                
                if (isTarget) {
                    content += '<span class="highlight-line">' + lineNum + ': ' + lineContent + '</span>\\\\n';
                } else {
                    content += lineNum + ': ' + lineContent + '\\\\n';
                }
            });
            
            content += '</code></pre></div>';
        } else {
            content += '<div class="no-code-message">';
            content += '<i class="fas fa-info-circle"></i>';
            content += '<p>Code context not available for this issue.</p>';
            content += '</div>';
        }
        
        content += '</div></div>';
        
        modalBody.innerHTML = content;
        modal.style.display = 'block';
    }
    
    // Helper functions
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function getFileName(path) {
        if (!path) return 'Unknown';
        const parts = path.split('/');
        return parts[parts.length - 1];
    }
    
    function truncateMessage(message) {
        const maxLength = 80;
        if (message && message.length > maxLength) {
            return message.substring(0, maxLength - 3) + '...';
        }
        return message || '';
    }
    
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
    
    function showLoadingStatus(text) {
        document.getElementById('loadingStatus').style.display = 'block';
        document.getElementById('loadingText').textContent = text;
    }
    
    function hideLoadingStatus() {
        document.getElementById('loadingStatus').style.display = 'none';
    }
    
    function closeModal() {
        document.getElementById('codeModal').style.display = 'none';
    }
    
    // Close modal on outside click
    window.onclick = function(event) {
        const modal = document.getElementById('codeModal');
        if (event.target === modal) {
            closeModal();
        }
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }
    
    // Make functions available globally for inline event handlers
    window.filterData = filterData;
    window.setSeverityFilter = setSeverityFilter;
    window.closeModal = closeModal;
    window.debounce = debounce;
    
    // Recovery function for troubleshooting
    window.recoverDashboard = function() {
        console.log('🔧 Running comprehensive dashboard recovery...');
        
        // Force recalculate container dimensions
        const scrollContainer = document.getElementById('scrollContainer');
        if (!scrollContainer) {
            console.error('❌ Scroll container not found!');
            return;
        }
        
        // Ensure container has proper height
        if (!scrollContainer.style.height || scrollContainer.style.height === '0px') {
            scrollContainer.style.height = '600px';
            scrollContainer.style.minHeight = '400px';
            console.log('📐 Applied default container height');
        }
        
        // Get fresh measurements
        const rect = scrollContainer.getBoundingClientRect();
        const computedStyle = window.getComputedStyle(scrollContainer);
        
        // Reset state with valid values
        state.scrollTop = 0;
        state.visibleStart = 0;
        state.visibleEnd = Math.min(50, state.filteredIssues.length);
        state.containerHeight = Math.max(400, rect.height || 600);
        
        console.log('📊 Recovery state:', {
            issues: state.allIssues.length,
            filtered: state.filteredIssues.length,
            containerHeight: state.containerHeight,
            containerStyle: {
                height: computedStyle.height,
                minHeight: computedStyle.minHeight,
                maxHeight: computedStyle.maxHeight,
                overflow: computedStyle.overflow
            }
        });
        
        // Re-filter and render
        filterData();
        
        // Force multiple render attempts
        let rendered = false;
        for (let i = 0; i < 3; i++) {
            renderVisibleRows();
            const tbody = document.getElementById('issuesBody');
            if (tbody && tbody.children.length > 0) {
                rendered = true;
                break;
            }
            console.log(\`Recovery render attempt \${i + 1} failed, retrying...\`);
        }
        
        // Scroll to top
        scrollContainer.scrollTop = 0;
        
        console.log(rendered ? '✅ Recovery complete!' : '❌ Recovery failed after 3 attempts');
        console.log('Final state:', {
            rowsRendered: document.getElementById('issuesBody').children.length,
            containerHeight: state.containerHeight,
            scrollHeight: scrollContainer.scrollHeight
        });
        
        // Provide diagnostic info if recovery failed
        if (!rendered) {
            console.log('🔍 Diagnostic info:');
            console.log('- Issues data present:', state.allIssues.length > 0);
            console.log('- Filtered issues:', state.filteredIssues.length);
            console.log('- Container found:', !!scrollContainer);
            console.log('- Tbody found:', !!document.getElementById('issuesBody'));
            console.log('- Spacers found:', !!document.getElementById('spacerTop'), !!document.getElementById('spacerBottom'));
        }
    };
  `;
}
