#!/bin/bash
# CPPCheck Studio Installation Script

set -e

INSTALL_DIR="${HOME}/.local/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Installing CPPCheck Studio..."

# Check for cppcheck
if ! command -v cppcheck &> /dev/null; then
    echo "❌ Error: cppcheck not found!"
    echo "Please install cppcheck first:"
    echo "  macOS:    brew install cppcheck"
    echo "  Ubuntu:   sudo apt-get install cppcheck"
    echo "  Arch:     sudo pacman -S cppcheck"
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found!"
    exit 1
fi

# Create install directory if needed
mkdir -p "$INSTALL_DIR"

# Create a wrapper script that knows where the Python scripts are
cat > "$INSTALL_DIR/cppcheck-studio" << EOF
#!/bin/bash
# CPPCheck Studio wrapper
exec python3 "$SCRIPT_DIR/cppcheck-studio" "\$@"
EOF

chmod +x "$INSTALL_DIR/cppcheck-studio"

# Check if install dir is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  $INSTALL_DIR is not in your PATH"
    echo "Add this to your shell config (.bashrc, .zshrc, etc):"
    echo ""
    echo "    export PATH=\"\$PATH:$INSTALL_DIR\""
    echo ""
fi

echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  cppcheck-studio --help    # Show help"
echo "  cppcheck-studio .         # Analyze current directory"
echo "  cppcheck-studio --init    # Create config file"
echo ""

# Test installation
if command -v cppcheck-studio &> /dev/null; then
    echo "✅ cppcheck-studio is ready to use!"
else
    echo "⚠️  Please add $INSTALL_DIR to your PATH and restart your shell"
fi