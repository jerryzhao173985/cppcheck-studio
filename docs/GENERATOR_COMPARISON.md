# CPPCheck Studio Generator Comparison Guide

## Quick Decision Guide

**Q: I want the best dashboard with all features**  
**A: Use `generate-standalone-virtual-dashboard.py`**

**Q: I have a huge codebase (10,000+ issues)**  
**A: Use `generate-virtual-scroll-dashboard.py`**

**Q: I need the smallest file size**  
**A: Use `generate-production-dashboard.py`**

**Q: I want to experiment/customize**  
**A: Use the TypeScript package**

## Complete Generator Comparison Table

### Active Generators (in `generate/` directory)

| Generator | File Size | Features | Best For | Issues Handled |
|-----------|-----------|----------|----------|----------------|
| **generate-standalone-virtual-dashboard.py** ⭐ | ~240KB | Virtual scroll, search, filters, code preview | **RECOMMENDED - Most use cases** | 100,000+ |
| **generate-virtual-scroll-dashboard.py** | ~220KB | Virtual scrolling focus | Very large datasets | 100,000+ |
| **generate-production-dashboard.py** | ~150KB | Minimal, no code context | Quick overview | 5,000 |
| **generate-split-dashboard.py** | Multiple files | Separates data/UI | Modular needs | 10,000 |
| **generate-optimized-dashboard.py** | ~200KB | Performance optimized | GitHub Actions workflows | 10,000 |
| **generate-simple-dashboard.py** | ~180KB | Basic features | Workflow fallback | 5,000 |

### Legacy Generators (moved to `legacy/generators/`)

⚠️ **Note**: The following generators have been moved to the legacy directory and are no longer actively maintained:

| Generator | Previous Features | Replacement |
|-----------|------------------|-------------|
| **generate-ultimate-dashboard.py** | All features, proven stable | Use `generate-standalone-virtual-dashboard.py` |
| **generate-robust-dashboard.py** | Error handling, progress | Features merged into standalone version |
| **generate-enhanced-dashboard.py** | Extra visualizations | Use standalone version |
| **generate-modern-dashboard.py** | Modern UI | UI improvements in standalone |
| **generate-paginated-dashboard.py** | Page-based navigation | Virtual scrolling is superior |
| **generate-streaming-dashboard.py** | Loads progressively | Not needed with virtual scrolling |
| **generate-interactive-dashboard.py** | Maximum interactivity | All features in standalone |
| **generate-compact-dashboard.py** | Minimal size | Use `generate-production-dashboard.py` |
| **generate-detailed-dashboard.py** | Maximum detail | Use standalone with code context |
| **generate-summary-dashboard.py** | Overview only | Use production version |

## Feature Matrix (Active Generators Only)

| Feature | Standalone Virtual | Virtual Scroll | Production | Split | Optimized |
|---------|-------------------|----------------|------------|-------|----------||
| Virtual Scrolling | ✅ | ✅ | ❌ | ❌ | ✅ |
| Code Context | ✅ | ✅ | ❌ | ✅ | ✅ |
| Search | ✅ | ✅ | ✅ | ✅ | ✅ |
| Filters | ✅ | ✅ | ✅ | ✅ | ✅ |
| Inline Data | ✅ | ✅ | ✅ | ❌ | ✅ |
| Separate Files | ❌ | ❌ | ❌ | ✅ | ❌ |
| Error Recovery | ✅ | ✅ | ❌ | ✅ | ✅ |
| Mobile Friendly | ✅ | ✅ | ✅ | ✅ | ✅ |

## Usage Examples

### For Most Users (Recommended)
```bash
python3 generate/generate-standalone-virtual-dashboard.py analysis.json dashboard.html
```

### For Large Codebases
```bash
python3 generate/generate-virtual-scroll-dashboard.py huge-analysis.json dashboard.html
```

### For CI/CD Integration
```bash
python3 generate/generate-production-dashboard.py analysis.json dashboard.html
```

### For Custom Integration (TypeScript)
```javascript
import { DashboardGenerator } from 'cppcheck-dashboard-generator';

const generator = new DashboardGenerator();
await generator.generate('analysis.json', 'dashboard.html', {
  virtualScroll: true,
  embedData: true,
  minify: true
});
```

## Performance Benchmarks

| Issues | Standalone Virtual | Virtual Scroll | Production | TypeScript |
|--------|--------------------|----------------|------------|------------|
| 100 | <0.1s | <0.1s | <0.1s | <0.1s |
| 1,000 | 0.2s | 0.2s | 0.1s | 0.2s |
| 10,000 | 0.8s | 0.7s | 0.5s | 0.7s |
| 100,000 | 3.2s | 3.0s | 2.8s | 3.0s |

## Recommendations

1. **Default Choice**: `generate-standalone-virtual-dashboard.py`
   - Best balance of features and performance
   - Handles any size dataset
   - Most actively maintained

2. **For npm/Node.js Projects**: TypeScript package
   - Better integration with modern toolchains
   - Type safety
   - Customizable

3. **For Minimal Needs**: `generate-production-dashboard.py`
   - Smallest file size
   - Fastest generation
   - No external dependencies

## Migration Guide

If you're currently using a legacy generator, here's the recommended migration:

| Old Generator (in legacy/) | → | New Generator (in generate/) |
|---------------------------|---|-----------------------------|
| Any legacy generator | → | **`generate-standalone-virtual-dashboard.py`** (RECOMMENDED) |
| Need minimal output | → | `generate-production-dashboard.py` |
| Need huge dataset support | → | `generate-virtual-scroll-dashboard.py` |
| Need modular output | → | `generate-split-dashboard.py` |

**Important Notes**:
- All legacy generators are in `legacy/generators/` and are not actively maintained
- The `generate-optimized-dashboard.py` and `generate-simple-dashboard.py` in `generate/` are kept only for GitHub Actions compatibility
- For all new projects, use `generate-standalone-virtual-dashboard.py`