# GitHub Pages Deployment - IMPORTANT!

## 🔴 Why GitHub Pages Keeps Going 404

GitHub Pages deployments expire after a period of inactivity. The deployment workflow ONLY runs when:
1. Files in `docs/` folder change
2. The deploy-docs.yml workflow itself changes
3. Manual trigger via workflow_dispatch

## ✅ Permanent Solutions Applied

1. **Added scheduled deployment** - Runs every 6 hours to keep site alive
2. **Added workflow dependencies** - Now deploys when analyze-on-demand.yml changes
3. **Manual trigger available** - Can always run via GitHub UI

## 🚨 Quick Fix When 404 Happens

```bash
# Run this command to fix 404 immediately:
gh workflow run deploy-docs.yml

# Wait 1 minute, then check:
curl -I https://jerryzhao173985.github.io/cppcheck-studio/ | head -1
```

## 📋 Deployment Checklist

Before making changes:
- [ ] Check current site status
- [ ] Note which files you're changing

After making changes:
- [ ] If you changed non-docs files, manually trigger deployment
- [ ] Wait 1 minute for deployment
- [ ] Verify site is still accessible

## 🔧 How to Check Deployment Status

```bash
# Check if site is up
curl -I https://jerryzhao173985.github.io/cppcheck-studio/ | head -1

# Check recent deployments
gh run list --workflow=deploy-docs.yml --limit=3

# Trigger new deployment
gh workflow run deploy-docs.yml
```

## 📝 Remember

- GitHub Pages needs regular deployments to stay active
- The scheduled cron job (every 6 hours) should prevent most 404s
- Always check site after making workflow changes
- Manual deployment takes ~1 minute to complete