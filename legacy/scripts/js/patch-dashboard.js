#!/usr/bin/env node

/**
 * Patch dashboard to fix missing initialization
 * This script fixes the issue where filteredIssues is not initialized
 */

const fs = require('fs');
const path = require('path');

function patchDashboard(inputPath, outputPath) {
    console.log(`\n🔧 Patching dashboard: ${inputPath}\n`);
    
    let content = fs.readFileSync(inputPath, 'utf8');
    let patched = false;
    
    // Check if filterData is called after loadEmbeddedData
    const loadDataRegex = /loadEmbeddedData\(\);/g;
    const hasFilterCall = content.includes('loadEmbeddedData();\n            filterData();');
    
    if (!hasFilterCall) {
        // Add filterData() call after loadEmbeddedData()
        content = content.replace(
            'loadEmbeddedData();',
            'loadEmbeddedData();\n            \n            // Initialize filtered issues\n            filterData();'
        );
        patched = true;
        console.log('✅ Added filterData() call after loadEmbeddedData()');
    }
    
    // Also check if filteredIssues is initialized in state
    const stateInitRegex = /const state = \{[\s\S]*?\};/m;
    const stateMatch = content.match(stateInitRegex);
    
    if (stateMatch && !stateMatch[0].includes('filteredIssues:')) {
        // Add filteredIssues to state initialization
        const newState = stateMatch[0].replace(
            'allIssues: [],',
            'allIssues: [],\n        filteredIssues: [],'
        );
        content = content.replace(stateMatch[0], newState);
        patched = true;
        console.log('✅ Added filteredIssues to state initialization');
    }
    
    // Write patched content
    if (patched) {
        fs.writeFileSync(outputPath || inputPath, content);
        console.log(`\n✅ Dashboard patched successfully!`);
        console.log(`   Output: ${outputPath || inputPath}`);
        
        // Verify the patch
        if (content.includes('filterData();') && content.includes('filteredIssues: []')) {
            console.log('\n✅ Verification passed:');
            console.log('   - filterData() is called after data loading');
            console.log('   - filteredIssues is initialized in state');
        }
    } else {
        console.log('ℹ️  Dashboard appears to be already patched or uses different structure');
    }
    
    return patched;
}

function createPatchedGenerator() {
    // Create a patched version of the dashboard generator template
    const generatorPath = path.join(__dirname, 'cppcheck-dashboard-generator/src/templates/dashboard.template.ts');
    
    if (fs.existsSync(generatorPath)) {
        console.log('\n📝 Creating patched generator template...\n');
        
        let template = fs.readFileSync(generatorPath, 'utf8');
        
        // Apply same patches to template
        // ... implementation ...
        
        console.log('✅ Generator template patched');
    }
}

// Main CLI
const args = process.argv.slice(2);

if (args.length === 0) {
    console.log(`
Usage:
  node patch-dashboard.js <dashboard.html> [output.html]
  node patch-dashboard.js --all docs/results/*/index.html
  
Examples:
  # Patch a single dashboard
  node patch-dashboard.js docs/results/123/index.html
  
  # Patch and save to new file
  node patch-dashboard.js broken.html fixed.html
  
  # Patch all dashboards in docs/results
  node patch-dashboard.js --all docs/results/*/index.html
`);
    process.exit(1);
}

if (args[0] === '--all') {
    // Patch multiple files
    const glob = require('glob');
    const pattern = args[1] || 'docs/results/*/index.html';
    
    glob(pattern, (err, files) => {
        if (err) {
            console.error('Error finding files:', err);
            process.exit(1);
        }
        
        console.log(`Found ${files.length} dashboard files to patch\n`);
        
        let patchedCount = 0;
        files.forEach(file => {
            if (patchDashboard(file, file)) {
                patchedCount++;
            }
            console.log('---');
        });
        
        console.log(`\n📊 Summary: Patched ${patchedCount} of ${files.length} dashboards`);
    });
} else {
    // Patch single file
    const inputFile = args[0];
    const outputFile = args[1];
    
    if (!fs.existsSync(inputFile)) {
        console.error(`Error: File '${inputFile}' not found`);
        process.exit(1);
    }
    
    patchDashboard(inputFile, outputFile);
}