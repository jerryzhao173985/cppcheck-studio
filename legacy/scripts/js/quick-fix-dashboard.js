#!/usr/bin/env node
/**
 * Quick fix for dashboard scrolling issues
 * Usage: node quick-fix-dashboard.js <dashboard.html>
 */

const fs = require('fs');

function fixDashboard(filePath) {
    console.log(`🔧 Fixing dashboard: ${filePath}`);
    
    let html = fs.readFileSync(filePath, 'utf8');
    
    // Check if the fix is already applied
    if (html.includes('// SCROLLING FIX APPLIED')) {
        console.log('✅ Dashboard already has the fix applied');
        return;
    }
    
    // Find the initialize function
    const initializePattern = /function initialize\(\) {[\s\S]*?} catch \(error\) {[\s\S]*?}\s*}/;
    const match = html.match(initializePattern);
    
    if (!match) {
        console.error('❌ Could not find initialize function');
        return;
    }
    
    // Add debug logging and ensure filterData is called
    const fixedInitialize = `function initialize() {
        try {
            // SCROLLING FIX APPLIED
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
            
            // Force an initial render after a short delay
            setTimeout(() => {
                console.log('🔄 Forcing render...');
                renderVisibleRows();
            }, 100);
            
            hideLoadingStatus();
        } catch (error) {
            console.error('Initialization error:', error);
            alert('Failed to load dashboard: ' + error.message);
        }
    }`;
    
    // Replace the initialize function
    html = html.replace(initializePattern, fixedInitialize);
    
    // Also add a debug function to manually trigger rendering
    const debugCode = `
    
    // Debug function to manually trigger rendering
    window.debugDashboard = function() {
        console.log('=== Dashboard Debug Info ===');
        console.log('All issues:', state.allIssues.length);
        console.log('Filtered issues:', state.filteredIssues.length);
        console.log('Visible range:', state.visibleStart, '-', state.visibleEnd);
        console.log('Container height:', state.containerHeight);
        console.log('Scroll top:', state.scrollTop);
        
        // Force filter and render
        filterData();
        renderVisibleRows();
        
        console.log('✅ Forced render complete');
    };
    
    // Add keyboard shortcut for debugging (Ctrl+D)
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            window.debugDashboard();
        }
    });
    </script>`;
    
    // Insert debug code before closing body tag
    html = html.replace('</script>\n</body>', debugCode + '\n</body>');
    
    // Write the fixed file
    const outputPath = filePath.replace('.html', '-fixed.html');
    fs.writeFileSync(outputPath, html, 'utf8');
    
    console.log(`✅ Fixed dashboard saved to: ${outputPath}`);
    console.log('\n📝 Instructions:');
    console.log('1. Open the fixed dashboard in your browser');
    console.log('2. Check the browser console for debug messages');
    console.log('3. If issues still don\'t show, press Ctrl+D to force render');
    console.log('4. Check console for diagnostic information');
}

// Main
if (process.argv.length < 3) {
    console.error('Usage: node quick-fix-dashboard.js <dashboard.html>');
    process.exit(1);
}

const dashboardPath = process.argv[2];
if (!fs.existsSync(dashboardPath)) {
    console.error(`Error: File not found: ${dashboardPath}`);
    process.exit(1);
}

fixDashboard(dashboardPath);