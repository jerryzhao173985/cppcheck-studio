#!/bin/bash

# Test the GitHub Actions workflow locally
set -e

echo "🧪 Testing CPPCheck GitHub Actions Workflow Locally"
echo "=================================================="
echo ""

# Create a temporary directory
WORK_DIR=$(mktemp -d)
echo "📂 Working directory: $WORK_DIR"
cd "$WORK_DIR"

# Copy necessary files
echo "📋 Copying project files..."
cp -r "$OLDPWD/cppcheck-dashboard-generator" .
cp "$OLDPWD/xml2json.py" .
cp "$OLDPWD/add-code-context.py" .

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
if ! command -v cppcheck &> /dev/null; then
    echo "❌ cppcheck not found. Please install it first."
    echo "   macOS: brew install cppcheck"
    echo "   Ubuntu: sudo apt-get install cppcheck"
    exit 1
fi

# Build dashboard generator
echo ""
echo "🔨 Building dashboard generator..."
cd cppcheck-dashboard-generator
npm ci
npm run build
npm link
cd ..

# Create test C++ files (same as in workflow)
echo ""
echo "📝 Creating test C++ files..."
mkdir -p test-cpp-project/src
cat > test-cpp-project/src/main.cpp << 'EOF'
#include <iostream>
#include <vector>

class TestClass {
private:
    int* data;
    int size;
public:
    TestClass(int s) : size(s) {
        data = new int[size];
    }
    
    // Missing destructor - memory leak!
    
    void process() {
        int uninitializedVar;
        std::cout << uninitializedVar << std::endl; // Using uninitialized variable
        
        int* ptr = nullptr;
        *ptr = 10; // Null pointer dereference
    }
    
    void unnecessaryFunction(int param) {
        // Unused parameter
        int localVar = 5;
        // Missing return statement for non-void function
    }
};

int main() {
    std::vector<int> v;
    v[10] = 5; // Out of bounds access
    
    TestClass* obj = new TestClass(10);
    obj->process();
    // Missing delete - memory leak
    
    return 0;
}
EOF

# Run CPPCheck
echo ""
echo "🔍 Running CPPCheck analysis..."
cd test-cpp-project
cppcheck \
    --enable=all \
    --inconclusive \
    --std=c++17 \
    --xml \
    --xml-version=2 \
    src/ 2> ../cppcheck-results.xml
cd ..

# Convert to JSON
echo ""
echo "📊 Converting results to JSON..."
python3 xml2json.py cppcheck-results.xml > analysis.json

# Add code context
echo ""
echo "📝 Adding code context..."
cd test-cpp-project
python3 ../add-code-context.py ../analysis.json ../analysis-with-context.json
cd ..

# Generate dashboard
echo ""
echo "🎨 Generating dashboard..."
cppcheck-dashboard \
    analysis-with-context.json \
    test-dashboard.html \
    --title "Test Project Analysis" \
    --project "TestCppProject"

# Validate results
echo ""
echo "✅ Validating results..."

# Check file exists
if [ ! -f test-dashboard.html ]; then
    echo "❌ Dashboard file not created!"
    exit 1
fi

# Check file size
FILE_SIZE=$(ls -lh test-dashboard.html | awk '{print $5}')
echo "📊 Dashboard size: $FILE_SIZE"

# Check content
if grep -q "issuesData" test-dashboard.html && \
   grep -q "codeContextData" test-dashboard.html && \
   grep -q "virtual-scroll" test-dashboard.html; then
    echo "✅ Dashboard contains all required elements"
else
    echo "❌ Dashboard missing required elements"
    exit 1
fi

# Show summary
echo ""
echo "📊 Analysis Summary:"
python3 << 'EOF'
import json
with open('analysis-with-context.json') as f:
    data = json.load(f)
    issues = data.get('issues', [])
    by_severity = {}
    for issue in issues:
        sev = issue.get('severity', 'unknown')
        by_severity[sev] = by_severity.get(sev, 0) + 1
    
    print(f"Total issues: {len(issues)}")
    for sev, count in sorted(by_severity.items()):
        print(f"  {sev}: {count}")
    
    print("\n📝 Sample issues:")
    for issue in issues[:5]:
        print(f"  - {issue.get('file', 'unknown')}:{issue.get('line', '?')} - {issue.get('message', 'no message')[:60]}...")
EOF

# Copy dashboard to original directory
echo ""
echo "📁 Copying dashboard to: $OLDPWD/test-dashboard.html"
cp test-dashboard.html "$OLDPWD/"

echo ""
echo "🎉 Test completed successfully!"
echo "📂 View dashboard: $OLDPWD/test-dashboard.html"
echo ""

# Cleanup
cd "$OLDPWD"
rm -rf "$WORK_DIR"