# CPPCheck Studio

Transform CPPCheck static analysis results into beautiful, interactive HTML dashboards.

## Features

- **Virtual Scrolling** - Handle 100,000+ issues smoothly
- **Interactive Filtering** - Real-time search and severity filters
- **Code Context** - Preview issues with surrounding code
- **Standalone HTML** - No server required, works offline
- **Zero Dependencies** - Python version needs no packages
- **Unified CLI** - Simple command-line interface for all operations

## Quick Start

### Instant Setup

```bash
# Run the interactive quick start
python3 quickstart.py
```

This will guide you through analyzing your code and generating your first dashboard.

### Manual Setup

#### Option 1: Unified CLI (Recommended)

```bash
# Show available commands
python3 cppcheck-studio.py --help

# Analyze and generate dashboard
python3 cppcheck-studio.py analyze analysis.json

# Add code context first
python3 cppcheck-studio.py add-context analysis.json
python3 cppcheck-studio.py analyze analysis-with-context.json

# Show statistics
python3 cppcheck-studio.py stats analysis.json
```

#### Option 2: Direct Python Scripts

```bash
# Add code context
python3 add-code-context.py analysis.json

# Generate dashboard (virtual scrolling)
python3 generate/generate-standalone-virtual-dashboard.py analysis-with-context.json dashboard.html

# Generate minimal dashboard
python3 generate/generate-production-dashboard.py analysis.json minimal.html
```

#### Option 3: TypeScript/Node.js

```bash
# Build the package
cd cppcheck-dashboard-generator
npm install && npm run build

# Generate dashboard
node dist/cli.js ../analysis.json ../dashboard.html
```

## Running CPPCheck

First, analyze your C++ code with CPPCheck:

```bash
# Basic analysis
cppcheck --enable=all src/ --output-file=analysis.json

# Recommended: with more details
cppcheck --enable=all --std=c++17 --suppress=missingInclude \
         --output-file=analysis.json --template=gcc src/
```

## CLI Commands

The unified CLI (`cppcheck-studio.py`) provides these commands:

- **analyze** - Generate dashboard from analysis JSON
  - `--virtual` - Use virtual scrolling for large datasets
  - `--minimal` - Generate minimal dashboard without code
  - `--force` - Overwrite existing output
  
- **add-context** - Add code context to analysis
  - `--lines N` - Context lines before/after (default: 5)
  
- **stats** - Show analysis statistics
- **validate** - Validate JSON format

## Available Generators

### Python Scripts
- `generate-standalone-virtual-dashboard.py` - Best for large datasets (virtual scrolling)
- `generate-ultimate-dashboard.py` - Feature-rich for <5000 issues
- `generate-production-dashboard.py` - Minimal size, no code context

### TypeScript Package
- Full CLI with options (`--title`, `--project`, etc.)
- Programmatic API for integration
- TypeScript type safety

## Real-World Performance

Tested on LPZRobots C++ codebase:
- 2,975 issues analyzed
- < 1 second load time
- 3MB standalone HTML file

## Requirements

- **Python version**: Python 3.6+
- **TypeScript version**: Node.js 14+
- **CPPCheck**: Latest version recommended

## Installation

### Python (No installation needed!)
```bash
git clone <repository>
cd cppcheck-studio
python3 cppcheck-studio.py --help
```

### TypeScript/Node.js
```bash
cd cppcheck-dashboard-generator
npm install
npm run build
npm link  # Optional: install globally
```

## Contributing

Contributions are welcome! The codebase is clean and well-documented:
- Python scripts have type hints and docstrings
- TypeScript code is fully typed
- Both implementations create identical output

## License

MIT License - see LICENSE file for details