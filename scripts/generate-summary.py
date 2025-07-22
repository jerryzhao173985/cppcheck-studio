#!/usr/bin/env python3
"""Generate a summary of CPPCheck analysis results."""

import json
import sys
from collections import Counter

def generate_summary(json_file):
    """Generate a text summary of the analysis results."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        issues = data.get('issues', [])
        if not issues:
            print("No issues found!")
            return
        
        # Count by severity
        severity_counts = Counter(issue['severity'] for issue in issues)
        
        # Count by type
        type_counts = Counter(issue['id'] for issue in issues)
        
        # Print summary
        print(f"Total Issues: {len(issues)}")
        print("\nBy Severity:")
        for severity in ['error', 'warning', 'style', 'performance', 'portability', 'information']:
            count = severity_counts.get(severity, 0)
            if count > 0:
                print(f"  {severity.capitalize()}: {count}")
        
        print(f"\nTop 10 Issue Types:")
        for issue_type, count in type_counts.most_common(10):
            print(f"  {issue_type}: {count}")
        
        # Files with most issues
        file_counts = Counter(issue['file'] for issue in issues if 'file' in issue)
        print(f"\nTop 5 Files with Issues:")
        for file_path, count in file_counts.most_common(5):
            print(f"  {file_path}: {count} issues")
        
    except Exception as e:
        print(f"Error generating summary: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate-summary.py <analysis.json>")
        sys.exit(1)
    
    generate_summary(sys.argv[1])