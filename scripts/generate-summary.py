#!/usr/bin/env python3
import json
import sys

def generate_summary(json_file):
    with open(json_file) as f:
        data = json.load(f)
        issues = data.get('issues', [])
        by_severity = {}
        for issue in issues:
            sev = issue.get('severity', 'unknown')
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        print(f'Total issues: {len(issues)}')
        for sev, count in sorted(by_severity.items()):
            print(f'  {sev}: {count}')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_summary(sys.argv[1])
    else:
        generate_summary('analysis.json')