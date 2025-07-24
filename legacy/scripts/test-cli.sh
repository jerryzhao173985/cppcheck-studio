#!/bin/bash
# Quick test of CPPCheck Studio CLI

echo "Testing CPPCheck Studio CLI..."
echo ""

# Test help
echo "1. Testing help command:"
python3 bin/cppcheck-studio --help
echo ""

# Test version
echo "2. Testing version:"
python3 bin/cppcheck-studio --version
echo ""

echo "✅ Basic tests complete!"
echo ""
echo "To test full functionality:"
echo "  python3 bin/cppcheck-studio init"
echo "  python3 bin/cppcheck-studio analyze"
echo "  python3 bin/cppcheck-studio dashboard"