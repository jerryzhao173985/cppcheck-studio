#!/usr/bin/env node

/**
 * Fix deployed dashboard issues
 * This script diagnoses and fixes common problems with deployed dashboards
 */

const fs = require('fs');
const path = require('path');

function diagnoseDashboard(filePath) {
    console.log(`\n🔍 Diagnosing dashboard: ${filePath}\n`);
    
    const content = fs.readFileSync(filePath, 'utf8');
    const issues = [];
    const fixes = [];
    
    // 1. Check for issues data
    const issuesMatch = content.match(/<script id="issuesData"[^>]*>([\s\S]*?)<\/script>/);
    if (!issuesMatch) {
        issues.push('❌ No issues data script found');
        fixes.push('Add issues data script tag');
    } else {
        const issuesText = issuesMatch[1].trim();
        const lines = issuesText.split('\n').filter(line => line.trim());
        
        if (lines.length === 0) {
            issues.push('❌ Issues data is empty');
            fixes.push('Ensure analysis produces results');
        } else {
            console.log(`✅ Found ${lines.length} issues in data`);
            
            // Validate first few lines
            let validCount = 0;
            for (let i = 0; i < Math.min(5, lines.length); i++) {
                try {
                    JSON.parse(lines[i]);
                    validCount++;
                } catch (e) {
                    issues.push(`❌ Invalid JSON at line ${i + 1}: ${e.message}`);
                    console.log(`   Line ${i + 1}: ${lines[i].substring(0, 100)}...`);
                }
            }
            
            if (validCount === Math.min(5, lines.length)) {
                console.log('✅ Data format is valid JSONL');
            }
        }
    }
    
    // 2. Check for required DOM elements
    const requiredElements = [
        'issuesBody',
        'searchInput',
        'scrollContainer',
        'issuesList'
    ];
    
    const missingElements = [];
    requiredElements.forEach(id => {
        if (!content.includes(`id="${id}"`) && !content.includes(`id='${id}'`)) {
            missingElements.push(id);
        }
    });
    
    if (missingElements.length > 0) {
        issues.push(`❌ Missing DOM elements: ${missingElements.join(', ')}`);
        fixes.push('Dashboard template is incomplete');
    } else {
        console.log('✅ All required DOM elements present');
    }
    
    // 3. Check for rendering functions
    const requiredFunctions = [
        'renderVisibleRows',
        'createIssueRow',
        'loadEmbeddedData',
        'filterData'
    ];
    
    const missingFunctions = [];
    requiredFunctions.forEach(func => {
        const regex = new RegExp(`function\\s+${func}|${func}\\s*=\\s*function|const\\s+${func}\\s*=`);
        if (!regex.test(content)) {
            missingFunctions.push(func);
        }
    });
    
    if (missingFunctions.length > 0) {
        issues.push(`❌ Missing functions: ${missingFunctions.join(', ')}`);
        fixes.push('JavaScript code is incomplete');
    } else {
        console.log('✅ All required functions present');
    }
    
    // 4. Check initialization
    if (!content.includes('DOMContentLoaded') && !content.includes('initialize()')) {
        issues.push('❌ No initialization code found');
        fixes.push('Add DOMContentLoaded event listener');
    } else {
        console.log('✅ Initialization code present');
    }
    
    // 5. Check for common errors
    if (content.includes('state.allIssues = []') && !content.includes('state.allIssues = issuesLines')) {
        issues.push('⚠️  State might not be populated with issues');
        fixes.push('Ensure loadEmbeddedData() assigns parsed issues to state.allIssues');
    }
    
    // Print summary
    console.log('\n📊 Summary:');
    if (issues.length === 0) {
        console.log('✅ Dashboard appears to be correctly structured');
        console.log('\nIf issues are still not showing, check:');
        console.log('1. Browser console for JavaScript errors');
        console.log('2. Network tab for failed resource loads');
        console.log('3. CSS styles that might hide the content');
    } else {
        console.log(`Found ${issues.length} issues:\n`);
        issues.forEach(issue => console.log(`  ${issue}`));
        
        console.log('\n🔧 Suggested fixes:');
        fixes.forEach(fix => console.log(`  - ${fix}`));
    }
    
    return { issues, fixes };
}

function createMinimalTestDashboard(outputPath) {
    console.log('\n🔨 Creating minimal test dashboard...\n');
    
    const testData = [
        { id: 'TEST001', severity: 'error', message: 'Test error message', file: 'test.cpp', line: 10 },
        { id: 'TEST002', severity: 'warning', message: 'Test warning message', file: 'test.cpp', line: 20 },
        { id: 'TEST003', severity: 'style', message: 'Test style message', file: 'test.cpp', line: 30 }
    ];
    
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimal Test Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
        .error { color: red; }
        .warning { color: orange; }
        .style { color: blue; }
    </style>
</head>
<body>
    <h1>Minimal Test Dashboard</h1>
    <p id="status">Loading...</p>
    
    <table>
        <thead>
            <tr>
                <th>Severity</th>
                <th>Message</th>
                <th>File</th>
                <th>Line</th>
            </tr>
        </thead>
        <tbody id="issuesBody"></tbody>
    </table>
    
    <script id="issuesData" type="application/x-ndjson">
${testData.map(issue => JSON.stringify(issue)).join('\n')}
    </script>
    
    <script>
        // Simple dashboard implementation
        function loadData() {
            const script = document.getElementById('issuesData');
            const lines = script.textContent.trim().split('\\n');
            const issues = [];
            
            lines.forEach(line => {
                if (line.trim()) {
                    try {
                        issues.push(JSON.parse(line));
                    } catch (e) {
                        console.error('Failed to parse:', line);
                    }
                }
            });
            
            return issues;
        }
        
        function renderIssues(issues) {
            const tbody = document.getElementById('issuesBody');
            tbody.innerHTML = '';
            
            issues.forEach(issue => {
                const row = document.createElement('tr');
                row.innerHTML = \`
                    <td class="\${issue.severity}">\${issue.severity}</td>
                    <td>\${issue.message}</td>
                    <td>\${issue.file}</td>
                    <td>\${issue.line}</td>
                \`;
                tbody.appendChild(row);
            });
            
            document.getElementById('status').textContent = \`Loaded \${issues.length} issues\`;
        }
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {
            const issues = loadData();
            renderIssues(issues);
            console.log('Dashboard initialized with', issues.length, 'issues');
        });
    </script>
</body>
</html>`;
    
    fs.writeFileSync(outputPath, html);
    console.log(`✅ Created minimal test dashboard: ${outputPath}`);
    console.log('   This dashboard has basic functionality to verify rendering works');
}

// Main CLI
const args = process.argv.slice(2);

if (args.length === 0) {
    console.log(`
Usage:
  node fix-deployed-dashboard.js diagnose <dashboard.html>
  node fix-deployed-dashboard.js test-minimal <output.html>
  
Examples:
  # Diagnose an existing dashboard
  node fix-deployed-dashboard.js diagnose docs/results/*/index.html
  
  # Create a minimal test dashboard
  node fix-deployed-dashboard.js test-minimal minimal-test.html
`);
    process.exit(1);
}

const command = args[0];

switch (command) {
    case 'diagnose':
        if (args.length < 2) {
            console.error('Missing dashboard file path');
            process.exit(1);
        }
        diagnoseDashboard(args[1]);
        break;
        
    case 'test-minimal':
        if (args.length < 2) {
            console.error('Missing output file path');
            process.exit(1);
        }
        createMinimalTestDashboard(args[1]);
        break;
        
    default:
        console.error(`Unknown command: ${command}`);
        process.exit(1);
}