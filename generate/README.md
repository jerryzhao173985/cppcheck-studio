# Dashboard Generators

This directory contains various dashboard generators for CPPCheck Studio.

## Available Generators

### 1. `generate-optimized-dashboard-codefix.py` (RECOMMENDED)
- **Status**: ✅ Production Ready - Code Context Fixed
- **Description**: Optimized dashboard with proper code context display
- **Features**:
  - Correctly displays code context from `add-code-context.py`
  - Shows inline code preview (1-2 lines) in issue list
  - Full code context with highlighting in modal
  - File grouping and sidebar navigation
  - Progress tracking (viewed/fixed)
  - Search and filtering
  - Export remaining issues
- **Usage**: `python3 generate-optimized-dashboard-codefix.py analysis-with-context.json output.html`

### 2. `generate-optimized-dashboard.py`
- **Status**: ⚠️ Has code context display bug
- **Description**: Original optimized dashboard (doesn't show code context properly)
- **Issue**: Looks for `issue.context.code_lines` instead of `issue.code_context.lines`

### 3. `generate-optimized-dashboard-fixed.py`
- **Status**: ✅ Working (older fix)
- **Description**: Earlier fix attempt that restored modal functionality

### 4. `generate-enhanced-dashboard.py`
- **Status**: ✅ Working
- **Description**: Beautiful UI with animations and enhanced features

### 5. `generate-simple-dashboard.py`
- **Status**: ✅ Working
- **Description**: Simple dashboard without JSONL issues

### 6. `generate-standalone-virtual-dashboard.py`
- **Status**: ✅ Working
- **Description**: Virtual scrolling for large datasets

## Code Context Structure

The `add-code-context.py` script generates code context with this structure:

```json
{
  "code_context": {
    "lines": [
      {
        "number": 123,
        "content": "    void myFunction() {",
        "is_target": false
      },
      {
        "number": 124,
        "content": "        someCode(); // issue here",
        "is_target": true
      },
      {
        "number": 125,
        "content": "    }",
        "is_target": false
      }
    ],
    "start_line": 120,
    "end_line": 130
  }
}
```

The fixed dashboard generator (`generate-optimized-dashboard-codefix.py`) correctly reads this structure.

## Workflow Integration

The GitHub Actions workflow prioritizes generators in this order:
1. `generate-optimized-dashboard-codefix.py` (with proper code context)
2. `generate-optimized-dashboard.py` (fallback)
3. `generate-enhanced-dashboard.py`
4. `generate-simple-dashboard.py`
5. TypeScript generator (if Python generators not found)