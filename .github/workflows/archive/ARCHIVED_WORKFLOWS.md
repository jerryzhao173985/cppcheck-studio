# Archived Workflows

This directory contains legacy workflows that have been replaced by the new structured CI/CD system.

## Migration Guide

### Replaced Workflows

| Old Workflow | Replacement | Notes |
|-------------|-------------|-------|
| `analyze-on-demand.yml` | `04-analyze.yml` + `reusable-analyze.yml` | Improved with caching and better error handling |
| `analyze-on-demand-v2.yml` | `reusable-analyze.yml` | Merged into reusable component |
| `analyze-lpzrobots.yml` | `04-analyze.yml` | Use generic workflow with lpzrobots repo |
| `analyze-repository-dispatch.yml` | `04-analyze.yml` | Unified entry point |
| `update-analysis-gallery.yml` | Built into `reusable-analyze.yml` | Automatic gallery updates |
| `update-analysis-results.yml` | Built into `reusable-analyze.yml` | Integrated deployment |
| `test-cppcheck.yml` | `01-test.yml` | Comprehensive test suite |
| `simple-test.yml` | `01-test.yml` | Part of integration tests |
| `example-analysis.yml` | Use `04-analyze.yml` | |
| `cppcheck-analysis.yml` | `04-analyze.yml` | Standardized workflow |

### Still Active (Keep)

These workflows are still in use and should NOT be moved:

- `process-analysis-request.yml` - Queue processor (scheduled)
- `deploy-docs.yml` - GitHub Pages deployment
- `api-proxy.yml` - API endpoint handler
- `trigger-analysis-service.yml` - Service trigger
- `analyze-showcase.yml` - Demo/showcase workflow

### How to Use New Workflows

1. **For manual analysis:**
   ```bash
   gh workflow run 04-analyze.yml -f repository="owner/repo"
   ```

2. **For API triggers:**
   ```bash
   curl -X POST \
     -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/$OWNER/$REPO/dispatches \
     -d '{"event_type":"analyze-repo","client_payload":{"repository":"target/repo"}}'
   ```

3. **For testing:**
   - All tests run automatically on PR/push
   - Manual: `gh workflow run 01-test.yml`

## Archive Date

Workflows archived on: [DATE]

## Restoration

If you need to restore any workflow:
1. Copy from this archive directory
2. Update to use new patterns (caching, reusable workflows)
3. Test thoroughly before enabling