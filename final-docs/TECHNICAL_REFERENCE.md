# Technical Reference Guide

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Web Frontend  │────▶│  Backend Service │────▶│  GitHub Actions │
│  (GitHub Pages) │     │   (Node.js/API)  │     │   (Workflows)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                         │
         ▼                       ▼                         ▼
   LocalStorage            Database/Cache            Artifacts/Pages
```

## API Endpoints

### Trigger Analysis
```http
POST /api/analyze
Content-Type: application/json

{
  "repository": "owner/repo",
  "branch": "main",
  "maxFiles": 500
}

Response:
{
  "success": true,
  "analysisId": "1234567890-abc123",
  "estimatedTime": "2-5 minutes"
}
```

### Check Status
```http
GET /api/analysis/{analysisId}/status

Response:
{
  "analysisId": "1234567890-abc123",
  "status": "in_progress|completed|failed",
  "startedAt": "2025-01-22T10:00:00Z"
}
```

### Get Results
```http
GET /api/analysis/{analysisId}/results

Response:
{
  "analysisId": "1234567890-abc123",
  "dashboardUrl": "https://...",
  "summary": {
    "filesAnalyzed": 150,
    "totalIssues": 42,
    "errors": 5,
    "warnings": 12
  }
}
```

## GitHub Actions Workflows

### 1. Manual Trigger
```yaml
name: Analyze External C++ Repository
on:
  workflow_dispatch:
    inputs:
      repository:
        required: true
        type: string
```

### 2. API Trigger
```yaml
on:
  repository_dispatch:
    types: [analyze-repo]
    
# Access payload via:
# ${{ github.event.client_payload.repository }}
```

### 3. Automatic on Push
```yaml
on:
  push:
    branches: [ main ]
```

## Dashboard Generator CLI

### Installation
```bash
cd cppcheck-dashboard-generator
npm install -g .
```

### Usage
```bash
# Basic usage
cppcheck-dashboard analysis.json output.html

# With options
cppcheck-dashboard analysis.json output.html \
  --title "My Project Analysis" \
  --project "ProjectName" \
  --verbose
```

### Programmatic Usage
```typescript
import { DashboardGenerator } from 'cppcheck-dashboard-generator';

const generator = new DashboardGenerator({
    title: 'Analysis Results',
    verbose: true
});

await generator.generate('analysis.json', 'output.html');
```

## Data Formats

### CPPCheck XML Output
```xml
<?xml version="1.0" encoding="UTF-8"?>
<results version="2">
    <errors>
        <error id="nullPointer" 
               severity="error" 
               msg="Null pointer dereference">
            <location file="main.cpp" line="42"/>
        </error>
    </errors>
</results>
```

### Converted JSON Format
```json
{
  "issues": [
    {
      "id": "nullPointer",
      "severity": "error",
      "message": "Null pointer dereference",
      "file": "main.cpp",
      "line": 42,
      "codeContext": {
        "lineNumber": 42,
        "lineContent": "    *ptr = 5;",
        "beforeLines": ["int* ptr = nullptr;"],
        "afterLines": ["return 0;"]
      }
    }
  ]
}
```

### JSONL Format (Dashboard)
```jsonl
{"id":"nullPointer","severity":"error","message":"...","file":"main.cpp","line":42}
{"id":"uninitvar","severity":"warning","message":"...","file":"utils.cpp","line":15}
```

## Security Considerations

### Token Storage
```javascript
// NEVER do this client-side:
const GITHUB_TOKEN = 'ghp_xxxxxxxxxxxx'; // ❌

// Instead, use environment variables server-side:
const GITHUB_TOKEN = process.env.GITHUB_TOKEN; // ✅
```

### Input Validation
```javascript
function validateRepository(input) {
    // Sanitize input
    const cleaned = input.trim().replace(/[^a-zA-Z0-9\-_\/]/g, '');
    
    // Validate format
    if (!cleaned.match(/^[a-zA-Z0-9\-_]+\/[a-zA-Z0-9\-_]+$/)) {
        throw new Error('Invalid repository format');
    }
    
    return cleaned;
}
```

### CORS Configuration
```javascript
app.use((req, res, next) => {
    // Restrict to specific origins in production
    const allowedOrigins = [
        'https://jerryzhao173985.github.io',
        'http://localhost:3000'
    ];
    
    const origin = req.headers.origin;
    if (allowedOrigins.includes(origin)) {
        res.setHeader('Access-Control-Allow-Origin', origin);
    }
    
    next();
});
```

## Performance Optimizations

### Virtual Scrolling
```javascript
// Only render visible rows
const visibleStart = Math.floor(scrollTop / rowHeight);
const visibleEnd = Math.min(
    visibleStart + Math.ceil(viewportHeight / rowHeight),
    totalRows
);

// Create spacer for non-visible rows
const topSpacer = visibleStart * rowHeight;
const bottomSpacer = (totalRows - visibleEnd) * rowHeight;
```

### Data Loading
```javascript
// Use JSONL for streaming
issuesData.split('\n').forEach(line => {
    if (line) {
        const issue = JSON.parse(line);
        processIssue(issue);
    }
});
```

### Caching Strategy
```javascript
// LocalStorage for client-side caching
const CACHE_KEY = 'cppcheck-analysis-cache';
const CACHE_DURATION = 3600000; // 1 hour

function getCachedAnalysis(repoId) {
    const cached = localStorage.getItem(`${CACHE_KEY}-${repoId}`);
    if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        if (Date.now() - timestamp < CACHE_DURATION) {
            return data;
        }
    }
    return null;
}
```

## Error Handling

### Workflow Errors
```yaml
- name: Run analysis
  run: |
    cppcheck ... || {
      echo "::error::CPPCheck analysis failed"
      exit 1
    }
```

### API Errors
```javascript
try {
    const result = await triggerAnalysis(repo);
    return { success: true, data: result };
} catch (error) {
    console.error('Analysis failed:', error);
    return {
        success: false,
        error: error.message,
        code: error.code || 'UNKNOWN_ERROR'
    };
}
```

### Frontend Error Display
```javascript
function showError(message) {
    const errorEl = document.getElementById('error-message');
    errorEl.textContent = message;
    errorEl.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorEl.style.display = 'none';
    }, 5000);
}
```

## Deployment Guide

### GitHub Pages Setup
1. Enable Pages in repository settings
2. Set source to `main` branch `/docs` folder
3. Wait for deployment (usually 2-5 minutes)
4. Access at: `https://[username].github.io/[repository]/`

### Backend Deployment (Heroku Example)
```json
// package.json
{
  "scripts": {
    "start": "node trigger-service.js"
  },
  "engines": {
    "node": "18.x"
  }
}
```

```bash
heroku create cppcheck-api
heroku config:set GITHUB_TOKEN=your_token
git push heroku main
```

### Environment Variables
```bash
# Required
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Optional
PORT=3000
CALLBACK_URL=https://your-app.com/webhook
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## Monitoring & Logging

### GitHub Actions Logs
```yaml
- name: Debug information
  run: |
    echo "Repository: ${{ env.REPO }}"
    echo "Files found: ${{ env.FILE_COUNT }}"
    echo "Issues: ${{ env.ISSUE_COUNT }}"
```

### Application Logging
```javascript
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

// Usage
logger.info('Analysis started', { repository, analysisId });
```

### Performance Metrics
```javascript
// Track analysis duration
const startTime = Date.now();

// ... perform analysis ...

const duration = Date.now() - startTime;
console.log(`Analysis completed in ${duration}ms`);

// Send to analytics
analytics.track('analysis_completed', {
    repository,
    duration,
    filesAnalyzed,
    issuesFound
});
```

## Troubleshooting

### Common Issues

1. **Workflow not triggering**
   - Check GitHub token permissions (needs `repo` scope)
   - Verify workflow file syntax
   - Check Actions tab for errors

2. **Dashboard not loading**
   - Verify JSONL format (newlines not escaped)
   - Check browser console for errors
   - Ensure file size < 100MB

3. **API timeout**
   - Increase timeout limits
   - Implement retry logic
   - Use webhook callbacks for long operations

### Debug Commands
```bash
# Test workflow locally
act -j analyze

# Check GitHub API rate limits
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit

# Validate workflow syntax
yamllint .github/workflows/*.yml
```