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
        # First check if file exists and has content
        file_size = Path(xml_file).stat().st_size
        print(f"Debug: XML file size is {file_size} bytes", file=sys.stderr)
        
        if file_size == 0:
            print("Warning: XML file is empty", file=sys.stderr)
            return {"issues": [], "metadata": {"empty_file": True}}
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Debug: print root element
        print(f"Debug: Root element is '{root.tag}'", file=sys.stderr)
        
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        # Try to read the file content for debugging
        try:
            with open(xml_file, 'r') as f:
                content = f.read()[:500]
                print(f"Debug: First 500 chars of XML: {content}", file=sys.stderr)
        except:
            pass
        return {"issues": [], "metadata": {"parse_error": str(e)}}
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return {"issues": [], "metadata": {"error": str(e)}}
    
    issues = []
    
    # Handle multiple cppcheck formats
    # Format 1: <results><error .../>...</results>
    # Format 2: <results><errors><error .../></errors></results>
    # Format 3: <results version="2"><cppcheck version="..."/><errors><error .../>
    
    # Find all error elements
    errors = root.findall('.//error')
    print(f"Debug: Found {len(errors)} error elements", file=sys.stderr)
    
    # Also check for empty results
    if len(errors) == 0:
        # Check if this is just an empty results file
        if root.tag == 'results' or root.tag == 'results':
            print("Info: No errors found in CPPCheck analysis (clean code!)", file=sys.stderr)
            return {"issues": [], "metadata": {"clean": True}}
    
    for error in errors:
        issue = {}
        
        # Get attributes
        issue['id'] = error.get('id', '')
        issue['severity'] = error.get('severity', 'unknown')
        issue['message'] = error.get('msg', '') or error.get('verbose', '')
        
        # Skip certain non-issues
        if issue['id'] in ['noValidConfiguration', 'toomanyconfigs', 'syntaxError']:
            print(f"Debug: Skipping {issue['id']}: {issue['message']}", file=sys.stderr)
            continue
            
        # Get location info - handle multiple location elements
        locations = error.findall('location')
        if locations:
            # Use the first location (primary)
            location = locations[0]
            issue['file'] = location.get('file', '')
            line = location.get('line', '0')
            issue['line'] = int(line) if line.isdigit() else 0
            
            # Add additional locations if present
            if len(locations) > 1:
                issue['additional_locations'] = []
                for loc in locations[1:]:
                    issue['additional_locations'].append({
                        'file': loc.get('file', ''),
                        'line': int(loc.get('line', '0')) if loc.get('line', '0').isdigit() else 0
                    })
        else:
            # Try to get from error attributes (old format)
            issue['file'] = error.get('file', '')
            line = error.get('line', '0')
            issue['line'] = int(line) if line.isdigit() else 0
        
        # Only add if we have meaningful data
        if issue['message'] and (issue['file'] or issue['id']):
            issues.append(issue)
    
    # Add metadata about the analysis
    metadata = {
        "total_errors_in_xml": len(errors),
        "valid_issues": len(issues),
        "cppcheck_version": root.find('.//cppcheck[@version]').get('version', 'unknown') if root.find('.//cppcheck[@version]') is not None else 'unknown'
    }
    
    print(f"Info: Converted {len(issues)} valid issues from {len(errors)} total errors", file=sys.stderr)
    
    return {"issues": issues, "metadata": metadata}

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