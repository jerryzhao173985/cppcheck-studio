#!/usr/bin/env node
/**
 * Fix scrolling issues in all deployed dashboards
 * This addresses the root cause: container height calculation
 */

const fs = require('fs');
const path = require('path');

function fixDashboard(filePath) {
    let html = fs.readFileSync(filePath, 'utf8');
    
    // Check if already fixed
    if (html.includes('// COMPREHENSIVE FIX APPLIED')) {
        return false;
    }
    
    // Fix 1: Ensure container height is calculated correctly
    const setupVirtualScrollPattern = /function setupVirtualScroll\(\) {[\s\S]*?window\.addEventListener\('resize', updateContainerHeight\);/;
    const fixedSetupVirtualScroll = `function setupVirtualScroll() {
        // COMPREHENSIVE FIX APPLIED
        const viewport = document.getElementById('viewport');
        const scrollContainer = document.getElementById('scrollContainer');
        
        // Update container height on resize
        const updateContainerHeight = () => {
            // Fix: Ensure minimum height and proper calculation
            const rect = scrollContainer.getBoundingClientRect();
            state.containerHeight = Math.max(400, rect.height - 100); // Minimum 400px
            console.log('Container height updated:', state.containerHeight);
            renderVisibleRows();
        };
        
        updateContainerHeight();
        window.addEventListener('resize', updateContainerHeight);`;
    
    html = html.replace(setupVirtualScrollPattern, fixedSetupVirtualScroll);
    
    // Fix 2: Ensure renderVisibleRows handles empty state properly
    const renderVisibleRowsPattern = /function renderVisibleRows\(\) {[\s\S]*?state\.visibleEnd = Math\.min\(state\.filteredIssues\.length, visibleEnd\);/;
    
    if (renderVisibleRowsPattern.test(html)) {
        const fixedRenderVisibleRows = `function renderVisibleRows() {
        // Ensure we have issues to render
        if (!state.filteredIssues || state.filteredIssues.length === 0) {
            console.warn('No filtered issues to render');
            return;
        }
        
        const totalHeight = state.filteredIssues.length * CONFIG.ROW_HEIGHT;
        const visibleStart = Math.floor(state.scrollTop / CONFIG.ROW_HEIGHT) - CONFIG.VISIBLE_BUFFER;
        const visibleEnd = Math.ceil((state.scrollTop + state.containerHeight) / CONFIG.ROW_HEIGHT) + CONFIG.VISIBLE_BUFFER;
        
        state.visibleStart = Math.max(0, visibleStart);
        state.visibleEnd = Math.min(state.filteredIssues.length, visibleEnd);`;
        
        html = html.replace(renderVisibleRowsPattern, fixedRenderVisibleRows);
    }
    
    // Fix 3: Add explicit height to virtual scroll container
    const containerStylePattern = /\.virtual-scroll-container\s*{\s*([^}]+)}/;
    const containerStyleMatch = html.match(containerStylePattern);
    
    if (containerStyleMatch && !containerStyleMatch[1].includes('min-height')) {
        const updatedStyle = `.virtual-scroll-container {${containerStyleMatch[1]}
        min-height: 400px;
        height: calc(100vh - 300px);
    }`;
        html = html.replace(containerStylePattern, updatedStyle);
    }
    
    // Fix 4: Add recovery mechanism
    const recoveryCode = `
    // Auto-recovery mechanism
    setTimeout(() => {
        if (state.filteredIssues.length > 0 && document.getElementById('issuesBody').children.length === 0) {
            console.warn('⚠️ No rows rendered, forcing recovery...');
            state.containerHeight = 600; // Force reasonable height
            renderVisibleRows();
        }
    }, 500);
    
    // Manual recovery function
    window.recoverDashboard = function() {
        console.log('🔧 Running dashboard recovery...');
        
        // Reset state
        state.scrollTop = 0;
        state.visibleStart = 0;
        state.visibleEnd = 50;
        state.containerHeight = document.getElementById('scrollContainer').clientHeight || 600;
        
        // Re-filter and render
        filterData();
        renderVisibleRows();
        
        // Scroll to top
        document.getElementById('scrollContainer').scrollTop = 0;
        
        console.log('✅ Recovery complete');
        console.log('Issues to render:', state.filteredIssues.length);
        console.log('Rows rendered:', document.getElementById('issuesBody').children.length);
    };
    </script>`;
    
    // Insert recovery code
    html = html.replace('</script>\n</body>', recoveryCode + '\n</body>');
    
    fs.writeFileSync(filePath, html, 'utf8');
    return true;
}

// Fix a single file or directory
const target = process.argv[2];

if (!target) {
    console.log('Usage: node fix-all-dashboards.js <file-or-directory>');
    process.exit(1);
}

if (fs.statSync(target).isDirectory()) {
    // Fix all HTML files in directory
    let fixed = 0;
    const files = fs.readdirSync(target);
    
    files.forEach(file => {
        if (file.endsWith('.html')) {
            const filePath = path.join(target, file);
            if (fixDashboard(filePath)) {
                console.log(`✅ Fixed: ${file}`);
                fixed++;
            }
        }
    });
    
    console.log(`\n🎉 Fixed ${fixed} dashboards`);
} else {
    // Fix single file
    if (fixDashboard(target)) {
        console.log(`✅ Fixed: ${target}`);
    } else {
        console.log('ℹ️  Dashboard already has fixes applied');
    }
}

console.log('\n📝 If issues persist:');
console.log('1. Open browser console (F12)');
console.log('2. Run: recoverDashboard()');
console.log('3. Check for error messages');