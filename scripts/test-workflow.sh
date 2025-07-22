#!/bin/bash

# Test script to verify the complete workflow

echo "🧪 Testing CPPCheck Studio Workflow"
echo "=================================="

# 1. Check if site is up
echo "1️⃣ Checking if site is accessible..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://jerryzhao173985.github.io/cppcheck-studio/)
if [ "$STATUS" = "200" ]; then
    echo "✅ Site is up!"
else
    echo "❌ Site is down (HTTP $STATUS)"
    exit 1
fi

# 2. Generate analysis ID
ANALYSIS_ID="test-$(date +%s)-$(echo $RANDOM)"
REPO="${1:-nlohmann/json}"

echo ""
echo "2️⃣ Test Configuration:"
echo "   Repository: $REPO"
echo "   Analysis ID: $ANALYSIS_ID"

# 3. Trigger workflow via CLI (if gh is available)
if command -v gh &> /dev/null; then
    echo ""
    echo "3️⃣ Triggering workflow via GitHub CLI..."
    gh workflow run analyze-on-demand.yml \
        -f repository="$REPO" \
        -f analysis_id="$ANALYSIS_ID" \
        -f branch="main" \
        -f max_files=100
    
    echo "✅ Workflow triggered!"
    echo ""
    echo "4️⃣ Monitor progress at:"
    echo "   https://github.com/jerryzhao173985/cppcheck-studio/actions"
    echo ""
    echo "5️⃣ Check results at:"
    echo "   https://jerryzhao173985.github.io/cppcheck-studio/results/$ANALYSIS_ID/"
else
    echo ""
    echo "3️⃣ Manual trigger instructions:"
    echo "   1. Go to: https://github.com/jerryzhao173985/cppcheck-studio/actions/workflows/analyze-on-demand.yml"
    echo "   2. Click 'Run workflow'"
    echo "   3. Enter:"
    echo "      - Repository: $REPO"
    echo "      - Analysis ID: $ANALYSIS_ID"
    echo "   4. Click 'Run workflow' button"
fi

echo ""
echo "6️⃣ Expected workflow steps:"
echo "   ✓ Clone $REPO"
echo "   ✓ Find C++ files"
echo "   ✓ Run cppcheck analysis"
echo "   ✓ Generate HTML dashboard"
echo "   ✓ Commit results to docs/results/$ANALYSIS_ID/"
echo "   ✓ Update api/gallery.json"
echo "   ✓ Deploy to GitHub Pages"

echo ""
echo "🔍 To check status:"
echo "   curl https://jerryzhao173985.github.io/cppcheck-studio/api/status/$ANALYSIS_ID.json"