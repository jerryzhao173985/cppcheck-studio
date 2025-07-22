#!/bin/bash

# Demo script to test GitHub Actions workflow locally
# This simulates what the GitHub Action does

set -e

echo "🔍 CPPCheck Dashboard Demo - GitHub Actions Simulation"
echo "====================================================="

# Check if a repository URL was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <github-repo-url>"
    echo "Example: $0 https://github.com/nlohmann/json"
    exit 1
fi

REPO_URL=$1
REPO_NAME=$(basename "$REPO_URL" .git)

echo "📦 Repository: $REPO_URL"
echo "📁 Project: $REPO_NAME"
echo ""

# Check dependencies
echo "Checking dependencies..."
command -v cppcheck >/dev/null 2>&1 || { echo "❌ cppcheck is required but not installed. Install with: sudo apt-get install cppcheck"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ python3 is required but not installed."; exit 1; }

# Create temp directory
WORK_DIR=$(mktemp -d)
echo "📂 Working directory: $WORK_DIR"
cd "$WORK_DIR"

# Clone repository
echo ""
echo "📥 Cloning repository..."
git clone --depth 1 "$REPO_URL" project || { echo "❌ Failed to clone repository"; exit 1; }

# Install dashboard generator
echo ""
echo "📦 Installing cppcheck-dashboard-generator..."
npm pack "$OLDPWD/cppcheck-dashboard-generator" > /dev/null
npm install -g cppcheck-dashboard-generator-*.tgz > /dev/null

# Run analysis
echo ""
echo "🔍 Running CPPCheck analysis..."
cd project

# Find C++ files (limit to 50 for demo)
find . -type f \( -name "*.cpp" -o -name "*.cc" -o -name "*.h" -o -name "*.hpp" \) | head -50 > cpp_files.txt
FILE_COUNT=$(wc -l < cpp_files.txt)

if [ $FILE_COUNT -eq 0 ]; then
    echo "❌ No C++ files found!"
    exit 1
fi

echo "📄 Found $FILE_COUNT C++ files to analyze"

# Run cppcheck
cppcheck \
    --enable=all \
    --suppress=missingIncludeSystem \
    --std=c++17 \
    --xml \
    --xml-version=2 \
    --file-list=cpp_files.txt \
    2> ../cppcheck-results.xml

cd ..

# Convert to JSON
echo ""
echo "📊 Converting results..."
python3 "$OLDPWD/xml2json.py" cppcheck-results.xml > analysis.json

# Add code context
cd project
python3 "$OLDPWD/add-code-context.py" ../analysis.json ../analysis-with-context.json
cd ..

# Generate dashboard
echo ""
echo "🎨 Generating dashboard..."
cppcheck-dashboard \
    analysis-with-context.json \
    "${REPO_NAME}-dashboard.html" \
    --title "${REPO_NAME} CPPCheck Analysis" \
    --project "${REPO_NAME}"

# Copy to original directory
cp "${REPO_NAME}-dashboard.html" "$OLDPWD/"

# Summary
echo ""
echo "✅ Analysis complete!"
echo ""
echo "📊 Summary:"
python3 -c "
import json
with open('analysis.json') as f:
    data = json.load(f)
    issues = data.get('issues', [])
    by_severity = {}
    for issue in issues:
        sev = issue.get('severity', 'unknown')
        by_severity[sev] = by_severity.get(sev, 0) + 1
    
    print(f'   Total issues: {len(issues)}')
    for sev, count in sorted(by_severity.items()):
        print(f'   {sev}: {count}')
"

echo ""
echo "📂 Dashboard saved to: $OLDPWD/${REPO_NAME}-dashboard.html"
echo "🌐 Open in browser: file://$OLDPWD/${REPO_NAME}-dashboard.html"
echo ""
echo "🎯 This simulates what the GitHub Action would do!"

# Cleanup
cd "$OLDPWD"
rm -rf "$WORK_DIR"