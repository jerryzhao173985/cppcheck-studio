#!/usr/bin/env python3
import json
import sys
from collections import defaultdict

def generate_report(json_file):
    with open(json_file) as f:
        data = json.load(f)
        issues = data.get('issues', [])
        
        # Statistics
        by_severity = defaultdict(int)
        by_file = defaultdict(int)
        by_id = defaultdict(int)
        
        for issue in issues:
            by_severity[issue.get('severity', 'unknown')] += 1
            by_file[issue.get('file', 'unknown')] += 1
            by_id[issue.get('id', 'unknown')] += 1
        
        # Report
        print('# LPZRobots CPPCheck Analysis Report')
        print()
        print(f'**Total Issues:** {len(issues)}')
        if data.get('truncated'):
            print(f'**Note:** Results truncated from {data.get("original_count", "?")} to {len(issues)} issues')
        print()
        
        print('## Issues by Severity')
        for sev in ['error', 'warning', 'performance', 'style', 'information']:
            if sev in by_severity:
                print(f'- **{sev.capitalize()}:** {by_severity[sev]}')
        print()
        
        print('## Top 10 Files with Most Issues')
        for file, count in sorted(by_file.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f'- {file}: {count} issues')
        print()
        
        print('## Top 10 Issue Types')
        for issue_id, count in sorted(by_id.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f'- {issue_id}: {count} occurrences')
        print()
        
        print('## Components Analyzed')
        components = set()
        for issue in issues:
            file = issue.get('file', '')
            if '/' in file:
                components.add(file.split('/')[0])
        for comp in sorted(components):
            comp_issues = sum(1 for i in issues if i.get('file', '').startswith(comp + '/'))
            print(f'- **{comp}:** {comp_issues} issues')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_report(sys.argv[1])
    else:
        generate_report('analysis.json')