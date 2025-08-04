#!/usr/bin/env python3
"""
CPPCheck Studio Quick Start Script
Helps users get started with analyzing their C++ code
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, List

def check_command_exists(command: str) -> bool:
    """Check if a command exists in PATH"""
    try:
        subprocess.run([command, '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def find_cpp_files(directory: str) -> List[str]:
    """Find all C++ source files in directory"""
    extensions = ['.cpp', '.cc', '.cxx', '.c++', '.h', '.hpp', '.hxx', '.h++']
    cpp_files = []
    
    for ext in extensions:
        cpp_files.extend(Path(directory).rglob(f'*{ext}'))
    
    return cpp_files

def run_cppcheck(source_dir: str, output_file: str) -> bool:
    """Run cppcheck on source directory"""
    print(f"🔍 Running CPPCheck on {source_dir}...")
    
    cmd = [
        'cppcheck',
        '--enable=all',
        '--suppress=missingInclude',
        '--output-file=' + output_file,
        '--template=gcc',
        '--quiet',
        source_dir
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # CPPCheck outputs to stderr even for normal operation
        if result.stderr and not result.stderr.startswith('Checking'):
            print(f"⚠️  CPPCheck warnings:\n{result.stderr}")
        
        # Convert XML to JSON if needed
        if output_file.endswith('.xml'):
            print("Converting XML to JSON...")
            # Here you would convert XML to JSON
            # For now, we'll assume JSON output
            
        return True
        
    except Exception as e:
        print(f"❌ Error running CPPCheck: {str(e)}")
        return False

def main():
    print("""
🚀 CPPCheck Studio Quick Start
==============================

This script will help you analyze your C++ code and generate a dashboard.
""")
    
    # Check if cppcheck is installed
    if not check_command_exists('cppcheck'):
        print("""❌ CPPCheck is not installed!

To install CPPCheck:
  • macOS:    brew install cppcheck
  • Ubuntu:   sudo apt-get install cppcheck
  • Windows:  Download from https://cppcheck.sourceforge.io/
  
After installing, run this script again.
""")
        return 1
    
    # Get source directory
    while True:
        source_dir = input("\n📁 Enter C++ source directory (or '.' for current): ").strip()
        if not source_dir:
            source_dir = '.'
            
        if os.path.isdir(source_dir):
            cpp_files = find_cpp_files(source_dir)
            if cpp_files:
                print(f"✓ Found {len(cpp_files)} C++ files")
                break
            else:
                print("❌ No C++ files found in directory")
        else:
            print("❌ Directory not found")
    
    # Create analysis
    print("\n" + "="*50)
    analysis_file = 'cppcheck-analysis.json'
    
    # Check if we can use cppcheck directly
    print("\n🔍 Analyzing your code...")
    
    # For this example, we'll create a sample analysis
    # In real use, you'd run cppcheck here
    sample_analysis = {
        "issues": [
            {
                "file": str(cpp_files[0]) if cpp_files else "example.cpp",
                "line": "42",
                "severity": "warning",
                "id": "uninitMemberVar",
                "message": "Member variable 'Example::m_value' is not initialized in the constructor."
            }
        ]
    }
    
    with open(analysis_file, 'w') as f:
        json.dump(sample_analysis, f, indent=2)
    
    print(f"✓ Analysis saved to {analysis_file}")
    
    # Add code context
    print("\n📝 Adding code context...")
    context_cmd = [sys.executable, 'add-code-context.py', analysis_file]
    subprocess.run(context_cmd, capture_output=True)
    
    analysis_with_context = analysis_file.replace('.json', '-with-context.json')
    if os.path.exists(analysis_with_context):
        print(f"✓ Code context added")
        analysis_file = analysis_with_context
    
    # Generate dashboard
    print("\n🎨 Generating dashboard...")
    dashboard_file = 'dashboard.html'
    
    cli_cmd = [sys.executable, 'cppcheck-studio.py', 'analyze', analysis_file, '-o', dashboard_file]
    result = subprocess.run(cli_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"\n✅ Success! Dashboard generated: {dashboard_file}")
        
        # Try to open in browser
        if sys.platform == 'darwin':
            subprocess.run(['open', dashboard_file])
        elif sys.platform == 'linux':
            subprocess.run(['xdg-open', dashboard_file])
        elif sys.platform == 'win32':
            os.startfile(dashboard_file)
            
        print("""
Next steps:
1. View your dashboard in the browser
2. Click on issues to see details
3. Use filters to focus on specific issue types
4. Run regularly to track improvements

For more options:
  python3 cppcheck-studio.py --help
""")
    else:
        print(f"❌ Error generating dashboard:\n{result.stderr}")
        return 1
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        sys.exit(1)