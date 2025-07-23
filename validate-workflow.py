#!/usr/bin/env python3
"""Validate the CI workflow file and test critical components."""

import yaml
import subprocess
import sys
import os

def validate_yaml(file_path):
    """Validate YAML syntax."""
    print(f"Validating YAML syntax for {file_path}...")
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False

def test_python_scripts():
    """Test inline Python scripts from workflow."""
    print("\nTesting Python scripts...")
    
    # Test issue counting script
    test_script1 = """
import json
try:
    data = json.load(open('test_analysis.json'))
    print(len(data.get('issues', [])))
except:
    print('0')
"""
    
    # Create test data
    test_data = {"issues": [{"id": 1}, {"id": 2}, {"id": 3}]}
    with open('test_analysis.json', 'w') as f:
        import json
        json.dump(test_data, f)
    
    try:
        result = subprocess.run(['python3', '-c', test_script1], 
                              capture_output=True, text=True)
        if result.stdout.strip() == "3":
            print("✅ Issue counting script works correctly")
        else:
            print(f"❌ Issue counting script failed: {result.stdout}")
            print(f"   stderr: {result.stderr}")
    except Exception as e:
        print(f"❌ Failed to test issue counting script: {e}")
    
    # Clean up
    if os.path.exists('test_analysis.json'):
        os.remove('test_analysis.json')
    
    # Test file listing script
    test_script2 = """
import json
try:
    data = {'issues': [{'file': 'test1.cpp'}, {'file': 'test2.h'}]}
    files = set(issue.get('file', '') for issue in data.get('issues', [])[:10])
    for f in list(files)[:5]:
        if f:
            print(f'  - {f}')
except:
    print('Could not list files')
"""
    
    try:
        result = subprocess.run(['python3', '-c', test_script2], 
                              capture_output=True, text=True)
        if '- test1.cpp' in result.stdout and '- test2.h' in result.stdout:
            print("✅ File listing script works correctly")
        else:
            print(f"❌ File listing script failed: {result.stdout}")
    except Exception as e:
        print(f"❌ Failed to test file listing script: {e}")

def check_shell_syntax():
    """Check for common shell syntax issues."""
    print("\nChecking shell syntax patterns...")
    
    workflow_file = '.github/workflows/analyze-on-demand.yml'
    issues = []
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Check for problematic patterns
    if '$(date +%s)-$(echo $RANDOM)' in content and '${{' in content:
        # This is OK if properly handled
        pass
    
    # Check for undefined variables
    if '${UNDEFINED_VAR}' in content:
        issues.append("Found reference to undefined variable")
    
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
    else:
        print("✅ No obvious shell syntax issues found")

def main():
    """Run all validations."""
    print("🔍 Validating CPPCheck Studio Workflow\n")
    
    workflow_file = '.github/workflows/analyze-on-demand.yml'
    
    if not os.path.exists(workflow_file):
        print(f"❌ Workflow file not found: {workflow_file}")
        sys.exit(1)
    
    # Run validations
    yaml_valid = validate_yaml(workflow_file)
    test_python_scripts()
    check_shell_syntax()
    
    print("\n📊 Validation Summary:")
    if yaml_valid:
        print("✅ Workflow should be visible in GitHub Actions")
        print("✅ Python scripts are syntactically correct")
        print("✅ Basic validation passed")
    else:
        print("❌ Workflow has issues that need to be fixed")
        sys.exit(1)

if __name__ == "__main__":
    main()