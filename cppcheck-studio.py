#!/usr/bin/env python3
"""
CPPCheck Studio - Unified CLI for C++ Static Analysis Dashboard Generation

Transform CPPCheck JSON output into beautiful, interactive HTML dashboards.
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import os

VERSION = "2.0.0"

class Colors:
    """Terminal color codes for pretty output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_color(message: str, color: str = Colors.ENDC) -> None:
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.ENDC}")

def validate_json_file(filepath: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Validate CPPCheck JSON file
    
    Returns:
        Tuple of (is_valid, error_message, data)
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return False, f"File not found: {filepath}", None
            
        if not path.is_file():
            return False, f"Not a file: {filepath}", None
            
        with open(path, 'r') as f:
            data = json.load(f)
            
        # Check if it's a valid CPPCheck format
        if not isinstance(data, dict):
            return False, "Invalid format: Expected JSON object", None
            
        if 'issues' not in data:
            # Try wrapping array in issues key for compatibility
            if isinstance(data, list):
                data = {'issues': data}
            else:
                return False, "Invalid format: Missing 'issues' key", None
                
        issue_count = len(data.get('issues', []))
        return True, None, data
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}", None
    except Exception as e:
        return False, f"Error reading file: {str(e)}", None

def analyze_issues(data: Dict) -> Dict[str, int]:
    """Analyze issues and return statistics"""
    issues = data.get('issues', [])
    stats = {
        'total': len(issues),
        'error': 0,
        'warning': 0,
        'style': 0,
        'performance': 0,
        'portability': 0,
        'information': 0,
        'with_context': 0
    }
    
    for issue in issues:
        severity = issue.get('severity', 'unknown').lower()
        if severity in stats:
            stats[severity] += 1
        if 'code_context' in issue:
            stats['with_context'] += 1
            
    return stats

def run_generator(generator_script: str, input_file: str, output_file: str) -> bool:
    """Run a Python generator script"""
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        generator_path = script_dir / generator_script
        
        if not generator_path.exists():
            print_color(f"Error: Generator not found: {generator_path}", Colors.RED)
            return False
            
        cmd = [sys.executable, str(generator_path), input_file, output_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print_color(f"Error: {result.stderr}", Colors.RED)
            return False
            
        return True
    except Exception as e:
        print_color(f"Error running generator: {str(e)}", Colors.RED)
        return False

def main():
    parser = argparse.ArgumentParser(
        description='CPPCheck Studio - Transform C++ static analysis into interactive dashboards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze analysis.json                    # Generate dashboard (uses recommended virtual scroll)
  %(prog)s analyze analysis.json -o report.html    # Specify output file
  %(prog)s analyze analysis.json --minimal          # Generate minimal dashboard without code
  
  %(prog)s add-context analysis.json               # Add code context to analysis file
  %(prog)s stats analysis.json                     # Show analysis statistics
  %(prog)s validate analysis.json                  # Validate JSON format

For more information, visit: https://github.com/yourusername/cppcheck-studio
        """
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Generate dashboard from analysis JSON')
    analyze_parser.add_argument('input', help='CPPCheck JSON analysis file')
    analyze_parser.add_argument('-o', '--output', help='Output HTML file (default: dashboard.html)')
    analyze_parser.add_argument('--minimal', action='store_true', help='Generate minimal dashboard without code context (not recommended)')
    analyze_parser.add_argument('--force', action='store_true', help='Overwrite existing output file')
    
    # Add context command
    context_parser = subparsers.add_parser('add-context', help='Add code context to analysis file')
    context_parser.add_argument('input', help='CPPCheck JSON analysis file')
    context_parser.add_argument('-o', '--output', help='Output file (default: <input>-with-context.json)')
    context_parser.add_argument('--lines', type=int, default=3, help='Context lines before/after (default: 3)')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show analysis statistics')
    stats_parser.add_argument('input', help='CPPCheck JSON analysis file')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate JSON format')
    validate_parser.add_argument('input', help='CPPCheck JSON analysis file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Print header
    print_color(f"\n🔧 CPPCheck Studio v{VERSION}", Colors.BOLD)
    print_color("=" * 50, Colors.BLUE)
    
    if args.command == 'validate':
        is_valid, error, data = validate_json_file(args.input)
        if is_valid:
            stats = analyze_issues(data)
            print_color(f"✓ Valid CPPCheck JSON file", Colors.GREEN)
            print_color(f"  Total issues: {stats['total']}", Colors.GREEN)
        else:
            print_color(f"✗ Invalid file: {error}", Colors.RED)
            return 1
            
    elif args.command == 'stats':
        is_valid, error, data = validate_json_file(args.input)
        if not is_valid:
            print_color(f"Error: {error}", Colors.RED)
            return 1
            
        stats = analyze_issues(data)
        print_color("\n📊 Analysis Statistics", Colors.BOLD)
        print(f"  Total Issues: {stats['total']}")
        print(f"  - Errors:      {stats['error']} ({stats['error']/max(stats['total'],1)*100:.1f}%)")
        print(f"  - Warnings:    {stats['warning']} ({stats['warning']/max(stats['total'],1)*100:.1f}%)")
        print(f"  - Style:       {stats['style']} ({stats['style']/max(stats['total'],1)*100:.1f}%)")
        print(f"  - Performance: {stats['performance']} ({stats['performance']/max(stats['total'],1)*100:.1f}%)")
        print(f"  - With Code:   {stats['with_context']} ({stats['with_context']/max(stats['total'],1)*100:.1f}%)")
        
    elif args.command == 'add-context':
        output_file = args.output or args.input.replace('.json', '-with-context.json')
        
        print_color(f"Adding code context to {Path(args.input).name}...", Colors.BLUE)
        
        # Run add-code-context.py
        if run_generator('add-code-context.py', args.input, output_file):
            print_color(f"✓ Code context added successfully!", Colors.GREEN)
            print_color(f"  Output: {output_file}", Colors.GREEN)
        else:
            return 1
            
    elif args.command == 'analyze':
        # Validate input
        is_valid, error, data = validate_json_file(args.input)
        if not is_valid:
            print_color(f"Error: {error}", Colors.RED)
            return 1
            
        stats = analyze_issues(data)
        output_file = args.output or 'dashboard.html'
        
        # Check if output exists
        if Path(output_file).exists() and not args.force:
            print_color(f"Output file already exists: {output_file}", Colors.YELLOW)
            print_color("Use --force to overwrite", Colors.YELLOW)
            return 1
            
        # Select appropriate generator
        # Virtual scroll dashboard is the recommended default - it has the most features
        if args.minimal:
            generator = 'generate/generate-production-dashboard.py'
            generator_name = 'Minimal Dashboard'
        else:
            # Always use virtual scroll by default - it's the best implementation
            generator = 'generate/generate-standalone-virtual-dashboard.py'
            generator_name = 'Virtual Scroll Dashboard (Recommended)'
            
        print_color(f"\n📈 Generating {generator_name}", Colors.BOLD)
        print_color(f"  Input:  {args.input} ({stats['total']} issues)", Colors.BLUE)
        print_color(f"  Output: {output_file}", Colors.BLUE)
        
        start_time = time.time()
        
        if run_generator(generator, args.input, output_file):
            elapsed = time.time() - start_time
            file_size = Path(output_file).stat().st_size / 1024 / 1024  # MB
            
            print_color(f"\n✓ Dashboard generated successfully!", Colors.GREEN)
            print_color(f"  Time:     {elapsed:.2f}s", Colors.GREEN)
            print_color(f"  Size:     {file_size:.2f} MB", Colors.GREEN)
            print_color(f"  Location: {Path(output_file).absolute()}", Colors.GREEN)
            
            # Try to open in browser
            if sys.platform == 'darwin':
                subprocess.run(['open', output_file], capture_output=True)
            elif sys.platform == 'linux':
                subprocess.run(['xdg-open', output_file], capture_output=True)
        else:
            return 1
    
    print()
    return 0

if __name__ == '__main__':
    sys.exit(main())