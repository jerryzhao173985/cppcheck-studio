# GitHub Actions Workflows for CPPCheck Studio

This directory contains GitHub Actions workflows that automatically run CPPCheck analysis on C++ repositories and generate interactive HTML dashboards.

## Available Workflows

### 1. CPPCheck Analysis Dashboard (`cppcheck-analysis.yml`)

**Trigger**: Push to main/develop, Pull Requests, Manual dispatch

This workflow analyzes the current repository (if it contains C++ files) or an external repository.

**Features**:
- Automatic analysis on push/PR
- Generates interactive HTML dashboard
- Uploads artifacts for download
- Posts PR comments with results
- Optional GitHub Pages deployment

**Usage**:
```yaml
# Triggered automatically on push/PR
# Or manually with optional repo URL
```

### 2. Analyze External C++ Repository (`analyze-cpp-repo.yml`)

**Trigger**: Manual dispatch only

Analyze any public C++ repository on GitHub.

**Inputs**:
- `repository`: GitHub repository in `owner/repo` format (e.g., `opencv/opencv`)
- `branch`: Branch to analyze (default: `main`)
- `path`: Subdirectory to analyze (optional)
- `max_files`: Maximum files to analyze (default: 100)

**Example**:
1. Go to Actions tab
2. Select "Analyze External C++ Repository"
3. Click "Run workflow"
4. Enter repository details
5. Download the generated dashboard from artifacts

### 3. Example C++ Project Analysis (`example-analysis.yml`)

**Trigger**: Weekly schedule or manual dispatch

Analyzes popular C++ projects as examples:
- JSON for Modern C++
- Catch2
- fmt
- spdlog

## Dashboard Features

The generated HTML dashboards include:
- 📊 **Virtual Scrolling**: Handle thousands of issues efficiently
- 🔍 **Search & Filter**: Find issues by file, message, or severity
- 📝 **Code Context**: View the actual code around each issue
- 🎨 **Syntax Highlighting**: Beautiful code display
- 📱 **Responsive**: Works on all devices
- 💾 **Standalone**: Single HTML file, works offline

## Setup Instructions

### For Your Own Repository

1. Copy the `.github/workflows` directory to your C++ repository
2. Ensure your repository has C++ files (`.cpp`, `.h`, etc.)
3. Push to main branch or create a PR
4. Check the Actions tab for results

### Required Secrets

No secrets required! The workflows use the automatic `GITHUB_TOKEN`.

### Optional: GitHub Pages Deployment

To enable automatic deployment to GitHub Pages:

1. Go to Settings → Pages
2. Set Source to "GitHub Actions"
3. The dashboard will be available at: `https://[username].github.io/[repo]/`

## Example Usage

### Analyzing a Pull Request

When you create a PR with C++ changes:
1. The workflow runs automatically
2. Downloads and analyzes your code
3. Generates a dashboard
4. Posts a comment with results and download link

### Analyzing External Project

```bash
# Via GitHub UI:
1. Go to Actions → "Analyze External C++ Repository"
2. Click "Run workflow"
3. Enter: repository: "google/googletest"
4. Wait for completion
5. Download dashboard artifact
```

### Viewing Results

1. Go to the workflow run
2. Scroll to "Artifacts"
3. Download `cppcheck-dashboard`
4. Open the HTML file in your browser
5. Explore the interactive dashboard!

## Dashboard Navigation

- **Search Bar**: Type to filter issues in real-time
- **Severity Filters**: Click buttons to show/hide by severity
- **Code Preview**: Click the 👁️ icon to see code context
- **Virtual Scroll**: Smoothly handle large result sets

## Customization

### Modify Analysis Settings

Edit the cppcheck command in the workflow:
```yaml
cppcheck \
  --enable=all \              # Enable all checks
  --std=c++17 \              # C++ standard
  --suppress=missingInclude \ # Suppress specific warnings
  ...
```

### Change Dashboard Title

```yaml
cppcheck-dashboard \
  analysis.json \
  dashboard.html \
  --title "My Custom Title" \
  --project "My Project Name"
```

## Troubleshooting

### No C++ Files Found
- Ensure your repository contains `.cpp`, `.h`, or similar files
- Check the `path` parameter if analyzing subdirectories

### Large Repositories
- Increase `max_files` parameter (may take longer)
- Or focus on specific directories with `path` parameter

### Dashboard Not Loading
- Ensure JavaScript is enabled in your browser
- Try a different browser if issues persist

## Examples

### Popular C++ Projects to Try

- `nlohmann/json` - JSON for Modern C++
- `google/googletest` - Google Test Framework  
- `opencv/opencv` - Computer Vision Library
- `pytorch/pytorch` - Machine Learning Framework
- `tensorflow/tensorflow` - Machine Learning Platform
- `catchorg/Catch2` - Test Framework
- `fmtlib/fmt` - Formatting Library

## Contributing

To improve these workflows:
1. Fork the repository
2. Modify workflows in `.github/workflows/`
3. Test on your fork
4. Submit a pull request

## License

These workflows are part of CPPCheck Studio and are MIT licensed.