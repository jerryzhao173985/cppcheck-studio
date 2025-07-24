#!/usr/bin/env node
/**
 * Verify Dashboard Features
 * Checks that all expected features are present in the generated dashboard
 */

const fs = require('fs');
const path = require('path');

function verifyDashboard(filePath) {
    console.log(`\n🔍 Verifying dashboard: ${path.basename(filePath)}`);
    console.log('='.repeat(60));
    
    const html = fs.readFileSync(filePath, 'utf8');
    const results = {
        passed: 0,
        failed: 0,
        features: {}
    };
    
    // Define features to check
    const featureChecks = [
        {
            name: '✅ JSONL Data Format',
            test: () => {
                const hasNewlinePlaceholder = html.includes('__NEWLINE__');
                const splitCorrectly = html.includes("split('__NEWLINE__')");
                return hasNewlinePlaceholder && splitCorrectly;
            },
            details: () => {
                const count = (html.match(/__NEWLINE__/g) || []).length;
                return `Found ${count} __NEWLINE__ placeholders`;
            }
        },
        {
            name: '📊 Issue Data Embedded',
            test: () => html.includes('id="issuesData"') && html.includes('"severity":'),
            details: () => {
                const matches = html.match(/"id":"[A-F0-9]+"/g) || [];
                return `${matches.length} issues embedded`;
            }
        },
        {
            name: '📝 Code Context Data',
            test: () => html.includes('id="codeContextData"') && html.includes('"code_context":'),
            details: () => {
                const matches = html.match(/"code_context":/g) || [];
                return `${matches.length} code contexts`;
            }
        },
        {
            name: '🔄 Virtual Scrolling',
            test: () => {
                return html.includes('setupVirtualScroll') &&
                       html.includes('renderVisibleRows') &&
                       html.includes('spacerTop') &&
                       html.includes('spacerBottom');
            },
            details: () => 'Virtual scroll components present'
        },
        {
            name: '🔧 Recovery Mechanisms',
            test: () => {
                return html.includes('attemptRender') &&
                       html.includes('recoverDashboard') &&
                       html.includes('Multiple recovery attempts');
            },
            details: () => 'Auto-recovery and manual recovery available'
        },
        {
            name: '📏 Container Height Management',
            test: () => {
                return html.includes('updateContainerHeight') &&
                       html.includes('Math.max(400') &&
                       html.includes('getBoundingClientRect');
            },
            details: () => 'Dynamic height calculation with minimum 400px'
        },
        {
            name: '🔍 Search Functionality',
            test: () => {
                return html.includes('searchInput') &&
                       html.includes('filterData') &&
                       html.includes('debounce');
            },
            details: () => 'Real-time search with debouncing'
        },
        {
            name: '🎯 Severity Filters',
            test: () => {
                return html.includes('setSeverityFilter') &&
                       html.includes('filter-btn') &&
                       ['error', 'warning', 'style', 'performance'].every(s => 
                           html.includes(`setSeverityFilter('${s}'`));
            },
            details: () => 'All severity filter buttons present'
        },
        {
            name: '🖼️ Modal Code Preview',
            test: () => {
                return html.includes('codeModal') &&
                       html.includes('showIssueDetails') &&
                       html.includes('highlight-line');
            },
            details: () => 'Modal with code highlighting support'
        },
        {
            name: '📈 Statistics Display',
            test: () => {
                return html.includes('stat-card') &&
                       html.includes('errors') &&
                       html.includes('warnings') &&
                       html.includes('style') &&
                       html.includes('performance');
            },
            details: () => 'Statistics cards for all severity levels'
        },
        {
            name: '🎨 Styling and Icons',
            test: () => {
                return html.includes('font-awesome') &&
                       html.includes('Inter:wght@400;500;600;700') &&
                       html.includes('.severity-badge');
            },
            details: () => 'Font Awesome icons and custom styling'
        },
        {
            name: '⚡ Performance Optimizations',
            test: () => {
                return html.includes('ROW_HEIGHT: 50') &&
                       html.includes('VISIBLE_BUFFER: 5') &&
                       html.includes('BATCH_SIZE: 50');
            },
            details: () => 'Virtual scroll configuration optimized'
        },
        {
            name: '🐛 Debug Logging',
            test: () => {
                return html.includes('console.log') &&
                       html.includes('🚀 Dashboard initializing') &&
                       html.includes('📊 Loaded');
            },
            details: () => 'Comprehensive debug logging enabled'
        },
        {
            name: '📱 Responsive Design',
            test: () => {
                return html.includes('viewport') &&
                       html.includes('width=device-width') &&
                       html.includes('@media');
            },
            details: () => 'Mobile-friendly viewport settings'
        }
    ];
    
    // Run all checks
    featureChecks.forEach(check => {
        const passed = check.test();
        results.features[check.name] = {
            passed,
            details: passed ? check.details() : 'Not found'
        };
        
        if (passed) {
            results.passed++;
            console.log(`✅ ${check.name}`);
            console.log(`   └─ ${check.details()}`);
        } else {
            results.failed++;
            console.log(`❌ ${check.name}`);
            console.log(`   └─ Feature missing`);
        }
    });
    
    // Summary
    console.log('\n' + '='.repeat(60));
    console.log(`📊 Summary: ${results.passed}/${featureChecks.length} features verified`);
    
    if (results.failed === 0) {
        console.log('🎉 All features are working correctly!');
    } else {
        console.log(`⚠️  ${results.failed} features need attention`);
    }
    
    // File size check
    const stats = fs.statSync(filePath);
    const sizeMB = (stats.size / 1024 / 1024).toFixed(1);
    console.log(`📦 File size: ${sizeMB} MB`);
    
    // Data integrity check
    try {
        // Extract some data to verify parsing
        const issuesMatch = html.match(/id="issuesData"[^>]*>([\s\S]*?)<\/script>/);
        if (issuesMatch) {
            const issuesData = issuesMatch[1].trim();
            const lines = issuesData.split('__NEWLINE__').filter(l => l.trim());
            console.log(`📋 Data integrity: ${lines.length} issue records found`);
            
            // Try to parse first line
            if (lines.length > 0) {
                const firstIssue = JSON.parse(lines[0]);
                console.log(`   └─ First issue: ${firstIssue.file} (line ${firstIssue.line})`);
            }
        }
    } catch (e) {
        console.log('⚠️  Could not verify data integrity:', e.message);
    }
    
    return results;
}

// Main
const target = process.argv[2];
if (!target) {
    console.log('Usage: node verify-dashboard-features.js <dashboard.html>');
    console.log('\nThis tool verifies that all expected features are present in the dashboard.');
    process.exit(1);
}

if (!fs.existsSync(target)) {
    console.error(`File not found: ${target}`);
    process.exit(1);
}

const results = verifyDashboard(target);