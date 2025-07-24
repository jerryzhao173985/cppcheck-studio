#!/bin/bash
# Script to create GitHub job summary
# This avoids YAML parsing issues with HERE documents

DASHBOARD_URL="$1"
REPO="$2"
BRANCH="$3"
COMMIT_SHA="$4"
ANALYSIS_ID="$5"
FILE_COUNT="${6:-0}"
ISSUE_COUNT="${7:-0}"

cat << 'SUMMARY_EOF'
# 🎯 CPPCheck Analysis Complete!

> ### [🔗 **CLICK HERE TO VIEW YOUR INTERACTIVE DASHBOARD** →](DASHBOARD_URL_PLACEHOLDER)
> 
> The dashboard includes:
> - **Virtual scrolling** for smooth navigation through all ISSUE_COUNT_PLACEHOLDER issues
> - **Code context preview** showing the exact lines where issues occur
> - **Real-time search and filtering** by severity, file, or message
> - **Detailed issue information** with line numbers and descriptions

---

## 📊 Analysis Summary

| Property | Value |
|----------|-------|
| **Repository** | `REPO_PLACEHOLDER` |
| **Branch** | `BRANCH_PLACEHOLDER` |
| **Commit** | `COMMIT_PLACEHOLDER` |
| **Analysis ID** | `ANALYSIS_ID_PLACEHOLDER` |
| **Files Analyzed** | **FILE_COUNT_PLACEHOLDER** |
| **Total Issues** | **ISSUE_COUNT_PLACEHOLDER** |

## 📈 Issue Breakdown
```
SUMMARY_EOF

# Add summary content if available
if [ -f output/summary.txt ]; then
    cat output/summary.txt
else
    echo "Summary not available"
fi

cat << 'SUMMARY_EOF2'
```

## 🔗 Additional Links
- [📂 Download Analysis Artifacts](ARTIFACTS_URL_PLACEHOLDER)
- [🔍 View Workflow Logs](WORKFLOW_URL_PLACEHOLDER)
- [📊 API Status Endpoint](https://jerryzhao173985.github.io/cppcheck-studio/api/status/ANALYSIS_ID_PLACEHOLDER.json)

## 💡 Dashboard Tips
1. **Can't see issues?** Press `F12` to open console, then run `recoverDashboard()`
2. **Use keyboard shortcuts**: 
   - `/` to focus search
   - `1-5` to filter by severity
   - `ESC` to close modals
3. **Share the dashboard**: The URL is permanent and can be bookmarked

---

<details>
<summary>📝 Debug Information</summary>

- Workflow Run: WORKFLOW_RUN_ID
- Triggered by: EVENT_NAME
- Runner: RUNNER_OS
- Analysis completed at: COMPLETED_AT

</details>
SUMMARY_EOF2