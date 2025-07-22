# 🎯 CPPCheck Studio - Complete Workflow Demo

This guide demonstrates the complete workflow of using CPPCheck Studio to analyze a large C++ codebase, from initial setup to generating professional dashboards.

## 📋 Table of Contents
1. [Environment Setup](#1-environment-setup)
2. [Running CPPCheck Analysis](#2-running-cppcheck-analysis)
3. [Data Processing](#3-data-processing)
4. [Dashboard Generation](#4-dashboard-generation)
5. [Using the Dashboard](#5-using-the-dashboard)
6. [Advanced Features](#6-advanced-features)
7. [Integration Examples](#7-integration-examples)
8. [Troubleshooting](#8-troubleshooting)

## 1. Environment Setup

### Prerequisites Installation

```bash
# macOS
brew install cppcheck python3

# Ubuntu/Debian
sudo apt-get install cppcheck python3 python3-pip

# Verify installations
cppcheck --version  # Should be 2.0 or higher
python3 --version   # Should be 3.6 or higher
```

### Clone CPPCheck Studio

```bash
# Clone the repository
git clone https://github.com/yourusername/cppcheck-studio.git
cd cppcheck-studio

# Make scripts executable
chmod +x *.py
```

## 2. Running CPPCheck Analysis

### Basic Analysis

```bash
# Navigate to your C++ project
cd /path/to/your/cpp/project

# Run basic analysis
cppcheck --enable=all --xml --xml-version=2 . 2> cppcheck_results.xml
```

### Advanced Analysis Options

```bash
# Comprehensive analysis with all checks
cppcheck \
  --enable=all \
  --inconclusive \
  --std=c++17 \
  --platform=unix64 \
  --inline-suppr \
  --suppress=missingIncludeSystem \
  --xml --xml-version=2 \
  -I include/ \
  -I src/include/ \
  src/ lib/ 2> cppcheck_results.xml

# With custom configuration
cppcheck \
  --enable=all \
  --library=std.cfg \
  --library=posix.cfg \
  --addon=cert \
  --addon=misra \
  --xml --xml-version=2 \
  . 2> cppcheck_results.xml
```

### Example: Analyzing LPZRobots

```bash
cd ~/simulator/lpz
cppcheck \
  --enable=all \
  --inconclusive \
  --std=c++17 \
  --xml --xml-version=2 \
  -I selforg/ \
  -I ode_robots/ \
  -I include/ \
  selforg/ ode_robots/ 2> cppcheck_lpzrobots.xml
```

## 3. Data Processing

### Convert XML to JSON

```bash
# Basic conversion
python3 ~/cppcheck-studio/xml2json.py cppcheck_results.xml analysis.json

# Output:
# ✅ Parsed 2975 issues from XML
# ✅ Converted to JSON format
# ✅ Output written to analysis.json
```

### Add Code Context

```bash
# Add code snippets to each issue
python3 ~/cppcheck-studio/add-code-context.py analysis.json analysis-with-context.json

# Output:
# 📂 Processing 2975 issues...
# ✅ Successfully added code context to 2890 issues (97.14%)
# ⚠️  Skipped 85 issues (line 0 or file not found)
# 💾 Output written to analysis-with-context.json
```

### Verify Data

```bash
# Check issue counts
jq '.issues | length' analysis-with-context.json
# 2975

# Check severity distribution
jq '.issues | group_by(.severity) | map({severity: .[0].severity, count: length})' analysis-with-context.json
# [
#   {"severity": "error", "count": 772},
#   {"severity": "information", "count": 85},
#   {"severity": "performance", "count": 31},
#   {"severity": "portability", "count": 2},
#   {"severity": "style", "count": 1932},
#   {"severity": "warning", "count": 153}
# ]
```

## 4. Dashboard Generation

### Option 1: Virtual Scroll Dashboard (Recommended)

```bash
# Generate the best dashboard with all features
python3 ~/cppcheck-studio/generate-standalone-virtual-dashboard.py \
  analysis-with-context.json \
  my-project-dashboard.html

# Output:
# ✅ Standalone virtual scroll dashboard generated: my-project-dashboard.html
#    Total issues: 2975
#    Issues with code context: 2890
#    File size: 3.2 MB
#    No server required - works with file:// protocol
```

### Option 2: Lightweight Dashboard

```bash
# For smaller file size without code context
python3 ~/cppcheck-studio/generate-production-dashboard.py \
  analysis.json \
  lightweight-dashboard.html

# Output:
# ✅ Dashboard generated successfully!
#    Total issues: 2975
#    File size: 240 KB
```

### Option 3: Split Data Dashboard

```bash
# Generates separate JSONL files for better performance
python3 ~/cppcheck-studio/generate-virtual-scroll-dashboard.py \
  analysis-with-context.json \
  split-dashboard.html

# Output:
# ✅ Virtual scroll dashboard generated: split-dashboard.html
#    Data directory: dashboard_data/
#    - issues.jsonl: 675.8 KB
#    - code_context.jsonl: 2655.6 KB

# Note: Requires HTTP server due to CORS
python3 -m http.server 8080
# Open http://localhost:8080/split-dashboard.html
```

## 5. Using the Dashboard

### Opening the Dashboard

```bash
# macOS
open my-project-dashboard.html

# Linux
xdg-open my-project-dashboard.html

# Windows
start my-project-dashboard.html
```

### Dashboard Features Demo

#### 1. Overview Statistics
- **Error Card (Red)**: Shows 772 errors (25.9%)
- **Warning Card (Orange)**: Shows 153 warnings (5.1%)
- **Style Card (Blue)**: Shows 1932 style issues (64.9%)
- **Performance Card (Green)**: Shows 31 performance issues (1.0%)

#### 2. Search Functionality
```
Search examples:
- "memory leak" → Find all memory-related issues
- "controller.h" → Show issues in specific file
- "override" → Find missing override specifiers
- "CA88A3A1" → Find specific issue by ID
```

#### 3. Severity Filtering
- Click **"All (2975)"** to show all issues
- Click **"Errors (772)"** to show only errors
- Click **"Warnings (153)"** to show only warnings
- Click **"Style (1932)"** to show style issues
- Click **"Performance (31)"** to show performance issues

#### 4. Code Context Preview
1. Click any row with blue indicator (▌)
2. Modal shows:
   - Full file path
   - Line number
   - Complete error message
   - 5 lines before and after the issue
   - Highlighted problem line

#### 5. Virtual Scrolling
- Scroll through 2975 issues smoothly
- Only ~20-30 rows rendered at a time
- No lag or memory issues
- Instant response to scrolling

## 6. Advanced Features

### Custom Suppressions

Create `suppressions.txt`:
```
// Suppress all unusedFunction in test files
unusedFunction:*test*.cpp

// Suppress specific warning
uninitMemberVar:src/legacy/old_code.cpp:42

// Suppress by error id
[id:nullPointer]
```

Run with suppressions:
```bash
cppcheck --suppressions-list=suppressions.txt --enable=all --xml --xml-version=2 . 2> results.xml
```

### Incremental Analysis

```bash
# Only analyze changed files
git diff --name-only HEAD~1 | grep -E '\.(cpp|h|hpp)$' > changed_files.txt
cppcheck --file-list=changed_files.txt --enable=all --xml --xml-version=2 2> incremental.xml
```

### Custom Rules

Create `custom-rules.xml`:
```xml
<rules>
  <rule>
    <pattern>malloc\s*\(</pattern>
    <message>
      <id>customMalloc</id>
      <severity>style</severity>
      <summary>Use new instead of malloc in C++</summary>
    </message>
  </rule>
</rules>
```

Run with custom rules:
```bash
cppcheck --rule-file=custom-rules.xml --enable=all --xml --xml-version=2 . 2> results.xml
```

## 7. Integration Examples

### Git Pre-commit Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Run cppcheck on staged files
git diff --cached --name-only --diff-filter=ACM | grep -E '\.(cpp|h|hpp)$' | \
  xargs cppcheck --enable=warning,style --error-exitcode=1

if [ $? -ne 0 ]; then
  echo "❌ CPPCheck found issues. Please fix before committing."
  exit 1
fi
```

### CI/CD Integration

#### GitHub Actions
```yaml
name: CPPCheck Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install CPPCheck
        run: sudo apt-get install -y cppcheck
      
      - name: Run Analysis
        run: |
          cppcheck --enable=all --xml --xml-version=2 src/ 2> cppcheck.xml
          
      - name: Convert to JSON
        run: python3 scripts/xml2json.py cppcheck.xml analysis.json
        
      - name: Generate Dashboard
        run: |
          python3 scripts/add-code-context.py analysis.json analysis-with-context.json
          python3 scripts/generate-standalone-virtual-dashboard.py \
            analysis-with-context.json dashboard.html
      
      - name: Upload Dashboard
        uses: actions/upload-artifact@v3
        with:
          name: cppcheck-dashboard
          path: dashboard.html
          
      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const analysis = JSON.parse(fs.readFileSync('analysis.json'));
            const errors = analysis.issues.filter(i => i.severity === 'error').length;
            const warnings = analysis.issues.filter(i => i.severity === 'warning').length;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## CPPCheck Analysis Results\n\n` +
                    `- **Errors**: ${errors}\n` +
                    `- **Warnings**: ${warnings}\n` +
                    `- **Total Issues**: ${analysis.issues.length}\n\n` +
                    `[View Full Dashboard](https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId})`
            })
```

#### GitLab CI
```yaml
cppcheck:
  stage: test
  script:
    - apt-get update && apt-get install -y cppcheck python3
    - cppcheck --enable=all --xml --xml-version=2 src/ 2> cppcheck.xml
    - python3 scripts/xml2json.py cppcheck.xml analysis.json
    - python3 scripts/add-code-context.py analysis.json analysis-with-context.json
    - python3 scripts/generate-standalone-virtual-dashboard.py analysis-with-context.json dashboard.html
  artifacts:
    paths:
      - dashboard.html
    reports:
      static_analysis: dashboard.html
    expire_in: 1 week
```

### Makefile Integration

```makefile
.PHONY: analyze dashboard clean-analysis

CPPCHECK_OPTIONS = --enable=all --inconclusive --std=c++17
DASHBOARD_SCRIPT = ~/cppcheck-studio/generate-standalone-virtual-dashboard.py

analyze:
	@echo "🔍 Running CPPCheck analysis..."
	@cppcheck $(CPPCHECK_OPTIONS) --xml --xml-version=2 src/ 2> cppcheck.xml
	@python3 ~/cppcheck-studio/xml2json.py cppcheck.xml analysis.json
	@echo "✅ Analysis complete: analysis.json"

dashboard: analyze
	@echo "📊 Generating dashboard..."
	@python3 ~/cppcheck-studio/add-code-context.py analysis.json analysis-with-context.json
	@python3 $(DASHBOARD_SCRIPT) analysis-with-context.json dashboard.html
	@echo "✅ Dashboard ready: dashboard.html"
	@open dashboard.html

clean-analysis:
	@rm -f cppcheck.xml analysis.json analysis-with-context.json dashboard.html
	@echo "🧹 Cleaned analysis files"
```

## 8. Troubleshooting

### Common Issues and Solutions

#### Issue: "No code context available"
**Cause**: Issues at line 0 (file-level messages)  
**Solution**: This is normal for information severity issues

#### Issue: Large dashboard file size
**Solution**: Use production dashboard without code context:
```bash
python3 generate-production-dashboard.py analysis.json small-dashboard.html
```

#### Issue: Dashboard won't load
**Cause**: Browser memory limit with huge datasets  
**Solution**: Use split data version with HTTP server

#### Issue: Missing issues in dashboard
**Check**: Verify JSON conversion worked:
```bash
# Count issues in XML
grep -c "<error" cppcheck.xml

# Count issues in JSON
jq '.issues | length' analysis.json
```

#### Issue: Code context not showing
**Check**: Ensure files exist at paths in analysis:
```bash
# List unique file paths
jq -r '.issues[].file' analysis.json | sort | uniq

# Verify files exist
jq -r '.issues[].file' analysis.json | sort | uniq | xargs ls -la
```

### Performance Tips

1. **For Large Codebases**
   - Use `--file-list` to analyze specific files
   - Enable only needed checks (not `--enable=all`)
   - Use suppressions for third-party code

2. **For Faster Analysis**
   ```bash
   # Use multiple threads
   cppcheck -j 4 --enable=all --xml --xml-version=2 . 2> results.xml
   ```

3. **For Smaller Dashboards**
   - Skip code context addition
   - Use production dashboard generator
   - Filter out low-priority issues

## 📊 Summary

CPPCheck Studio provides a complete workflow for C++ static analysis:

1. **Analysis** - Run cppcheck with appropriate options
2. **Conversion** - Transform XML to JSON format
3. **Enhancement** - Add code context for better debugging
4. **Visualization** - Generate interactive HTML dashboard
5. **Review** - Use virtual scrolling, search, and filters
6. **Integration** - Automate with CI/CD pipelines

The resulting dashboard handles thousands of issues efficiently while providing a professional, responsive interface for code quality management.

---

*Happy analyzing! 🚀*