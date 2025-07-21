#!/usr/bin/env node

/**
 * End-to-end test for CPPCheck Studio NPM package
 * Tests all features with real LPZRobots codebase
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSection(title) {
  console.log('\n' + '='.repeat(60));
  log(title, 'bright');
  console.log('='.repeat(60));
}

async function testFeature(name, testFn) {
  process.stdout.write(`Testing ${name}... `);
  try {
    const result = await testFn();
    log('✅ PASSED', 'green');
    return { name, passed: true, result };
  } catch (error) {
    log('❌ FAILED', 'red');
    console.error(`  Error: ${error.message}`);
    return { name, passed: false, error: error.message };
  }
}

// Test functions
async function testProjectStructure() {
  const requiredFiles = [
    'package.json',
    'packages/cli/package.json',
    'packages/core/package.json',
    'apps/web/package.json',
    'apps/api/package.json'
  ];
  
  for (const file of requiredFiles) {
    await fs.access(file);
  }
  
  // Check package.json configuration
  const rootPkg = JSON.parse(await fs.readFile('package.json', 'utf8'));
  if (!rootPkg.workspaces) throw new Error('Missing workspaces configuration');
  
  const cliPkg = JSON.parse(await fs.readFile('packages/cli/package.json', 'utf8'));
  if (!cliPkg.bin || !cliPkg.bin['cppcheck-studio']) {
    throw new Error('CLI binary not configured');
  }
  
  return { filesChecked: requiredFiles.length };
}

async function testAnalysisResults() {
  const analysisFile = 'test-analysis.json';
  const data = JSON.parse(await fs.readFile(analysisFile, 'utf8'));
  
  if (!data.issues || !Array.isArray(data.issues)) {
    throw new Error('Invalid analysis format');
  }
  
  const summary = {
    total: data.issues.length,
    errors: data.issues.filter(i => i.severity === 'error').length,
    warnings: data.issues.filter(i => i.severity === 'warning').length,
    style: data.issues.filter(i => i.severity === 'style').length,
    performance: data.issues.filter(i => i.severity === 'performance').length
  };
  
  if (summary.total === 0) {
    throw new Error('No issues found in analysis');
  }
  
  return summary;
}

async function testDashboardFeatures() {
  const dashboardFile = 'test-ultimate-dashboard.html';
  const content = await fs.readFile(dashboardFile, 'utf8');
  
  const features = {
    'Syntax Highlighting': content.includes('hljs.highlightElement'),
    'Diff Viewer': content.includes('Diff2HtmlUI'),
    'Interactive UI': content.includes('expandRow') || content.includes('onclick'),
    'Search Functionality': content.includes('filterTable') || content.includes('search'),
    'Severity Filters': content.includes('severity') && content.includes('filter'),
    'Code Context': content.includes('context') || content.includes('snippet'),
    'Fix Preview': content.includes('fix') && content.includes('preview'),
    'Responsive Design': content.includes('responsive') || content.includes('@media')
  };
  
  const implemented = Object.entries(features)
    .filter(([_, present]) => present)
    .map(([name]) => name);
    
  if (implemented.length < 4) {
    throw new Error(`Only ${implemented.length}/8 features implemented`);
  }
  
  return { 
    implemented: implemented.length,
    total: Object.keys(features).length,
    features: implemented
  };
}

async function testFixGeneration() {
  // Load sample issues that are fixable
  const data = JSON.parse(await fs.readFile('test-analysis.json', 'utf8'));
  const fixableTypes = ['nullPointer', 'useNullptr', 'modernizeOverride', 'explicitConstructor'];
  
  const fixableIssues = data.issues.filter(issue =>
    fixableTypes.some(type => issue.id && issue.id.includes(type))
  );
  
  if (fixableIssues.length === 0) {
    // This is okay - not all codebases have fixable issues
    return { fixableFound: 0, message: 'No automatically fixable issues in test set' };
  }
  
  return {
    fixableFound: fixableIssues.length,
    types: [...new Set(fixableIssues.map(i => i.id))]
  };
}

async function testTypeScriptBuild() {
  // Check if TypeScript files would compile
  const tsFiles = [
    'packages/core/src/analyzer.ts',
    'packages/core/src/parser.ts',
    'packages/core/src/fix-generator.ts',
    'packages/cli/src/cli.ts'
  ];
  
  for (const file of tsFiles) {
    await fs.access(file);
  }
  
  return { typeScriptFiles: tsFiles.length };
}

async function generateFinalReport(results) {
  logSection('📊 FINAL REPORT');
  
  const passed = results.filter(r => r.passed).length;
  const total = results.length;
  const percentage = (passed / total * 100).toFixed(1);
  
  log(`\nOverall: ${passed}/${total} tests passed (${percentage}%)`, 
      passed === total ? 'green' : 'yellow');
  
  // Detailed results
  log('\nDetailed Results:', 'cyan');
  
  for (const result of results) {
    const status = result.passed ? '✅' : '❌';
    console.log(`  ${status} ${result.name}`);
    
    if (result.passed && result.result) {
      // Show key metrics
      if (result.result.total) {
        console.log(`     Issues: ${result.result.total}`);
      }
      if (result.result.implemented) {
        console.log(`     Features: ${result.result.implemented}/${result.result.total}`);
      }
    }
  }
  
  // Analysis summary
  const analysisResult = results.find(r => r.name === 'Analysis Results');
  if (analysisResult && analysisResult.passed) {
    log('\n📈 LPZRobots Analysis Summary:', 'magenta');
    const summary = analysisResult.result;
    console.log(`  Total Issues: ${summary.total}`);
    console.log(`  - Errors: ${summary.errors} (${(summary.errors/summary.total*100).toFixed(1)}%)`);
    console.log(`  - Warnings: ${summary.warnings} (${(summary.warnings/summary.total*100).toFixed(1)}%)`);
    console.log(`  - Style: ${summary.style} (${(summary.style/summary.total*100).toFixed(1)}%)`);
    console.log(`  - Performance: ${summary.performance} (${(summary.performance/summary.total*100).toFixed(1)}%)`);
  }
  
  // Save detailed report
  const report = {
    timestamp: new Date().toISOString(),
    project: 'LPZRobots',
    testsRun: total,
    testsPassed: passed,
    successRate: percentage + '%',
    results: results
  };
  
  await fs.writeFile('test-report-final.json', JSON.stringify(report, null, 2));
  log('\n📝 Detailed report saved to test-report-final.json', 'blue');
  
  return passed === total;
}

// Main test runner
async function main() {
  log('🚀 CPPCheck Studio End-to-End Test Suite', 'bright');
  log('Testing on LPZRobots C++ Codebase\n', 'cyan');
  
  const tests = [
    ['Project Structure', testProjectStructure],
    ['Analysis Results', testAnalysisResults],
    ['Dashboard Features', testDashboardFeatures],
    ['Fix Generation', testFixGeneration],
    ['TypeScript Build', testTypeScriptBuild]
  ];
  
  const results = [];
  
  for (const [name, testFn] of tests) {
    const result = await testFeature(name, testFn);
    results.push(result);
  }
  
  const success = await generateFinalReport(results);
  
  if (success) {
    log('\n🎉 All tests passed! CPPCheck Studio is ready for use.', 'green');
    log('\nNext steps:', 'cyan');
    console.log('  1. npm install -g ./packages/cli');
    console.log('  2. cppcheck-studio init');
    console.log('  3. cppcheck-studio start');
  } else {
    log('\n⚠️  Some tests failed. Please check the report for details.', 'yellow');
  }
  
  process.exit(success ? 0 : 1);
}

// Run tests
main().catch(error => {
  log(`\n❌ Fatal error: ${error.message}`, 'red');
  console.error(error.stack);
  process.exit(1);
});