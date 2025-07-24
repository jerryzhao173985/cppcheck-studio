# 🗺️ Where Is Everything? - Quick Reference Card

## 🎯 For Daily Use (Active Code)

| What You Need | Where It Is Now | Example |
|--------------|-----------------|---------|
| **Generate Dashboard** | `generate/` | `python3 generate/generate-standalone-virtual-dashboard.py` |
| **Convert XML→JSON** | `utils/` | `python3 utils/xml2json-simple.py` |
| **Add Code Context** | `utils/` | `python3 utils/add-code-context.py` |
| **TypeScript Package** | `cppcheck-dashboard-generator/` | `npm install && npm run build` |
| **Documentation** | `docs/` | `docs/QUICK_START.md` |
| **Run Tests** | `tests/` | `./tests/run_tests.sh` |
| **Examples** | `examples/` | `./examples/quickstart.sh` |

## 📦 Legacy Items (Reference Only)

| What You're Looking For | Where It Moved To | Why It Moved |
|------------------------|-------------------|--------------|
| **Old Generators** | `legacy/generators/` | 14 deprecated generators |
| `generate-ultimate-dashboard.py` | `legacy/generators/` | Use `standalone-virtual` instead |
| `generate-simple-dashboard.py` | `legacy/generators/` | Use `production` instead |
| `generate-enhanced-dashboard.py` | `legacy/generators/` | Use `standalone-virtual` instead |
| **HTML Dashboards** | `legacy/outputs/` | Test outputs, not source code |
| All `.html` files from root | `legacy/outputs/root-dashboards/` | 28 test dashboards |
| `reports/` directory | `legacy/outputs/reports/` | More test outputs |
| **Monorepo Attempt** | `legacy/monorepo/` | Incomplete implementation |
| `apps/` directory | `legacy/monorepo/apps/` | Unfinished Next.js/Express |
| `packages/` directory | `legacy/monorepo/packages/` | Unfinished npm packages |
| **Scripts & Tools** | `legacy/scripts/` | Old/redundant utilities |
| JavaScript files (`*.js`) | `legacy/scripts/js/` | Dashboard fix scripts |
| Shell scripts (`test-*.sh`) | `legacy/scripts/sh/` | Test scripts |
| Python utilities | `legacy/scripts/python/` | Analysis scripts |
| **Documentation** | `legacy/docs/` | Old/redundant docs |
| Technical docs | `legacy/docs/all-md/` | Moved documentation |
| Workflow summaries | `legacy/docs/` | CI/CD documentation |

## 🔍 Common Searches

### "I used to use generate-ultimate-dashboard.py"
→ Now use: `generate/generate-standalone-virtual-dashboard.py`

### "Where's my test dashboard HTML?"
→ Check: `legacy/outputs/root-dashboards/` or `legacy/outputs/reports/`

### "Where's the incomplete CLI?"
→ It's in: `legacy/monorepo/packages/cli/`

### "Where are the workflow fix documents?"
→ Moved to: `legacy/docs/` (various CI fix summaries)

### "Where's add-code-context.py?"
→ Still active in: `utils/add-code-context.py`

### "Where's the virtual scroll TypeScript duplicate?"
→ Moved to: `legacy/experimental/cppcheck-virtual-dashboard/`

## 📊 Summary Statistics

| Category | Before | After | Location |
|----------|--------|-------|----------|
| **Root Items** | 105 | 17 | Clean root |
| **Python Generators** | 19 | 4 | `generate/` |
| **Deprecated Generators** | - | 14 | `legacy/generators/` |
| **HTML Files in Root** | 28 | 0 | `legacy/outputs/` |
| **Essential Utils** | Mixed | 2 | `utils/` |
| **Documentation** | Scattered | Organized | `docs/` + `legacy/docs/` |

## 💡 Pro Tips

1. **Starting fresh?** Only look at non-legacy directories
2. **Need old code?** Check `legacy/` with the path mappings above
3. **Contributing?** Only modify files outside `legacy/`
4. **Can't find something?** It's probably in `legacy/` - use the tables above

---
*This guide shows where everything moved during the January 2025 cleanup*