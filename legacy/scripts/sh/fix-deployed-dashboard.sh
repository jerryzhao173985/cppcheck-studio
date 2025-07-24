#!/bin/bash
# Fix deployed dashboards that are using the old format

DASHBOARD_URL="${1:-https://jerryzhao173985.github.io/cppcheck-studio/results/1753203010230-acau0p806/index.html}"
OUTPUT_FILE="${2:-fixed-deployed-dashboard.html}"

echo "🔧 Fixing deployed dashboard..."
echo "URL: $DASHBOARD_URL"

# Download the dashboard
curl -s "$DASHBOARD_URL" -o temp-dashboard.html

# Check if download was successful
if [ ! -f temp-dashboard.html ]; then
    echo "❌ Failed to download dashboard"
    exit 1
fi

# Create a fixed version with proper newline handling
cat > fix-script.js << 'EOF'
const fs = require('fs');

// Read the dashboard
let html = fs.readFileSync('temp-dashboard.html', 'utf8');

// Fix 1: Replace the loadEmbeddedData function to handle newlines properly
const fixedLoadEmbeddedData = `
        // Load embedded JSONL data
        function loadEmbeddedData() {
            try {
                // Parse issues data
                const issuesScript = document.getElementById('issuesData');
                const issuesText = issuesScript.textContent.trim();
                
                // Try multiple splitting methods to handle different formats
                let issuesLines = [];
                
                // First try splitting on actual newlines
                if (issuesText.includes('\\n')) {
                    issuesLines = issuesText.split('\\n').filter(line => line.trim());
                    console.log('Split on newline characters:', issuesLines.length);
                }
                // Then try __NEWLINE__ placeholder
                else if (issuesText.includes('__NEWLINE__')) {
                    issuesLines = issuesText.split('__NEWLINE__').filter(line => line.trim());
                    console.log('Split on __NEWLINE__ placeholder:', issuesLines.length);
                }
                // Fallback: try to extract JSON objects with regex
                else {
                    const jsonRegex = /\\{[^}]+\\}/g;
                    const matches = issuesText.match(jsonRegex) || [];
                    issuesLines = matches;
                    console.log('Extracted JSON objects with regex:', issuesLines.length);
                }
                
                state.allIssues = issuesLines.map((line, index) => {
                    try {
                        const issue = typeof line === 'string' ? JSON.parse(line) : line;
                        // Generate ID if missing
                        if (!issue.id) {
                            issue.id = 'ISSUE_' + index;
                        }
                        return issue;
                    } catch (e) {
                        console.error('Failed to parse issue line ' + index + ':', e);
                        return null;
                    }
                }).filter(Boolean);
                
                console.log('✅ Loaded', state.allIssues.length, 'issues');
                
                // Parse code context data (if exists)
                const codeScript = document.getElementById('codeContextData');
                if (codeScript) {
                    const codeText = codeScript.textContent.trim();
                    
                    let codeLines = [];
                    if (codeText.includes('\\n')) {
                        codeLines = codeText.split('\\n').filter(line => line.trim());
                    } else if (codeText.includes('__NEWLINE__')) {
                        codeLines = codeText.split('__NEWLINE__').filter(line => line.trim());
                    }
                    
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
                    
                    console.log('✅ Loaded code context for', state.codeContextMap.size, 'issues');
                } else {
                    console.log('ℹ️ No code context data found');
                }
                
                // If no issues loaded, show error
                if (state.allIssues.length === 0) {
                    throw new Error('No issues could be parsed from the data');
                }
                
            } catch (error) {
                console.error('Failed to load embedded data:', error);
                // Try to provide helpful error message
                document.getElementById('issuesCount').textContent = 'Error: Failed to load issues';
                throw error;
            }
        }`;

// Replace the loadEmbeddedData function
const loadEmbeddedDataRegex = /function loadEmbeddedData\(\)\s*{[\s\S]*?^        }/m;
html = html.replace(loadEmbeddedDataRegex, fixedLoadEmbeddedData);

// Fix 2: Add recovery mechanism if not present
if (!html.includes('window.recoverDashboard')) {
    const recoveryCode = `
    
    // Recovery function for troubleshooting
    window.recoverDashboard = function() {
        console.log('🔧 Running dashboard recovery...');
        
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
        
        // Reset state
        state.scrollTop = 0;
        state.visibleStart = 0;
        state.visibleEnd = Math.min(50, state.filteredIssues.length);
        state.containerHeight = scrollContainer.clientHeight || 600;
        
        console.log('📊 Recovery state:', {
            issues: state.allIssues.length,
            filtered: state.filteredIssues.length,
            containerHeight: state.containerHeight
        });
        
        // Re-filter and render
        filterData();
        renderVisibleRows();
        
        // Scroll to top
        scrollContainer.scrollTop = 0;
        
        console.log('✅ Recovery complete');
    };
    </script>`;
    
    // Insert before closing body tag
    html = html.replace('</script>\n</body>', '</script>' + recoveryCode + '\n</body>');
}

// Fix 3: Update the initialization to be more robust
if (!html.includes('attemptRender')) {
    const robustInit = `
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
                
                // Ensure initial render happens
                setTimeout(() => {
                    renderVisibleRows();
                    // Check if render succeeded
                    const tbody = document.getElementById('issuesBody');
                    if (state.filteredIssues.length > 0 && tbody && tbody.children.length === 0) {
                        console.warn('⚠️ No rows rendered, forcing recovery...');
                        state.containerHeight = document.getElementById('scrollContainer').clientHeight || 600;
                        renderVisibleRows();
                    }
                }, 100);
                
                hideLoadingStatus();
            } catch (error) {
                console.error('Initialization error:', error);
                document.getElementById('issuesCount').textContent = 'Error: ' + error.message;
            }
        }`;
    
    // Replace the initialize function
    const initRegex = /function initialize\(\)\s*{[\s\S]*?^        }/m;
    html = html.replace(initRegex, robustInit);
}

// Write the fixed file
fs.writeFileSync('fixed-dashboard.html', html, 'utf8');
console.log('✅ Fixed dashboard saved');
EOF

# Run the fix script
node fix-script.js

# Move the result
mv fixed-dashboard.html "$OUTPUT_FILE"

# Cleanup
rm -f temp-dashboard.html fix-script.js

echo "✅ Fixed dashboard saved to: $OUTPUT_FILE"
echo ""
echo "📝 To use the fixed dashboard:"
echo "1. Open $OUTPUT_FILE in your browser"
echo "2. Check the console for any errors"
echo "3. If issues still don't show, press F12 and run: recoverDashboard()"