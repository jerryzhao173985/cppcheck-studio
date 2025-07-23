#!/usr/bin/env python3
"""Extract issue breakdown by severity from CPPCheck analysis JSON."""

import json
import sys

def extract_issue_breakdown(json_file):
    """Extract issue counts by severity type."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        issues = data.get('issues', [])
        
        # Count by severity
        severity_counts = {
            'error': 0,
            'warning': 0,
            'style': 0,
            'performance': 0,
            'portability': 0,
            'information': 0
        }
        
        for issue in issues:
            severity = issue.get('severity', 'unknown')
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        # Create breakdown in gallery-compatible format
        breakdown = {
            'total': len(issues),
            'error': severity_counts['error'],
            'warning': severity_counts['warning'],
            'style': severity_counts['style'],
            'performance': severity_counts['performance'],
            'portability': severity_counts['portability'],
            'information': severity_counts['information']
        }
        
        # Output as JSON
        print(json.dumps(breakdown))
        
    except Exception as e:
        # Return empty breakdown on error
        print(json.dumps({
            'total': 0,
            'error': 0,
            'warning': 0,
            'style': 0,
            'performance': 0,
            'portability': 0,
            'information': 0
        }))
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: extract-issue-breakdown.py <analysis.json>", file=sys.stderr)
        sys.exit(1)
    
    extract_issue_breakdown(sys.argv[1])