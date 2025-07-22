#!/bin/bash

echo "🧪 Simple CPPCheck Dashboard Test"
echo "================================"

# Create test C++ file
mkdir -p test-project
cat > test-project/test.cpp << 'EOF'
#include <iostream>

int main() {
    int* ptr = nullptr;
    *ptr = 10;  // Null pointer dereference
    
    int uninit;
    std::cout << uninit;  // Uninitialized variable
    
    int* leak = new int[10];  // Memory leak
    
    return 0;
}
EOF

# Run cppcheck
echo "Running CPPCheck..."
cppcheck --enable=all --xml --xml-version=2 test-project/ 2> test-results.xml

echo "XML Output:"
cat test-results.xml

# Convert to JSON
echo -e "\nConverting to JSON..."
python3 xml2json-simple.py test-results.xml > test-analysis.json

echo "JSON Output:"
cat test-analysis.json

# Build and use dashboard generator
echo -e "\nBuilding dashboard generator..."
cd cppcheck-dashboard-generator
npm run build

echo -e "\nGenerating dashboard..."
node dist/cli.js ../test-analysis.json ../test-dashboard.html --title "Simple Test"

cd ..

if [ -f test-dashboard.html ]; then
    echo -e "\n✅ Dashboard generated successfully!"
    echo "Size: $(ls -lh test-dashboard.html | awk '{print $5}')"
    echo "Open: file://$(pwd)/test-dashboard.html"
else
    echo -e "\n❌ Dashboard generation failed!"
fi

# Cleanup
rm -rf test-project