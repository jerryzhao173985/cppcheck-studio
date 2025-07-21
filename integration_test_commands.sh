#!/bin/bash
# CPPCheck Studio Integration Test Commands
# Run from /Users/jerry/simulator/lpz directory

echo "Starting CPPCheck Studio Integration Test..."

# 1. Run fresh cppcheck analysis
echo "Step 1: Running cppcheck analysis..."
tools/cppcheck/cppcheck cpp17 --format json > cppcheck-studio/integration-test-raw.json

# Extract the actual JSON report from the output
LATEST_REPORT=$(ls -t tools/cppcheck/reports/cpp17_migration/*/report.json | head -1)
cp "$LATEST_REPORT" cppcheck-studio/integration-test.json

# 2. Generate dashboard
echo "Step 2: Generating dashboard..."
cd cppcheck-studio
python3 generate-ultimate-dashboard.py integration-test.json integration-dashboard.html

# 3. List available scripts
echo "Step 3: Available cppcheck scripts:"
ls -la ../tools/cppcheck/scripts/

# 4. Test fix generation (demo only)
echo "Step 4: Testing fix generation..."
cd ../tools/cppcheck
python3 scripts/fix_generator.py "$LATEST_REPORT" /dev/null

# 5. Check metrics (currently broken)
echo "Step 5: Checking metrics..."
python3 scripts/metrics.py --help

echo "Integration test complete. Check integration-dashboard.html for results."
echo "Full report available at: cppcheck-studio/INTEGRATION_TEST_REPORT.md"