#!/usr/bin/env python3
"""Generate a detailed Markdown report of CPPCheck analysis results."""

import json
import sys
from collections import defaultdict

def generate_report(json_file):
    """Generate a detailed Markdown report."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        issues = data.get('issues', [])
        if not issues:
            print("# Analysis Report\n\nNo issues found!")
            return
        
        # Group by severity
        by_severity = defaultdict(list)
        for issue in issues:
            by_severity[issue['severity']].append(issue)
        
        # Print report
        print("# CPPCheck Analysis Report")
        print(f"\nTotal Issues: **{len(issues)}**\n")
        
        # Summary table
        print("## Summary")
        print("| Severity | Count |")
        print("|----------|-------|")
        for severity in ['error', 'warning', 'style', 'performance', 'portability', 'information']:
            if severity in by_severity:
                print(f"| {severity.capitalize()} | {len(by_severity[severity])} |")
        
        # Detailed issues by severity
        for severity in ['error', 'warning', 'style', 'performance', 'portability', 'information']:
            if severity not in by_severity:
                continue
                
            print(f"\n## {severity.capitalize()} Issues ({len(by_severity[severity])})")
            
            for issue in by_severity[severity][:20]:  # Limit to 20 per category
                file_location = f"{issue.get('file', 'unknown')}:{issue.get('line', '?')}"
                print(f"\n### `{issue['id']}` - {file_location}")
                print(f"\n{issue['message']}")
                
                # Add code context if available
                if 'codeContext' in issue:
                    context = issue['codeContext']
                    print("\n```cpp")
                    if 'beforeLines' in context:
                        for line in context['beforeLines'][-2:]:
                            print(line)
                    if 'lineContent' in context:
                        print(f">>> {context['lineContent']}  // Line {context.get('lineNumber', '?')}")
                    if 'afterLines' in context:
                        for line in context['afterLines'][:2]:
                            print(line)
                    print("```")
            
            if len(by_severity[severity]) > 20:
                print(f"\n*... and {len(by_severity[severity]) - 20} more {severity} issues*")
        
    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate-detailed-report.py <analysis.json>")
        sys.exit(1)
    
    generate_report(sys.argv[1])