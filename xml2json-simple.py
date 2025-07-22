#!/usr/bin/env python3
"""
Simple XML to JSON converter for CPPCheck results
Works without lxml dependency using built-in xml.etree
"""

import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_cppcheck_xml(xml_file):
    """Parse CPPCheck XML output and convert to JSON format"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        return {"issues": []}
    
    issues = []
    
    # Handle both cppcheck formats
    # Format 1: <results><error .../>...</results>
    # Format 2: <results><errors><error .../></errors></results>
    
    # Find all error elements
    errors = root.findall('.//error')
    
    for error in errors:
        issue = {}
        
        # Get attributes
        issue['id'] = error.get('id', '')
        issue['severity'] = error.get('severity', 'unknown')
        issue['message'] = error.get('msg', '') or error.get('verbose', '')
        
        # Get location info
        location = error.find('location')
        if location is not None:
            issue['file'] = location.get('file', '')
            line = location.get('line', '0')
            issue['line'] = int(line) if line.isdigit() else 0
        else:
            # Try to get from error attributes
            issue['file'] = error.get('file', '')
            line = error.get('line', '0')
            issue['line'] = int(line) if line.isdigit() else 0
        
        # Only add if we have meaningful data
        if issue['message'] and (issue['file'] or issue['id']):
            issues.append(issue)
    
    return {"issues": issues}

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 xml2json-simple.py <cppcheck-results.xml>", file=sys.stderr)
        sys.exit(1)
    
    xml_file = sys.argv[1]
    if not Path(xml_file).exists():
        print(f"Error: File '{xml_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Parse and convert
    result = parse_cppcheck_xml(xml_file)
    
    # Output JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()