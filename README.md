# CPPCheck Studio 🎯

**Transform CPPCheck JSON output into beautiful, interactive HTML dashboards with virtual scrolling.**

## 🚀 Quick Start (2 minutes)

```bash
# 1. Run CPPCheck on your C++ code
cppcheck --enable=all --format=json your-project/ > analysis.json

# 2. Generate dashboard with unified CLI
python3 cppcheck-studio.py analyze analysis.json

# 3. Open in browser
open dashboard.html
```

### With Code Context (Recommended)

```bash
# Add code snippets around issues
python3 cppcheck-studio.py add-context analysis.json
python3 cppcheck-studio.py analyze analysis-with-context.json
```

## 📁 What's in this package?

```
cppcheck-studio/
├── cppcheck-studio.py             # 🎯 Unified CLI (NEW!)
├── add-code-context.py            # Enhanced code context tool
├── quickstart.py                  # Interactive setup wizard
│
├── generate/                      # Python dashboard generators
│   ├── generate-standalone-virtual-dashboard.py  # ⭐ DEFAULT - Virtual scrolling
│   ├── generate-production-dashboard.py         # Minimal size option
│   ├── generate-virtual-scroll-dashboard.py     # Legacy virtual scroll
│   ├── generate-split-dashboard.py              # Splits data into files
│   ├── generate-optimized-dashboard.py          # GitHub Actions compatible
│   └── generate-simple-dashboard.py             # GitHub Actions fallback
│
├── cppcheck-dashboard-generator/  # TypeScript/npm package
│   ├── src/                      # TypeScript source files
│   ├── dist/                     # Compiled JavaScript
│   └── package.json              # npm configuration
│
├── scripts/                       # Workflow support scripts
│   └── Various utility scripts for CI/CD
│
└── docs/                         # Documentation
    └── Comprehensive guides and references
    ├── GENERATOR_COMPARISON.md   # Which generator to use
    └── TROUBLESHOOTING.md       # Common issues
```

## 🎯 Which Generator Should I Use?

| Generator | Best For | Output Size | Max Issues |
|-----------|----------|-------------|------------|
| **standalone-virtual** ⭐ | Most users | ~240KB | 100,000+ |
| **production** | CI/CD, minimal size | ~150KB | 10,000 |
| **virtual-scroll** | Huge codebases | ~200KB | 1,000,000+ |
| **split** | Modular integration | Varies | Unlimited |

## 🔥 Features

- ✅ **Virtual Scrolling** - Handle millions of issues smoothly
- ✅ **Instant Search** - Filter issues in real-time
- ✅ **Code Preview** - See code context for each issue
- ✅ **Zero Dependencies** - Pure HTML/JS, works offline
- ✅ **Responsive Design** - Works on all devices
- ✅ **Export Ready** - Share via email or web

## 📦 Installation Options

### Option 1: Python (No Installation)
```bash
git clone https://github.com/jerryzhao173985/cppcheck-studio.git
cd cppcheck-studio
# Ready to use!
```

### Option 2: npm Package
```bash
npm install -g @jerryzhao173985/cppcheck-dashboard-generator
cppcheck-dashboard analysis.json dashboard.html
```

## 📖 Documentation

- [Quick Start Guide](docs/QUICK_START.md) - Detailed setup and usage
- [Generator Comparison](docs/GENERATOR_COMPARISON.md) - Feature comparison  
- [Architecture](docs/ARCHITECTURE.md) - How it works
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

## 🤝 Contributing

Found a bug? Have a feature request? [Open an issue](https://github.com/jerryzhao173985/cppcheck-studio/issues)!

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

**Note**: Everything else has been moved to `legacy/` for reference. The core functionality is in the directories shown above.