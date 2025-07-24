# Dashboard Error Reference Guide

## 🚨 Common Dashboard Errors and Solutions

### Error 1: "Loading..." Stuck Forever

**Symptoms**:
- Dashboard shows statistics but table says "Loading..."
- No error messages in console
- Page appears to load completely

**Root Causes**:
1. JavaScript template literal parsing error
2. JSONL data has literal newlines breaking the script
3. Silent script failure - no errors shown

**Quick Fix**:
1. Open browser console (F12)
2. Copy and paste the emergency fix from `emergency-fix-deployed.html`
3. Dashboard should immediately show issues

**Permanent Fix**:
Regenerate dashboard with updated generator or Python script

---

### Error 2: No Rows Visible Despite Having Issues

**Symptoms**:
- Statistics show issue count (e.g., "3,277 issues")
- Table is empty or shows only headers
- Console shows "Rendering 0 rows"

**Root Causes**:
1. Container height is 0 or invalid
2. Virtual scrolling calculations failing
3. Race condition during initialization

**Quick Fix**:
```javascript
// In browser console:
window.recoverDashboard();
```

**If that doesn't work**:
```javascript
// Force container height and render
document.getElementById('scrollContainer').style.height = '600px';
window.state.containerHeight = 600;
window.forceRender();
```

---

### Error 3: "TypeError: Cannot read property 'length' of undefined"

**Symptoms**:
- Console error about undefined.length
- Dashboard partially loads then stops

**Root Cause**:
- state.allIssues or state.filteredIssues is undefined

**Quick Fix**:
```javascript
// Initialize state properly
window.state = window.state || {};
window.state.allIssues = [];
window.state.filteredIssues = [];
window.state.codeContextMap = new Map();

// Then reload data
window.loadEmbeddedData();
window.filterData();
```

---

### Error 4: Search/Filter Not Working

**Symptoms**:
- Typing in search box does nothing
- Severity filter buttons don't filter
- All issues always shown

**Root Causes**:
1. Event handlers not attached
2. filterData function not available globally

**Quick Fix**:
```javascript
// Re-attach event handlers
document.getElementById('searchInput').oninput = () => window.filterData();

// Make functions global
window.filterData = filterData;
window.setSeverityFilter = setSeverityFilter;
```

---

### Error 5: Code Preview Modal Empty

**Symptoms**:
- Clicking eye icon shows modal
- Modal has no code content
- Shows "Code context not available"

**Root Causes**:
1. Code context data not loaded
2. Missing codeContextData script
3. ID mismatch between issues and context

**Check**:
```javascript
// Check if code context exists
console.log(window.state.codeContextMap.size);  // Should be > 0

// Check for code context script
console.log(document.getElementById('codeContextData'));  // Should not be null
```

**Fix**:
Dashboard needs to be regenerated with code context included

---

### Error 6: Performance Issues / Lag

**Symptoms**:
- Scrolling is choppy
- Search is slow
- Browser becomes unresponsive

**Root Causes**:
1. Too many DOM elements rendered
2. Debouncing not working
3. Very large dataset (>10,000 issues)

**Quick Fix**:
```javascript
// Reduce visible buffer
window.CONFIG.VISIBLE_BUFFER = 2;  // Default is 5

// Increase debounce times
window.CONFIG.SCROLL_DEBOUNCE = 50;  // Default is 10
window.CONFIG.SEARCH_DEBOUNCE = 500;  // Default is 300
```

---

## 🔍 Diagnostic Commands

### Check Dashboard State
```javascript
// Complete state dump
console.log({
  totalIssues: window.state.allIssues?.length || 0,
  filteredIssues: window.state.filteredIssues?.length || 0,
  codeContexts: window.state.codeContextMap?.size || 0,
  containerHeight: window.state.containerHeight,
  visibleRange: [window.state.visibleStart, window.state.visibleEnd],
  currentFilter: window.state.currentFilter,
  currentSearch: window.state.currentSearch
});
```

### Check DOM Elements
```javascript
// Verify all required elements exist
const elements = [
  'scrollContainer', 'issuesBody', 'searchInput', 
  'issuesCount', 'spacerTop', 'spacerBottom',
  'issuesData', 'codeContextData'
];

elements.forEach(id => {
  const el = document.getElementById(id);
  console.log(`${id}: ${el ? '✓' : '✗'}`);
});
```

### Check Data Integrity
```javascript
// Sample first few issues
console.log('First 3 issues:', window.state.allIssues?.slice(0, 3));

// Check for malformed issues
const invalid = window.state.allIssues?.filter(issue => !issue.id || !issue.file);
console.log('Invalid issues:', invalid?.length || 0);

// Check embedded data format
const script = document.getElementById('issuesData');
const preview = script?.textContent.substring(0, 200);
console.log('Data format:', preview);
```

---

## 🛠️ Universal Recovery Script

If all else fails, run this comprehensive recovery:

```javascript
(function recoverCompletely() {
  console.log('🚑 Running complete dashboard recovery...');
  
  // 1. Ensure state exists
  window.state = window.state || {
    allIssues: [],
    filteredIssues: [],
    codeContextMap: new Map(),
    currentFilter: 'all',
    currentSearch: '',
    visibleStart: 0,
    visibleEnd: 0,
    scrollTop: 0,
    containerHeight: 600
  };
  
  // 2. Fix container
  const container = document.getElementById('scrollContainer');
  if (container) {
    container.style.height = '600px';
    container.style.minHeight = '400px';
    container.style.overflowY = 'auto';
  }
  
  // 3. Try to load data
  try {
    if (typeof loadEmbeddedData === 'function') {
      loadEmbeddedData();
    } else {
      // Manual data load
      const script = document.getElementById('issuesData');
      if (script) {
        const text = script.textContent.trim();
        let lines = [];
        
        if (text.includes('__NEWLINE__')) {
          lines = text.split('__NEWLINE__');
        } else if (text.includes('\n')) {
          lines = text.split(/\r?\n/);
        } else {
          lines = text.match(/\{[^{}]*\}/g) || [];
        }
        
        window.state.allIssues = lines
          .filter(l => l.trim())
          .map(l => {
            try { return JSON.parse(l); } 
            catch { return null; }
          })
          .filter(Boolean);
      }
    }
    
    // 4. Initialize filtered issues
    window.state.filteredIssues = window.state.allIssues;
    
    // 5. Force render
    if (typeof filterData === 'function') filterData();
    if (typeof renderVisibleRows === 'function') {
      window.state.visibleStart = 0;
      window.state.visibleEnd = Math.min(50, window.state.filteredIssues.length);
      renderVisibleRows();
    }
    
    // 6. Update UI
    const count = document.getElementById('issuesCount');
    if (count) {
      count.textContent = `Showing all ${window.state.allIssues.length} issues`;
    }
    
    console.log('✅ Recovery complete!', {
      issues: window.state.allIssues.length,
      rendered: document.querySelectorAll('#issuesBody tr').length
    });
    
  } catch (error) {
    console.error('❌ Recovery failed:', error);
  }
})();
```

---

## 📞 When to Regenerate

Regenerate the dashboard if:
1. Emergency fixes don't work
2. Data appears corrupted
3. You need code context that's missing
4. Performance is unacceptable

**Regenerate with Python** (Recommended):
```bash
python3 generate-standalone-virtual-dashboard.py analysis-with-context.json new-dashboard.html
```

**Regenerate with updated TypeScript**:
```bash
cd cppcheck-dashboard-generator
npm install && npm run build && npm link
cppcheck-dashboard analysis.json dashboard.html
```

---

## 🚀 Prevention Tips

1. **Always use Python generator** for production dashboards
2. **Test locally** before deploying
3. **Check browser console** after deployment
4. **Keep emergency fix handy** for quick recovery
5. **Monitor dashboard health** with health check tool

---

**Last Updated**: January 2025
**Applies To**: CPPCheck Studio v1.0.0+