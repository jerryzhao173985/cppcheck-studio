#!/usr/bin/env python3
"""
Validate GitHub Actions workflow YAML files
"""

import yaml
import sys
import re

def validate_workflow(file_path):
    """Validate a GitHub Actions workflow file."""
    print(f"Validating {file_path}...")
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Parse YAML
        workflow = yaml.safe_load(content)
        
        print("✅ YAML syntax is valid")
        
        # Check for common issues
        issues = []
        
        # Check for remaining ${{ env.VAR }} references in shell scripts
        env_refs = re.findall(r'\$\{\{\s*env\.[A-Z_]+\s*\}\}', content)
        if env_refs:
            # Filter out valid uses (in if conditions, etc.)
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if '${{ env.' in line and not line.strip().startswith('if:') and 'run:' not in line:
                    # Check if it's inside a run block
                    if i > 5:
                        context = '\n'.join(lines[i-5:i])
                        if 'run: |' in context:
                            issues.append(f"Line {i}: Found ${{ env.VAR }} in shell script - should use ${'{'}VAR{'}'}")
        
        # Check heredocs are properly indented
        heredoc_pattern = r'cat\s*>\s*.*\s*<<\s*[\'"]?\w+[\'"]?'
        for match in re.finditer(heredoc_pattern, content):
            start_pos = match.start()
            line_num = content[:start_pos].count('\n') + 1
            # Get the line and check indentation
            line_start = content.rfind('\n', 0, start_pos) + 1
            line = content[line_start:content.find('\n', start_pos)]
            if line.startswith('        '):  # Should have at least 8 spaces
                # Check the next line has proper indentation
                next_line_start = content.find('\n', start_pos) + 1
                next_line = content[next_line_start:content.find('\n', next_line_start)]
                if next_line and not next_line.startswith('          '):  # Should have at least 10 spaces
                    issues.append(f"Line {line_num + 1}: Heredoc content not properly indented")
        
        # Report issues
        if issues:
            print("\n⚠️  Found potential issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✅ No common issues found")
            
        # Check workflow structure
        if 'jobs' in workflow:
            print(f"✅ Found {len(workflow['jobs'])} job(s)")
            for job_name, job in workflow['jobs'].items():
                if 'steps' in job:
                    print(f"  - Job '{job_name}' has {len(job['steps'])} steps")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            print(f"   Error at line {mark.line + 1}, column {mark.column + 1}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else ".github/workflows/analyze-on-demand.yml"
    sys.exit(0 if validate_workflow(file_path) else 1)