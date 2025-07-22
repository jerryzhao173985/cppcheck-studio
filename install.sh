#!/bin/bash
# CPPCheck Studio Installation Script
# Installs CPPCheck Studio and its dependencies

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Installation directory
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local}"
BIN_DIR="$INSTALL_DIR/bin"
LIB_DIR="$INSTALL_DIR/lib/cppcheck-studio"

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════╗"
echo "║    CPPCheck Studio Installation Script    ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${NC}"

# Check OS
OS=$(uname -s)
if [[ "$OS" == "Darwin" ]]; then
    echo -e "${GREEN}✓${NC} Detected macOS"
elif [[ "$OS" == "Linux" ]]; then
    echo -e "${GREEN}✓${NC} Detected Linux"
else
    echo -e "${RED}✗${NC} Unsupported OS: $OS"
    exit 1
fi

# Check Python
echo -n "Checking Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"
    
    # Check version >= 3.6
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3,6) else 1)'; then
        echo -e "${GREEN}✓${NC} Python version is compatible"
    else
        echo -e "${RED}✗${NC} Python 3.6 or higher is required"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} Python 3 not found"
    echo "Please install Python 3.6 or higher"
    exit 1
fi

# Check cppcheck
echo -n "Checking cppcheck... "
if command -v cppcheck &> /dev/null; then
    CPPCHECK_VERSION=$(cppcheck --version | grep -oE '[0-9]+\.[0-9]+')
    echo -e "${GREEN}✓${NC} Found cppcheck $CPPCHECK_VERSION"
else
    echo -e "${YELLOW}⚠${NC} cppcheck not found"
    echo ""
    echo "Would you like to install cppcheck? (y/n)"
    read -r INSTALL_CPPCHECK
    
    if [[ "$INSTALL_CPPCHECK" == "y" ]]; then
        if [[ "$OS" == "Darwin" ]]; then
            if command -v brew &> /dev/null; then
                echo "Installing cppcheck with Homebrew..."
                brew install cppcheck
            else
                echo -e "${RED}✗${NC} Homebrew not found. Please install Homebrew first."
                echo "Visit: https://brew.sh"
                exit 1
            fi
        elif [[ "$OS" == "Linux" ]]; then
            if command -v apt-get &> /dev/null; then
                echo "Installing cppcheck with apt..."
                sudo apt-get update && sudo apt-get install -y cppcheck
            elif command -v yum &> /dev/null; then
                echo "Installing cppcheck with yum..."
                sudo yum install -y cppcheck
            else
                echo -e "${RED}✗${NC} No supported package manager found"
                echo "Please install cppcheck manually"
                exit 1
            fi
        fi
    else
        echo -e "${YELLOW}⚠${NC} Continuing without cppcheck"
        echo "You'll need to install it later to use analysis features"
    fi
fi

# Create directories
echo ""
echo "Creating installation directories..."
mkdir -p "$BIN_DIR"
mkdir -p "$LIB_DIR"

# Copy files
echo "Installing CPPCheck Studio..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy executable
cp -f "$SCRIPT_DIR/bin/cppcheck-studio" "$BIN_DIR/"
chmod +x "$BIN_DIR/cppcheck-studio"

# Copy library files
cp -rf "$SCRIPT_DIR/lib/"* "$LIB_DIR/"

# Copy generator scripts
if [[ -d "$SCRIPT_DIR/generate" ]]; then
    cp -rf "$SCRIPT_DIR/generate" "$LIB_DIR/"
fi

# Copy add-code-context.py
if [[ -f "$SCRIPT_DIR/add-code-context.py" ]]; then
    cp -f "$SCRIPT_DIR/add-code-context.py" "$LIB_DIR/"
fi

# Copy xml2json.py
if [[ -f "$SCRIPT_DIR/xml2json.py" ]]; then
    cp -f "$SCRIPT_DIR/xml2json.py" "$LIB_DIR/"
fi

# Copy templates if they exist
if [[ -d "$SCRIPT_DIR/templates" ]]; then
    cp -rf "$SCRIPT_DIR/templates" "$LIB_DIR/"
fi

# Update PATH if needed
echo ""
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}⚠${NC} $BIN_DIR is not in your PATH"
    
    # Detect shell
    if [[ -n "$ZSH_VERSION" ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ -n "$BASH_VERSION" ]]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    echo "Would you like to add it to your PATH? (y/n)"
    read -r ADD_PATH
    
    if [[ "$ADD_PATH" == "y" ]]; then
        echo "" >> "$SHELL_RC"
        echo "# CPPCheck Studio" >> "$SHELL_RC"
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_RC"
        echo -e "${GREEN}✓${NC} Added to $SHELL_RC"
        echo "Please run: source $SHELL_RC"
    fi
else
    echo -e "${GREEN}✓${NC} $BIN_DIR is already in PATH"
fi

# Create symlink for system-wide installation (optional)
if [[ -w "/usr/local/bin" ]]; then
    echo ""
    echo "Would you like to create a system-wide symlink? (y/n)"
    echo "This will allow all users to run 'cppcheck-studio'"
    read -r CREATE_SYMLINK
    
    if [[ "$CREATE_SYMLINK" == "y" ]]; then
        ln -sf "$BIN_DIR/cppcheck-studio" /usr/local/bin/cppcheck-studio
        echo -e "${GREEN}✓${NC} Created symlink in /usr/local/bin"
    fi
fi

# Shell completions (future enhancement)
# echo ""
# echo "Installing shell completions..."
# if [[ -d "/usr/local/share/bash-completion/completions" ]]; then
#     cp "$SCRIPT_DIR/completions/cppcheck-studio.bash" "/usr/local/share/bash-completion/completions/"
# fi

# Success message
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation completed successfully!  ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo "CPPCheck Studio has been installed to:"
echo "  Executable: $BIN_DIR/cppcheck-studio"
echo "  Libraries:  $LIB_DIR/"
echo ""
echo "To get started:"
echo "  1. Run: cppcheck-studio init"
echo "  2. Run: cppcheck-studio analyze"
echo "  3. Run: cppcheck-studio serve"
echo ""
echo "For help: cppcheck-studio --help"
echo ""

# Quick test
if command -v cppcheck-studio &> /dev/null; then
    echo -e "${GREEN}✓${NC} Installation verified - cppcheck-studio is available"
else
    echo -e "${YELLOW}⚠${NC} Please add $BIN_DIR to your PATH or run:"
    echo "  export PATH=\"\$PATH:$BIN_DIR\""
fi