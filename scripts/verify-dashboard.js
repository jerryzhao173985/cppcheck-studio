#!/usr/bin/env node

/**
 * Verify that a dashboard file contains the expected structure
 */

const fs = require('fs');
const path = require('path');

function verifyDashboard(filePath) {
    try {
        // Check if file exists
        if (!fs.existsSync(filePath)) {
            console.error(`❌ Dashboard file not found: ${filePath}`);
            process.exit(1);
        }

        // Read file content
        const content = fs.readFileSync(filePath, 'utf8');
        const fileName = path.basename(filePath);

        console.log(`📋 Verifying dashboard: ${fileName}`);

        // Check for essential elements
        const checks = {
            'HTML structure': content.includes('<!DOCTYPE html>') && content.includes('</html>'),
            'Issues data': content.includes('issuesData') || content.includes('const issues ='),
            'Virtual scrolling': content.includes('virtual-scroll') || content.includes('VirtualScroll'),
            'Search functionality': content.includes('searchIssues') || content.includes('filterData'),
            'Severity filters': content.includes('filterBySeverity') || content.includes('severity-filter'),
            'Code context': content.includes('codeContext') || content.includes('code_context'),
            'Statistics': content.includes('stats') || content.includes('statistics')
        };

        let allPassed = true;
        for (const [check, passed] of Object.entries(checks)) {
            if (passed) {
                console.log(`✅ ${check}`);
            } else {
                console.log(`⚠️  ${check} - not found`);
                allPassed = false;
            }
        }

        // Get file size
        const stats = fs.statSync(filePath);
        const fileSizeInMB = (stats.size / (1024 * 1024)).toFixed(2);
        console.log(`📊 File size: ${fileSizeInMB} MB`);

        // Count issues if possible
        const issuesMatch = content.match(/const issues = (\[[\s\S]*?\]);/);
        if (issuesMatch) {
            try {
                const issues = eval(issuesMatch[1]);
                console.log(`📈 Total issues: ${issues.length}`);
            } catch (e) {
                // Ignore if we can't parse
            }
        }

        if (allPassed) {
            console.log(`\n✅ Dashboard verification passed!`);
            process.exit(0);
        } else {
            console.log(`\n⚠️  Dashboard verification completed with warnings`);
            process.exit(0); // Don't fail the build
        }

    } catch (error) {
        console.error(`❌ Error verifying dashboard: ${error.message}`);
        process.exit(1);
    }
}

// Main
if (process.argv.length < 3) {
    console.error('Usage: node verify-dashboard.js <dashboard-file>');
    process.exit(1);
}

const dashboardFile = process.argv[2];
verifyDashboard(dashboardFile);