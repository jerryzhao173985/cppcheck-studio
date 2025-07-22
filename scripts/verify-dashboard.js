#!/usr/bin/env node
/**
 * Verify and debug dashboard issues
 * Usage: node verify-dashboard.js <dashboard.html or analysis.json>
 */

const fs = require('fs');
const path = require('path');

function verifyDashboard(filePath) {
    console.log(`\n🔍 Verifying: ${filePath}\n`);
    
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Check if it's JSON or HTML
    if (filePath.endsWith('.json')) {
        verifyJSON(content);
        return;
    }
    
    const html = content;
    
    // Extract embedded JSONL data
    const issuesMatch = html.match(/<script id="issuesData"[^>]*>([\s\S]*?)<\/script>/);
    const codeMatch = html.match(/<script id="codeContextData"[^>]*>([\s\S]*?)<\/script>/);
    
    if (!issuesMatch) {
        console.error('❌ No issues data found in dashboard!');
        return;
    }
    
    // Parse JSONL data
    const issuesText = issuesMatch[1].trim();
    const issuesLines = issuesText.split('\n').filter(line => line.trim());
    
    console.log(`📊 Dashboard Statistics:`);
    console.log(`   Total issue lines: ${issuesLines.length}`);
    
    // Parse issues
    const issues = [];
    const parseErrors = [];
    
    issuesLines.forEach((line, index) => {
        try {
            const issue = JSON.parse(line);
            issues.push(issue);
        } catch (e) {
            parseErrors.push({ line: index + 1, error: e.message, content: line.substring(0, 100) });
        }
    });
    
    console.log(`   Successfully parsed: ${issues.length} issues`);
    console.log(`   Parse errors: ${parseErrors.length}`);
    
    if (parseErrors.length > 0) {
        console.log('\n❌ Parse Errors:');
        parseErrors.slice(0, 5).forEach(err => {
            console.log(`   Line ${err.line}: ${err.error}`);
            console.log(`   Content: ${err.content}...`);
        });
    }
    
    // Analyze issues
    if (issues.length > 0) {
        const severities = {};
        const files = new Set();
        const repos = new Set();
        
        issues.forEach(issue => {
            severities[issue.severity] = (severities[issue.severity] || 0) + 1;
            if (issue.file) {
                files.add(issue.file);
                // Extract repository from file path
                const match = issue.file.match(/^([^\/]+)\//);
                if (match) repos.add(match[1]);
            }
        });
        
        console.log('\n📈 Issue Breakdown:');
        Object.entries(severities).forEach(([sev, count]) => {
            console.log(`   ${sev}: ${count}`);
        });
        
        console.log(`\n📁 Unique files: ${files.size}`);
        console.log(`📦 Repositories found: ${Array.from(repos).join(', ')}`);
        
        // Show sample issues
        console.log('\n📋 Sample Issues:');
        issues.slice(0, 5).forEach((issue, i) => {
            console.log(`\n   Issue ${i + 1}:`);
            console.log(`   - File: ${issue.file || 'N/A'}`);
            console.log(`   - Line: ${issue.line || 'N/A'}`);
            console.log(`   - Severity: ${issue.severity || 'N/A'}`);
            console.log(`   - Message: ${(issue.message || 'N/A').substring(0, 80)}...`);
            console.log(`   - ID: ${issue.id || 'N/A'}`);
        });
    }
    
    // Check code context
    if (codeMatch) {
        const codeText = codeMatch[1].trim();
        const codeLines = codeText.split('\n').filter(line => line.trim());
        console.log(`\n📝 Code Context:`);
        console.log(`   Total entries: ${codeLines.length}`);
        
        let validContext = 0;
        codeLines.forEach(line => {
            try {
                const data = JSON.parse(line);
                if (data.id && data.code_context) validContext++;
            } catch (e) {
                // Ignore
            }
        });
        console.log(`   Valid contexts: ${validContext}`);
    }
    
    // Check if initialization code exists
    console.log('\n🔧 Dashboard Setup:');
    const hasFilterData = html.includes('function filterData()');
    const hasInitialize = html.includes('function initialize()');
    const callsFilterData = html.includes('filterData()');
    
    console.log(`   Has filterData function: ${hasFilterData ? '✅' : '❌'}`);
    console.log(`   Has initialize function: ${hasInitialize ? '✅' : '❌'}`);
    console.log(`   Calls filterData: ${callsFilterData ? '✅' : '❌'}`);
    
    // Check for common issues
    console.log('\n⚠️  Potential Issues:');
    
    if (issuesLines.length === 0) {
        console.log('   - No issues data embedded in dashboard');
    }
    
    if (issues.length === 0 && issuesLines.length > 0) {
        console.log('   - JSONL parsing failed for all lines');
    }
    
    if (!callsFilterData) {
        console.log('   - filterData() may not be called during initialization');
    }
    
    // Check for wrong repository data
    const titleMatch = html.match(/<title>([^<]+)<\/title>/);
    const h1Match = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
    
    if (titleMatch && h1Match) {
        const titleRepo = titleMatch[1].match(/(\w+\/\w+)/);
        const actualRepos = Array.from(repos);
        
        if (titleRepo && actualRepos.length > 0) {
            const expectedRepo = titleRepo[1].split('/')[1];
            const hasExpectedFiles = actualRepos.some(r => r.includes(expectedRepo));
            
            if (!hasExpectedFiles) {
                console.log(`   - Title says "${titleRepo[1]}" but data contains: ${actualRepos.join(', ')}`);
            }
        }
    }
    
    console.log('\n✅ Verification complete!\n');
}

function verifyJSON(jsonContent) {
    try {
        const data = JSON.parse(jsonContent);
        const issues = data.issues || [];
        
        console.log(`📊 JSON Analysis Statistics:`);
        console.log(`   Total issues: ${issues.length}`);
        
        // Analyze issues
        const severities = {};
        const files = new Set();
        const repos = new Set();
        let withContext = 0;
        
        issues.forEach(issue => {
            severities[issue.severity] = (severities[issue.severity] || 0) + 1;
            if (issue.file) {
                files.add(issue.file);
                // Extract repository from file path
                const match = issue.file.match(/^([^\/]+)\//);
                if (match) repos.add(match[1]);
            }
            if (issue.code_context) withContext++;
        });
        
        console.log('\n📈 Issue Breakdown:');
        Object.entries(severities).forEach(([sev, count]) => {
            console.log(`   ${sev}: ${count}`);
        });
        
        console.log(`\n📁 Unique files: ${files.size}`);
        console.log(`📦 Repositories found: ${Array.from(repos).join(', ')}`);
        console.log(`📝 Issues with code context: ${withContext}`);
        
        // Show sample issues
        console.log('\n📋 Sample Issues:');
        issues.slice(0, 5).forEach((issue, i) => {
            console.log(`\n   Issue ${i + 1}:`);
            console.log(`   - File: ${issue.file || 'N/A'}`);
            console.log(`   - Line: ${issue.line || 'N/A'}`);
            console.log(`   - Severity: ${issue.severity || 'N/A'}`);
            console.log(`   - Message: ${(issue.message || 'N/A').substring(0, 80)}...`);
            console.log(`   - Has context: ${!!issue.code_context}`);
        });
        
    } catch (e) {
        console.error('❌ Failed to parse JSON:', e.message);
    }
}

// Main
if (process.argv.length < 3) {
    console.error('Usage: node verify-dashboard.js <dashboard.html or analysis.json>');
    process.exit(1);
}

const dashboardPath = process.argv[2];
if (!fs.existsSync(dashboardPath)) {
    console.error(`Error: File not found: ${dashboardPath}`);
    process.exit(1);
}

verifyDashboard(dashboardPath);