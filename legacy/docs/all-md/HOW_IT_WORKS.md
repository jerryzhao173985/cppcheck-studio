# How CPPCheck Studio Works - Complete Flow

## 🎯 Overview

CPPCheck Studio provides automated C++ static analysis for any GitHub repository with a web interface for triggering and viewing results.

## 🔄 Complete Workflow

### 1. User Triggers Analysis (Web Interface)

1. Go to: https://jerryzhao173985.github.io/cppcheck-studio/
2. Enter repository (e.g., `nlohmann/json`)
3. Click "Analyze" button
4. Get unique Analysis ID (e.g., `1753188976457-89qbltmpe`)

### 2. Workflow Dispatch

1. Modal shows with:
   - Repository name (click to copy)
   - Analysis ID (click to copy)
   - Direct link to GitHub Actions

2. User goes to GitHub Actions:
   - Clicks "Run workflow"
   - Pastes repository name
   - Pastes analysis ID (optional but recommended)
   - Clicks green "Run workflow" button

### 3. Analysis Workflow Runs

The `analyze-on-demand.yml` workflow:

```yaml
1. Parse inputs (repository, analysis_id, branch)
2. Clone the target repository
3. Find all C++ files (up to max_files limit)
4. Run cppcheck static analysis
5. Convert XML results to JSON
6. Add code context around issues
7. Generate HTML dashboard
8. Create metadata and status files
9. Commit results to docs/results/{analysis_id}/
10. Update api/gallery.json
11. Trigger GitHub Pages deployment
```

### 4. Real-Time Status Updates

While the workflow runs:
- Creates `api/status/{analysis_id}.json`
- Website polls this endpoint every 5 seconds
- Shows progress: "Analysis in progress..."
- Links to workflow run on GitHub

### 5. Results Storage

When complete, creates:
```
docs/
├── results/
│   └── {analysis_id}/
│       ├── index.html      # Interactive dashboard
│       └── metadata.json    # Analysis metadata
├── api/
│   ├── gallery.json        # All analyses list
│   ├── status/
│   │   └── {analysis_id}.json  # Status tracking
│   └── analyses/
│       └── {analysis_id}.json  # Analysis details
```

### 6. Automatic Deployment

- GitHub Pages deploys on every push
- Self-healing: checks every 30 minutes
- Auto-deploys if 404 detected
- Status badge shows health

### 7. User Views Results

1. Website automatically shows results when ready
2. Dashboard URL: `/results/{analysis_id}/`
3. Interactive features:
   - Search and filter issues
   - View code context
   - Sort by severity
   - Export results

## 🔧 Key Components

### Workflows

1. **analyze-on-demand.yml**
   - Main analysis workflow
   - Triggered manually via workflow_dispatch
   - Requires: repository, optional analysis_id

2. **analyze-repository-dispatch.yml**
   - API-triggered version
   - For programmatic triggering
   - Accepts webhooks

3. **deploy-docs.yml**
   - Deploys to GitHub Pages
   - Runs on every push
   - Self-healing with scheduled runs

4. **check-deployment.yml**
   - Monitors site health
   - Auto-fixes 404 errors
   - Creates issues if problems persist

### Frontend Components

1. **index.html**
   - Main interface
   - Repository input
   - Analysis history
   - Status polling

2. **simple-trigger.js**
   - Generates analysis IDs
   - Creates workflow URLs
   - Handles status checking

3. **gallery.html**
   - Shows all analyses
   - Searchable/filterable
   - Links to dashboards

### API Structure

```
api/
├── gallery.json          # List of all analyses
├── index.json           # Same as gallery (compatibility)
├── status/{id}.json     # Real-time status
└── analyses/{id}.json   # Analysis metadata
```

## 🚨 Common Issues & Solutions

### 1. Workflow Fails with Permission Error

**Error**: `Permission denied to github-actions[bot]`

**Solution**: Already fixed! Workflow now has:
```yaml
permissions:
  contents: write
  pages: write
  id-token: write
```

### 2. Site Shows 404

**Error**: GitHub Pages returns 404

**Solution**: Automatically fixed! 
- Deployment runs every 2 hours
- Check-deployment runs every 30 minutes
- Manual fix: `gh workflow run deploy-docs.yml`

### 3. Analysis Not Found

**Error**: Polling doesn't find results

**Causes**:
- Workflow still running
- Analysis ID mismatch
- Results not yet deployed

**Solution**: 
- Check workflow status on GitHub
- Verify analysis ID matches
- Wait for deployment (1-2 minutes)

## 📊 Example Analysis

For repository `nlohmann/json`:
- Files analyzed: 100-500
- Issues found: Typically 50-200
- Time: 2-5 minutes
- Dashboard size: ~300KB

## 🔐 Security

- Only public repositories supported
- No credentials stored
- GitHub Actions handles authentication
- Read-only analysis
- Results are public via GitHub Pages

## 🎯 Success Metrics

✅ Workflow completes successfully
✅ Results appear in gallery
✅ Dashboard is accessible
✅ Status updates in real-time
✅ History tracking works
✅ Site stays online (self-healing)

## 📝 Testing

Run the test script:
```bash
./scripts/test-workflow.sh nlohmann/json
```

This will:
1. Check site status
2. Generate test analysis ID
3. Show trigger instructions
4. Provide monitoring URLs