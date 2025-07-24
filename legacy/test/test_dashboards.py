#!/usr/bin/env python3
"""Test script to analyze and compare both dashboards"""

import os
import json
from bs4 import BeautifulSoup
import re

def analyze_dashboard(html_file):
    """Analyze a dashboard HTML file"""
    print(f"\n=== Analyzing {html_file} ===")
    
    if not os.path.exists(html_file):
        print(f"ERROR: File {html_file} not found!")
        return None
    
    file_size = os.path.getsize(html_file) / (1024 * 1024)  # MB
    print(f"File size: {file_size:.2f} MB")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Check for external dependencies
    print("\nExternal Dependencies:")
    scripts = soup.find_all('script', src=True)
    for script in scripts:
        print(f"  - {script['src']}")
    
    links = soup.find_all('link', href=True)
    css_links = [link for link in links if 'css' in link.get('rel', [])]
    for link in css_links:
        print(f"  - {link['href']}")
    
    # Check for JavaScript functionality
    print("\nJavaScript Features:")
    js_content = ""
    for script in soup.find_all('script'):
        if not script.get('src'):
            js_content += script.string or ""
    
    features = {
        'Search functionality': 'searchInput' in js_content or 'search' in js_content,
        'Filter functionality': 'filter' in js_content.lower(),
        'Modal/popup': 'modal' in js_content.lower(),
        'Event listeners': 'addEventListener' in js_content,
        'DOM manipulation': 'getElementById' in js_content or 'querySelector' in js_content,
        'Code highlighting': 'highlight' in js_content.lower() or 'hljs' in js_content,
        'Data visualization': 'chart' in js_content.lower() or 'plot' in js_content.lower(),
        'Export functionality': 'export' in js_content.lower() or 'download' in js_content.lower(),
        'Sort functionality': 'sort' in js_content.lower(),
        'Statistics display': 'stats' in js_content.lower() or 'count' in js_content.lower()
    }
    
    for feature, present in features.items():
        print(f"  - {feature}: {'✅' if present else '❌'}")
    
    # Check for issues data
    print("\nData Analysis:")
    issues_match = re.search(r'const issuesData = (\[.*?\]);', js_content, re.DOTALL)
    if issues_match:
        try:
            issues_data = json.loads(issues_match.group(1))
            print(f"  - Total issues embedded: {len(issues_data)}")
            
            # Count by severity
            severity_counts = {}
            for issue in issues_data:
                severity = issue.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            print("  - Issues by severity:")
            for severity, count in sorted(severity_counts.items()):
                print(f"    - {severity}: {count}")
        except:
            print("  - ERROR: Could not parse issues data")
    else:
        print("  - No embedded issues data found")
    
    # Check UI elements
    print("\nUI Elements:")
    ui_elements = {
        'Search box': soup.find('input', {'type': 'search'}) or soup.find('input', {'id': 'searchInput'}),
        'Filter buttons': soup.find_all('button', class_=re.compile('filter')),
        'Issues table': soup.find('table') or soup.find('div', class_=re.compile('table')),
        'Statistics cards': soup.find_all('div', class_=re.compile('stat|card')),
        'Header': soup.find('header') or soup.find('div', class_=re.compile('header')),
        'Charts/Graphs': soup.find('canvas') or soup.find('div', {'id': re.compile('chart|graph')}),
        'Export buttons': soup.find_all('button', string=re.compile('export|download', re.I))
    }
    
    for element, found in ui_elements.items():
        if isinstance(found, list):
            print(f"  - {element}: {'✅' if found else '❌'} ({len(found)} found)")
        else:
            print(f"  - {element}: {'✅' if found else '❌'}")
    
    return {
        'file_size': file_size,
        'features': features,
        'ui_elements': {k: bool(v) if not isinstance(v, list) else len(v) > 0 for k, v in ui_elements.items()},
        'has_data': bool(issues_match)
    }

def main():
    dashboard1 = "test-dashboard-final.html"
    dashboard2 = "test-enhanced.html"
    
    results1 = analyze_dashboard(dashboard1)
    results2 = analyze_dashboard(dashboard2)
    
    print("\n\n=== COMPARISON SUMMARY ===")
    
    if results1 and results2:
        print(f"\nFile Size:")
        print(f"  - {dashboard1}: {results1['file_size']:.2f} MB")
        print(f"  - {dashboard2}: {results2['file_size']:.2f} MB")
        print(f"  - Size difference: {abs(results2['file_size'] - results1['file_size']):.2f} MB")
        
        print(f"\nFeature Comparison:")
        all_features = set(results1['features'].keys()) | set(results2.get('features', {}).keys())
        for feature in sorted(all_features):
            d1_has = results1['features'].get(feature, False)
            d2_has = results2.get('features', {}).get(feature, False)
            
            if d1_has and d2_has:
                status = "✅ Both"
            elif d1_has:
                status = "⚠️  Dashboard 1 only"
            elif d2_has:
                status = "⚠️  Dashboard 2 only"
            else:
                status = "❌ Neither"
            
            print(f"  - {feature}: {status}")
        
        print(f"\n=== RECOMMENDATIONS ===")
        
        if results2['file_size'] > 10:
            print("⚠️  Enhanced dashboard is very large (>10MB), may have performance issues")
        
        feature_count1 = sum(results1['features'].values())
        feature_count2 = sum(results2.get('features', {}).values())
        
        if feature_count1 > feature_count2:
            print("✅ Dashboard 1 (test-dashboard-final.html) has more features")
        elif feature_count2 > feature_count1:
            print("✅ Dashboard 2 (test-enhanced.html) has more features")
        else:
            print("✅ Both dashboards have similar feature sets")
        
        if results1['file_size'] < results2['file_size'] / 10:
            print("✅ Dashboard 1 is much more efficient in file size")
        
        print("\n=== PRODUCTION READINESS ===")
        if results1['file_size'] < 1 and feature_count1 >= 7:
            print("✅ Dashboard 1 appears production-ready: small size, good features")
        else:
            print("⚠️  Dashboard 1 may need optimization")
            
        if results2['file_size'] > 5:
            print("❌ Dashboard 2 is too large for production use")
        elif feature_count2 >= 7:
            print("⚠️  Dashboard 2 has good features but needs size optimization")

if __name__ == "__main__":
    main()