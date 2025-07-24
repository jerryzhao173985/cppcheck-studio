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

## 📁 What's in this package?

```
cppcheck-studio/
├── generate/                      # Python dashboard generators
│   ├── generate-standalone-virtual-dashboard.py  # ⭐ RECOMMENDED - All features
│   ├── generate-production-dashboard.py         # Minimal size, fast
│   ├── generate-virtual-scroll-dashboard.py     # For huge datasets (100k+ issues)  
│   └── generate-split-dashboard.py              # Splits data into multiple files
│
├── cppcheck-dashboard-generator/  # TypeScript/npm package (same features)
│   └── Full npm package with TypeScript implementation
│
├── utils/                         # Helper utilities
│   ├── xml2json-simple.py        # Convert CPPCheck XML to JSON
│   └── add-code-context.py       # Add code snippets to issues
│
├── examples/                      # Sample data and scripts
│   └── quickstart.sh             # Example workflow
│
└── docs/                         # Documentation
    ├── QUICK_START.md           # Detailed getting started
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