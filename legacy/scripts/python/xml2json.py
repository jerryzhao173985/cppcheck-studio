#!/usr/bin/env python3
"""
Convert CPPCheck XML output to JSON format
"""

import xml.etree.ElementTree as ET
import json
import sys
from pathlib import Path

def convert_xml_to_json(xml_file, json_file):
    """Convert cppcheck XML to JSON format"""
    
    try:
        # Parse XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        issues = []
        
        # Find all errors
        for error in root.findall('.//error'):
            # Get basic attributes
            severity = error.get('severity', 'style')
            msg = error.get('msg', '')
            error_id = error.get('id', '')
            
            # Get location information
            for location in error.findall('location'):
                issue = {
                    'file': location.get('file', ''),
                    'line': location.get('line', '0'),
                    'column': location.get('column', '0'),
                    'severity': severity,
                    'message': msg,
                    'id': error_id
                }
                issues.append(issue)
                break  # Only take first location for now
            
            # Handle errors without location
            if not error.findall('location'):
                issue = {
                    'file': '',
                    'line': '0',
                    'column': '0',
                    'severity': severity,
                    'message': msg,
                    'id': error_id
                }
                issues.append(issue)
        
        # Create JSON structure
        data = {
            'issues': issues,
            'total': len(issues)
        }
        
        # Write JSON
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"✅ Converted {len(issues)} issues from XML to JSON")
        return True
        
    except Exception as e:
        print(f"❌ Error converting XML to JSON: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: xml2json.py <input.xml> <output.json>")
        sys.exit(1)
        
    xml_file = sys.argv[1]
    json_file = sys.argv[2]
    
    if convert_xml_to_json(xml_file, json_file):
        sys.exit(0)
    else:
        sys.exit(1)