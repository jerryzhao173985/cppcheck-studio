# CPPCheck Studio

<p align="center">
  <a href="https://jerryzhao173985.github.io/cppcheck-studio/"><img src="https://img.shields.io/badge/GitHub%20Pages-online-success" alt="GitHub Pages Status"></a>
  <a href="https://github.com/jerryzhao173985/cppcheck-studio/actions/workflows/deploy-docs.yml"><img src="https://github.com/jerryzhao173985/cppcheck-studio/actions/workflows/deploy-docs.yml/badge.svg" alt="Deploy Status"></a>
  <img src="https://img.shields.io/badge/version-2.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/python-%3E%3D3.6-brightgreen.svg" alt="Python">
  <img src="https://img.shields.io/badge/node-%3E%3D14.0-green.svg" alt="Node">
  <img src="https://img.shields.io/badge/typescript-5.3-blue.svg" alt="TypeScript">
</p>

<p align="center">
  <b>Transform CPPCheck static analysis into beautiful, interactive dashboards</b>
</p>

## 🌟 Overview

CPPCheck Studio provides **two complete, production-ready implementations** for visualizing C++ static analysis results:

### 1. TypeScript/Node.js Package ✅
Modern npm package with full TypeScript support, CLI interface, and programmatic API.

### 2. Python Scripts Collection ✅
Battle-tested generators with multiple dashboard styles and zero dependencies.

Both create identical, stunning dashboards featuring:
- **🚀 Virtual Scrolling** - Smoothly handle 100,000+ issues
- **📊 Interactive Statistics** - Visual severity breakdown
- **🔍 Real-time Search** - Instant filtering
- **📝 Code Preview** - See issues in context
- **📦 Standalone HTML** - Works offline, no server needed

## 🚀 Quick Start

### TypeScript/Node.js Version

```bash
# Clone and build
git clone <repository>
cd cppcheck-studio/cppcheck-dashboard-generator
npm install && npm run build

# Generate dashboard
node dist/cli.js analysis.json dashboard.html

# Or install globally
npm link
cppcheck-dashboard analysis.json dashboard.html
```

### Python Version

```bash
# No installation needed! Just run:
python3 generate/generate-standalone-virtual-dashboard.py analysis.json dashboard.html
```

## 📊 Real World Results

Successfully tested on the LPZRobots C++ codebase:
- **2,975 issues** analyzed and visualized
- **2,837 issues** with full code context
- **< 1 second** load time
- **3MB** standalone HTML file

## 🎯 Which Version Should I Use?

### Use TypeScript Version If You:
- Want npm package management
- Need TypeScript type safety
- Plan to integrate programmatically
- Prefer modern JavaScript tooling

### Use Python Version If You:
- Want zero setup/dependencies
- Need multiple dashboard styles
- Prefer proven, stable solution
- Work in Python ecosystem

## 📖 Complete Usage Guide

### Step 1: Run CPPCheck Analysis
```bash
# Basic analysis
cppcheck --enable=all src/ --output-file=analysis.json

# With more details (recommended)
cppcheck --enable=all --std=c++17 --suppress=missingInclude \
         --output-file=analysis.json --template=gcc src/
```

### Step 2: Add Code Context (Optional but Recommended)
```bash
# This adds the actual code snippets around each issue
python3 add-code-context.py analysis.json analysis-with-context.json
```

### Step 3: Generate Dashboard

**TypeScript Version:**
```bash
cppcheck-dashboard analysis-with-context.json my-dashboard.html \
  --title "My Project Analysis" \
  --project "MyProject v1.0"
```

**Python Version:**
```bash
# Virtual scroll (best for large datasets)
python3 generate/generate-standalone-virtual-dashboard.py \
  analysis-with-context.json my-dashboard.html

# Ultimate dashboard (recommended for <5000 issues)
python3 generate/generate-ultimate-dashboard.py \
  analysis-with-context.json my-dashboard.html
```

### Step 4: View Results
```bash
# Open in default browser
open my-dashboard.html  # macOS
xdg-open my-dashboard.html  # Linux
start my-dashboard.html  # Windows
```

## 🎨 Dashboard Features

### Interactive Elements
- **Search Bar** - Filter issues in real-time
- **Severity Filters** - One-click filtering by type
- **Statistics Cards** - Visual issue breakdown
- **Virtual Table** - Smooth scrolling through thousands of rows
- **Code Preview** - Click to see issue in context

### Example Statistics
```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   ERRORS    │ │  WARNINGS   │ │   STYLE     │ │ PERFORMANCE │
│    772      │ │    153      │ │   1,932     │ │     31      │
│  (25.9%)    │ │   (5.1%)    │ │  (64.9%)    │ │   (1.0%)   │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

## 🛠️ Installation

### TypeScript Package

```bash
# From source
cd cppcheck-dashboard-generator
npm install
npm run build
npm link  # Makes 'cppcheck-dashboard' command available

# For development
npm run dev  # Watch mode
```

### Python Scripts

No installation required! Just ensure Python 3.6+ is installed:
```bash
python3 --version  # Should be 3.6+
```

## 📁 Project Structure

```
cppcheck-studio/
├── cppcheck-dashboard-generator/    # TypeScript npm package
│   ├── src/                        # Source files
│   ├── dist/                       # Compiled output
│   └── bin/                        # CLI executable
│
├── generate/                       # Python generators
│   ├── generate-standalone-virtual-dashboard.py
│   ├── generate-ultimate-dashboard.py
│   └── ...                        # Other variants
│
├── data/                          # Sample data
│   └── analysis-with-context.json # LPZRobots analysis
│
└── docs/                          # Documentation
```

## 🧪 Advanced Usage

### Programmatic API (TypeScript)

```typescript
import { StandaloneVirtualDashboardGenerator } from 'cppcheck-dashboard-generator';

const generator = new StandaloneVirtualDashboardGenerator({
  input: 'analysis.json',
  output: 'dashboard.html',
  title: 'My Custom Analysis',
  projectName: 'MyProject'
});

await generator.generate();
```

### Python Dashboard Types

1. **standalone-virtual** - Best for 5,000+ issues
2. **ultimate** - Best for <5,000 issues  
3. **production** - Minimal size, no code
4. **robust** - Enhanced error handling
5. **split** - Separate data files

## 🚨 Troubleshooting

### Common Issues

**No data showing in dashboard**
- Check JSON format is valid
- Ensure file paths are correct
- Look for errors in browser console

**Performance issues**
- Use virtual scroll version for large datasets
- Check available browser memory
- Try production dashboard for minimal size

**Code context missing**
- Run `add-code-context.py` first
- Ensure source files are accessible
- Check file paths in JSON

## 🔗 Integration Examples

### CI/CD Pipeline
```yaml
# GitHub Actions example
- name: Run CPPCheck
  run: cppcheck --enable=all src/ --output-file=analysis.json

- name: Generate Dashboard
  run: |
    npm install -g cppcheck-dashboard-generator
    cppcheck-dashboard analysis.json dashboard.html

- name: Upload Dashboard
  uses: actions/upload-artifact@v3
  with:
    name: cppcheck-dashboard
    path: dashboard.html
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
cppcheck --enable=all src/ --output-file=.cppcheck.json
python3 generate/generate-production-dashboard.py .cppcheck.json .cppcheck.html
echo "CPPCheck dashboard generated: .cppcheck.html"
```

## 📈 Performance Benchmarks

| Issues Count | File Size | Load Time | Scroll Performance |
|-------------|-----------|-----------|-------------------|
| 100         | 50 KB     | <0.1s     | 60 FPS           |
| 1,000       | 500 KB    | <0.5s     | 60 FPS           |
| 10,000      | 5 MB      | <1s       | 60 FPS           |
| 100,000     | 50 MB     | <3s       | 55-60 FPS        |

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Tested extensively on the LPZRobots project
- Virtual scrolling inspired by modern web best practices
- Built with love for the C++ community

---

**Note**: The directories `apps/` and `packages/` contain incomplete monorepo scaffolding and should not be used. Use `cppcheck-dashboard-generator/` for TypeScript or `generate/` for Python.