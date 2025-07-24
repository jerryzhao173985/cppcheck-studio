#!/bin/bash

# Update all deployed dashboards with the fix
# This script patches all existing dashboards to ensure they initialize properly

echo "🔧 Updating all deployed dashboards..."
echo ""

# Find all dashboard HTML files
DASHBOARDS=$(find docs/results -name "index.html" -type f 2>/dev/null)
TOTAL=$(echo "$DASHBOARDS" | grep -c .)

if [ $TOTAL -eq 0 ]; then
    echo "No dashboards found in docs/results/"
    exit 0
fi

echo "Found $TOTAL dashboards to check"
echo ""

PATCHED=0
ALREADY_OK=0
ERRORS=0

# Check each dashboard
while IFS= read -r dashboard; do
    if [ -z "$dashboard" ]; then
        continue
    fi
    
    echo -n "Checking $dashboard... "
    
    # Check if it needs patching
    if grep -q "filterData();" "$dashboard" && grep -q "filteredIssues: \[\]" "$dashboard"; then
        echo "✅ Already OK"
        ((ALREADY_OK++))
    else
        # Create backup
        cp "$dashboard" "${dashboard}.backup"
        
        # Apply patch
        if node patch-dashboard.js "$dashboard" > /dev/null 2>&1; then
            echo "✅ Patched"
            ((PATCHED++))
        else
            echo "❌ Error"
            ((ERRORS++))
            # Restore backup on error
            mv "${dashboard}.backup" "$dashboard"
        fi
    fi
done <<< "$DASHBOARDS"

echo ""
echo "📊 Summary:"
echo "   Already OK: $ALREADY_OK"
echo "   Patched: $PATCHED"
echo "   Errors: $ERRORS"
echo "   Total: $TOTAL"

# Clean up backups for successful patches
if [ $ERRORS -eq 0 ]; then
    find docs/results -name "*.backup" -type f -delete 2>/dev/null
    echo ""
    echo "✅ All dashboards updated successfully!"
else
    echo ""
    echo "⚠️  Some dashboards had errors. Backups preserved as .backup files"
fi

# Rebuild the TypeScript generator to ensure future dashboards are correct
echo ""
echo "🔨 Rebuilding dashboard generator..."
cd cppcheck-dashboard-generator
npm run build
cd ..

echo ""
echo "✅ Update complete!"