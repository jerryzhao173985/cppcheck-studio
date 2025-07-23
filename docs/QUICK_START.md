# 🚀 CPPCheck Studio Quick Start Guide

Get started analyzing C++ code in under 5 minutes!

## Installation

### Option 1: Python (Recommended for Quick Start)
```bash
# Clone the repository
git clone https://github.com/jerryzhao173985/cppcheck-studio.git
cd cppcheck-studio

# No installation needed! Python scripts work directly
```

### Option 2: TypeScript/npm Package
```bash
# Install globally
npm install -g cppcheck-dashboard-generator

# Or in your project
npm install cppcheck-dashboard-generator
```

## Basic Usage

### Step 1: Run CPPCheck on Your Code
```bash
# Analyze your C++ project
cppcheck --enable=all --xml --xml-version=2 your-cpp-project/ 2> analysis.xml

# Convert XML to JSON
python3 cppcheck-studio/xml2json-simple.py analysis.xml > analysis.json
```

### Step 2: Generate Interactive Dashboard
```bash
# Recommended: Use the standalone virtual dashboard generator
python3 cppcheck-studio/generate/generate-standalone-virtual-dashboard.py \
  analysis.json \
  dashboard.html

# Open in browser
open dashboard.html  # macOS
xdg-open dashboard.html  # Linux
```

## Common Use Cases

### 1. Analyze a GitHub Repository
```bash
# Use the GitHub Action (easiest)
# Go to: https://github.com/jerryzhao173985/cppcheck-studio/actions
# Click "On-Demand Repository Analysis v3"
# Enter repository details and run
```

### 2. Add Code Context (Recommended)
```bash
# Add code snippets around each issue
python3 cppcheck-studio/add-code-context.py \
  analysis.json \
  analysis-with-context.json \
  --base-path /path/to/your/project

# Generate dashboard with context
python3 cppcheck-studio/generate/generate-standalone-virtual-dashboard.py \
  analysis-with-context.json \
  dashboard.html
```

### 3. Large Codebase (10,000+ issues)
```bash
# Use virtual scrolling dashboard
python3 cppcheck-studio/generate/generate-virtual-scroll-dashboard.py \
  large-analysis.json \
  dashboard.html
```

### 4. CI/CD Integration
```yaml
# GitHub Actions example
- name: Run CPPCheck
  run: |
    cppcheck --enable=all --xml --xml-version=2 . 2> analysis.xml
    python3 xml2json-simple.py analysis.xml > analysis.json
    python3 generate/generate-production-dashboard.py analysis.json dashboard.html
    
- name: Upload Dashboard
  uses: actions/upload-artifact@v4
  with:
    name: cppcheck-dashboard
    path: dashboard.html
```

## Dashboard Features

### Interactive Elements
- 🔍 **Search**: Filter issues by keyword
- 🏷️ **Severity Filters**: Click to show/hide by severity
- 👁️ **Code Preview**: Click eye icon to see code context
- 📊 **Statistics**: Summary cards with issue breakdown
- ⚡ **Virtual Scrolling**: Handles 100,000+ issues smoothly

### Keyboard Shortcuts
- `/` - Focus search box
- `Esc` - Clear search
- `1-5` - Toggle severity filters

## Examples

### Example 1: Quick Analysis
```bash
# Simplest possible usage
cppcheck --xml --xml-version=2 main.cpp 2> result.xml
python3 xml2json-simple.py result.xml > result.json
python3 generate/generate-simple-dashboard.py result.json dashboard.html
```

### Example 2: Full Featured Analysis
```bash
# Complete analysis with all features
PROJECT_DIR="/path/to/project"
OUTPUT_DIR="cppcheck-results"

mkdir -p $OUTPUT_DIR
cd $PROJECT_DIR

# Run comprehensive analysis
cppcheck \
  --enable=all \
  --inconclusive \
  --std=c++17 \
  --platform=native \
  --xml \
  --xml-version=2 \
  . 2> $OUTPUT_DIR/analysis.xml

# Convert and add context
cd $OUTPUT_DIR
python3 $OLDPWD/cppcheck-studio/xml2json-simple.py analysis.xml > analysis.json
python3 $OLDPWD/cppcheck-studio/add-code-context.py \
  analysis.json \
  analysis-with-context.json \
  --base-path $PROJECT_DIR

# Generate dashboard
python3 $OLDPWD/cppcheck-studio/generate/generate-standalone-virtual-dashboard.py \
  analysis-with-context.json \
  dashboard.html

echo "Dashboard ready at: $OUTPUT_DIR/dashboard.html"
```

## Troubleshooting

### No Issues Found?
```bash
# Make sure to enable all checks
cppcheck --enable=all --inconclusive ...

# Check XML output isn't empty
cat analysis.xml
```

### Dashboard Generation Failed?
```bash
# Check JSON is valid
python3 -m json.tool analysis.json > /dev/null

# Use simple generator as fallback
python3 generate/generate-simple-dashboard.py analysis.json dashboard.html
```

### Memory Issues with Large Files?
```bash
# Use streaming generator
python3 generate/generate-virtual-scroll-dashboard.py large.json dashboard.html
```

## Next Steps

1. 📖 Read [Generator Comparison](GENERATOR_COMPARISON.md) to choose the best generator
2. 🔧 Check [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues
3. 🎨 Customize dashboard appearance with CSS
4. 🤖 Set up automated analysis with GitHub Actions

## Get Help

- 📝 [Full Documentation](https://github.com/jerryzhao173985/cppcheck-studio#readme)
- 🐛 [Report Issues](https://github.com/jerryzhao173985/cppcheck-studio/issues)
- 💬 [Discussions](https://github.com/jerryzhao173985/cppcheck-studio/discussions)