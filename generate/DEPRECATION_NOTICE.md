# ⚠️ Generator Deprecation Notice

## Important: Generator Consolidation

To simplify CPPCheck Studio and improve maintainability, we are consolidating from 18 generators to 4 core generators.

## 🔄 Migration Guide

### Core Generators (Recommended)

These generators are actively maintained:

**Note**: `generate-optimized-dashboard.py` and `generate-simple-dashboard.py` have been restored for GitHub Actions workflow compatibility.

1. **`generate-standalone-virtual-dashboard.py`** ✅
   - **Default choice for most users**
   - All features, virtual scrolling, handles any size

2. **`generate-production-dashboard.py`** ✅
   - Minimal size, fastest generation
   - Best for CI/CD and quick reports

3. **`generate-virtual-scroll-dashboard.py`** ✅
   - Optimized for very large datasets (100k+ issues)
   - Memory efficient virtual scrolling

4. **`generate-split-dashboard.py`** ✅
   - Separates data and UI into multiple files
   - Best for modular integration

### Deprecated Generators → Migration Path

| Deprecated Generator | Migrate To | Reason |
|---------------------|------------|---------|
| `generate-dashboard.py` | `generate-standalone-virtual-dashboard.py` | Superseded by virtual scrolling version |
| `generate-ultimate-dashboard.py` | `generate-standalone-virtual-dashboard.py` | Same features, better performance |
| `generate-optimized-dashboard.py` | `generate-standalone-virtual-dashboard.py` | Optimizations now in standalone |
| `generate-simple-dashboard.py` | `generate-production-dashboard.py` | Production is simpler and faster |
| `generate-robust-dashboard.py` | `generate-standalone-virtual-dashboard.py` | Robustness built into core |
| `generate-enhanced-dashboard.py` | `generate-standalone-virtual-dashboard.py` | Enhancements merged |
| `generate-modern-dashboard.py` | `generate-standalone-virtual-dashboard.py` | Modern UI is default |
| `generate-dashboard-v2.py` | `generate-standalone-virtual-dashboard.py` | Legacy version |
| `generate-dashboard-v3.py` | `generate-standalone-virtual-dashboard.py` | Legacy version |
| `generate-paginated-dashboard.py` | `generate-split-dashboard.py` | Use split for modular output |
| `generate-interactive-dashboard.py` | `generate-standalone-virtual-dashboard.py` | All dashboards are interactive |
| `generate-compact-dashboard.py` | `generate-production-dashboard.py` | Production is most compact |
| `generate-detailed-dashboard.py` | `generate-standalone-virtual-dashboard.py` | Details available in all |

## 📅 Deprecation Timeline

- **January 2025**: Deprecation announced (this notice)
- **February 2025**: Deprecation warnings added to old generators
- **March 2025**: Old generators moved to `legacy/` directory
- **April 2025**: Old generators removed from main branch

## 🔧 How to Update Your Scripts

### If you're using deprecated generators in scripts:

```bash
# Old (deprecated)
python3 generate/generate-ultimate-dashboard.py input.json output.html

# New (recommended)
python3 generate/generate-standalone-virtual-dashboard.py input.json output.html
```

### If you're using specific features:

- **Virtual scrolling**: Already in `generate-standalone-virtual-dashboard.py`
- **Minimal size**: Use `generate-production-dashboard.py`
- **Very large datasets**: Use `generate-virtual-scroll-dashboard.py`
- **Modular output**: Use `generate-split-dashboard.py`

## ❓ FAQ

**Q: Will my existing dashboards still work?**
A: Yes, generated dashboards are standalone HTML files and will continue to work.

**Q: Do the new generators have all the features?**
A: Yes, all features have been consolidated into the 4 core generators.

**Q: What if I need a specific feature from a deprecated generator?**
A: Please open an issue - we'll ensure the feature is available in a core generator.

## 📞 Need Help?

- Open an issue: https://github.com/jerryzhao173985/cppcheck-studio/issues
- Join discussions: https://github.com/jerryzhao173985/cppcheck-studio/discussions