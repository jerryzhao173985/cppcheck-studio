# 🚀 CPPCheck Studio - Demo Usage Guide

## Quick Demo

### 1. View the Production Dashboard
```bash
open FINAL_PRODUCTION_DASHBOARD.html
```

This shows the analysis of **2,975 issues** found in LPZRobots with:
- Interactive filtering by severity
- Real-time search
- Click any row to see code context
- Professional UI with statistics

### 2. Generate Your Own Dashboard

#### Step 1: Run Analysis
```bash
cd /Users/jerry/simulator/lpz
tools/cppcheck/cppcheck cpp17 --format json > my-analysis.json
```

#### Step 2: Generate Dashboard
```bash
cd cppcheck-studio
python3 generate-ultimate-dashboard.py ../my-analysis.json my-dashboard.html
open my-dashboard.html
```

### 3. Use the NPM Package (After npm install)

```bash
# Install dependencies first
npm install

# Global install
npm install -g ./packages/cli

# Initialize a project
cppcheck-studio init

# Start web interface
cppcheck-studio start

# Run analysis
cppcheck-studio analyze --profile cpp17

# Apply fixes (dry-run)
cppcheck-studio fix --dry-run
```

## Dashboard Features Demo

### Search Functionality
- Type in search box to filter issues
- Searches across files, messages, and IDs

### Severity Filters
- Click buttons: All, Errors, Warnings, Style, Performance
- Updates table in real-time

### Code Preview
- Click the code icon on any issue
- Shows modal with code context (if available)

### Statistics
- Hover over cards for animations
- Shows percentages and counts

## Analysis Profiles Available

1. **quick** - Fast analysis for development
2. **full** - Comprehensive analysis
3. **cpp17** - C++17 modernization focus
4. **memory** - Memory safety checks
5. **performance** - Performance optimizations

## Example Commands

```bash
# List available profiles
tools/cppcheck/cppcheck list

# Run quick analysis
tools/cppcheck/cppcheck quick

# Run with specific files
tools/cppcheck/cppcheck quick --files src/main.cpp src/utils.cpp

# Generate HTML report
tools/cppcheck/cppcheck cpp17 --format html
```

## Pre-commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/sh
# Run cppcheck on staged C++ files
files=$(git diff --cached --name-only | grep -E '\.(cpp|hpp|h)$')
if [ -n "$files" ]; then
    tools/cppcheck/cppcheck quick --files $files
fi
```

## Success Metrics

- **2,975 issues** analyzed successfully
- **240KB** dashboard size (loads instantly)
- **11 seconds** analysis time
- **100%** interactive features working

Enjoy using CPPCheck Studio! 🎉