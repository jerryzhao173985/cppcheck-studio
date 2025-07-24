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

def add_code_context_to_analysis(input_file, output_file, context_lines=5, base_path=None):
    """Add code context to all issues in the analysis"""
    
    # Load existing analysis
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    issues = data.get('issues', [])
    
    print(f"📂 Processing {len(issues)} issues...")
    
    # Determine base path if not provided
    if base_path is None:
        # Check if we're in a subdirectory of the repository
        base_path = os.getcwd()
    
    print(f"📁 Base path for files: {base_path}")
    
    # Process each issue
    processed = 0
    skipped = 0
    file_not_found = 0
    
    for issue in issues:
        file_path = issue.get('file', '')
        line_str = issue.get('line', '0')
        
        try:
            line_number = int(line_str) if isinstance(line_str, str) else line_str
        except:
            line_number = 0
        
        if file_path and line_number > 0:
            # Try multiple path resolutions
            possible_paths = [
                file_path,  # Original path
                os.path.join(base_path, file_path),  # Path relative to base
            ]
            
            # Safely remove leading ./ or /
            if file_path.startswith('./'):
                possible_paths.append(os.path.join(base_path, file_path[2:]))
            elif file_path.startswith('/') and not os.path.isabs(file_path):
                # Only strip leading / if it's not an absolute path
                possible_paths.append(os.path.join(base_path, file_path[1:]))
            
            # Also try removing common prefixes
            if file_path.startswith('target-repo/'):
                possible_paths.append(file_path[len('target-repo/'):])
                possible_paths.append(os.path.join(base_path, file_path[len('target-repo/'):]))
            
            found_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    found_path = path
                    break
            
            if found_path:
                context = extract_code_context(found_path, line_number, context_lines)
                if context:
                    issue['code_context'] = context
                    processed += 1
                else:
                    skipped += 1
                    print(f"⚠️  Could not extract context from {found_path}:{line_number}")
            else:
                file_not_found += 1
                if file_not_found <= 5:  # Only print first 5 to avoid spam
                    print(f"❌ File not found: {file_path}")
                    print(f"   Tried paths: {possible_paths[:2]}")
        else:
            skipped += 1
            if line_number == 0:
                print(f"⚠️  Skipped issue with line 0: {file_path}")
    
    # Save enhanced analysis
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    success_rate = (processed / len(issues) * 100) if issues else 0
    print(f"\n📊 Summary:")
    print(f"✅ Successfully added code context to {processed} issues ({success_rate:.1f}%)")
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} issues (line 0 or extraction failed)")
    if file_not_found > 0:
        print(f"❌ Could not find {file_not_found} files")
        if file_not_found > 5:
            print(f"   (showing first 5 only)")
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
    parser.add_argument('--base-path', type=str, default=None,
                       help='Base path where source files are located (default: current directory)')
    
    args = parser.parse_args()
    
    add_code_context_to_analysis(args.input_file, args.output_file, args.lines, args.base_path)