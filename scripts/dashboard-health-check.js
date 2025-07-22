#!/usr/bin/env node
/**
 * Dashboard Health Check
 * Verifies that a dashboard is functioning correctly
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

async function checkDashboard(filePath) {
    console.log(`🔍 Checking dashboard: ${filePath}`);
    
    const html = fs.readFileSync(filePath, 'utf8');
    const dom = new JSDOM(html, { 
        runScripts: 'dangerously',
        resources: 'usable',
        beforeParse(window) {
            // Mock console for capturing logs
            window.console = {
                log: (...args) => console.log('[Dashboard]', ...args),
                warn: (...args) => console.warn('[Dashboard]', ...args),
                error: (...args) => console.error('[Dashboard]', ...args),
            };
        }
    });
    
    const window = dom.window;
    const document = window.document;
    
    // Wait for initialization
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const health = {
        file: path.basename(filePath),
        status: 'healthy',
        issues: [],
        stats: {}
    };
    
    // Check 1: Dashboard elements exist
    const requiredElements = [
        { id: 'scrollContainer', name: 'Scroll Container' },
        { id: 'issuesBody', name: 'Issues Table Body' },
        { id: 'searchInput', name: 'Search Input' },
        { id: 'issuesCount', name: 'Issues Count Display' },
        { id: 'spacerTop', name: 'Top Spacer' },
        { id: 'spacerBottom', name: 'Bottom Spacer' }
    ];
    
    for (const elem of requiredElements) {
        if (!document.getElementById(elem.id)) {
            health.status = 'unhealthy';
            health.issues.push(`Missing element: ${elem.name} (#${elem.id})`);
        }
    }
    
    // Check 2: Data loaded
    if (window.state) {
        health.stats.totalIssues = window.state.allIssues?.length || 0;
        health.stats.filteredIssues = window.state.filteredIssues?.length || 0;
        health.stats.codeContextCount = window.state.codeContextMap?.size || 0;
        health.stats.containerHeight = window.state.containerHeight || 0;
        
        if (health.stats.totalIssues === 0) {
            health.status = 'unhealthy';
            health.issues.push('No issues loaded');
        }
        
        if (health.stats.containerHeight <= 0) {
            health.status = 'warning';
            health.issues.push('Container height is invalid');
        }
    } else {
        health.status = 'unhealthy';
        health.issues.push('State object not initialized');
    }
    
    // Check 3: Rows rendered
    const tbody = document.getElementById('issuesBody');
    if (tbody) {
        health.stats.renderedRows = tbody.children.length;
        
        if (health.stats.filteredIssues > 0 && health.stats.renderedRows === 0) {
            health.status = 'unhealthy';
            health.issues.push('No rows rendered despite having issues');
        }
    }
    
    // Check 4: JSONL data integrity
    const issuesScript = document.getElementById('issuesData');
    if (issuesScript) {
        const lines = issuesScript.textContent.trim().split('\n');
        let validLines = 0;
        let invalidLines = 0;
        
        for (const line of lines) {
            if (line.trim()) {
                try {
                    JSON.parse(line);
                    validLines++;
                } catch {
                    invalidLines++;
                }
            }
        }
        
        health.stats.jsonlLines = { valid: validLines, invalid: invalidLines };
        
        if (invalidLines > 0) {
            health.status = 'warning';
            health.issues.push(`${invalidLines} invalid JSONL lines found`);
        }
    } else {
        health.status = 'unhealthy';
        health.issues.push('No embedded issues data found');
    }
    
    // Check 5: Recovery function exists
    if (!window.recoverDashboard) {
        health.status = 'warning';
        health.issues.push('Recovery function not available');
    }
    
    return health;
}

async function checkDirectory(dirPath) {
    const results = [];
    const files = fs.readdirSync(dirPath);
    
    for (const file of files) {
        if (file.endsWith('.html') && !file.includes('index.html')) {
            const filePath = path.join(dirPath, file);
            try {
                const health = await checkDashboard(filePath);
                results.push(health);
            } catch (error) {
                results.push({
                    file,
                    status: 'error',
                    issues: [`Failed to check: ${error.message}`]
                });
            }
        }
    }
    
    return results;
}

// Create API endpoint data
function createHealthEndpoint(results) {
    const summary = {
        total: results.length,
        healthy: results.filter(r => r.status === 'healthy').length,
        warning: results.filter(r => r.status === 'warning').length,
        unhealthy: results.filter(r => r.status === 'unhealthy').length,
        error: results.filter(r => r.status === 'error').length,
        lastChecked: new Date().toISOString()
    };
    
    return {
        summary,
        dashboards: results
    };
}

// Main
async function main() {
    const target = process.argv[2];
    
    if (!target) {
        console.error('Usage: node dashboard-health-check.js <file-or-directory>');
        process.exit(1);
    }
    
    try {
        let results;
        
        if (fs.statSync(target).isDirectory()) {
            results = await checkDirectory(target);
        } else {
            results = [await checkDashboard(target)];
        }
        
        // Display results
        console.log('\n📊 Health Check Results:');
        console.log('========================');
        
        for (const result of results) {
            const icon = {
                healthy: '✅',
                warning: '⚠️',
                unhealthy: '❌',
                error: '💥'
            }[result.status];
            
            console.log(`\n${icon} ${result.file}: ${result.status.toUpperCase()}`);
            
            if (result.stats) {
                console.log('  📈 Stats:');
                console.log(`     - Total issues: ${result.stats.totalIssues}`);
                console.log(`     - Filtered issues: ${result.stats.filteredIssues}`);
                console.log(`     - Rendered rows: ${result.stats.renderedRows}`);
                console.log(`     - Container height: ${result.stats.containerHeight}px`);
                console.log(`     - Code contexts: ${result.stats.codeContextCount}`);
            }
            
            if (result.issues.length > 0) {
                console.log('  ⚠️  Issues:');
                result.issues.forEach(issue => {
                    console.log(`     - ${issue}`);
                });
            }
        }
        
        // Create health endpoint file if checking directory
        if (fs.statSync(target).isDirectory()) {
            const healthData = createHealthEndpoint(results);
            const outputPath = path.join(target, 'health.json');
            fs.writeFileSync(outputPath, JSON.stringify(healthData, null, 2));
            console.log(`\n📝 Health endpoint written to: ${outputPath}`);
            
            // Summary
            console.log('\n📊 Summary:');
            console.log(`   Healthy: ${healthData.summary.healthy}/${healthData.summary.total}`);
            console.log(`   Warnings: ${healthData.summary.warning}`);
            console.log(`   Unhealthy: ${healthData.summary.unhealthy}`);
            console.log(`   Errors: ${healthData.summary.error}`);
        }
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

// Check if jsdom is installed
try {
    require('jsdom');
    main();
} catch {
    console.log('📦 Installing required dependency: jsdom');
    require('child_process').execSync('npm install jsdom', { stdio: 'inherit' });
    console.log('✅ Dependency installed. Please run the command again.');
}