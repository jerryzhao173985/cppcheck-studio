#!/bin/bash

# Quick test of LPZRobots analysis with includes
set -e

echo "=== Quick LPZRobots Test ==="

# Run cppcheck on a few files with proper includes
echo "Running cppcheck on selforg controllers..."

cppcheck \
    --enable=warning,style,performance \
    --suppress=missingIncludeSystem \
    --std=c++17 \
    -I../lpz/selforg \
    -I../lpz/selforg/controller \
    -I../lpz/selforg/utils \
    -I../lpz/selforg/matrix \
    --xml \
    --xml-version=2 \
    ../lpz/selforg/controller/sox.cpp \
    ../lpz/selforg/controller/sos.cpp \
    ../lpz/selforg/controller/dep.cpp \
    2> quick-test.xml

# Convert and analyze
echo "Converting results..."
python3 xml2json-simple.py quick-test.xml > quick-test.json

# Show summary
echo "Summary:"
python3 -c "
import json
with open('quick-test.json') as f:
    data = json.load(f)
    issues = data.get('issues', [])
    print(f'Total issues: {len(issues)}')
    
    by_sev = {}
    for i in issues:
        sev = i.get('severity', 'unknown')
        by_sev[sev] = by_sev.get(sev, 0) + 1
    
    for sev, count in sorted(by_sev.items()):
        print(f'  {sev}: {count}')
"

# Generate quick dashboard
cd cppcheck-dashboard-generator
npx tsx src/cli.ts ../quick-test.json ../quick-dashboard.html \
    --title "LPZRobots Quick Test" \
    --project "sox/sos/dep controllers"

cd ..
echo "Dashboard: quick-dashboard.html"