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

def add_code_context_to_analysis(input_file, output_file):
    """Add code context to all issues in the analysis"""
    
    # Load existing analysis
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    issues = data.get('issues', [])
    
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
            context = extract_code_context(file_path, line_number)
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
    
    print(f"✅ Code context added to {processed} issues")
    print(f"⚠️  Skipped {skipped} issues (file not found or invalid line)")
    print(f"📄 Enhanced analysis saved to: {output_file}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: add-code-context.py <analysis.json> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'analysis-with-context.json'
    
    add_code_context_to_analysis(input_file, output_file)