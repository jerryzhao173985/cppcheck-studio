#!/usr/bin/env python3
"""
Add code context to existing cppcheck analysis JSON
Reads actual source files to provide context around issues
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

def print_progress(current: int, total: int, prefix: str = "Progress") -> None:
    """Print progress bar"""
    if total == 0:
        return
    percent = current / total * 100
    bar_length = 40
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    sys.stdout.write(f'\r{prefix}: |{bar}| {percent:.1f}% ({current}/{total})')
    sys.stdout.flush()
    if current == total:
        print()  # New line when complete

def extract_code_context(file_path: str, line_number: int, context_lines: int = 5) -> Optional[Dict[str, Any]]:
    """
    Extract code context around a specific line
    
    Args:
        file_path: Path to source file
        line_number: Target line number (1-based)
        context_lines: Number of lines before/after to include
        
    Returns:
        Dictionary with code context or None if error
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None
            
        # Try multiple encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']
        lines = None
        
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                break
            except UnicodeDecodeError:
                continue
                
        if lines is None:
            return None
        
        # Calculate line range
        total_lines = len(lines)
        if line_number > total_lines or line_number < 1:
            return None
            
        start = max(0, line_number - context_lines - 1)
        end = min(total_lines, line_number + context_lines)
        
        # Extract lines with metadata
        context = {
            'lines': [],
            'file': str(path),
            'total_lines': total_lines
        }
        
        for i in range(start, end):
            context['lines'].append({
                'number': i + 1,
                'content': lines[i].rstrip('\n\r'),
                'is_target': (i + 1) == line_number
            })
        
        return context
        
    except Exception as e:
        # Silently skip files that can't be read
        return None

def validate_analysis_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Validate and load analysis JSON file"""
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"❌ Error: File not found: {file_path}")
            return None
            
        with open(path, 'r') as f:
            data = json.load(f)
            
        # Handle both array and object formats
        if isinstance(data, list):
            data = {'issues': data}
        elif not isinstance(data, dict) or 'issues' not in data:
            print(f"❌ Error: Invalid JSON format. Expected 'issues' array.")
            return None
            
        return data
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON file: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        return None

def add_code_context_to_analysis(
    input_file: str, 
    output_file: str, 
    context_lines: int = 5,
    verbose: bool = False
) -> bool:
    """
    Add code context to all issues in the analysis
    
    Returns:
        True if successful, False otherwise
    """
    # Load and validate input
    data = validate_analysis_file(input_file)
    if not data:
        return False
    
    issues = data.get('issues', [])
    if not issues:
        print("⚠️  No issues found in analysis file")
        return True
        
    print(f"📂 Processing {len(issues)} issues from {Path(input_file).name}")
    
    # Track statistics
    processed = 0
    skipped_no_file = 0
    skipped_no_line = 0
    unique_files = set()
    start_time = time.time()
    
    # Process each issue
    for idx, issue in enumerate(issues):
        print_progress(idx + 1, len(issues), "Processing")
        
        file_path = issue.get('file', '')
        line_str = str(issue.get('line', '0'))
        
        # Skip if already has context
        if 'code_context' in issue:
            processed += 1
            continue
        
        try:
            line_number = int(line_str)
        except (ValueError, TypeError):
            line_number = 0
        
        if not file_path:
            skipped_no_file += 1
            continue
            
        if line_number <= 0:
            skipped_no_line += 1
            continue
            
        # Try to extract context
        context = extract_code_context(file_path, line_number, context_lines)
        if context:
            issue['code_context'] = context
            processed += 1
            unique_files.add(file_path)
        else:
            skipped_no_file += 1
            if verbose:
                print(f"\n⚠️  Could not read: {file_path}")
    
    # Save enhanced analysis
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"\n❌ Error writing output file: {str(e)}")
        return False
    
    # Print summary
    elapsed = time.time() - start_time
    success_rate = (processed / len(issues) * 100) if issues else 0
    
    print(f"\n✅ Code context added successfully!")
    print(f"   Processed: {processed}/{len(issues)} issues ({success_rate:.1f}%)")
    print(f"   Files accessed: {len(unique_files)}")
    if skipped_no_file > 0:
        print(f"   Skipped (file not found): {skipped_no_file}")
    if skipped_no_line > 0:
        print(f"   Skipped (no line number): {skipped_no_line}")
    print(f"   Time: {elapsed:.2f}s")
    print(f"   Output: {output_path.absolute()}")
    
    # Check output file size
    file_size = output_path.stat().st_size / 1024 / 1024  # MB
    if file_size > 10:
        print(f"   ⚠️  Large file: {file_size:.1f} MB (consider using virtual scroll dashboard)")
    
    return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Add code context to CPPCheck analysis JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analysis.json                           # Add context, output to analysis-with-context.json
  %(prog)s analysis.json output.json               # Specify output file
  %(prog)s analysis.json --lines 10               # Include 10 lines before/after
  %(prog)s analysis.json -v                       # Verbose mode

Notes:
  - Automatically handles different file encodings
  - Skips files that cannot be read
  - Shows progress bar for large analyses
        """
    )
    
    parser.add_argument('input_file', help='Input JSON file from cppcheck analysis')
    parser.add_argument('output_file', nargs='?', 
                       help='Output JSON file (default: <input>-with-context.json)')
    parser.add_argument('--lines', '-l', type=int, default=5,
                       help='Context lines before/after (default: 5)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show verbose output')
    
    args = parser.parse_args()
    
    # Determine output file
    if not args.output_file:
        input_path = Path(args.input_file)
        args.output_file = str(input_path.parent / f"{input_path.stem}-with-context.json")
    
    # Process
    success = add_code_context_to_analysis(
        args.input_file, 
        args.output_file, 
        args.lines,
        args.verbose
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()