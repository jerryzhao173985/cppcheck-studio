# CPPCheck Studio Makefile
# Professional C++ Static Analysis Tool

.PHONY: all install uninstall test clean help check-deps dev analyze dashboard

# Installation directories
PREFIX ?= $(HOME)/.local
BINDIR = $(PREFIX)/bin
LIBDIR = $(PREFIX)/lib/cppcheck-studio
SCRIPT_DIR := $(shell pwd)

# Colors
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m

# Default target
all: help

help:
	@echo "$(BLUE)CPPCheck Studio - Makefile Targets$(NC)"
	@echo ""
	@echo "Installation:"
	@echo "  make install       Install CPPCheck Studio to $(PREFIX)"
	@echo "  make uninstall     Remove CPPCheck Studio"
	@echo ""
	@echo "Development:"
	@echo "  make check-deps    Check dependencies"
	@echo "  make test          Run tests"
	@echo "  make clean         Clean generated files"
	@echo ""
	@echo "Usage:"
	@echo "  make analyze       Analyze current directory"
	@echo "  make dashboard     Generate dashboard from last analysis"
	@echo ""
	@echo "Options:"
	@echo "  PREFIX=<path>      Set installation prefix (default: ~/.local)"

check-deps:
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@echo -n "Python 3: "
	@if command -v python3 >/dev/null 2>&1; then \
		echo "$(GREEN)✓$(NC) Found $$(python3 --version)"; \
	else \
		echo "$(RED)✗$(NC) Not found"; \
		exit 1; \
	fi
	@echo -n "cppcheck: "
	@if command -v cppcheck >/dev/null 2>&1; then \
		echo "$(GREEN)✓$(NC) Found $$(cppcheck --version | head -1)"; \
	else \
		echo "$(YELLOW)⚠$(NC) Not found (optional but recommended)"; \
	fi

install: check-deps
	@echo "$(BLUE)Installing CPPCheck Studio...$(NC)"
	@mkdir -p $(BINDIR)
	@mkdir -p $(LIBDIR)
	
	@echo "Installing executable..."
	@cp -f bin/cppcheck-studio $(BINDIR)/
	@chmod +x $(BINDIR)/cppcheck-studio
	
	@echo "Installing libraries..."
	@cp -rf lib/* $(LIBDIR)/
	
	@if [ -d templates ]; then \
		echo "Installing templates..."; \
		cp -rf templates $(LIBDIR)/; \
	fi
	
	@echo ""
	@echo "$(GREEN)Installation complete!$(NC)"
	@echo "Installed to: $(PREFIX)"
	@echo ""
	@echo "Make sure $(BINDIR) is in your PATH:"
	@echo "  export PATH=\"\$$PATH:$(BINDIR)\""
	@echo ""
	@echo "To get started:"
	@echo "  cppcheck-studio init"
	@echo "  cppcheck-studio analyze"
	@echo "  cppcheck-studio serve"

uninstall:
	@echo "$(BLUE)Uninstalling CPPCheck Studio...$(NC)"
	@rm -f $(BINDIR)/cppcheck-studio
	@rm -rf $(LIBDIR)
	@echo "$(GREEN)Uninstallation complete!$(NC)"

test:
	@echo "$(BLUE)Running tests...$(NC)"
	@python3 -m pytest tests/ -v 2>/dev/null || echo "$(YELLOW)No tests found$(NC)"

clean:
	@echo "$(BLUE)Cleaning...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf .cppcheck-studio/ 2>/dev/null || true
	@rm -f *.html 2>/dev/null || true
	@echo "$(GREEN)Clean complete!$(NC)"

# Convenience targets for common operations
analyze:
	@if [ -f $(BINDIR)/cppcheck-studio ]; then \
		$(BINDIR)/cppcheck-studio analyze; \
	else \
		echo "$(RED)Error: CPPCheck Studio not installed. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

dashboard:
	@if [ -f $(BINDIR)/cppcheck-studio ]; then \
		$(BINDIR)/cppcheck-studio dashboard; \
	else \
		echo "$(RED)Error: CPPCheck Studio not installed. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi

# Development target
dev:
	@echo "$(BLUE)Running in development mode...$(NC)"
	@python3 bin/cppcheck-studio $(ARGS)