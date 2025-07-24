# GitHub Actions Setup Guide

This guide shows how to set up automatic CPPCheck analysis with dashboard generation for your C++ projects.

## Quick Start

### 1. For Your Own C++ Repository

Copy this workflow to your repository:

```yaml
# .github/workflows/cppcheck.yml
name: CPPCheck Analysis

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  analyze:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup CPPCheck Dashboard
      run: |
        # Install cppcheck
        sudo apt-get update && sudo apt-get install -y cppcheck
        
        # Install dashboard generator
        npm install -g cppcheck-dashboard-generator
    
    - name: Run Analysis
      run: |
        # Run cppcheck
        cppcheck --enable=all --xml --xml-version=2 . 2> results.xml
        
        # Convert to JSON (you'll need to add xml2json.py to your repo)
        python3 xml2json.py results.xml > analysis.json
        
        # Generate dashboard
        cppcheck-dashboard analysis.json dashboard.html \
          --title "${{ github.repository }} Analysis" \
          --project "${{ github.repository }}"
    
    - name: Upload Dashboard
      uses: actions/upload-artifact@v4
      with:
        name: cppcheck-dashboard
        path: dashboard.html
```

### 2. Using CPPCheck Studio's Workflows

1. Fork the cppcheck-studio repository
2. Go to Actions tab
3. Enable workflows
4. Run "Analyze External C++ Repository"
5. Enter any GitHub C++ repository URL

## Workflow Features

### Automatic PR Comments

The workflow automatically comments on PRs with analysis results:

```
## 🔍 CPPCheck Analysis Results

**Total issues found:** 42

### 📊 Dashboard
Download: [CPPCheck Dashboard](link-to-artifact)

### 📝 Summary
View the detailed analysis results in the uploaded dashboard HTML file.
```

### GitHub Pages Deployment

To automatically deploy dashboards to GitHub Pages:

1. Enable GitHub Pages in repository settings
2. Add deployment step to workflow:

```yaml
- name: Deploy to Pages
  if: github.ref == 'refs/heads/main'
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./
    publish_branch: gh-pages
```

### Badge Generation

Add a status badge to your README:

```markdown
![CPPCheck](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/USERNAME/GIST_ID/raw/cppcheck-badge.json)
```

## Example Runs

### Popular C++ Projects

Try these repositories with the "Analyze External C++ Repository" workflow:

| Project | Repository | Description |
|---------|------------|-------------|
| JSON for Modern C++ | `nlohmann/json` | Popular JSON library |
| Google Test | `google/googletest` | Testing framework |
| OpenCV | `opencv/opencv` | Computer vision library |
| Catch2 | `catchorg/Catch2` | Test framework |
| fmt | `fmtlib/fmt` | Formatting library |

### Sample Dashboard Output

The generated dashboard includes:
- Total issue count with breakdown by severity
- Virtual scrolling for large result sets
- Real-time search and filtering
- Code context preview
- Responsive design

## Advanced Configuration

### Custom CPPCheck Options

```yaml
- name: Run CPPCheck with Custom Options
  run: |
    cppcheck \
      --enable=all \
      --inconclusive \
      --std=c++20 \
      --suppress=missingIncludeSystem \
      --suppress=unmatchedSuppression \
      --inline-suppr \
      --error-exitcode=0 \
      --xml --xml-version=2 \
      src/ 2> results.xml
```

### Analyzing Specific Directories

```yaml
- name: Analyze Only Source Directory
  run: |
    cppcheck src/ include/ --xml --xml-version=2 2> results.xml
```

### Setting File Limits

For large repositories:

```yaml
- name: Analyze Limited Files
  run: |
    find . -name "*.cpp" -o -name "*.h" | head -100 > files.txt
    cppcheck --file-list=files.txt --xml --xml-version=2 2> results.xml
```

## Integration Examples

### With CMake Projects

```yaml
- name: Configure and Analyze
  run: |
    cmake -B build
    cppcheck --project=build/compile_commands.json --xml 2> results.xml
```

### With Specific Standards

```yaml
- name: C++20 Analysis
  run: |
    cppcheck --std=c++20 --enable=all . 2> results.xml
```

### Incremental Analysis (PR only)

```yaml
- name: Analyze Changed Files Only
  if: github.event_name == 'pull_request'
  run: |
    # Get changed files
    git diff --name-only origin/main...HEAD | grep -E '\.(cpp|h|hpp|cc|cxx)$' > changed_files.txt
    
    # Analyze only changed files
    if [ -s changed_files.txt ]; then
      cppcheck --file-list=changed_files.txt --xml 2> results.xml
    fi
```

## Troubleshooting

### Common Issues

1. **No C++ files found**
   - Check file extensions (.cpp, .h, .cc, etc.)
   - Verify directory structure

2. **Dashboard not generated**
   - Ensure cppcheck-dashboard-generator is installed
   - Check for valid JSON output

3. **Large analysis times**
   - Limit files analyzed
   - Use specific directories
   - Disable certain checks

### Debug Mode

Add verbose output:

```yaml
- name: Debug Analysis
  run: |
    cppcheck --verbose --debug . 2>&1 | tee cppcheck.log
```

## Next Steps

1. **Customize** the analysis for your project needs
2. **Schedule** regular analysis runs
3. **Integrate** with your CI/CD pipeline
4. **Track** improvements over time

For more information, see the [workflow documentation](.github/workflows/README.md).