# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Project Overview

**CPPCheck Studio** is a C++ static analysis visualization tool that transforms raw cppcheck output into interactive HTML dashboards. This project was created to analyze the LPZRobots codebase and consists of:

1. **Python Dashboard Generators** - Multiple scripts that create static HTML dashboards from cppcheck JSON output
2. **Monorepo Structure** (partially implemented) - A Next.js/TypeScript architecture that exists but is not fully functional
3. **Analysis Tools** - Python scripts for running cppcheck and processing results

### Current State
- **What Works**: Python scripts that generate beautiful static HTML dashboards from cppcheck analysis
- **What's Partially Implemented**: TypeScript/Next.js monorepo structure with basic scaffolding
- **Primary Use Case**: Analyzing the LPZRobots C++ codebase (2,975 issues found)

### Key Context
This project was developed as a proof-of-concept for visualizing C++ static analysis results. The core functionality lives in the Python dashboard generators, while the TypeScript/npm package structure represents an aspirational architecture that is not yet complete.

## 🏗️ What Actually Works

### Python Dashboard Generators (FUNCTIONAL)
The core functionality is in the Python scripts that generate static HTML dashboards:

```
cppcheck-studio/
├── generate-ultimate-dashboard.py      # ✅ Best dashboard (240KB, production-ready)
├── generate-virtual-scroll-dashboard.py # ✅ For large datasets (virtual scrolling)
├── generate-robust-dashboard.py        # ✅ Error handling, chunked rendering
├── generate-production-dashboard.py    # ✅ Minimal, no code context
├── generate-split-dashboard.py         # ✅ Splits data into separate files
└── add-code-context.py                # ✅ Adds code snippets to analysis
```

### Generated Dashboards
- **FINAL_PRODUCTION_DASHBOARD.html** - The main output showing LPZRobots analysis
- **Interactive features**: Search, filter by severity, code preview modals
- **Statistics**: 2,975 issues (772 errors, 153 warnings, 1,932 style, 31 performance)
- **Performance**: Loads in < 2 seconds, 240KB file size

### Analysis Workflow
1. Run cppcheck on C++ code to get JSON output
2. Optionally add code context with `add-code-context.py`
3. Generate dashboard with one of the Python scripts
4. Open HTML file in browser

## 🚧 What's Partially Implemented

### TypeScript/Node.js Structure (SCAFFOLDING ONLY)
```
├── apps/
│   ├── web/     # Next.js app with only landing page
│   └── api/     # Express server with route stubs
├── packages/
│   ├── core/    # TypeScript types and interfaces
│   ├── ui/      # Basic React components
│   └── cli/     # CLI structure (not connected to cppcheck)
```

**Status**: This represents an aspirational architecture but is not functional. The actual analysis is done by Python scripts, not the TypeScript code.

## 🛠️ How to Use This Project

### For Static Dashboard Generation (WORKS NOW)

1. **Run CPPCheck Analysis**
```bash
# From the lpz directory
cd /Users/jerry/simulator/lpz
tools/cppcheck/cppcheck cpp17 --format json > analysis.json
```

2. **Generate Dashboard**
```bash
cd cppcheck-studio
# Best option for production use:
python3 generate-ultimate-dashboard.py ../analysis.json my-dashboard.html

# For large datasets with virtual scrolling:
python3 generate-virtual-scroll-dashboard.py ../analysis.json virtual-dashboard.html

# Open in browser
open my-dashboard.html
```

3. **Add Code Context (Optional)**
```bash
# This adds code snippets around each issue
python3 add-code-context.py analysis.json analysis-with-context.json
python3 generate-ultimate-dashboard.py analysis-with-context.json dashboard-with-code.html
```

### Dashboard Features
- **Search**: Real-time filtering of issues
- **Severity Filters**: Click All/Errors/Warnings/Style/Performance buttons
- **Code Preview**: Click the eye icon to see code context (if available)
- **Statistics**: Summary cards showing issue breakdown
- **Responsive**: Works on all screen sizes

### For Development (EXPERIMENTAL)

The TypeScript/Node.js structure exists but is not fully functional:

```bash
# Install dependencies
npm install

# Try to run development servers (may not work properly)
npm run dev

# The CLI exists but doesn't actually run cppcheck
npm install -g ./packages/cli
cppcheck-studio --help
```

## 📊 Analysis Results - LPZRobots

### Issues Found
The project successfully analyzed the LPZRobots C++ codebase:
- **Total Issues**: 2,975
- **Errors**: 772 (25.9%) - Critical issues requiring fixes
- **Warnings**: 153 (5.1%) - Potential problems
- **Style**: 1,932 (64.9%) - Code style and modernization
- **Performance**: 31 (1.0%) - Optimization opportunities

### Common C++ Issues Identified
1. Missing `override` specifiers on virtual functions
2. Uninitialized member variables in constructors
3. Missing `explicit` on single-parameter constructors
4. C-style casts instead of `static_cast`
5. Functions that should be marked `const`
6. Pass-by-value where pass-by-const-reference would be better
7. Using `NULL` instead of `nullptr`
8. Postfix increment/decrement where prefix would be more efficient

## 🔧 Dashboard Comparison

### Available Dashboard Generators

1. **generate-ultimate-dashboard.py** ✅ RECOMMENDED
   - File size: ~240KB
   - Features: All interactive features, clean UI
   - Performance: Excellent, loads instantly
   - Use case: Production dashboards

2. **generate-virtual-scroll-dashboard.py** ✅ For Large Datasets
   - Virtual scrolling for 10,000+ issues
   - Memory efficient
   - JSONL data format
   - Use case: Very large codebases

3. **generate-robust-dashboard.py** ✅ Error Handling
   - Comprehensive error handling
   - Chunked rendering (100 issues at a time)
   - Progress indicators
   - Use case: When reliability is critical

4. **generate-production-dashboard.py** ✅ Minimal
   - No embedded code context
   - Smallest file size
   - Use case: Quick overview without code

5. **generate-split-dashboard.py** ✅ Modular
   - Separates issues and context into different files
   - Use case: When you need to process data separately

## 🐛 Known Issues & Limitations

### Current State

1. **Python Scripts Work** ✅
   - All dashboard generators function correctly
   - Successfully analyzes C++ code via cppcheck
   - Generates beautiful interactive dashboards

2. **TypeScript/Node.js Incomplete** ⚠️
   - Monorepo structure exists but isn't functional
   - CLI doesn't actually call cppcheck
   - API endpoints are stubs only
   - No database implementation
   - Next.js app only has landing page

3. **Integration Issues** ⚠️
   - Fix automation pipeline incomplete
   - Metrics tracking non-functional
   - No automatic fix generation from reports

### Common Problems & Solutions

#### Problem: Dashboard shows no issues
**Solution**: Make sure your cppcheck JSON output is valid. The wrapper script may add extra text.
```bash
# Extract just the JSON from the output
tools/cppcheck/cppcheck cpp17 --format json | tail -n +4 > analysis.json
```

#### Problem: Code context not showing
**Solution**: Use add-code-context.py before generating dashboard
```bash
python3 add-code-context.py analysis.json analysis-with-context.json
```

#### Problem: Dashboard too large
**Solution**: Use generate-virtual-scroll-dashboard.py for large datasets or generate-production-dashboard.py for minimal size

## 📈 Performance Characteristics

### Dashboard Performance
- **Ultimate Dashboard**: ~240KB, loads in <2s, handles 3,000 issues well
- **Virtual Scroll**: Handles 10,000+ issues, only renders visible rows
- **Production Dashboard**: Smallest size, no code context, fastest load

### Analysis Performance
- CPPCheck analysis: ~11 seconds for LPZRobots codebase
- Dashboard generation: <1 second
- File size impact: Each issue with code context adds ~500 bytes

## 🎯 Purpose and Goals

### Original Intent
This project was created to analyze the LPZRobots C++ codebase and visualize the static analysis results in an interactive way. The goal was to make it easier to understand and prioritize the 2,975 issues found.

### What Was Achieved
1. **Beautiful HTML Dashboards** - Multiple Python generators that create interactive visualizations
2. **Code Context Integration** - Ability to see the actual code around each issue
3. **Virtual Scrolling** - Handle large datasets efficiently
4. **Multiple Output Formats** - Different dashboards for different use cases

### What Wasn't Completed
1. **Full NPM Package** - The TypeScript/Node.js structure exists but isn't connected to cppcheck
2. **Real-time Analysis** - The WebSocket infrastructure exists but isn't used
3. **Fix Automation** - Fix patterns are defined but not automatically applied
4. **Database Storage** - Prisma is configured but no schema exists
5. **Web Application** - Only the landing page was implemented

## 🚀 If You Want to Extend This Project

### To Make the TypeScript/Node.js Parts Work

1. **Connect CLI to Actual cppcheck**
   - Modify `packages/cli/src/commands/analyze.ts` to actually execute cppcheck
   - Parse the JSON output and store results
   - Implement the fix application logic

2. **Build the Web Dashboard**
   - Create `/app/dashboard/page.tsx` in the Next.js app
   - Port the HTML dashboard logic to React components
   - Connect to the API endpoints

3. **Implement the Database**
   - Create Prisma schema for projects and analyses
   - Run migrations
   - Update API endpoints to use database

4. **Add Authentication**
   - Implement JWT auth in the API
   - Add login/register pages
   - Protect routes

### To Improve the Python Scripts

1. **Add More Dashboard Types**
   - Trend analysis over time
   - Comparison between analyses
   - Team/developer statistics

2. **Enhance Fix Generation**
   - Connect to the fix patterns in TypeScript code
   - Generate fix files automatically
   - Add more fix patterns

3. **Better Integration**
   - Create a unified Python CLI that wraps all scripts
   - Add progress bars and better error handling
   - Support more cppcheck output formats

## 📋 Working Instructions for Claude

### Understanding the Repository

1. **This is primarily a Python dashboard generator project**
   - The core functionality is in the Python scripts
   - The TypeScript/Node.js code is aspirational/incomplete
   - Focus on the Python scripts for actual functionality

2. **The main use case is analyzing LPZRobots**
   - 2,975 issues have been found and visualized
   - The dashboards successfully display these issues
   - This is a proof-of-concept for C++ analysis visualization

### When Asked to Work on This Project

1. **For Dashboard Generation**
   ```bash
   # Use the Python scripts that actually work
   python3 generate-ultimate-dashboard.py input.json output.html
   ```

2. **For TypeScript Development**
   - Understand that most TypeScript code is scaffolding
   - The CLI doesn't actually run cppcheck
   - The API endpoints are mostly stubs
   - The web app only has a landing page

3. **For Improvements**
   - Focus on enhancing the Python scripts
   - Or work on connecting the TypeScript code to actual functionality
   - Don't assume the npm package works - it doesn't fully

### Key Files to Understand

1. **Working Files**
   - `generate-ultimate-dashboard.py` - Best dashboard generator
   - `add-code-context.py` - Adds code snippets
   - `FINAL_PRODUCTION_DASHBOARD.html` - Example output

2. **Partially Working**
   - `packages/cli/` - CLI structure exists but doesn't run cppcheck
   - `apps/web/` - Only has landing page
   - `apps/api/` - Routes defined but not implemented

3. **Documentation**
   - `FINAL_SOLUTION_SUMMARY.md` - Explains the dashboard problem/solution
   - `INTEGRATION_TEST_REPORT.md` - Shows what works and what doesn't
   - `DEMO_USAGE.md` - How to use the Python scripts

## 🚀 Quick Reference

### Working Commands (Python)
```bash
# Generate ultimate dashboard (recommended)
python3 generate-ultimate-dashboard.py analysis.json dashboard.html

# Add code context to analysis
python3 add-code-context.py analysis.json analysis-with-context.json

# Generate virtual scroll dashboard (for large datasets)
python3 generate-virtual-scroll-dashboard.py analysis.json virtual.html

# Generate minimal dashboard (no code context)
python3 generate-production-dashboard.py analysis.json minimal.html
```

### File Locations
- **Analysis Results**: `analysis-with-context.json` (2,975 issues)
- **Generated Dashboards**: `FINAL_PRODUCTION_DASHBOARD.html` and others
- **Python Scripts**: Root directory of cppcheck-studio
- **TypeScript Code**: `apps/` and `packages/` directories

### Dashboard Files Explained
- **FINAL_PRODUCTION_DASHBOARD.html** - The main working dashboard
- **VIRTUAL_SCROLL_DASHBOARD.html** - Uses virtual scrolling
- **ROBUST_DASHBOARD.html** - Has error handling
- **Multiple test dashboards** - Various experiments

### Common Tasks
```bash
# View the working dashboard
open FINAL_PRODUCTION_DASHBOARD.html

# Run analysis on LPZRobots
cd /Users/jerry/simulator/lpz
tools/cppcheck/cppcheck cpp17 --format json > analysis.json

# Generate new dashboard
cd cppcheck-studio
python3 generate-ultimate-dashboard.py ../analysis.json new-dashboard.html
```

## 📚 Summary

### What This Project Is
- A collection of Python scripts that generate beautiful HTML dashboards from cppcheck output
- Successfully analyzed LPZRobots with 2,975 issues found
- Creates interactive, searchable, filterable visualizations of C++ static analysis

### What Works
- All Python dashboard generators (use `generate-ultimate-dashboard.py` for best results)
- Interactive features: search, filter, code preview
- Virtual scrolling for large datasets
- Multiple dashboard styles for different needs

### What Doesn't Work
- The npm package doesn't actually run cppcheck
- TypeScript CLI is just scaffolding
- API endpoints are stubs
- Database not implemented
- Web app only has landing page

### How to Use It
1. Run cppcheck to get JSON output
2. Use Python scripts to generate HTML dashboards
3. Open HTML files in browser
4. Don't rely on the TypeScript/Node.js parts - they're incomplete

### Key Understanding
This is primarily a **Python-based dashboard generator** for cppcheck results, with an **aspirational but incomplete** TypeScript/Node.js architecture. The Python scripts are production-ready; the TypeScript code is not.

---

*Last updated: January 2025 - Based on analysis of actual codebase state*