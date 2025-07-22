#!/bin/bash

echo "Comparing Python and TypeScript dashboard outputs..."

# Extract issue counts from both files
python_issues=$(grep -m1 "total issues" ../python-output.html | grep -o "[0-9]* total" | cut -d' ' -f1)
ts_issues=$(grep -m1 "total issues" typescript-output.html | grep -o "[0-9]* total" | cut -d' ' -f1)

python_context=$(grep -m1 "with code context" ../python-output.html | grep -o "[0-9]* with" | cut -d' ' -f1)
ts_context=$(grep -m1 "with code context" typescript-output.html | grep -o "[0-9]* with" | cut -d' ' -f1)

echo "Python version: $python_issues issues, $python_context with context"
echo "TypeScript version: $ts_issues issues, $ts_context with context"

if [ "$python_issues" = "$ts_issues" ] && [ "$python_context" = "$ts_context" ]; then
    echo "✅ Issue counts match!"
else
    echo "❌ Issue counts differ!"
fi

# Check if both files render correctly
echo -e "\nTo verify dashboards work correctly:"
echo "1. Open: file://$(pwd)/../python-output.html"
echo "2. Open: file://$(pwd)/typescript-output.html"
echo "3. Both should show issues with virtual scrolling"