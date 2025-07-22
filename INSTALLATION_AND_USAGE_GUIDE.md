# CPPCheck Studio - Complete Installation & Usage Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Generating CPPCheck Data](#generating-cppcheck-data)
4. [Creating Dashboards](#creating-dashboards)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### For TypeScript Version
- Node.js >= 14.0
- npm or yarn
- Git (for cloning repository)

### For Python Version
- Python >= 3.6
- No additional dependencies required

### For Running CPPCheck
- CPPCheck installed (`brew install cppcheck` on macOS)
- C++ source code to analyze

## Installation

### Option 1: TypeScript/Node.js Package

```bash
# Clone the repository
git clone <repository-url>
cd cppcheck-studio/cppcheck-dashboard-generator

# Install dependencies
npm install

# Build the TypeScript code
npm run build

# Option A: Use directly
node dist/cli.js --help

# Option B: Install globally
npm link
cppcheck-dashboard --help
```

### Option 2: Python Scripts (No Installation Required)

```bash
# Clone the repository
git clone <repository-url>
cd cppcheck-studio

# Scripts are ready to use immediately
python3 generate/generate-standalone-virtual-dashboard.py --help
```

## Generating CPPCheck Data

### Step 1: Run CPPCheck Analysis

```bash
# Basic analysis
cppcheck --enable=all --output-format=json src/ > analysis.json

# With specific C++ standard
cppcheck --enable=all --std=c++17 --output-format=json src/ > analysis.json

# With multiple directories
cppcheck --enable=all --output-format=json src/ include/ lib/ > analysis.json

# Specific checks only
cppcheck --enable=warning,style,performance --output-format=json src/ > analysis.json
```

### Step 2: Add Code Context (Optional but Recommended)

```bash
# This adds code snippets around each issue for better understanding
python3 add-code-context.py analysis.json analysis-with-context.json
```

## Creating Dashboards

### Using TypeScript Version

```bash
# Basic usage
cd cppcheck-dashboard-generator
node dist/cli.js ../analysis.json ../dashboard.html

# With custom title and project name
node dist/cli.js ../analysis.json ../dashboard.html \
  --title "My Project Analysis" \
  --project "MyAwesomeProject"

# Using the test data
node dist/cli.js ../data/analysis-with-context.json test-dashboard.html
```

### Using Python Version

```bash
# Recommended: Virtual scrolling dashboard
python3 generate/generate-standalone-virtual-dashboard.py analysis.json dashboard.html

# Alternative generators:

# Ultimate dashboard (smaller file, all features)
python3 generate/generate-ultimate-dashboard.py analysis.json dashboard.html

# Production dashboard (minimal size, no code context)
python3 generate/generate-production-dashboard.py analysis.json dashboard.html

# Robust dashboard (enhanced error handling)
python3 generate/generate-robust-dashboard.py analysis.json dashboard.html
```

### Opening the Dashboard

```bash
# macOS
open dashboard.html

# Linux
xdg-open dashboard.html

# Windows
start dashboard.html

# Or simply drag the HTML file to your browser
```

## Advanced Usage

### Programmatic Usage (TypeScript)

```typescript
// In your TypeScript/JavaScript project
import { StandaloneVirtualDashboardGenerator } from 'cppcheck-dashboard-generator';

async function generateDashboard() {
  const generator = new StandaloneVirtualDashboardGenerator({
    input: 'analysis.json',
    output: 'dashboard.html',
    title: 'Code Quality Report',
    projectName: 'MyProject'
  });
  
  await generator.generate();
  console.log('Dashboard created!');
}
```

### Integrating with Build Systems

#### Makefile
```makefile
.PHONY: analyze dashboard

analyze:
	cppcheck --enable=all --output-format=json src/ > analysis.json
	python3 add-code-context.py analysis.json analysis-with-context.json

dashboard: analyze
	python3 generate/generate-standalone-virtual-dashboard.py \
	  analysis-with-context.json dashboard.html
	open dashboard.html

# Or with TypeScript version
dashboard-ts: analyze
	cd cppcheck-dashboard-generator && \
	node dist/cli.js ../analysis-with-context.json ../dashboard.html
```

#### NPM Scripts (package.json)
```json
{
  "scripts": {
    "analyze": "cppcheck --enable=all --output-format=json src/ > analysis.json",
    "add-context": "python3 add-code-context.py analysis.json analysis-with-context.json",
    "dashboard": "node cppcheck-dashboard-generator/dist/cli.js analysis-with-context.json dashboard.html",
    "report": "npm run analyze && npm run add-context && npm run dashboard"
  }
}
```

#### GitHub Actions
```yaml
name: Code Analysis

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
          cppcheck --enable=all --output-format=json src/ > analysis.json
          python3 add-code-context.py analysis.json analysis-with-context.json
          
      - name: Generate Dashboard
        run: |
          python3 generate/generate-standalone-virtual-dashboard.py \
            analysis-with-context.json dashboard.html
            
      - name: Upload Dashboard
        uses: actions/upload-artifact@v3
        with:
          name: cppcheck-dashboard
          path: dashboard.html
```

### Handling Large Projects

For projects with thousands of issues:

```bash
# Use virtual scrolling dashboard (handles 100,000+ issues)
python3 generate/generate-standalone-virtual-dashboard.py large-analysis.json dashboard.html

# Or TypeScript version (also has virtual scrolling)
node cppcheck-dashboard-generator/dist/cli.js large-analysis.json dashboard.html
```

### Filtering Analysis Results

You can pre-filter the JSON before generating dashboards:

```python
# filter_issues.py
import json

with open('analysis.json', 'r') as f:
    data = json.load(f)

# Filter only errors and warnings
filtered_issues = [
    issue for issue in data['issues'] 
    if issue.get('severity') in ['error', 'warning']
]

with open('filtered-analysis.json', 'w') as f:
    json.dump({'issues': filtered_issues}, f, indent=2)
```

## Troubleshooting

### Common Issues

#### 1. Dashboard shows no data
**Problem**: Empty or malformed JSON
**Solution**: 
```bash
# Check JSON validity
python3 -m json.tool analysis.json > /dev/null
# If error, check cppcheck output format
```

#### 2. Code context not showing
**Problem**: Missing code context in JSON
**Solution**: Run `add-code-context.py` before generating dashboard

#### 3. Performance issues with large files
**Problem**: Too many issues causing slow load
**Solution**: Use virtual scrolling dashboard or filter issues first

#### 4. TypeScript build errors
**Problem**: Missing dependencies or wrong Node version
**Solution**:
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Debugging Tips

1. **Check JSON structure**:
```bash
# View first few issues
cat analysis.json | python3 -m json.tool | head -50
```

2. **Test with sample data**:
```bash
# Use provided test data
python3 generate/generate-standalone-virtual-dashboard.py \
  data/analysis-with-context.json test.html
```

3. **Enable verbose output** (Python):
```python
# Add to generator scripts for debugging
print(f"Processing {len(issues)} issues...")
```

## Best Practices

1. **Always add code context** for better issue understanding
2. **Use virtual scrolling** for projects with 1000+ issues
3. **Regular analysis** - Integrate into CI/CD pipeline
4. **Archive dashboards** - Keep historical data for trends
5. **Filter strategically** - Focus on errors first, then warnings

## Example Workflow

Complete workflow for a C++ project:

```bash
# 1. Clone CPPCheck Studio
git clone <repository-url>
cd cppcheck-studio

# 2. Analyze your C++ project
cppcheck --enable=all --std=c++17 --output-format=json \
  ~/my-cpp-project/src > my-analysis.json

# 3. Add code context
python3 add-code-context.py my-analysis.json my-analysis-with-context.json

# 4. Generate dashboard (choose one)

# Option A: TypeScript version
cd cppcheck-dashboard-generator
npm install && npm run build
node dist/cli.js ../my-analysis-with-context.json ../my-dashboard.html

# Option B: Python version
python3 generate/generate-standalone-virtual-dashboard.py \
  my-analysis-with-context.json my-dashboard.html

# 5. View results
open my-dashboard.html
```

## Next Steps

- Explore different dashboard types
- Customize styles in TypeScript version
- Set up automated analysis in CI/CD
- Create custom filters for your project
- Share dashboards with your team

---

For more information, see:
- [PROJECT_UNIFIED_DOCUMENTATION.md](PROJECT_UNIFIED_DOCUMENTATION.md)
- [README.md](README.md)
- [CLAUDE.md](CLAUDE.md)