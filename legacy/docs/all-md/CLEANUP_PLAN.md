# 🧹 CPPCheck Studio - Cleanup & Compaction Plan

## Current State: CLUTTERED
- **100+ files** visible at root level
- **19 generators** when only 5 are needed
- **Duplicate implementations** (TypeScript AND Python for same functionality)
- **Incomplete monorepo** structure (apps/, packages/)
- **28+ HTML files** scattered everywhere
- **Overlapping documentation** with no clear hierarchy

## Target State: COMPACT & CLEAR

### 🎯 Essential Core Structure
```
cppcheck-studio/
├── README.md                           # Clear getting started
├── LICENSE                             # MIT license
├── CLAUDE.md                           # AI assistant guide
│
├── generate/                           # 5 CORE Python generators only
│   ├── standalone-virtual.py          # Default choice (renamed for clarity)
│   ├── production.py                  # Minimal size
│   ├── virtual-scroll.py              # Large datasets
│   ├── streaming.py                   # Progressive loading
│   └── split-output.py                # Modular files
│
├── typescript/                         # Complete npm package (renamed)
│   └── [TypeScript implementation]
│
├── utils/                              # Essential utilities only
│   ├── add-code-context.py
│   └── xml2json.py
│
├── examples/                           # Sample data & usage
│   ├── sample-analysis.json
│   └── quickstart.sh
│
├── docs/                               # Minimal essential docs
│   ├── QUICKSTART.md
│   ├── FAQ.md
│   └── ARCHITECTURE.md
│
└── legacy/                             # Everything else moved here
    ├── deprecated-generators/
    ├── experimental/
    ├── old-docs/
    └── test-outputs/
```

## 🔨 Cleanup Actions

### 1. Create Legacy Directory Structure
```bash
mkdir -p legacy/{generators,experimental,docs,outputs,scripts}
```

### 2. Move Deprecated Generators
```bash
# Move 14 deprecated generators
mv generate/generate-{ultimate,simple,enhanced,optimized,debug,final,perfect,working,fixed,embedded}*.py legacy/generators/
```

### 3. Move Experimental/Incomplete Code
```bash
# Move monorepo attempt
mv apps/ packages/ legacy/experimental/

# Move duplicate implementation
mv cppcheck-virtual-dashboard/ legacy/experimental/
```

### 4. Clean Root Directory
```bash
# Move all HTML files
mv *.html legacy/outputs/

# Move test/demo scripts
mv test-*.sh demo-*.sh legacy/scripts/

# Move report directories
mv reports/ demo-output/ legacy/outputs/
```

### 5. Simplify Generator Names
```bash
cd generate/
mv generate-standalone-virtual-dashboard.py standalone-virtual.py
mv generate-production-dashboard.py production.py
mv generate-virtual-scroll-dashboard.py virtual-scroll.py
mv generate-split-dashboard.py split-output.py
```

### 6. Consolidate Documentation
```bash
# Keep only essential docs
cd docs/
mkdir ../legacy/docs
mv *.md ../legacy/docs/  # Move all first
mv ../legacy/docs/{README.md,QUICKSTART.md,FAQ.md,ARCHITECTURE.md} .  # Bring back essentials
```

### 7. Create Clear Examples
```bash
mkdir examples
echo '#!/bin/bash
# Quick example: Generate dashboard from cppcheck output
cppcheck --xml --xml-version=2 src/ 2> analysis.xml
python3 utils/xml2json.py analysis.xml > analysis.json
python3 generate/standalone-virtual.py analysis.json dashboard.html
echo "✅ Dashboard created: dashboard.html"' > examples/quickstart.sh
chmod +x examples/quickstart.sh
```

## 📋 Final Checklist

After cleanup, the root should have:
- [ ] 3 documentation files (README, LICENSE, CLAUDE)
- [ ] 5 directories (generate, typescript, utils, examples, docs)
- [ ] 1 legacy directory containing everything else
- [ ] NO loose HTML files
- [ ] NO test scripts
- [ ] NO duplicate implementations visible

## 🎯 Result

Users will immediately see:
1. **generate/** → "Oh, these are the Python generators"
2. **typescript/** → "This is the npm package"
3. **utils/** → "These help with data preparation"
4. **examples/** → "Here's how to use it"
5. **docs/** → "If I need more info"

Everything else is tucked away in `legacy/` for reference but not cluttering the main view.