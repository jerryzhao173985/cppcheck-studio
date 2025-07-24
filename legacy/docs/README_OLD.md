# CPPCheck Studio 🎯

**Transform CPPCheck JSON output into beautiful, interactive HTML dashboards with virtual scrolling.**

## 🚀 Quick Start (2 minutes)

```bash
# 1. Run CPPCheck on your C++ code
cppcheck --enable=all --xml --xml-version=2 your-project/ 2> analysis.xml

# 2. Convert XML to JSON
python3 utils/xml2json-simple.py analysis.xml > analysis.json

# 3. Generate dashboard (choose one):
python3 generate/generate-standalone-virtual-dashboard.py analysis.json dashboard.html

# 4. Open in browser
open dashboard.html
```

### 1. TypeScript/Node.js Package ✅
Modern npm package with full TypeScript support, CLI interface, and programmatic API.

### 2. Python Scripts Collection ✅
Battle-tested generators with multiple dashboard styles and zero dependencies.

Both create identical, stunning dashboards featuring:
- **🚀 Virtual Scrolling** - Smoothly handle 100,000+ issues
- **📊 Interactive Statistics** - Visual severity breakdown
- **🔍 Real-time Search** - Instant filtering across all fields
- **📝 Code Preview** - See issues in context
- **📦 Standalone HTML** - Works offline, no server needed
- **🎨 Beautiful Gallery** - Browse all analyses

## 🚀 Quick Start

**Get started in under 5 minutes!** See our **[📖 Quick Start Guide](docs/QUICK_START.md)**

### Fastest Path

```bash
# 1. Run CPPCheck
cppcheck --enable=all --xml --xml-version=2 your-project/ 2> analysis.xml

# 2. Convert to JSON
python3 xml2json-simple.py analysis.xml > analysis.json

# 3. Generate Dashboard
python3 generate/generate-standalone-virtual-dashboard.py analysis.json dashboard.html

# 4. Open in Browser
open dashboard.html  # macOS
# or
xdg-open dashboard.html  # Linux
```

## 📚 Documentation

### Getting Started
- **[📖 Quick Start Guide](docs/QUICK_START.md)** - Get running in 5 minutes
- **[🔍 Generator Comparison](docs/GENERATOR_COMPARISON.md)** - Which generator should you use?
- **[🔧 Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Advanced Topics
- **[📋 Implementation Plan](docs/IMPLEMENTATION_PLAN.md)** - Project roadmap
- **[📊 Master Plan Summary](MASTER_PLAN_SUMMARY.md)** - Transformation vision
- **[🤖 Claude Instructions](CLAUDE.md)** - AI assistant guide

### Reference
- **[📁 Documentation Index](docs/INDEX.md)** - All documentation
- **[🗄️ Archive](docs/archive/INDEX.md)** - Historical documents

## 🎯 Which Generator Should I Use?

**Quick Decision:**
- **Most Users**: `generate-standalone-virtual-dashboard.py` ✨
- **Large Codebases (10k+ issues)**: `generate-virtual-scroll-dashboard.py` 🚀
- **Minimal Size**: `generate-production-dashboard.py` 📦
- **Custom Integration**: TypeScript package 🛠️

See **[📊 Complete Comparison](docs/GENERATOR_COMPARISON.md)** for details.

## 🛠️ Installation

### Python Version (No Dependencies!)
```bash
git clone https://github.com/jerryzhao173985/cppcheck-studio.git
cd cppcheck-studio
# That's it! Python scripts work directly
```

### TypeScript/Node.js Version
```bash
cd cppcheck-dashboard-generator
npm install
npm run build
npm link  # Optional: install globally
```

## 💡 Common Use Cases

### 1. Analyze a GitHub Repository
Use our GitHub Action for the easiest experience:
1. Go to [Actions](https://github.com/jerryzhao173985/cppcheck-studio/actions)
2. Click "On-Demand Repository Analysis v3"
3. Enter repository details
4. Get your dashboard!

### 2. Add Code Context (Recommended)
```bash
# Add code snippets around each issue
python3 add-code-context.py analysis.json analysis-with-context.json --base-path /path/to/project

# Generate dashboard with context
python3 generate/generate-standalone-virtual-dashboard.py analysis-with-context.json dashboard.html
```

### 3. CI/CD Integration
```yaml
- name: Generate CPPCheck Dashboard
  run: |
    cppcheck --enable=all --xml --xml-version=2 . 2> analysis.xml
    python3 xml2json-simple.py analysis.xml > analysis.json
    python3 generate/generate-production-dashboard.py analysis.json dashboard.html
```

## 📊 Real-World Results

Successfully analyzed **[LPZRobots](https://github.com/georgmartius/lpzrobots)** C++ codebase:
- ✅ **2,975 issues** found and visualized
- ✅ **200 files** analyzed in under 3 minutes
- ✅ **99.7% success rate** for code context
- ✅ **210KB dashboard** with full interactivity

## 🤝 Contributing

We welcome contributions! Please see our [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) for current priorities:
- Consolidating generators (18 → 5)
- Improving test coverage
- Simplifying workflows
- Creating tutorials

## 📅 Roadmap

### Current Focus
- ✅ Two complete implementations (Python & TypeScript)
- ✅ Virtual scrolling for large datasets
- ✅ GitHub Actions integration
- 🚧 Generator consolidation
- 🚧 Comprehensive test suite

### Coming Soon
- 📦 Published npm package
- 🎥 Video tutorials
- 🔌 VSCode extension
- ☁️ Cloud service

## 🙏 Acknowledgments

This project emerged from the need to visualize static analysis results for the [LPZRobots](https://github.com/georgmartius/lpzrobots) project. Special thanks to the C++ community for feedback and contributions.

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

<p align="center">
  <i>Transform your static analysis from overwhelming text to actionable insights</i>
</p>

<p align="center">
  <a href="https://jerryzhao173985.github.io/cppcheck-studio/">Live Demo</a> •
  <a href="docs/QUICK_START.md">Quick Start</a> •
  <a href="https://github.com/jerryzhao173985/cppcheck-studio/issues">Report Bug</a> •
  <a href="https://github.com/jerryzhao173985/cppcheck-studio/discussions">Discussions</a>
</p>