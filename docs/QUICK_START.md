# 🚀 CPPCheck Studio - Quick Start Guide

Get up and running with CPPCheck Studio in under 2 minutes!

## 📦 Installation

### Option 1: Quick Install (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/cppcheck-studio.git
cd cppcheck-studio

# Run installer
./install.sh

# Add to PATH if needed (installer will tell you)
export PATH="$PATH:$HOME/.local/bin"
```

### Option 2: Direct Usage
```bash
# No installation needed - run directly
cd cppcheck-studio
./cppcheck-studio /path/to/your/project
```

## 🎯 Basic Usage

### 1. Analyze Current Project
```bash
# In your C++ project directory
cppcheck-studio .

# Opens dashboard automatically!
```

### 2. Analyze Specific Directories
```bash
cppcheck-studio src/ include/ lib/
```

### 3. Custom Output
```bash
cppcheck-studio src/ -o report.html
```

## ⚡ Quick Commands

### Minimal Dashboard (Fast, No Code)
```bash
cppcheck-studio . --no-code
```

### Different Dashboard Types
```bash
# Virtual scroll (default) - Best for large projects
cppcheck-studio . --type virtual

# Robust - With error handling
cppcheck-studio . --type robust

# Minimal - Smallest file size
cppcheck-studio . --type minimal
```

## ⚙️ Configuration

### Create Config File
```bash
cppcheck-studio --init
```

### Example `.cppcheckstudio.json`
```json
{
  "cppcheck": {
    "enable": "all",
    "std": "c++17",
    "inconclusive": true,
    "suppress": ["unusedFunction"]
  },
  "dashboard": {
    "type": "virtual",
    "include_code": true,
    "context_lines": 5
  }
}
```

## 🔧 Makefile Integration

Add to your `Makefile`:
```makefile
analyze:
	cppcheck-studio src/ -o build/analysis.html

clean: clean-analysis

clean-analysis:
	rm -f build/analysis.html
```

## 🎨 Dashboard Features

### Search & Filter
- 🔍 **Search**: Type to filter by file, message, or ID
- 🎯 **Severity**: Click buttons to filter by error/warning/style
- 📊 **Stats**: See issue breakdown at a glance

### Code Preview
- Click any issue to see the actual code
- 5 lines before and after the problem
- Syntax highlighted

### Performance
- Virtual scrolling handles 10,000+ issues
- Instant search and filtering
- Works offline, no dependencies

## 📊 Example Output

```
Running analysis on LPZRobots:
🔍 Running CPPCheck analysis...
✅ Analysis complete: cppcheck_results.xml
📄 Converting XML to JSON...
✅ Converted to JSON: analysis.json
📝 Adding code context...
✅ Added code context: analysis-with-context.json
📊 Generating dashboard...
✅ Dashboard generated: cppcheck-dashboard.html

🎉 Analysis complete!
📊 View dashboard: file:///Users/you/project/cppcheck-dashboard.html

Results:
- Total Issues: 2,975
- Errors: 772 (25.9%)
- Warnings: 153 (5.1%)
- Style: 1,932 (64.9%)
- Performance: 31 (1.0%)
```

## 🚨 Common Issues

### CPPCheck Not Found
```bash
# Install cppcheck first
brew install cppcheck      # macOS
apt install cppcheck       # Ubuntu
choco install cppcheck     # Windows
```

### Permission Denied
```bash
chmod +x install.sh
chmod +x cppcheck-studio
```

### Large Projects
Use `--no-code` for faster analysis of very large codebases:
```bash
cppcheck-studio . --no-code --type minimal
```

## 🎯 Pro Tips

### 1. CI/CD Integration
```yaml
# GitHub Actions
- name: Code Analysis
  run: |
    cppcheck-studio src/ -o analysis.html
    
- uses: actions/upload-artifact@v3
  with:
    name: analysis-report
    path: analysis.html
```

### 2. Git Hook
```bash
# .git/hooks/pre-push
#!/bin/bash
cppcheck-studio src/ --no-code -o .analysis.html
if [ -f .analysis.html ]; then
  echo "📊 Analysis complete: .analysis.html"
fi
```

### 3. Watch Mode
```bash
# Analyze on file change (requires fswatch)
fswatch -o src/ | xargs -n1 -I{} cppcheck-studio src/
```

## 📚 Next Steps

1. **Customize Analysis**: Edit `.cppcheckstudio.json`
2. **Integrate with Build**: Add to `Makefile` or `CMakeLists.txt`
3. **Set Up CI/CD**: Add to your pipeline
4. **Share Reports**: HTML files work everywhere

## 🆘 Need Help?

- Run `cppcheck-studio --help` for all options
- Check [COMPLETE_WORKFLOW_DEMO.md](COMPLETE_WORKFLOW_DEMO.md) for detailed guide
- Report issues on GitHub

---

**Ready to improve your C++ code quality? Start analyzing!** 🚀