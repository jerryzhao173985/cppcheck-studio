#!/bin/bash
# Script to reorganize documentation structure

echo "📚 Reorganizing CPPCheck Studio Documentation..."

# Create new directory structure
mkdir -p docs/getting-started
mkdir -p docs/user-guide  
mkdir -p docs/developer-guide
mkdir -p docs/reference
mkdir -p docs/archive/journey-logs
mkdir -p docs/archive/fix-summaries

# Move journey and fix documents to archive
echo "📦 Archiving journey logs..."
mv *JOURNEY*.md docs/archive/journey-logs/ 2>/dev/null
mv *FIX*.md docs/archive/fix-summaries/ 2>/dev/null
mv *LOG.md docs/archive/journey-logs/ 2>/dev/null

# Move specific documentation to appropriate folders
echo "📁 Organizing documentation..."

# User guide documents
mv HOW_VIRTUAL_DASHBOARD_WORKS.md docs/user-guide/ 2>/dev/null
mv DASHBOARD_GENERATOR_PATTERNS.md docs/user-guide/ 2>/dev/null
mv ISSUE_SEVERITY_FILTERING.md docs/user-guide/ 2>/dev/null

# Developer guide documents  
mv MODERNIZATION_*.md docs/developer-guide/ 2>/dev/null
mv DEEP_UNDERSTANDING_ANALYSIS.md docs/developer-guide/ 2>/dev/null
mv REFACTORING_*.md docs/developer-guide/ 2>/dev/null
mv PROJECT_UNIFIED_DOCUMENTATION.md docs/developer-guide/ 2>/dev/null

# Reference documents
mv WORKFLOW_FIXES_COMPLETE.md docs/reference/ 2>/dev/null
mv PYTHON_DASHBOARD_GENERATORS_GUIDE.md docs/reference/ 2>/dev/null

# Keep these at root level
echo "📌 Keeping essential docs at root..."
# README.md - Main entry point
# CLAUDE.md - AI instructions  
# LICENSE - Legal
# docs/QUICK_START.md - Quick start guide
# docs/GENERATOR_COMPARISON.md - Generator comparison
# docs/IMPLEMENTATION_PLAN.md - This plan

# Create index file for archived documents
echo "📑 Creating archive index..."
cat > docs/archive/INDEX.md << 'EOF'
# Archived Documentation

This directory contains historical documentation from the development journey.

## Journey Logs
Documents detailing the development process, debugging sessions, and problem-solving approaches.

## Fix Summaries  
Summaries of specific fixes and solutions implemented during development.

These documents are preserved for historical context and learning purposes.
EOF

# Create main documentation index
echo "📖 Creating documentation index..."
cat > docs/INDEX.md << 'EOF'
# CPPCheck Studio Documentation

## Quick Links
- [Quick Start Guide](QUICK_START.md)
- [Generator Comparison](GENERATOR_COMPARISON.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)

## Documentation Structure

### Getting Started
- Installation guides
- First analysis walkthrough
- Basic usage examples

### User Guide
- Dashboard features
- Generator selection
- CI/CD integration
- Troubleshooting

### Developer Guide  
- Architecture overview
- Contributing guidelines
- API reference
- Testing

### Reference
- CLI options
- Configuration
- Output formats

### Archive
- [Historical documentation](archive/INDEX.md)
EOF

echo "✅ Documentation reorganization complete!"
echo ""
echo "Summary:"
echo "- Created new directory structure"
echo "- Moved journey/fix logs to archive"
echo "- Organized docs by category"
echo "- Created index files"
echo ""
echo "Next steps:"
echo "1. Review the new structure in docs/"
echo "2. Update any broken links in README.md"
echo "3. Commit the reorganized structure"