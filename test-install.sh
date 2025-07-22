#!/bin/bash
# Test installation of CPPCheck Studio

set -e

echo "Testing CPPCheck Studio installation..."

# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
echo "Test directory: $TEST_DIR"

# Set installation directory
export INSTALL_DIR="$TEST_DIR/install"

# Run install script
echo "Running install.sh..."
./install.sh <<EOF
n
n
EOF

# Check if files were copied correctly
echo ""
echo "Checking installed files..."

check_file() {
    if [[ -f "$1" ]]; then
        echo "✓ Found: $1"
    else
        echo "✗ Missing: $1"
        exit 1
    fi
}

check_dir() {
    if [[ -d "$1" ]]; then
        echo "✓ Found directory: $1"
    else
        echo "✗ Missing directory: $1"
        exit 1
    fi
}

# Check installed structure
check_file "$INSTALL_DIR/bin/cppcheck-studio"
check_dir "$INSTALL_DIR/lib/cppcheck-studio"
check_file "$INSTALL_DIR/lib/cppcheck-studio/context.py"
check_file "$INSTALL_DIR/lib/cppcheck-studio/dashboard.py"
check_file "$INSTALL_DIR/lib/cppcheck-studio/add-code-context.py"
check_file "$INSTALL_DIR/lib/cppcheck-studio/xml2json.py"
check_dir "$INSTALL_DIR/lib/cppcheck-studio/generate"

# Check if executable is runnable
echo ""
echo "Testing executable..."
export PATH="$INSTALL_DIR/bin:$PATH"

if cppcheck-studio --help > /dev/null 2>&1; then
    echo "✓ cppcheck-studio --help works"
else
    echo "✗ cppcheck-studio --help failed"
    exit 1
fi

# Clean up
echo ""
echo "Cleaning up..."
rm -rf "$TEST_DIR"

echo ""
echo "✅ All installation tests passed!"