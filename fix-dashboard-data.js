#!/usr/bin/env node

/**
 * Fix Dashboard Data Format
 * 
 * This script helps convert between different data formats for the cppcheck-studio dashboards.
 * It can convert:
 * - JSONL to wrapped JSON format expected by TypeScript generator
 * - JSON to JSONL format
 * - Validate and fix existing dashboards
 */

const fs = require('fs');
const path = require('path');

function convertJsonlToJson(inputFile, outputFile) {
    console.log(`Converting JSONL to JSON: ${inputFile} -> ${outputFile}`);
    
    const content = fs.readFileSync(inputFile, 'utf8');
    const lines = content.split('\n').filter(line => line.trim());
    
    const issues = [];
    for (const line of lines) {
        try {
            const issue = JSON.parse(line);
            issues.push(issue);
        } catch (e) {
            console.error(`Failed to parse line: ${line}`);
        }
    }
    
    const outputData = {
        issues: issues,
        metadata: {
            generated_at: new Date().toISOString(),
            total_issues: issues.length
        }
    };
    
    fs.writeFileSync(outputFile, JSON.stringify(outputData, null, 2));
    console.log(`✅ Converted ${issues.length} issues`);
}

function convertJsonToJsonl(inputFile, outputFile) {
    console.log(`Converting JSON to JSONL: ${inputFile} -> ${outputFile}`);
    
    const content = fs.readFileSync(inputFile, 'utf8');
    const data = JSON.parse(content);
    
    const issues = data.issues || data;
    const jsonlLines = issues.map(issue => JSON.stringify(issue)).join('\n');
    
    fs.writeFileSync(outputFile, jsonlLines);
    console.log(`✅ Converted ${issues.length} issues`);
}

function validateDashboard(dashboardFile) {
    console.log(`Validating dashboard: ${dashboardFile}`);
    
    const content = fs.readFileSync(dashboardFile, 'utf8');
    
    // Check for embedded JSONL data
    const issuesMatch = content.match(/<script id="issuesData"[^>]*>([\s\S]*?)<\/script>/);
    const codeMatch = content.match(/<script id="codeContextData"[^>]*>([\s\S]*?)<\/script>/);
    
    if (!issuesMatch) {
        console.error('❌ No issues data found in dashboard');
        return false;
    }
    
    const issuesText = issuesMatch[1].trim();
    const issueLines = issuesText.split('\n').filter(line => line.trim());
    
    let validIssues = 0;
    let invalidIssues = 0;
    
    for (const line of issueLines) {
        try {
            JSON.parse(line);
            validIssues++;
        } catch (e) {
            invalidIssues++;
            console.error(`Invalid JSON line: ${line.substring(0, 100)}...`);
        }
    }
    
    console.log(`✅ Found ${validIssues} valid issues`);
    if (invalidIssues > 0) {
        console.log(`❌ Found ${invalidIssues} invalid issues`);
    }
    
    if (codeMatch) {
        const codeText = codeMatch[1].trim();
        const codeLines = codeText.split('\n').filter(line => line.trim());
        console.log(`✅ Found ${codeLines.length} code context entries`);
    }
    
    // Check for rendering functions
    const hasRenderFunction = content.includes('function renderVisibleRows');
    const hasCreateRowFunction = content.includes('function createIssueRow');
    const hasLoadDataFunction = content.includes('function loadEmbeddedData');
    
    console.log(`Render function: ${hasRenderFunction ? '✅' : '❌'}`);
    console.log(`Create row function: ${hasCreateRowFunction ? '✅' : '❌'}`);
    console.log(`Load data function: ${hasLoadDataFunction ? '✅' : '❌'}`);
    
    return validIssues > 0 && hasRenderFunction && hasCreateRowFunction;
}

function generateTestDashboard(outputFile) {
    console.log(`Generating test dashboard: ${outputFile}`);
    
    const testIssues = [
        {
            id: "TEST001",
            severity: "error",
            message: "Test error message",
            file: "test.cpp",
            line: 10
        },
        {
            id: "TEST002",
            severity: "warning",
            message: "Test warning message",
            file: "test.cpp",
            line: 20
        },
        {
            id: "TEST003",
            severity: "style",
            message: "Test style message",
            file: "test.cpp",
            line: 30
        }
    ];
    
    // Read the template from an existing dashboard
    const templatePath = path.join(__dirname, 'docs/results/1753195421158-vva0clkmc/index.html');
    if (fs.existsSync(templatePath)) {
        let template = fs.readFileSync(templatePath, 'utf8');
        
        // Replace the issues data
        const issuesJsonl = testIssues.map(issue => JSON.stringify(issue)).join('\n');
        template = template.replace(
            /<script id="issuesData"[^>]*>[\s\S]*?<\/script>/,
            `<script id="issuesData" type="application/x-ndjson">\n${issuesJsonl}\n</script>`
        );
        
        fs.writeFileSync(outputFile, template);
        console.log('✅ Test dashboard generated');
    } else {
        console.error('❌ Template dashboard not found');
    }
}

// Main CLI
const args = process.argv.slice(2);

if (args.length < 2) {
    console.log(`
Usage:
  node fix-dashboard-data.js jsonl-to-json <input.jsonl> <output.json>
  node fix-dashboard-data.js json-to-jsonl <input.json> <output.jsonl>
  node fix-dashboard-data.js validate <dashboard.html>
  node fix-dashboard-data.js test-dashboard <output.html>
  
Examples:
  # Convert JSONL analysis output to JSON for TypeScript generator
  node fix-dashboard-data.js jsonl-to-json analysis.jsonl analysis.json
  
  # Validate an existing dashboard
  node fix-dashboard-data.js validate docs/results/*/index.html
  
  # Generate a test dashboard
  node fix-dashboard-data.js test-dashboard test-dashboard.html
`);
    process.exit(1);
}

const command = args[0];

switch (command) {
    case 'jsonl-to-json':
        if (args.length < 3) {
            console.error('Missing input/output files');
            process.exit(1);
        }
        convertJsonlToJson(args[1], args[2]);
        break;
        
    case 'json-to-jsonl':
        if (args.length < 3) {
            console.error('Missing input/output files');
            process.exit(1);
        }
        convertJsonToJsonl(args[1], args[2]);
        break;
        
    case 'validate':
        if (args.length < 2) {
            console.error('Missing dashboard file');
            process.exit(1);
        }
        const isValid = validateDashboard(args[1]);
        process.exit(isValid ? 0 : 1);
        break;
        
    case 'test-dashboard':
        if (args.length < 2) {
            console.error('Missing output file');
            process.exit(1);
        }
        generateTestDashboard(args[1]);
        break;
        
    default:
        console.error(`Unknown command: ${command}`);
        process.exit(1);
}