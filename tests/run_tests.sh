#!/bin/bash
# Run all tests for CPPCheck Studio

echo "🧪 Running CPPCheck Studio Test Suite..."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
FAILED=0

# Run Python generator tests
echo "📝 Testing Python generators..."
python3 tests/test_generators.py -v
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python generator tests passed${NC}"
else
    echo -e "${RED}❌ Python generator tests failed${NC}"
    FAILED=1
fi
echo ""

# Test XML to JSON conversion
echo "🔄 Testing XML to JSON conversion..."
# Create test XML
cat > test_input.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<results version="2">
    <cppcheck version="2.13.0"/>
    <errors>
        <error id="uninitvar" severity="error" msg="Uninitialized variable: x" verbose="Uninitialized variable: x" file="test.cpp" line="10"/>
    </errors>
</results>
EOF

python3 xml2json-simple.py test_input.xml > test_output.json 2>/dev/null
if [ $? -eq 0 ] && [ -f test_output.json ]; then
    # Check JSON is valid
    python3 -m json.tool test_output.json > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ XML to JSON conversion test passed${NC}"
    else
        echo -e "${RED}❌ XML to JSON produced invalid JSON${NC}"
        FAILED=1
    fi
else
    echo -e "${RED}❌ XML to JSON conversion failed${NC}"
    FAILED=1
fi
rm -f test_input.xml test_output.json
echo ""

# Test TypeScript build
echo "📦 Testing TypeScript package build..."
cd cppcheck-dashboard-generator
npm install > /dev/null 2>&1
npm run build > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ TypeScript build test passed${NC}"
else
    echo -e "${RED}❌ TypeScript build failed${NC}"
    FAILED=1
fi
cd ..
echo ""

# Test that deprecated generators show warnings
echo "⚠️  Testing deprecation warnings..."
OUTPUT=$(python3 generate/generate-ultimate-dashboard.py 2>&1 | grep -i "deprecat")
if [ -n "$OUTPUT" ]; then
    echo -e "${GREEN}✅ Deprecation warnings working${NC}"
else
    echo -e "${YELLOW}⚠️  Deprecation warnings not showing${NC}"
fi
echo ""

# Summary
echo "📊 Test Summary:"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi