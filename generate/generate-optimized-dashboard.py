#!/usr/bin/env python3
"""
Optimized Dashboard Generator for CPPCheck Studio - FIXED VERSION
Restores code preview modal functionality while keeping optimizations


⚠️ DEPRECATION WARNING: This generator is deprecated and will be removed in April 2025.
Please use generate-standalone-virtual-dashboard.py instead.

See generate/DEPRECATION_NOTICE.md for migration guide.
"""

import sys
import warnings

# Show deprecation warning
warnings.warn(
    "\n⚠️  DEPRECATION: generate-optimized-dashboard.py is deprecated.\n"
    "   Please use generate-standalone-virtual-dashboard.py instead.\n"
    "   See generate/DEPRECATION_NOTICE.md for details.\n",
    DeprecationWarning,
    stacklevel=2
)
print("\n⚠️  This generator is deprecated. Please use generate-standalone-virtual-dashboard.py\n", file=sys.stderr)

import json
import sys
import os
from collections import defaultdict
from datetime import datetime
import html
import hashlib

class OptimizedDashboardGenerator:
    def __init__(self, issues_file):
        with open(issues_file, 'r') as f:
            data = json.load(f)
            
        # Handle both direct issues array and nested structure
        if isinstance(data, list):
            self.issues = data
        elif isinstance(data, dict) and 'issues' in data:
            self.issues = data['issues']
        else:
            raise ValueError("Invalid JSON structure")
        
        # Generate unique IDs for each issue
        for i, issue in enumerate(self.issues):
            issue['unique_id'] = hashlib.md5(f"{issue.get('file', '')}:{issue.get('line', '')}:{issue.get('id', '')}:{i}".encode()).hexdigest()[:8]
        
        # Group issues by file
        self.files_map = defaultdict(list)
        for issue in self.issues:
            file_path = issue.get('file', 'Unknown')
            self.files_map[file_path].append(issue)
        
        # Sort files by issue count (most issues first)
        self.sorted_files = sorted(self.files_map.items(), key=lambda x: len(x[1]), reverse=True)
        
        # Calculate statistics
        self.calculate_stats()
        
        # Generate fix patterns
        self.fix_patterns = self.generate_fix_patterns()
    
    def calculate_stats(self):
        self.stats = {
            'total': len(self.issues),
            'error': 0,
            'warning': 0,
            'style': 0,
            'performance': 0,
            'portability': 0,
            'information': 0
        }
        
        for issue in self.issues:
            severity = issue.get('severity', 'style')
            if severity in self.stats:
                self.stats[severity] += 1
    
    def generate_fix_patterns(self):
        """Generate quick fix suggestions based on issue patterns"""
        patterns = {
            'missingOverride': {
                'pattern': 'override',
                'suggestion': 'Add override specifier to virtual function',
                'fix_template': 'void functionName() override'
            },
            'passedByValue': {
                'pattern': 'passed by value',
                'suggestion': 'Pass by const reference instead',
                'fix_template': 'const Type& param'
            },
            'uninitMemberVar': {
                'pattern': 'not initialized',
                'suggestion': 'Initialize member in constructor',
                'fix_template': 'ClassName() : member() {}'
            },
            'cstyleCast': {
                'pattern': 'C-style cast',
                'suggestion': 'Use static_cast instead',
                'fix_template': 'static_cast<Type>(value)'
            },
            'useNullptr': {
                'pattern': 'NULL',
                'suggestion': 'Use nullptr instead of NULL',
                'fix_template': 'nullptr'
            },
            'constParameter': {
                'pattern': 'can be declared with const',
                'suggestion': 'Add const qualifier',
                'fix_template': 'const Type param'
            },
            'explicitConstructor': {
                'pattern': 'should be explicit',
                'suggestion': 'Add explicit keyword',
                'fix_template': 'explicit ClassName(param)'
            }
        }
        return patterns
    
    def get_fix_suggestion(self, issue):
        """Get quick fix suggestion for an issue"""
        message = issue.get('message', '').lower()
        for fix_id, pattern in self.fix_patterns.items():
            if pattern['pattern'] in message:
                return {
                    'id': fix_id,
                    'suggestion': pattern['suggestion'],
                    'template': pattern['fix_template']
                }
        return None
    
    def get_inline_code(self, issue):
        """Get 1-2 lines of code context"""
        # Check both old and new structure for compatibility
        code_context = issue.get('code_context', {})
        if code_context and 'lines' in code_context:
            lines = code_context['lines']
            target_line = issue.get('line', 0)
            
            # Find the target line in the context
            for i, line_info in enumerate(lines):
                if line_info.get('number') == target_line or line_info.get('is_target', False):
                    # Get the line and maybe one before/after
                    result = []
                    if i > 0:
                        result.append(lines[i-1])
                    result.append(line_info)
                    if i < len(lines) - 1 and len(result) < 2:
                        result.append(lines[i+1])
                    return result
        
        # Fallback to old structure if exists
        context = issue.get('context', {})
        if context and 'code_lines' in context:
            lines = context['code_lines']
            target_line = issue.get('line', 0)
            
            # Find the target line in the context
            for i, line_info in enumerate(lines):
                if line_info.get('line_number') == target_line:
                    # Get the line and maybe one before/after
                    result = []
                    if i > 0:
                        result.append(lines[i-1])
                    result.append(line_info)
                    if i < len(lines) - 1 and len(result) < 2:
                        result.append(lines[i+1])
                    return result
        return []
    
    def generate(self, output_file):
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Analysis - Optimized Dashboard</title>
    <style>
        /*
         * CSS Variable System Documentation
         * =================================
         * This dashboard uses CSS custom properties for theming and consistency.
         * 
         * Color Variables:
         * - All colors are defined as both hex (--color) and RGB (--color-rgb) values
         * - RGB values are used for alpha transparency with rgba()
         * - Hex values are used for solid colors
         * 
         * Usage Examples:
         * - Solid color: background: var(--bg-primary);
         * - With alpha: background: rgba(var(--bg-primary-rgb), 0.9);
         * - With fallback: color: var(--text-primary, #212529);
         * 
         * Theme Support:
         * - Light theme: Default :root variables
         * - Dark theme: [data-theme="dark"] overrides
         * - System preference: @media (prefers-color-scheme: dark)
         */
        
        /* CSS Custom Properties with RGB fallbacks for better compatibility */
        :root {{
            /* Primary colors as hex */
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #e9ecef;
            
            /* RGB equivalents for alpha transparency */
            --bg-primary-rgb: 255, 255, 255;
            --bg-secondary-rgb: 248, 249, 250;
            --bg-tertiary-rgb: 233, 236, 239;
            
            /* Text colors */
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --text-primary-rgb: 33, 37, 41;
            --text-secondary-rgb: 108, 117, 125;
            
            /* UI colors */
            --border-color: #dee2e6;
            --border-color-rgb: 222, 226, 230;
            --hover-bg: var(--bg-secondary);
            --hover-bg-rgb: var(--bg-secondary-rgb);
            
            /* Status colors */
            --error-color: #dc3545;
            --warning-color: #ffc107;
            --info-color: #0dcaf0;
            --success-color: #198754;
            --style-color: #6f42c1;
            
            /* Effects */
            --shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
            --shadow-hover: 0 2px 8px rgba(0, 0, 0, 0.15);
            --transition-speed: 200ms;
            
            /* Typography */
            --font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
        }}
        
        [data-theme="dark"] {{
            /* Primary colors as hex */
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --bg-tertiary: #3a3a3a;
            
            /* RGB equivalents for alpha transparency */
            --bg-primary-rgb: 26, 26, 26;
            --bg-secondary-rgb: 45, 45, 45;
            --bg-tertiary-rgb: 58, 58, 58;
            
            /* Text colors */
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --text-primary-rgb: 224, 224, 224;
            --text-secondary-rgb: 160, 160, 160;
            
            /* UI colors */
            --border-color: #404040;
            --border-color-rgb: 64, 64, 64;
            --hover-bg: var(--bg-tertiary);
            --hover-bg-rgb: var(--bg-tertiary-rgb);
            
            /* Effects */
            --shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
            --shadow-hover: 0 2px 8px rgba(0, 0, 0, 0.7);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
            font-size: 16px;
        }}
        
        /* Header */
        .header {{
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
            background: rgba(var(--bg-secondary-rgb), 0.95);
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .title {{
            font-size: 1.5em;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .stats-bar {{
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .stat-badge {{
            display: flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.85em;
            font-weight: 500;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        .stat-badge:hover {{
            transform: translateY(-1px);
        }}
        
        .stat-badge.error {{
            background: rgba(220, 53, 69, 0.1);
            color: var(--error-color);
            border: 1px solid rgba(220, 53, 69, 0.3);
        }}
        
        .stat-badge.warning {{
            background: rgba(255, 193, 7, 0.1);
            color: #f39c12;
            border: 1px solid rgba(255, 193, 7, 0.3);
        }}
        
        .stat-badge.style {{
            background: rgba(111, 66, 193, 0.1);
            color: var(--style-color);
            border: 1px solid rgba(111, 66, 193, 0.3);
        }}
        
        .stat-badge.performance {{
            background: rgba(25, 135, 84, 0.1);
            color: var(--success-color);
            border: 1px solid rgba(25, 135, 84, 0.3);
        }}
        
        .stat-badge.information {{
            background: rgba(13, 202, 240, 0.1);
            color: var(--info-color);
            border: 1px solid rgba(13, 202, 240, 0.3);
        }}
        
        /* Controls */
        .controls {{
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem;
            position: sticky;
            top: 73px;
            z-index: 90;
        }}
        
        .controls-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 300px;
            position: relative;
        }}
        
        .search-input {{
            width: 100%;
            padding: 0.5rem 2.5rem 0.5rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 0.85em;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: var(--style-color);
            box-shadow: 0 0 0 3px rgba(111, 66, 193, 0.1);
        }}
        
        .search-hint {{
            position: absolute;
            right: 0.75rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.75em;
            color: var(--text-secondary);
        }}
        
        .control-buttons {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .control-btn {{
            padding: 0.5rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .control-btn:hover {{
            background: var(--hover-bg);
            border-color: var(--style-color);
        }}
        
        .control-btn.active {{
            background: var(--style-color);
            color: white;
            border-color: var(--style-color);
        }}
        
        /* Main Content */
        .main-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem;
        }}
        
        /* Progress Bar */
        .progress-section {{
            margin-bottom: 2rem;
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
        }}
        
        .progress-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
            font-size: 0.85em;
        }}
        
        .progress-bar {{
            height: 8px;
            background: var(--bg-tertiary);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--success-color), var(--style-color));
            transition: width 0.3s;
        }}
        
        /* File Groups */
        .file-group {{
            margin-bottom: 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            overflow: hidden;
            transition: all 0.2s;
        }}
        
        .file-group:hover {{
            box-shadow: var(--shadow);
        }}
        
        .file-header {{
            padding: 1rem;
            background: var(--bg-secondary);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }}
        
        .file-header:hover {{
            background: var(--hover-bg);
        }}
        
        .file-info {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .file-name {{
            font-weight: 500;
            font-family: var(--font-mono);
            font-size: 0.85em;
        }}
        
        .issue-count {{
            font-size: 0.75em;
            color: var(--text-secondary);
        }}
        
        .severity-dots {{
            display: flex;
            gap: 2px;
        }}
        
        .severity-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }}
        
        .severity-dot.error {{ background: var(--error-color); }}
        .severity-dot.warning {{ background: var(--warning-color); }}
        .severity-dot.style {{ background: var(--style-color); }}
        .severity-dot.performance {{ background: var(--success-color); }}
        .severity-dot.information {{ background: var(--info-color); }}
        
        .file-toggle {{
            font-size: 0.75em;
            color: var(--text-secondary);
        }}
        
        /* Issues */
        .issues-container {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s;
        }}
        
        .issues-container.expanded {{
            max-height: none;
        }}
        
        .issue-item {{
            padding: 0.75rem 1rem;
            border-top: 1px solid var(--border-color);
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            transition: background 0.2s;
            cursor: pointer;
        }}
        
        .issue-item:hover {{
            background: var(--hover-bg);
        }}
        
        .issue-item.viewed {{
            opacity: 0.7;
        }}
        
        .issue-item.fixed {{
            text-decoration: line-through;
            opacity: 0.5;
        }}
        
        .issue-severity {{
            flex-shrink: 0;
            padding: 0.125rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75em;
            font-weight: 500;
        }}
        
        .issue-content {{
            flex: 1;
            min-width: 0;
        }}
        
        .issue-message {{
            font-size: 0.85em;
            margin-bottom: 0.25rem;
        }}
        
        .issue-code {{
            font-family: var(--font-mono);
            font-size: 0.8em;
            background: var(--bg-tertiary);
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            margin: 0.25rem 0;
            overflow-x: auto;
            white-space: pre;
        }}
        
        .issue-meta {{
            display: flex;
            gap: 1rem;
            font-size: 0.75em;
            color: var(--text-secondary);
        }}
        
        .issue-actions {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}
        
        .action-btn {{
            padding: 0.25rem 0.5rem;
            border: 1px solid var(--border-color);
            border-radius: 0.25rem;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 0.75em;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .action-btn:hover {{
            background: var(--hover-bg);
            border-color: var(--style-color);
        }}
        
        .fix-suggestion {{
            background: rgba(25, 135, 84, 0.1);
            color: var(--success-color);
            border-color: rgba(25, 135, 84, 0.3);
        }}
        
        /* Modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .modal.show {{
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 1;
        }}
        
        .modal-content {{
            background: var(--bg-primary);
            border-radius: 0.5rem;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
            max-width: 90%;
            max-height: 90%;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transform: scale(0.9);
            transition: transform 0.3s;
        }}
        
        .modal.show .modal-content {{
            transform: scale(1);
        }}
        
        .modal-header {{
            padding: 1rem;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .modal-title {{
            font-size: 1.125em;
            font-weight: 600;
        }}
        
        .modal-close {{
            background: none;
            border: none;
            font-size: 1.5em;
            cursor: pointer;
            color: var(--text-secondary);
            padding: 0;
            width: 2rem;
            height: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.25rem;
            transition: all 0.2s;
        }}
        
        .modal-close:hover {{
            background: var(--hover-bg);
            color: var(--text-primary);
        }}
        
        .modal-body {{
            padding: 1.5rem;
            overflow-y: auto;
            max-height: 70vh;
        }}
        
        .issue-details {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        .detail-section {{
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
        }}
        
        .detail-section h4 {{
            margin: 0 0 0.75rem 0;
            font-size: 1em;
            color: var(--text-primary);
        }}
        
        .code-context {{
            background: var(--bg-tertiary);
            border-radius: 0.5rem;
            overflow: hidden;
            font-family: var(--font-mono);
            font-size: 0.85em;
        }}
        
        .code-line {{
            display: flex;
            padding: 0.25rem 0.5rem;
            transition: background 0.2s;
        }}
        
        .code-line:hover {{
            background: var(--hover-bg);
        }}
        
        .code-line.highlighted {{
            background: rgba(255, 193, 7, 0.2);
            border-left: 3px solid var(--warning-color);
        }}
        
        .line-number {{
            color: var(--text-secondary);
            min-width: 3rem;
            text-align: right;
            padding-right: 1rem;
            user-select: none;
        }}
        
        .line-content {{
            flex: 1;
            white-space: pre;
            overflow-x: auto;
        }}
        
        /* Theme Toggle */
        .theme-toggle {{
            position: fixed;
            bottom: 1rem;
            right: 1rem;
            padding: 0.75rem;
            border-radius: 50%;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            cursor: pointer;
            box-shadow: var(--shadow);
            transition: all 0.2s;
        }}
        
        .theme-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        /* Toast */
        .toast {{
            position: fixed;
            bottom: 4rem;
            right: 1rem;
            padding: 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            box-shadow: var(--shadow);
            transform: translateX(400px);
            transition: transform 0.3s;
            z-index: 1000;
        }}
        
        .toast.show {{
            transform: translateX(0);
        }}
        
        /* Loading */
        .loading {{
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
        }}
        
        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-secondary);
        }}
        
        .empty-state h2 {{
            font-size: 1.5em;
            margin-bottom: 0.5rem;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            body {{
                font-size: 14px;
            }}
            
            .header-content {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .stats-bar {{
                font-size: 0.85em;
            }}
            
            .controls-content {{
                flex-direction: column;
                gap: 0.5rem;
            }}
            
            .search-box {{
                min-width: 100%;
                height: 44px; /* Touch target size */
                font-size: 16px; /* Prevent zoom on iOS */
            }}
            
            .control-btn {{
                font-size: 0.8rem;
                padding: 10px 12px;
                min-height: 44px; /* Touch target size */
            }}
            
            /* Enable horizontal scroll for issues */
            .issues-container {{
                padding: 10px;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
            
            .file-section {{
                min-width: 600px; /* Force horizontal scroll */
            }}
            
            .file-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
                padding: 10px;
            }}
            
            .file-info h3 {{
                font-size: 0.85em;
            }}
            
            .issue-item {{
                flex-direction: column;
                font-size: 0.85em;
                padding: 0.75rem;
            }}
            
            .modal-content {{
                max-width: 95%;
                max-height: 95%;
            }}
        }}
        
        /* Code Highlighting */
        .hljs-keyword {{ color: #d73a49; }}
        .hljs-string {{ color: #032f62; }}
        .hljs-comment {{ color: #6a737d; }}
        .hljs-number {{ color: #005cc5; }}
        .hljs-function {{ color: #6f42c1; }}
        
        /* Print Styles for Professional Reports */
        @media print {{
            /* Reset for print */
            * {{
                background: transparent !important;
                color: #000 !important;
                box-shadow: none !important;
                text-shadow: none !important;
            }}
            
            body {{
                font-size: 12pt;
                line-height: 1.5;
                font-family: Georgia, 'Times New Roman', serif;
                margin: 0;
                padding: 0;
            }}
            
            /* Hide interactive elements */
            .controls,
            .search-container,
            .filter-buttons,
            button,
            .action-btn,
            .toggle-fix,
            .fix-button,
            a[href^="#"],
            a[href^="javascript:"] {{
                display: none !important;
            }}
            
            /* Header styling */
            .header {{
                background: none !important;
                border-bottom: 2px solid #000;
                padding: 0 0 1em 0;
                margin-bottom: 1em;
            }}
            
            .title {{
                font-size: 24pt;
                font-weight: bold;
                margin-bottom: 0.5em;
                color: #000;
            }}
            
            /* Stats formatting */
            .stats-bar {{
                display: flex;
                justify-content: space-between;
                margin: 1em 0;
                page-break-inside: avoid;
            }}
            
            .stat-badge {{
                border: 1px solid #000;
                padding: 0.5em;
                text-align: center;
                flex: 1;
                margin: 0 0.25em;
            }}
            
            /* Tables */
            .issue-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 10pt;
                page-break-inside: auto;
            }}
            
            .issue-table th,
            .issue-table td {{
                border: 1px solid #000;
                padding: 0.5em;
                text-align: left;
            }}
            
            .issue-table th {{
                background-color: #f0f0f0 !important;
                font-weight: bold;
                position: sticky;
                top: 0;
            }}
            
            .issue-table tr {{
                page-break-inside: avoid;
                page-break-after: auto;
            }}
            
            /* Severity labels */
            .severity-badge {{
                font-weight: bold;
                padding: 0.2em 0.5em;
                border: 1px solid #000;
            }}
            
            /* URLs */
            a[href]:after {{
                content: " (" attr(href) ")";
                font-size: 80%;
                font-style: italic;
            }}
            
            /* Page setup */
            @page {{
                size: A4;
                margin: 0.75in;
            }}
            
            @page :first {{
                margin-top: 0.5in;
            }}
            
            /* Page numbers */
            .page-break {{
                page-break-before: always;
            }}
        }}
        
        /* Accessibility: High contrast mode */
        @media (prefers-contrast: high) {{
            :root {{
                --bg-primary: #ffffff;
                --bg-secondary: #f0f0f0;
                --text-primary: #000000;
                --text-secondary: #333333;
                --border-color: #000000;
                --error-color: #cc0000;
                --warning-color: #ff6600;
            }}
            
            .stat-badge,
            .severity-badge {{
                border-width: 2px;
            }}
            
            .issue-table th,
            .issue-table td {{
                border-width: 2px;
            }}
        }}
        
        /* Accessibility: Reduced motion */
        @media (prefers-reduced-motion: reduce) {{
            *,
            *::before,
            *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
                scroll-behavior: auto !important;
            }}
            
            .loading-spinner {{
                animation: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div style="display: flex; align-items: center; gap: 2rem; flex-wrap: wrap; justify-content: space-between; width: 100%;">
                <h1 class="title">
                    <span>🛡️</span>
                    <span>Code Analysis Dashboard</span>
                </h1>
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <a href="../../gallery.html" style="padding: 0.5rem 1rem; background: rgba(255,255,255,0.1); border-radius: 0.5rem; color: var(--text-primary); text-decoration: none; font-size: 0.85em; transition: all 0.2s;">
                        ← Back to Gallery
                    </a>
                    <a href="../../index.html" style="padding: 0.5rem 1rem; background: rgba(255,255,255,0.1); border-radius: 0.5rem; color: var(--text-primary); text-decoration: none; font-size: 0.85em; transition: all 0.2s;">
                        🏠 Home
                    </a>
                </div>
            </div>
            <div class="stats-bar" id="statsBar" style="margin-top: 1rem;">
                <div class="stat-badge total" onclick="filterBySeverity('all')">
                    <span>Total</span>
                    <span>{self.stats['total']}</span>
                </div>
                <div class="stat-badge error" onclick="filterBySeverity('error')">
                    <span>Errors</span>
                    <span>{self.stats['error']}</span>
                </div>
                <div class="stat-badge warning" onclick="filterBySeverity('warning')">
                    <span>Warnings</span>
                    <span>{self.stats['warning']}</span>
                </div>
                <div class="stat-badge style" onclick="filterBySeverity('style')">
                    <span>Style</span>
                    <span>{self.stats['style']}</span>
                </div>
                <div class="stat-badge performance" onclick="filterBySeverity('performance')">
                    <span>Performance</span>
                    <span>{self.stats['performance']}</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="controls">
        <div class="controls-content">
            <div class="search-box">
                <input type="text" class="search-input" id="searchInput" 
                       placeholder="Search issues... (e.g., 'error in .h', 'warning controller', 'override')"
                       onkeyup="handleSearch(event)">
                <span class="search-hint">Press /</span>
            </div>
            <div class="control-buttons">
                <button class="control-btn" onclick="toggleGrouping()">
                    Group by File
                </button>
                <button class="control-btn" onclick="exportData()">
                    Export
                </button>
                <button class="control-btn" onclick="showHelp()">
                    Help
                </button>
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="progress-section">
            <div class="progress-header">
                <span>Progress: <span id="progressText">0 / {self.stats['total']} issues reviewed</span></span>
                <span><span id="fixedCount">0</span> fixed</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill" style="width: 0%"></div>
            </div>
        </div>
        
        <div id="issuesContainer">
            <!-- Issues will be rendered here -->
        </div>
        
        <div class="loading" id="loading">
            Loading issues...
        </div>
        
        <div class="empty-state" id="emptyState" style="display: none;">
            <h2>No issues found</h2>
            <p>Try adjusting your filters or search criteria</p>
        </div>
    </div>
    
    <!-- Modal for code preview -->
    <div class="modal" id="codeModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title" id="modalTitle">Issue Details</h3>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Content will be inserted here -->
            </div>
        </div>
    </div>
    
    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
        <span id="themeIcon">🌙</span>
    </button>
    
    <div class="toast" id="toast"></div>
    
    <script>
        // Global state
        const state = {{
            issues: {json.dumps(self.issues)},
            fileGroups: {json.dumps(dict(self.sorted_files))},
            currentFilter: 'all',
            searchQuery: '',
            groupByFile: true,
            viewed: new Set(),
            fixed: new Set(),
            expandedFiles: new Set()
        }};
        
        // Fix patterns
        const fixPatterns = {json.dumps(self.fix_patterns)};
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            restoreState();
            applyTheme();
            renderIssues();
            updateProgress();
            
            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {{
                if (e.key === '/' && e.target.tagName !== 'INPUT') {{
                    e.preventDefault();
                    document.getElementById('searchInput').focus();
                }}
                if (e.key === 'Escape') {{
                    document.getElementById('searchInput').blur();
                    closeModal();
                }}
                if (e.key >= '1' && e.key <= '5' && e.ctrlKey) {{
                    e.preventDefault();
                    const severities = ['all', 'error', 'warning', 'style', 'performance'];
                    filterBySeverity(severities[parseInt(e.key) - 1]);
                }}
            }});
            
            // Hide loading
            document.getElementById('loading').style.display = 'none';
        }});
        
        // State management
        function saveState() {{
            const stateData = {{
                viewed: [...state.viewed],
                fixed: [...state.fixed],
                expandedFiles: [...state.expandedFiles],
                currentFilter: state.currentFilter,
                groupByFile: state.groupByFile
            }};
            localStorage.setItem('dashboardState', JSON.stringify(stateData));
        }}
        
        function restoreState() {{
            const saved = localStorage.getItem('dashboardState');
            if (saved) {{
                const data = JSON.parse(saved);
                state.viewed = new Set(data.viewed || []);
                state.fixed = new Set(data.fixed || []);
                state.expandedFiles = new Set(data.expandedFiles || []);
                state.currentFilter = data.currentFilter || 'all';
                state.groupByFile = data.groupByFile !== false;
            }}
        }}
        
        // Theme management
        function applyTheme() {{
            const theme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', theme);
            document.getElementById('themeIcon').textContent = theme === 'dark' ? '☀️' : '🌙';
        }}
        
        function toggleTheme() {{
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            document.getElementById('themeIcon').textContent = next === 'dark' ? '☀️' : '🌙';
        }}
        
        // Rendering
        function renderIssues() {{
            const container = document.getElementById('issuesContainer');
            container.innerHTML = '';
            
            const filteredIssues = getFilteredIssues();
            
            if (filteredIssues.length === 0) {{
                document.getElementById('emptyState').style.display = 'block';
                return;
            }}
            
            document.getElementById('emptyState').style.display = 'none';
            
            if (state.groupByFile) {{
                renderGroupedIssues(filteredIssues);
            }} else {{
                renderFlatIssues(filteredIssues);
            }}
        }}
        
        function renderGroupedIssues(issues) {{
            const container = document.getElementById('issuesContainer');
            const fileMap = new Map();
            
            // Group filtered issues by file
            issues.forEach(issue => {{
                const file = issue.file || 'Unknown';
                if (!fileMap.has(file)) {{
                    fileMap.set(file, []);
                }}
                fileMap.get(file).push(issue);
            }});
            
            // Sort files by issue count
            const sortedFiles = Array.from(fileMap.entries())
                .sort((a, b) => b[1].length - a[1].length);
            
            sortedFiles.forEach(([file, fileIssues]) => {{
                const fileGroup = createFileGroup(file, fileIssues);
                container.appendChild(fileGroup);
            }});
        }}
        
        function createFileGroup(file, issues) {{
            const group = document.createElement('div');
            group.className = 'file-group';
            
            const header = document.createElement('div');
            header.className = 'file-header';
            header.onclick = () => toggleFileGroup(file);
            
            const fileInfo = document.createElement('div');
            fileInfo.className = 'file-info';
            
            const fileName = document.createElement('div');
            fileName.className = 'file-name';
            fileName.textContent = file;
            
            const issueCount = document.createElement('div');
            issueCount.className = 'issue-count';
            issueCount.textContent = `${{issues.length}} issue${{issues.length > 1 ? 's' : ''}}`;
            
            const severityDots = document.createElement('div');
            severityDots.className = 'severity-dots';
            
            // Show severity distribution
            const severityCounts = {{}};
            issues.forEach(issue => {{
                const sev = issue.severity || 'style';
                severityCounts[sev] = (severityCounts[sev] || 0) + 1;
            }});
            
            ['error', 'warning', 'style', 'performance', 'information'].forEach(sev => {{
                const count = severityCounts[sev] || 0;
                for (let i = 0; i < Math.min(count, 5); i++) {{
                    const dot = document.createElement('div');
                    dot.className = `severity-dot ${{sev}}`;
                    severityDots.appendChild(dot);
                }}
            }});
            
            fileInfo.appendChild(fileName);
            fileInfo.appendChild(issueCount);
            fileInfo.appendChild(severityDots);
            
            const toggle = document.createElement('div');
            toggle.className = 'file-toggle';
            toggle.textContent = state.expandedFiles.has(file) ? '▼' : '▶';
            
            header.appendChild(fileInfo);
            header.appendChild(toggle);
            
            const issuesContainer = document.createElement('div');
            issuesContainer.className = 'issues-container';
            if (state.expandedFiles.has(file)) {{
                issuesContainer.classList.add('expanded');
            }}
            
            issues.forEach(issue => {{
                const issueEl = createIssueElement(issue);
                issuesContainer.appendChild(issueEl);
            }});
            
            group.appendChild(header);
            group.appendChild(issuesContainer);
            
            return group;
        }}
        
        function createIssueElement(issue) {{
            const item = document.createElement('div');
            item.className = 'issue-item';
            if (state.viewed.has(issue.unique_id)) {{
                item.classList.add('viewed');
            }}
            if (state.fixed.has(issue.unique_id)) {{
                item.classList.add('fixed');
            }}
            
            // Click on row shows details modal
            item.onclick = (e) => {{
                if (!e.target.classList.contains('action-btn')) {{
                    showIssueDetails(issue);
                }}
            }};
            
            // Severity badge
            const severity = document.createElement('div');
            severity.className = `issue-severity ${{issue.severity || 'style'}}`;
            severity.textContent = issue.severity || 'style';
            severity.style.background = getSeverityColor(issue.severity);
            severity.style.color = 'white';
            
            // Content
            const content = document.createElement('div');
            content.className = 'issue-content';
            
            const message = document.createElement('div');
            message.className = 'issue-message';
            message.textContent = issue.message || 'No message';
            
            // Inline code preview (1-2 lines)
            const codeLines = getInlineCode(issue);
            if (codeLines.length > 0) {{
                const codePreview = document.createElement('div');
                codePreview.className = 'issue-code';
                codePreview.textContent = codeLines.map(line => {{
                    // Handle both old format (line_number) and new format (number)
                    const lineNum = line.number || line.line_number || '?';
                    return `${{lineNum}}: ${{line.content}}`;
                }}).join('\\n');
                content.appendChild(codePreview);
            }}
            
            const meta = document.createElement('div');
            meta.className = 'issue-meta';
            meta.innerHTML = `
                <span>Line ${{issue.line || '?'}}</span>
                <span>ID: ${{issue.id || 'unknown'}}</span>
                <span>Column: ${{issue.column || '?'}}</span>
            `;
            
            content.appendChild(message);
            content.appendChild(meta);
            
            // Actions
            const actions = document.createElement('div');
            actions.className = 'issue-actions';
            
            // View button
            const viewBtn = document.createElement('button');
            viewBtn.className = 'action-btn';
            viewBtn.textContent = state.viewed.has(issue.unique_id) ? '✓ Viewed' : 'View';
            viewBtn.onclick = (e) => {{
                e.stopPropagation();
                markAsViewed(issue);
            }};
            
            // Fix button
            const fixBtn = document.createElement('button');
            fixBtn.className = 'action-btn';
            fixBtn.textContent = state.fixed.has(issue.unique_id) ? '✓ Fixed' : 'Fix';
            fixBtn.onclick = (e) => {{
                e.stopPropagation();
                markAsFixed(issue);
            }};
            
            actions.appendChild(viewBtn);
            actions.appendChild(fixBtn);
            
            // Quick fix suggestion
            const fix = getFixSuggestion(issue);
            if (fix) {{
                const fixSuggestion = document.createElement('button');
                fixSuggestion.className = 'action-btn fix-suggestion';
                fixSuggestion.textContent = '💡';
                fixSuggestion.title = fix.suggestion;
                fixSuggestion.onclick = (e) => {{
                    e.stopPropagation();
                    showFixSuggestion(fix);
                }};
                actions.appendChild(fixSuggestion);
            }}
            
            item.appendChild(severity);
            item.appendChild(content);
            item.appendChild(actions);
            
            return item;
        }}
        
        function renderFlatIssues(issues) {{
            const container = document.getElementById('issuesContainer');
            issues.forEach(issue => {{
                const issueEl = createIssueElement(issue);
                container.appendChild(issueEl);
            }});
        }}
        
        // Modal functions
        function showIssueDetails(issue) {{
            const modal = document.getElementById('codeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.textContent = `${{issue.file || 'Unknown'}}:${{issue.line || '?'}}`;
            
            let content = `
                <div class="issue-details">
                    <div class="detail-section">
                        <h4>Issue Information</h4>
                        <p><strong>Message:</strong> ${{escapeHtml(issue.message || 'No message')}}</p>
                        <p><strong>Severity:</strong> <span class="issue-severity ${{issue.severity || 'style'}}" style="background: ${{getSeverityColor(issue.severity)}}; color: white;">${{issue.severity || 'style'}}</span></p>
                        <p><strong>ID:</strong> ${{issue.id || 'unknown'}}</p>
                        <p><strong>Location:</strong> Line ${{issue.line || '?'}}, Column ${{issue.column || '?'}}</p>
                    </div>
            `;
            
            // Add code context if available
            // Check both new and old structure for code context
            const hasNewContext = issue.code_context && issue.code_context.lines;
            const hasOldContext = issue.context && issue.context.code_lines;
            
            if (hasNewContext || hasOldContext) {{
                content += `
                    <div class="detail-section">
                        <h4>Code Context</h4>
                        <div class="code-context">
                `;
                
                const lines = hasNewContext ? issue.code_context.lines : issue.context.code_lines;
                const isNewFormat = hasNewContext;
                
                lines.forEach(line => {{
                    const lineNum = isNewFormat ? line.number : line.line_number;
                    const isHighlighted = isNewFormat ? (line.is_target || lineNum === issue.line) : (lineNum === issue.line);
                    content += `
                        <div class="code-line ${{isHighlighted ? 'highlighted' : ''}}">
                            <span class="line-number">${{lineNum}}</span>
                            <span class="line-content">${{escapeHtml(line.content)}}</span>
                        </div>
                    `;
                }});
                
                content += `
                        </div>
                    </div>
                `;
            }}
            
            // Add quick fix if available
            const fix = getFixSuggestion(issue);
            if (fix) {{
                content += `
                    <div class="detail-section">
                        <h4>Quick Fix Suggestion</h4>
                        <p>${{fix.suggestion}}</p>
                        <code class="issue-code">${{escapeHtml(fix.template)}}</code>
                        <button class="action-btn fix-suggestion" onclick="copyToClipboard('${{escapeHtml(fix.template)}}')">
                            Copy Fix Template
                        </button>
                    </div>
                `;
            }}
            
            content += '</div>';
            
            modalBody.innerHTML = content;
            modal.classList.add('show');
            
            // Mark as viewed when opening details
            if (!state.viewed.has(issue.unique_id)) {{
                markAsViewed(issue);
            }}
        }}
        
        function closeModal() {{
            const modal = document.getElementById('codeModal');
            modal.classList.remove('show');
        }}
        
        // Click outside modal to close
        document.getElementById('codeModal').addEventListener('click', (e) => {{
            if (e.target.classList.contains('modal')) {{
                closeModal();
            }}
        }});
        
        // Filtering
        function getFilteredIssues() {{
            let filtered = state.issues;
            
            // Filter by severity
            if (state.currentFilter !== 'all') {{
                filtered = filtered.filter(issue => issue.severity === state.currentFilter);
            }}
            
            // Filter by search
            if (state.searchQuery) {{
                filtered = filtered.filter(issue => matchesSearch(issue, state.searchQuery));
            }}
            
            return filtered;
        }}
        
        function matchesSearch(issue, query) {{
            const parts = query.toLowerCase().split(' ');
            const issueText = `${{issue.message}} ${{issue.file}} ${{issue.id}}`.toLowerCase();
            
            return parts.every(part => {{
                // Check for severity filter
                if (['error', 'warning', 'style', 'performance'].includes(part)) {{
                    return issue.severity === part;
                }}
                
                // Check for file extension
                if (part.startsWith('.')) {{
                    return issue.file && issue.file.endsWith(part);
                }}
                
                // Check for file path
                if (part.includes('/')) {{
                    return issue.file && issue.file.includes(part);
                }}
                
                // General text search
                return issueText.includes(part);
            }});
        }}
        
        function filterBySeverity(severity) {{
            state.currentFilter = severity;
            
            // Update active button
            document.querySelectorAll('.stat-badge').forEach(badge => {{
                badge.classList.remove('active');
            }});
            
            if (severity === 'all') {{
                document.querySelector('.stat-badge.total').classList.add('active');
            }} else {{
                document.querySelector(`.stat-badge.${{severity}}`).classList.add('active');
            }}
            
            renderIssues();
            showToast(`Showing ${{severity === 'all' ? 'all issues' : severity + ' issues'}}`);
        }}
        
        function handleSearch(event) {{
            state.searchQuery = event.target.value;
            renderIssues();
        }}
        
        // Actions
        function markAsViewed(issue) {{
            if (!state.viewed.has(issue.unique_id)) {{
                state.viewed.add(issue.unique_id);
                saveState();
                updateProgress();
                renderIssues();
            }}
        }}
        
        function markAsFixed(issue) {{
            if (state.fixed.has(issue.unique_id)) {{
                state.fixed.delete(issue.unique_id);
            }} else {{
                state.fixed.add(issue.unique_id);
                state.viewed.add(issue.unique_id);
            }}
            saveState();
            updateProgress();
            renderIssues();
        }}
        
        function toggleFileGroup(file) {{
            if (state.expandedFiles.has(file)) {{
                state.expandedFiles.delete(file);
            }} else {{
                state.expandedFiles.add(file);
            }}
            saveState();
            renderIssues();
        }}
        
        function toggleGrouping() {{
            state.groupByFile = !state.groupByFile;
            saveState();
            renderIssues();
            showToast(state.groupByFile ? 'Grouping by file' : 'Flat view');
        }}
        
        // Progress tracking
        function updateProgress() {{
            const total = state.issues.length;
            const viewed = state.viewed.size;
            const fixed = state.fixed.size;
            
            document.getElementById('progressText').textContent = `${{viewed}} / ${{total}} issues reviewed`;
            document.getElementById('fixedCount').textContent = fixed;
            
            const percentage = total > 0 ? (viewed / total) * 100 : 0;
            document.getElementById('progressFill').style.width = `${{percentage}}%`;
        }}
        
        // Utilities
        function getSeverityColor(severity) {{
            const colors = {{
                error: '#dc3545',
                warning: '#f39c12',
                style: '#6f42c1',
                performance: '#198754',
                information: '#0dcaf0',
                portability: '#6c757d'
            }};
            return colors[severity] || '#6c757d';
        }}
        
        function getInlineCode(issue) {{
            // Check both new and old structure for compatibility
            const codeContext = issue.code_context;
            const oldContext = issue.context;
            
            let lines = null;
            let isNewFormat = false;
            
            if (codeContext && codeContext.lines) {{
                lines = codeContext.lines;
                isNewFormat = true;
            }} else if (oldContext && oldContext.code_lines) {{
                lines = oldContext.code_lines;
                isNewFormat = false;
            }}
            
            if (!lines) return [];
            
            const targetLine = issue.line;
            
            // Find the target line
            for (let i = 0; i < lines.length; i++) {{
                const lineNum = isNewFormat ? lines[i].number : lines[i].line_number;
                const isTarget = isNewFormat ? (lines[i].is_target || lineNum === targetLine) : (lineNum === targetLine);
                
                if (isTarget) {{
                    const result = [];
                    if (i > 0) result.push(lines[i-1]);
                    result.push(lines[i]);
                    if (i < lines.length - 1 && result.length < 2) {{
                        result.push(lines[i+1]);
                    }}
                    return result;
                }}
            }}
            
            return lines.slice(0, 2);
        }}
        
        function getFixSuggestion(issue) {{
            const message = (issue.message || '').toLowerCase();
            
            for (const [fixId, pattern] of Object.entries(fixPatterns)) {{
                if (message.includes(pattern.pattern)) {{
                    return {{
                        id: fixId,
                        suggestion: pattern.suggestion,
                        template: pattern.fix_template
                    }};
                }}
            }}
            
            return null;
        }}
        
        function showFixSuggestion(fix) {{
            showToast(`${{fix.suggestion}}: ${{fix.template}}`);
            copyToClipboard(fix.template);
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast('Copied to clipboard!');
            }}).catch(() => {{
                showToast('Failed to copy to clipboard');
            }});
        }}
        
        function showToast(message) {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 3000);
        }}
        
        function exportData() {{
            const exportData = {{
                issues: getFilteredIssues(),
                viewed: [...state.viewed],
                fixed: [...state.fixed],
                timestamp: new Date().toISOString()
            }};
            
            const blob = new Blob([JSON.stringify(exportData, null, 2)], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `code-analysis-export-${{Date.now()}}.json`;
            a.click();
            URL.revokeObjectURL(url);
            
            showToast('Data exported successfully');
        }}
        
        function showHelp() {{
            const helpText = `
Keyboard Shortcuts:
• / - Focus search
• Ctrl+1-5 - Filter by severity
• Esc - Close modal or unfocus search

Search Examples:
• "error in .h" - Errors in header files
• "warning controller" - Warnings with "controller"
• "style multiply" - Style issues with "multiply"
• ".cpp" - Issues in .cpp files

Actions:
• Click issue row - View full details and code context
• View button - Mark as viewed
• Fix button - Mark as fixed
• 💡 button - Copy quick fix template
            `;
            alert(helpText);
        }}
    </script>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Optimized dashboard generated: {output_file}")
        print(f"📊 Total issues: {self.stats['total']}")
        print(f"📁 Files with issues: {len(self.files_map)}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate-optimized-dashboard.py <input.json> <output.html>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    try:
        generator = OptimizedDashboardGenerator(input_file)
        generator.generate(output_file)
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()