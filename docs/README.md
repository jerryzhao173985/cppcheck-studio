# CPPCheck Studio - Usage Guide

## 🚀 Quick Start

This platform analyzes C++ repositories using CPPCheck and generates beautiful interactive dashboards.

### Live Demo
- **Platform**: https://jerryzhao173985.github.io/cppcheck-studio/
- **Sample Dashboard**: https://jerryzhao173985.github.io/cppcheck-studio/dashboard.html

## 📋 How to Analyze Your C++ Repository

### Option 1: GitHub Actions UI (Easiest)

1. Go to the [Analysis Workflow](https://github.com/jerryzhao173985/cppcheck-studio/actions/workflows/analyze-on-demand.yml)
2. Click "Run workflow"
3. Enter your repository (e.g., `nlohmann/json` or `opencv/opencv`)
4. Click the green "Run workflow" button
5. Wait 2-5 minutes for analysis to complete
6. Download the dashboard HTML from workflow artifacts

### Option 2: GitHub CLI

```bash
# Install GitHub CLI if you haven't already
brew install gh  # macOS
# or visit: https://cli.github.com/

# Run analysis
gh workflow run analyze-on-demand.yml \
  -R jerryzhao173985/cppcheck-studio \
  -f repository="owner/repo" \
  -f branch="main" \
  -f max_files=500

# Check status
gh run list -R jerryzhao173985/cppcheck-studio

# Download results when complete
gh run download <run-id> -R jerryzhao173985/cppcheck-studio
```

### Option 3: Direct API Call (Advanced)

If you have a GitHub Personal Access Token with `repo` scope:

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/jerryzhao173985/cppcheck-studio/actions/workflows/analyze-on-demand.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "repository": "pytorch/pytorch",
      "branch": "main",
      "max_files": 1000
    }
  }'
```

## 🔧 Setting Up Your Own Instance

If you want to fork this repository and use your own GitHub token:

1. Fork this repository
2. Go to Settings → Secrets and variables → Actions
3. Add a secret named `GH_TOKEN` with your GitHub Personal Access Token
   - The token needs `repo` and `workflow` scopes
4. Enable GitHub Pages in Settings → Pages
5. Your instance will be available at `https://YOUR_USERNAME.github.io/cppcheck-studio/`

## 📊 Understanding the Results

The generated dashboard shows:

- **Total Issues**: All problems found
- **Errors**: Critical issues that need fixing
- **Warnings**: Potential problems to review
- **Style**: Code style and modernization suggestions
- **Performance**: Optimization opportunities

Features:
- 🔍 Real-time search
- 🏷️ Filter by severity
- 📝 View code context
- 📊 Summary statistics

## 🌐 Web Interface Features

The web interface at https://jerryzhao173985.github.io/cppcheck-studio/ provides:

1. **Repository Input**: Enter any GitHub repository URL or owner/repo format
2. **Analysis Trigger**: Instructions for starting analysis
3. **History Tracking**: LocalStorage saves your analysis history
4. **Results Gallery**: View past analyses

## ⚙️ Workflow Parameters

When triggering analysis, you can customize:

- **repository**: GitHub repository in `owner/repo` format
- **branch**: Branch to analyze (default: `main`)
- **max_files**: Maximum C++ files to analyze (default: 500)

## 🔒 Security Notes

- GitHub tokens are never exposed in the frontend
- All API calls require proper authentication
- Analysis runs in isolated GitHub Actions environment
- Results are public via GitHub Pages (don't analyze private code)

## 📈 Examples

### Small Library
```bash
gh workflow run analyze-on-demand.yml \
  -R jerryzhao173985/cppcheck-studio \
  -f repository="nlohmann/json"
```

### Large Project (Limited Files)
```bash
gh workflow run analyze-on-demand.yml \
  -R jerryzhao173985/cppcheck-studio \
  -f repository="tensorflow/tensorflow" \
  -f max_files=1000
```

### Specific Branch
```bash
gh workflow run analyze-on-demand.yml \
  -R jerryzhao173985/cppcheck-studio \
  -f repository="opencv/opencv" \
  -f branch="4.x"
```

## 🤝 Contributing

Feel free to:
- Report issues
- Submit pull requests
- Request features
- Share your analysis results

## 📜 License

This project is open source. See the LICENSE file for details.