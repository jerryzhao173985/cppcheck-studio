#!/bin/bash
set -e

echo "🚀 CPPCheck Studio - Final Comprehensive Test"
echo "============================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local command=$2
    
    echo -e "${BLUE}Testing:${NC} $test_name"
    if eval "$command" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅ PASSED${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "  ${RED}❌ FAILED${NC}"
        ((TESTS_FAILED++))
    fi
}

# Change to project directory
cd /Users/jerry/simulator/lpz

echo "📁 Working Directory: $(pwd)"
echo ""

# 1. Test Python Dashboard Generators
echo -e "${YELLOW}=== Testing Dashboard Generators ===${NC}"
run_test "Ultimate Dashboard Generator" "cd cppcheck-studio && python3 generate-ultimate-dashboard.py test-analysis.json final-test-dashboard.html"
run_test "Enhanced Dashboard Generator" "python3 tools/cppcheck/scripts/generate_enhanced_dashboard.py cppcheck-studio/test-analysis.json cppcheck-studio/test-enhanced-dashboard.html"

# 2. Run Fresh Analysis
echo -e "\n${YELLOW}=== Running Fresh Cppcheck Analysis ===${NC}"
run_test "C++17 Analysis" "tools/cppcheck/cppcheck cpp17 > cppcheck-studio/fresh-analysis-output.txt 2>&1"

# 3. Test All Available Scripts
echo -e "\n${YELLOW}=== Testing Cppcheck Scripts ===${NC}"
run_test "Profile List" "tools/cppcheck/cppcheck list"
run_test "Quick Analysis" "tools/cppcheck/cppcheck quick | grep -q 'Analysis Summary'"
run_test "Help Command" "tools/cppcheck/cppcheck help | grep -q 'Usage'"

# 4. Check Generated Files
echo -e "\n${YELLOW}=== Checking Generated Files ===${NC}"
run_test "Dashboard HTML Exists" "[ -f cppcheck-studio/final-test-dashboard.html ]"
run_test "Dashboard Size Check" "[ $(stat -f%z cppcheck-studio/final-test-dashboard.html 2>/dev/null || stat -c%s cppcheck-studio/final-test-dashboard.html) -gt 100000 ]"

# 5. Validate JSON Files
echo -e "\n${YELLOW}=== Validating JSON Files ===${NC}"
run_test "Test Analysis JSON Valid" "python3 -m json.tool cppcheck-studio/test-analysis.json > /dev/null"
run_test "Package.json Valid" "python3 -m json.tool cppcheck-studio/package.json > /dev/null"

# 6. Check TypeScript Files
echo -e "\n${YELLOW}=== Checking TypeScript Configuration ===${NC}"
run_test "Root tsconfig.json Exists" "[ -f cppcheck-studio/tsconfig.json ]"
run_test "CLI tsconfig.json Exists" "[ -f cppcheck-studio/packages/cli/tsconfig.json ]"

# 7. Generate Final Dashboard
echo -e "\n${YELLOW}=== Generating Final Production Dashboard ===${NC}"
if [ -f "cppcheck-studio/test-analysis.json" ]; then
    cd cppcheck-studio
    python3 generate-ultimate-dashboard.py test-analysis.json FINAL_PRODUCTION_DASHBOARD.html
    echo -e "${GREEN}✅ Final dashboard generated: FINAL_PRODUCTION_DASHBOARD.html${NC}"
    
    # Show dashboard stats
    ISSUE_COUNT=$(grep -o '"severity"' test-analysis.json | wc -l)
    FILE_SIZE=$(du -h FINAL_PRODUCTION_DASHBOARD.html | cut -f1)
    echo -e "   Issues: ${BLUE}$ISSUE_COUNT${NC}"
    echo -e "   Size: ${BLUE}$FILE_SIZE${NC}"
else
    echo -e "${RED}❌ No analysis data found${NC}"
fi

# Summary
echo -e "\n${YELLOW}=== Test Summary ===${NC}"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed! CPPCheck Studio is ready for commit.${NC}"
else
    echo -e "\n${RED}⚠️  Some tests failed. Please review before committing.${NC}"
fi

# Open the final dashboard
echo -e "\n${BLUE}Opening final dashboard...${NC}"
open FINAL_PRODUCTION_DASHBOARD.html 2>/dev/null || echo "Please open FINAL_PRODUCTION_DASHBOARD.html manually"