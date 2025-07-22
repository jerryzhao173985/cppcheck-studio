# CPPCheck Studio - Standalone CLI Package

## Overview

The CPPCheck Studio CLI can be used as a standalone tool for any C++ project, not just LPZRobots.

## Installation

### Global Installation (Recommended)

```bash
npm install -g cppcheck-studio
```

### Local Installation

```bash
npm install --save-dev cppcheck-studio
```

## Usage

### Start the Web Interface

```bash
# Start the studio on default port 3000
cppcheck-studio start

# Custom port
cppcheck-studio start --port 8080

# With specific project
cppcheck-studio start --project /path/to/cpp/project
```

### Command Line Analysis

```bash
# Analyze current directory
cppcheck-studio analyze

# Analyze specific directory
cppcheck-studio analyze /path/to/project

# With specific profile
cppcheck-studio analyze --profile cpp17

# Output formats
cppcheck-studio analyze --format json > report.json
cppcheck-studio analyze --format html > report.html
```

### Fix Management

```bash
# Preview fixes (dry-run)
cppcheck-studio fix --dry-run

# Apply fixes with confidence threshold
cppcheck-studio fix --confidence 80

# Apply specific fix types
cppcheck-studio fix --types nullptr,override,explicit

# Interactive mode
cppcheck-studio fix --interactive
```

### CI/CD Integration

```bash
# Check mode for CI (exit with error if issues found)
cppcheck-studio check --threshold error

# Generate report for CI artifacts
cppcheck-studio analyze --format junit > test-results.xml
```

## Configuration

Create `.cppcheckstudio.json` in your project root:

```json
{
  "profile": "cpp17",
  "paths": ["src", "include"],
  "exclude": ["build/**", "third_party/**"],
  "incremental": true,
  "autoFix": {
    "enabled": true,
    "confidence": 85,
    "types": ["nullptr", "override", "explicit"]
  },
  "customRules": ["./rules/*.js"],
  "suppressions": [
    "missingInclude:*/external/*"
  ]
}
```

## Profiles

- `quick` - Fast analysis for development
- `full` - Comprehensive analysis
- `cpp17` - C++17 modernization focus
- `cpp20` - C++20 features
- `memory` - Memory safety checks
- `performance` - Performance optimizations

## Environment Variables

```bash
# API endpoint (for self-hosted)
CPPCHECK_STUDIO_API=http://localhost:3001

# Disable telemetry
CPPCHECK_STUDIO_TELEMETRY=false

# Custom cppcheck binary
CPPCHECK_BINARY=/usr/local/bin/cppcheck
```

## Programmatic API

```javascript
const { analyze, fix } = require('cppcheck-studio');

// Analyze project
const results = await analyze({
  paths: ['./src'],
  profile: 'cpp17'
});

// Apply fixes
const applied = await fix({
  issues: results.issues,
  dryRun: false,
  confidence: 90
});
```

## VS Code Extension

Install from marketplace: `cppcheck-studio`

Features:
- Inline diagnostics
- Quick fixes in editor
- Status bar integration
- Custom rule authoring

## Examples

### Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run quick analysis on staged files
files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(cpp|hpp|cc|h)$')
if [ -n "$files" ]; then
  cppcheck-studio analyze $files --profile quick --format summary
  if [ $? -ne 0 ]; then
    echo "❌ Fix C++ issues before committing"
    exit 1
  fi
fi
```

### GitHub Action

```yaml
name: C++ Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install CPPCheck Studio
        run: npm install -g cppcheck-studio
      
      - name: Run Analysis
        run: cppcheck-studio analyze --format github
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: cppcheck-report
          path: cppcheck-report.html
```

### Docker

```dockerfile
FROM node:18-alpine
RUN npm install -g cppcheck-studio
WORKDIR /workspace
CMD ["cppcheck-studio", "start"]
```

## Troubleshooting

### cppcheck not found

```bash
# Install cppcheck first
sudo apt-get install cppcheck  # Ubuntu/Debian
brew install cppcheck          # macOS
```

### Permission errors

```bash
# Use npx instead of global install
npx cppcheck-studio analyze
```

### Large codebase timeout

```bash
# Increase timeout and use incremental mode
cppcheck-studio analyze --timeout 3600 --incremental
```

## Support

- Documentation: https://docs.cppcheck.studio
- Issues: https://github.com/yourusername/cppcheck-studio/issues
- Discord: https://discord.gg/cppcheck