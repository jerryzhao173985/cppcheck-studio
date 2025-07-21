#!/usr/bin/env python3
"""Verify code context is properly embedded in the dashboard"""

import re
import json

# Read the dashboard file
with open('FINAL_WORKING_DASHBOARD_WITH_CODE.html', 'r') as f:
    content = f.read()

# Extract the embedded issues data
match = re.search(r'const issuesData = (\[.*?\]);', content, re.DOTALL)
if match:
    issues_json = match.group(1)
    # Parse the JSON
    try:
        issues = json.loads(issues_json)
        
        # Count issues with code context
        with_context = sum(1 for issue in issues if issue.get('code_context'))
        without_context = sum(1 for issue in issues if not issue.get('code_context'))
        
        print(f"✅ Dashboard Analysis:")
        print(f"   Total issues embedded: {len(issues)}")
        print(f"   Issues WITH code context: {with_context}")
        print(f"   Issues WITHOUT code context: {without_context}")
        
        # Show a sample issue with code context
        for i, issue in enumerate(issues[:10]):
            if issue.get('code_context'):
                print(f"\n📝 Sample issue with code context (index {i}):")
                print(f"   File: {issue['file']}")
                print(f"   Line: {issue['location']['line']}")
                print(f"   Severity: {issue['severity']}")
                print(f"   Message: {issue['message'][:80]}...")
                print(f"   Code context lines: {len(issue['code_context']['lines'])}")
                print(f"   Target line: {issue['code_context']['target_line']}")
                break
                
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse embedded JSON: {e}")
else:
    print("❌ Could not find embedded issues data in dashboard")