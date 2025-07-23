# Important: Virtual Scrolling Dashboard

## 🎯 Dashboard Configuration

The CI/CD pipeline is configured to use **`generate-standalone-virtual-dashboard.py`** as the primary dashboard generator because it:

- ✅ Provides virtual scrolling for handling large datasets efficiently
- ✅ Has all the features and correct implementation
- ✅ Delivers the best user experience
- ✅ Is the recommended and preferred dashboard format

## 📋 Generator Priority Order

1. **`generate-standalone-virtual-dashboard.py`** (PRIMARY - with virtual scrolling)
2. `generate-ultimate-dashboard.py` (fallback)
3. TypeScript generator (if npm package installed)
4. `generate-simple-dashboard.py` (last resort fallback)

## 🚀 Why Virtual Scrolling?

The virtual scrolling implementation:
- Handles 100,000+ issues without performance degradation
- Only renders visible rows for optimal performance
- Provides smooth scrolling experience
- Maintains all interactive features (search, filter, preview)

This ensures the best possible experience for users analyzing large C++ codebases.