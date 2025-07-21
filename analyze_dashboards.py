#!/usr/bin/env python3
"""Analyze and compare dashboards without external dependencies"""

import os
import json
import re

def analyze_dashboard(html_file):
    """Analyze a dashboard HTML file using basic Python"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {html_file}")
    print('='*60)
    
    if not os.path.exists(html_file):
        print(f"ERROR: File {html_file} not found!")
        return None
    
    # File size
    file_size_mb = os.path.getsize(html_file) / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JavaScript content
    js_content = ""
    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for match in script_matches:
        if not match.strip().startswith('src='):
            js_content += match
    
    # Check features
    print("\nFeatures detected:")
    features = {
        'Search functionality': bool(re.search(r'search|filter.*input', js_content, re.I)),
        'Filter buttons': bool(re.search(r'filter.*function|setFilter', js_content, re.I)),
        'Modal/popup': bool(re.search(r'modal|popup|dialog', js_content, re.I)),
        'Event listeners': 'addEventListener' in js_content,
        'DOM manipulation': bool(re.search(r'getElementById|querySelector', js_content)),
        'Code highlighting': bool(re.search(r'highlight|hljs|prism', js_content, re.I)),
        'Charts/Visualization': bool(re.search(r'chart|plot|graph|canvas', js_content, re.I)),
        'Export functionality': bool(re.search(r'export|download|save', js_content, re.I)),
        'Sorting': bool(re.search(r'sort\(|sortBy|orderBy', js_content, re.I)),
        'Real-time updates': bool(re.search(r'setInterval|setTimeout|refresh', js_content)),
        'Keyboard shortcuts': bool(re.search(r'keydown|keypress|keyCode', js_content, re.I)),
        'Copy to clipboard': bool(re.search(r'clipboard|copy.*text', js_content, re.I)),
        'Responsive design': bool(re.search(r'@media|responsive|mobile', content, re.I)),
        'Dark mode': bool(re.search(r'dark.*mode|theme.*toggle', content, re.I)),
        'Pagination': bool(re.search(r'page|pagination|limit.*offset', js_content, re.I))
    }
    
    for feature, present in features.items():
        print(f"  {'✅' if present else '❌'} {feature}")
    
    # Count issues data
    print("\nData analysis:")
    issues_match = re.search(r'const issuesData = (\[.*?\]);', js_content, re.DOTALL)
    if issues_match:
        try:
            # Basic counting without json parsing
            issues_text = issues_match.group(1)
            issue_count = issues_text.count('"file":')
            print(f"  - Embedded issues count: ~{issue_count}")
            
            # Count severities
            severities = {
                'error': issues_text.count('"severity": "error"') + issues_text.count('"severity":"error"'),
                'warning': issues_text.count('"severity": "warning"') + issues_text.count('"severity":"warning"'),
                'style': issues_text.count('"severity": "style"') + issues_text.count('"severity":"style"'),
                'performance': issues_text.count('"severity": "performance"') + issues_text.count('"severity":"performance"'),
                'information': issues_text.count('"severity": "information"') + issues_text.count('"severity":"information"')
            }
            
            print("  - Issues by severity:")
            for sev, count in severities.items():
                if count > 0:
                    print(f"    - {sev}: {count}")
        except Exception as e:
            print(f"  - Error parsing issues: {e}")
    else:
        print("  - No embedded issues data found")
    
    # Check for code contexts
    has_code_contexts = bool(re.search(r'codeContext|code_context|<pre.*<code', content, re.I))
    print(f"  - Has code contexts: {'✅' if has_code_contexts else '❌'}")
    
    # External dependencies
    print("\nExternal dependencies:")
    # Scripts
    script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)
    for src in script_srcs:
        print(f"  - Script: {src}")
    
    # CSS
    css_links = re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\'"]', content)
    for link in css_links:
        print(f"  - CSS: {link}")
    
    # Performance indicators
    print("\nPerformance indicators:")
    inline_styles = content.count('style=')
    inline_scripts = len([m for m in script_matches if not re.search(r'src=', m)])
    print(f"  - Inline styles: {inline_styles}")
    print(f"  - Inline scripts: {inline_scripts}")
    print(f"  - Total size: {file_size_mb:.2f} MB")
    
    if file_size_mb > 5:
        print("  ⚠️  Large file size may cause performance issues")
    elif file_size_mb > 1:
        print("  ⚠️  Consider optimizing file size")
    else:
        print("  ✅ Good file size for web delivery")
    
    return {
        'file_size': file_size_mb,
        'features': features,
        'feature_count': sum(features.values()),
        'has_data': bool(issues_match),
        'has_code_contexts': has_code_contexts,
        'external_deps': len(script_srcs) + len(css_links)
    }

def main():
    dashboards = [
        ("Ultimate Dashboard", "test-dashboard-final.html"),
        ("Enhanced Dashboard", "test-enhanced.html")
    ]
    
    results = {}
    for name, file in dashboards:
        print(f"\n{'#'*60}")
        print(f"# {name}")
        print('#'*60)
        results[name] = analyze_dashboard(file)
    
    # Comparison
    print(f"\n\n{'='*60}")
    print("COMPARISON SUMMARY")
    print('='*60)
    
    if all(results.values()):
        # Size comparison
        print("\nFile sizes:")
        for name, result in results.items():
            print(f"  - {name}: {result['file_size']:.2f} MB")
        
        # Feature comparison
        print("\nFeature counts:")
        for name, result in results.items():
            print(f"  - {name}: {result['feature_count']}/15 features")
        
        # Recommendations
        print(f"\n{'='*60}")
        print("RECOMMENDATIONS")
        print('='*60)
        
        # Find best option
        ultimate = results["Ultimate Dashboard"]
        enhanced = results["Enhanced Dashboard"]
        
        print("\n🏆 Production Recommendation:")
        
        if ultimate['file_size'] < 1 and ultimate['feature_count'] >= 10:
            print("  ✅ Ultimate Dashboard (test-dashboard-final.html)")
            print("     - Excellent file size")
            print("     - Rich feature set")
            print("     - Should load quickly")
        elif enhanced['file_size'] < 2 and enhanced['has_code_contexts']:
            print("  ✅ Enhanced Dashboard (test-enhanced.html)")
            print("     - Has code contexts")
            print("     - Reasonable file size")
        else:
            print("  ⚠️  Both dashboards need optimization")
        
        # Specific issues
        if enhanced['file_size'] > 10:
            print("\n❌ Enhanced Dashboard issues:")
            print("   - File too large for web delivery")
            print("   - Will cause slow page loads")
            print("   - Consider pagination or lazy loading")
        
        # Feature advantages
        print("\n📊 Feature comparison:")
        all_features = set()
        for result in results.values():
            all_features.update(result['features'].keys())
        
        for feature in sorted(all_features):
            ult_has = ultimate['features'].get(feature, False)
            enh_has = enhanced['features'].get(feature, False)
            
            if ult_has and not enh_has:
                print(f"  - {feature}: Ultimate only")
            elif enh_has and not ult_has:
                print(f"  - {feature}: Enhanced only")
        
        # Final verdict
        print("\n🎯 Final Verdict:")
        if ultimate['file_size'] < enhanced['file_size'] / 10 and ultimate['feature_count'] >= enhanced['feature_count'] - 2:
            print("  USE: Ultimate Dashboard (test-dashboard-final.html)")
            print("  - Much smaller file size")
            print("  - Similar features")
            print("  - Better performance")
        elif enhanced['has_code_contexts'] and enhanced['file_size'] < 5:
            print("  USE: Enhanced Dashboard (test-enhanced.html)")
            print("  - Has code contexts")
            print("  - Acceptable size")
        else:
            print("  OPTIMIZE: Both need work before production")

if __name__ == "__main__":
    main()