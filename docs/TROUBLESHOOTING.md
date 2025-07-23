# 🔧 CPPCheck Studio Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Python Scripts Not Found
**Problem**: `python3: command not found`
**Solution**:
```bash
# Install Python 3
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# Verify installation
python3 --version
```

#### npm Package Installation Fails
**Problem**: `npm install` fails with permission errors
**Solution**:
```bash
# Use a Node version manager
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
npm install -g cppcheck-dashboard-generator
```

### CPPCheck Issues

#### No Issues Found
**Problem**: CPPCheck returns empty results
**Common Causes & Solutions**:

1. **Not enabling all checks**
```bash
# Wrong
cppcheck src/

# Correct
cppcheck --enable=all --inconclusive src/
```

2. **Wrong file extensions**
```bash
# Make sure to include all C++ extensions
cppcheck --enable=all src/ --include=*.cpp --include=*.cc --include=*.cxx --include=*.h --include=*.hpp
```

3. **Suppressed errors**
```bash
# Check for suppression file
cat .cppcheck-suppressions
# Run without suppressions
cppcheck --enable=all --suppress=none src/
```

#### XML Output Is Empty
**Problem**: `analysis.xml` is empty or malformed
**Solution**:
```bash
# Check stderr redirection
cppcheck --xml --xml-version=2 src/ 2> analysis.xml

# Verify XML content
xmllint --format analysis.xml

# If empty, check permissions
ls -la analysis.xml
```

### Dashboard Generation Issues

#### JSON Conversion Fails
**Problem**: `xml2json-simple.py` fails with parsing error
**Debug Steps**:
```bash
# Check XML is valid
python3 -c "import xml.etree.ElementTree as ET; ET.parse('analysis.xml')"

# Check first few lines of XML
head -20 analysis.xml

# Try with debug mode
python3 xml2json-simple.py analysis.xml > analysis.json 2> debug.log
cat debug.log
```

#### Dashboard Is Blank
**Problem**: Generated HTML shows no data
**Common Causes**:

1. **Invalid JSON**
```bash
# Validate JSON
python3 -m json.tool analysis.json > /dev/null
# Check for errors
echo $?
```

2. **Wrong generator for data size**
```bash
# Check issue count
ISSUE_COUNT=$(jq '.issues | length' analysis.json)
echo "Found $ISSUE_COUNT issues"

# Use appropriate generator
if [ $ISSUE_COUNT -gt 10000 ]; then
  python3 generate/generate-virtual-scroll-dashboard.py analysis.json dashboard.html
else
  python3 generate/generate-standalone-virtual-dashboard.py analysis.json dashboard.html
fi
```

#### Memory Error During Generation
**Problem**: `MemoryError` or process killed
**Solutions**:

1. **Use streaming generator**
```bash
python3 generate/generate-streaming-dashboard.py large-analysis.json dashboard.html
```

2. **Increase memory limit**
```bash
# Check current limit
ulimit -v

# Increase limit (Linux)
ulimit -v unlimited
```

3. **Process in chunks**
```bash
# Split large JSON
python3 scripts/split-analysis.py analysis.json --chunks 10
# Generate separate dashboards
for chunk in chunk_*.json; do
  python3 generate/generate-production-dashboard.py $chunk dashboard_$chunk.html
done
```

### GitHub Actions Issues

#### Workflow Not Triggering
**Problem**: "Run workflow" button not appearing
**Solutions**:

1. **Check workflow syntax**
```bash
# Install actionlint
brew install actionlint  # macOS
actionlint .github/workflows/analyze-on-demand.yml
```

2. **Verify on default branch**
- Workflow must be on default branch (usually `main`)
- Check Settings → Actions → Workflow permissions

3. **Check workflow_dispatch**
```yaml
on:
  workflow_dispatch:  # Must have this
    inputs:
      repository:
        description: 'Repository to analyze'
        required: true
        type: string
```

#### Analysis Fails in CI
**Problem**: Works locally but fails in GitHub Actions
**Common Issues**:

1. **Different cppcheck version**
```yaml
# Pin specific version
- name: Install cppcheck
  run: |
    sudo apt-get update
    sudo apt-get install -y cppcheck=2.13
```

2. **Path issues**
```yaml
# Use absolute paths
- name: Run analysis
  run: |
    WORKSPACE=${{ github.workspace }}
    cd $WORKSPACE/target-repo
    cppcheck . 2> $WORKSPACE/analysis.xml
```

### Performance Issues

#### Slow Dashboard Loading
**Problem**: Dashboard takes >10 seconds to load
**Solutions**:

1. **Use virtual scrolling**
```bash
# Instead of ultimate dashboard
python3 generate/generate-virtual-scroll-dashboard.py analysis.json dashboard.html
```

2. **Minimize dashboard size**
```bash
# Remove code context for smaller file
python3 generate/generate-production-dashboard.py analysis.json dashboard.html
```

3. **Enable compression**
```bash
# Gzip the dashboard
gzip -k dashboard.html
# Serve with proper headers
python3 -m http.server --bind 0.0.0.0 8000
```

### Code Context Issues

#### Missing Code Context
**Problem**: Eye icon shows but no code preview
**Solution**:
```bash
# Add code context with correct base path
python3 add-code-context.py analysis.json analysis-with-context.json --base-path /absolute/path/to/project

# Verify context was added
jq '.issues[0].context' analysis-with-context.json
```

#### Wrong File Paths
**Problem**: Code context shows wrong files
**Solution**:
```bash
# Check file paths in JSON
jq '.issues[].file' analysis.json | sort | uniq

# Fix relative paths
cd /path/to/project
cppcheck . 2> analysis.xml  # Run from project root
```

## Debug Mode

Enable debug output for more information:

```bash
# Set debug environment variable
export CPPCHECK_STUDIO_DEBUG=1

# Run with verbose output
python3 -v generate/generate-standalone-virtual-dashboard.py analysis.json dashboard.html

# Check JavaScript console in browser
# Open dashboard.html, press F12, check Console tab
```

## Getting Help

If these solutions don't resolve your issue:

1. **Check existing issues**: https://github.com/jerryzhao173985/cppcheck-studio/issues
2. **Create detailed bug report** including:
   - Exact command used
   - Error message (full output)
   - Sample of input data
   - System information (OS, Python version)
3. **Join discussions**: https://github.com/jerryzhao173985/cppcheck-studio/discussions

## FAQ

**Q: Which generator should I use?**
A: See [Generator Comparison Guide](GENERATOR_COMPARISON.md)

**Q: Can I analyze languages other than C++?**
A: Currently only C/C++ is supported via cppcheck

**Q: How do I customize the dashboard appearance?**
A: Edit the CSS in the generator scripts or use browser developer tools

**Q: Can I merge multiple analysis results?**
A: Yes, use `scripts/merge-analyses.py` (coming soon)