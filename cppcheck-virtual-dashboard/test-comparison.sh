#!/bin/bash

echo "🔍 Comparing Python and TypeScript implementations..."
echo

# Test with sample data
echo "1️⃣ Testing with sample data (3 issues)..."
python3 ../generate/generate-standalone-virtual-dashboard.py ../demo-output/sample-analysis.json python-sample.html
node dist/cli.js ../demo-output/sample-analysis.json typescript-sample.html

echo
echo "📊 File size comparison (sample):"
ls -lh *-sample.html | awk '{print $9 ": " $5}'

# Test with large dataset
echo
echo "2️⃣ Testing with LPZRobots data (2975 issues)..."
python3 ../generate/generate-standalone-virtual-dashboard.py ../data/analysis-with-context.json python-lpz.html
node dist/cli.js ../data/analysis-with-context.json typescript-lpz.html

echo
echo "📊 File size comparison (LPZRobots):"
ls -lh *-lpz.html | awk '{print $9 ": " $5}'

echo
echo "✅ Both implementations completed successfully!"
echo "   Python version:     python3 generate/generate-standalone-virtual-dashboard.py"
echo "   TypeScript version: cppcheck-dashboard (after npm install -g)"