#!/usr/bin/env node
/**
 * Debug script for dashboards hanging at "Loading..."
 * This adds extensive error handling and logging
 */

const fs = require('fs');
const path = require('path');

function fixHangingDashboard(filePath) {
    console.log(`🔧 Fixing hanging dashboard: ${filePath}`);
    
    let html = fs.readFileSync(filePath, 'utf8');
    
    // Add comprehensive error handling to initialization
    const enhancedInitialize = `
    // HANGING FIX APPLIED
    function initialize() {
        console.log('🚀 Dashboard initializing (with hanging fix)...');
        
        try {
            // Show loading status
            const loadingEl = document.getElementById('loadingStatus');
            if (loadingEl) loadingEl.style.display = 'block';
            
            // Load issues with error handling
            try {
                loadEmbeddedData();
                console.log('📊 Data loaded successfully');
            } catch (dataError) {
                console.error('❌ Failed to load data:', dataError);
                document.getElementById('issuesCount').textContent = 'Error loading data';
                throw dataError;
            }
            
            // Set up virtual scrolling with error handling
            try {
                setupVirtualScroll();
                console.log('📜 Virtual scroll setup complete');
            } catch (scrollError) {
                console.error('❌ Failed to setup virtual scroll:', scrollError);
                // Continue anyway - data might still be viewable
            }
            
            // Filter data with error handling
            try {
                filterData();
                console.log('🎯 Data filtered successfully');
            } catch (filterError) {
                console.error('❌ Failed to filter data:', filterError);
                // Try to show all data unfiltered
                state.filteredIssues = state.allIssues;
            }
            
            // Hide loading status
            if (loadingEl) loadingEl.style.display = 'none';
            
            // Render with multiple attempts
            let renderSuccess = false;
            for (let attempt = 1; attempt <= 5; attempt++) {
                console.log(\`🔄 Render attempt \${attempt}/5...\`);
                
                try {
                    // Ensure container height
                    const scrollContainer = document.getElementById('scrollContainer');
                    if (scrollContainer && (!state.containerHeight || state.containerHeight <= 0)) {
                        state.containerHeight = scrollContainer.clientHeight || 600;
                        console.log('📏 Set container height:', state.containerHeight);
                    }
                    
                    renderVisibleRows();
                    
                    const tbody = document.getElementById('issuesBody');
                    if (tbody && tbody.children.length > 0) {
                        console.log(\`✅ Successfully rendered \${tbody.children.length} rows\`);
                        renderSuccess = true;
                        break;
                    }
                } catch (renderError) {
                    console.error(\`❌ Render attempt \${attempt} failed:\`, renderError);
                }
                
                // Wait before retry
                if (attempt < 5) {
                    await new Promise(resolve => setTimeout(resolve, 200 * attempt));
                }
            }
            
            if (!renderSuccess) {
                console.error('❌ All render attempts failed');
                document.getElementById('issuesCount').textContent = 'Error: Could not render issues';
                
                // Show diagnostic info
                console.log('🔍 Diagnostic info:');
                console.log('- All issues:', state.allIssues.length);
                console.log('- Filtered issues:', state.filteredIssues.length);
                console.log('- Container height:', state.containerHeight);
                console.log('- First issue:', state.allIssues[0]);
            }
            
        } catch (error) {
            console.error('💥 Critical initialization error:', error);
            console.error('Stack trace:', error.stack);
            
            // Update UI to show error
            const countEl = document.getElementById('issuesCount');
            if (countEl) {
                countEl.textContent = 'Error: ' + error.message;
            }
            
            // Don't show alert - just log
            console.error('Dashboard initialization failed:', error);
        }
    }
    
    // Make initialization async to support await
    async function initializeAsync() {
        await initialize();
    }
    
    // Replace DOMContentLoaded handler
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeAsync);
    } else {
        initializeAsync();
    }`;
    
    // Find and replace the initialize function
    const initPattern = /function initialize\(\)\s*{[\s\S]*?}\s*}\s*}/;
    const match = html.match(initPattern);
    
    if (match) {
        // Replace the entire initialize function
        const beforeInit = html.substring(0, match.index);
        const afterInit = html.substring(match.index + match[0].length);
        
        // Find where DOMContentLoaded is set up
        const domReadyPattern = /if\s*\(document\.readyState[\s\S]*?else\s*{\s*initialize\(\);\s*}/;
        const cleanedAfter = afterInit.replace(domReadyPattern, '');
        
        html = beforeInit + enhancedInitialize + cleanedAfter;
    } else {
        console.error('❌ Could not find initialize function');
        return;
    }
    
    // Add emergency data display function
    const emergencyDisplay = `
    
    // Emergency function to force display data
    window.emergencyShowData = function() {
        console.log('🚨 Emergency data display activated');
        
        try {
            // Get the data directly
            const issuesScript = document.getElementById('issuesData');
            const issuesText = issuesScript.textContent.trim();
            const lines = issuesText.split('\\n').filter(line => line.trim());
            
            console.log(\`Found \${lines.length} data lines\`);
            
            // Parse issues
            const issues = [];
            lines.forEach((line, index) => {
                try {
                    const issue = JSON.parse(line);
                    issues.push(issue);
                } catch (e) {
                    console.error(\`Failed to parse line \${index}:\`, e);
                }
            });
            
            console.log(\`Parsed \${issues.length} issues\`);
            
            // Force display
            state.allIssues = issues;
            state.filteredIssues = issues;
            state.containerHeight = 600;
            state.visibleStart = 0;
            state.visibleEnd = Math.min(50, issues.length);
            
            // Update count
            document.getElementById('issuesCount').textContent = \`Showing all \${issues.length} issues (emergency mode)\`;
            
            // Force render
            const tbody = document.getElementById('issuesBody');
            tbody.innerHTML = '';
            
            issues.slice(0, 50).forEach((issue, index) => {
                const row = document.createElement('tr');
                row.innerHTML = \`
                    <td></td>
                    <td>\${issue.file || 'Unknown'}</td>
                    <td>\${issue.line || '-'}</td>
                    <td><span class="severity-badge \${issue.severity}">\${issue.severity}</span></td>
                    <td>\${issue.message || 'No message'}</td>
                    <td>\${issue.id || '-'}</td>
                    <td><button onclick="alert('Issue: ' + '\${issue.id}')">View</button></td>
                \`;
                tbody.appendChild(row);
            });
            
            console.log('✅ Emergency display complete');
            
        } catch (error) {
            console.error('❌ Emergency display failed:', error);
        }
    };
    </script>`;
    
    // Insert emergency function before closing body tag
    html = html.replace('</script>\n</body>', '</script>' + emergencyDisplay + '\n</body>');
    
    // Save the fixed file
    const outputPath = filePath.replace('.html', '-hanging-fix.html');
    fs.writeFileSync(outputPath, html, 'utf8');
    
    console.log(`✅ Fixed dashboard saved to: ${outputPath}`);
    console.log('\n📝 Instructions:');
    console.log('1. Open the fixed dashboard in your browser');
    console.log('2. Open the browser console (F12)');
    console.log('3. Look for error messages during initialization');
    console.log('4. If still hanging, run: emergencyShowData()');
}

// Main
const target = process.argv[2];
if (!target) {
    console.error('Usage: node debug-dashboard-hanging.js <dashboard.html>');
    process.exit(1);
}

if (!fs.existsSync(target)) {
    console.error(`File not found: ${target}`);
    process.exit(1);
}

fixHangingDashboard(target);