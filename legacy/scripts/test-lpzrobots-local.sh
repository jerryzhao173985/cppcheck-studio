#!/bin/bash

# Test script to run LPZRobots analysis locally
set -e

echo "=== Testing LPZRobots Analysis Locally ==="

# Clone lpzrobots if not exists
if [ ! -d "../lpz" ]; then
    echo "Cloning LPZRobots repository..."
    git clone --depth 1 https://github.com/jerryzhao173985/lpz.git ../lpz
else
    echo "Using existing lpz directory..."
fi

# Run analysis
echo "Running CPPCheck analysis on selforg and ode_robots..."
cd ../lpz

# Create file list
find selforg ode_robots -type f \( -name "*.cpp" -o -name "*.cc" -o -name "*.h" -o -name "*.hpp" \) \
    -not -path "*/build/*" \
    -not -path "*/.git/*" \
    -not -path "*/examples/*" \
    -not -path "*/tests/*" > cpp_files.txt

FILE_COUNT=$(wc -l < cpp_files.txt)
echo "Found ${FILE_COUNT} files to analyze"

# Run cppcheck
echo "Running cppcheck..."
cppcheck \
    --enable=warning,style,performance,portability \
    --inconclusive \
    --suppress=missingIncludeSystem \
    --suppress=unmatchedSuppression \
    --suppress=missingInclude \
    --std=c++17 \
    --output-file=../cppcheck-studio/lpz-results.txt \
    --xml \
    --xml-version=2 \
    --file-list=cpp_files.txt \
    -j 4 \
    2> ../cppcheck-studio/lpz-results.xml || true

cd ../cppcheck-studio

# Convert and generate dashboard
echo "Converting results..."
python3 xml2json-simple.py lpz-results.xml > lpz-analysis.json

ISSUE_COUNT=$(python3 -c "import json; print(len(json.load(open('lpz-analysis.json'))['issues']))")
echo "Total issues found: ${ISSUE_COUNT}"

# Add code context
echo "Adding code context..."
cd ../lpz
python3 ../cppcheck-studio/add-code-context.py ../cppcheck-studio/lpz-analysis.json ../cppcheck-studio/lpz-analysis-context.json
cd ../cppcheck-studio

# Generate dashboard
echo "Generating dashboard..."
cd cppcheck-dashboard-generator
npm run generate -- ../lpz-analysis-context.json ../lpz-dashboard-local.html \
    --title "LPZRobots Local Analysis" \
    --project "LPZRobots (local test)"

cd ..

echo "=== Analysis Complete ==="
echo "Dashboard generated: lpz-dashboard-local.html"
echo "Open with: open lpz-dashboard-local.html"