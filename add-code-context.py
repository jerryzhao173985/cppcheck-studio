#!/usr/bin/env python3
"""
Add code context to existing cppcheck analysis JSON
Reads actual source files to provide context around issues
"""

import json
import os
from pathlib import Path

def extract_code_context(file_path, line_number, context_lines=5):
    """Extract code context around a specific line"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Calculate line range
        total_lines = len(lines)
        start = max(0, line_number - context_lines - 1)
        end = min(total_lines, line_number + context_lines)
        
        # Extract lines with metadata
        context = {
            'lines': []
        }
        
        for i in range(start, end):
            context['lines'].append({
                'number': i + 1,
                'content': lines[i].rstrip('\n'),
                'is_target': (i + 1) == line_number
            })
        
        return context
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def add_code_context_to_analysis(input_file, output_file, context_lines=5):
    """Add code context to all issues in the analysis"""
    
    # Load existing analysis
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    issues = data.get('issues', [])
    
    print(f"📂 Processing {len(issues)} issues...")
    
    # Process each issue
    processed = 0
    skipped = 0
    
    for issue in issues:
        file_path = issue.get('file', '')
        line_str = issue.get('line', '0')
        
        try:
            line_number = int(line_str)
        except:
            line_number = 0
        
        if file_path and line_number > 0 and os.path.exists(file_path):
            context = extract_code_context(file_path, line_number, context_lines)
            if context:
                issue['code_context'] = context
                processed += 1
            else:
                skipped += 1
        else:
            skipped += 1
    
    # Save enhanced analysis
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    success_rate = (processed / len(issues) * 100) if issues else 0
    print(f"✅ Successfully added code context to {processed} issues ({success_rate:.1f}%)")
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} issues (line 0 or file not found)")
    print(f"💾 Output written to {output_file}")

if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Add code context to cppcheck analysis JSON')
    parser.add_argument('input_file', help='Input JSON file from cppcheck analysis')
    parser.add_argument('output_file', nargs='?', default='analysis-with-context.json',
                       help='Output JSON file with code context (default: analysis-with-context.json)')
    parser.add_argument('--lines', type=int, default=5,
                       help='Number of context lines before and after the issue (default: 5)')
    
    args = parser.parse_args()
    
    add_code_context_to_analysis(args.input_file, args.output_file, args.lines)