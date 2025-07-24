#!/usr/bin/env node

// Test the emergency fix parsing strategies

const testData = {
    // Test 1: Data with actual newlines (most common issue)
    newlines: `{"id":"A001","file":"test.cpp","line":10,"severity":"error","message":"Test 1"}
{"id":"A002","file":"test.cpp","line":20,"severity":"warning","message":"Test 2"}
{"id":"A003","file":"test.cpp","line":30,"severity":"style","message":"Test 3"}`,
    
    // Test 2: Data with __NEWLINE__ placeholders (our fix)
    placeholders: `{"id":"B001","file":"test.cpp","line":10,"severity":"error","message":"Test 1"}__NEWLINE__{"id":"B002","file":"test.cpp","line":20,"severity":"warning","message":"Test 2"}__NEWLINE__{"id":"B003","file":"test.cpp","line":30,"severity":"style","message":"Test 3"}`,
    
    // Test 3: Malformed single line (worst case)
    singleLine: `{"id":"C001","file":"test.cpp","line":10,"severity":"error","message":"Test 1"}{"id":"C002","file":"test.cpp","line":20,"severity":"warning","message":"Test 2"}{"id":"C003","file":"test.cpp","line":30,"severity":"style","message":"Test 3"}`
};

function testParsing(name, data) {
    console.log(`\n🧪 Testing: ${name}`);
    console.log(`Input length: ${data.length} chars`);
    
    let issuesLines = [];
    
    // Strategy 1: Split on actual newlines
    if (data.includes('\n') || data.includes('\r\n')) {
        issuesLines = data.split(/\r?\n/).filter(line => line.trim());
        console.log('✅ Strategy 1 (newlines):', issuesLines.length, 'lines');
    }
    // Strategy 2: Split on __NEWLINE__
    else if (data.includes('__NEWLINE__')) {
        issuesLines = data.split('__NEWLINE__').filter(line => line.trim());
        console.log('✅ Strategy 2 (__NEWLINE__):', issuesLines.length, 'lines');
    }
    // Strategy 3: Extract JSON objects with regex
    else {
        const jsonMatches = data.match(/\{[^{}]*\}/g) || [];
        issuesLines = jsonMatches;
        console.log('✅ Strategy 3 (regex):', issuesLines.length, 'objects');
    }
    
    // Try parsing
    let parsed = 0;
    let failed = 0;
    
    issuesLines.forEach((line, index) => {
        try {
            const obj = JSON.parse(line);
            parsed++;
        } catch (e) {
            failed++;
            console.error(`  ❌ Failed to parse line ${index}:`, e.message);
        }
    });
    
    console.log(`📊 Results: ${parsed} parsed, ${failed} failed`);
    
    return parsed > 0;
}

console.log('🚑 Emergency Fix Parser Test\n');
console.log('This tests the parsing strategies used in the emergency fix.');

// Run tests
const results = {
    newlines: testParsing('Newline-separated data', testData.newlines),
    placeholders: testParsing('__NEWLINE__ placeholders', testData.placeholders),
    singleLine: testParsing('Single line JSON objects', testData.singleLine)
};

// Summary
console.log('\n📋 Summary:');
console.log('='.repeat(40));
Object.entries(results).forEach(([test, passed]) => {
    console.log(`${test}: ${passed ? '✅ PASS' : '❌ FAIL'}`);
});

// Test the actual emergency fix URL
console.log('\n🌐 Test on live dashboard:');
console.log('1. Open: https://jerryzhao173985.github.io/cppcheck-studio/results/1753203010230-acau0p806/index.html');
console.log('2. Open browser console (F12)');
console.log('3. Copy and paste the emergency fix from emergency-fix-deployed.html');
console.log('4. The dashboard should start showing issues immediately');