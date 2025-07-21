#!/usr/bin/env python3
"""
Test dashboard generation with real LPZRobots analysis results
"""

import json
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "cppcheck" / "scripts"))

from generate_enhanced_dashboard import EnhancedDashboardGenerator

def test_dashboard():
    # Load real analysis results
    results_file = Path("test-analysis.json")
    if not results_file.exists():
        print("❌ No test-analysis.json found. Run analysis first.")
        return False
        
    with open(results_file) as f:
        data = json.load(f)
        
    issues = data.get('issues', [])
    print(f"📊 Generating dashboard for {len(issues)} issues...")
    
    # Generate enhanced dashboard
    # The generator expects a dict with 'issues' key
    generator = EnhancedDashboardGenerator({'issues': issues})
    dashboard_path = Path("test-ultimate-dashboard.html")
    
    generator.generate_enhanced_dashboard(str(dashboard_path))
    
    if dashboard_path.exists():
        print(f"✅ Dashboard generated: {dashboard_path}")
        print(f"   Size: {dashboard_path.stat().st_size / 1024:.1f} KB")
        
        # Analyze dashboard features
        content = dashboard_path.read_text()
        
        print("\n🔍 Dashboard Feature Analysis:")
        features = {
            'Highlight.js syntax highlighting': 'hljs.highlightElement' in content,
            'Diff2html diff viewer': 'Diff2HtmlUI' in content,
            'Interactive fix preview': 'previewFix' in content,
            'Code context expansion': 'expandRow' in content,
            'Apply fix functionality': 'applyFix' in content,
            'Metrics visualization': 'generateMetricsCharts' in content,
            'Real-time search': 'filterTable' in content,
            'Severity filtering': 'severityFilter' in content,
            'Git integration': 'gitBlame' in content,
            'Export functionality': 'exportData' in content
        }
        
        passed = 0
        for feature, present in features.items():
            status = "✅" if present else "❌"
            print(f"   {status} {feature}")
            if present:
                passed += 1
                
        print(f"\n📈 Feature Coverage: {passed}/{len(features)} ({passed/len(features)*100:.1f}%)")
        
        # Check issue categorization
        print("\n📋 Issue Analysis:")
        severities = {}
        categories = {}
        
        for issue in issues[:100]:  # Sample first 100
            sev = issue.get('severity', 'unknown')
            severities[sev] = severities.get(sev, 0) + 1
            
            cat = 'other'
            issue_id = issue.get('id', '').lower()
            if 'nullptr' in issue_id:
                cat = 'modernization'
            elif 'override' in issue_id:
                cat = 'modernization'
            elif 'leak' in issue_id or 'uninit' in issue_id:
                cat = 'safety'
            elif 'performance' in issue.get('severity', ''):
                cat = 'performance'
                
            categories[cat] = categories.get(cat, 0) + 1
            
        print("   By Severity:")
        for sev, count in sorted(severities.items()):
            print(f"     - {sev}: {count}")
            
        print("   By Category:")
        for cat, count in sorted(categories.items()):
            print(f"     - {cat}: {count}")
            
        return True
    else:
        print("❌ Dashboard generation failed")
        return False

if __name__ == "__main__":
    test_dashboard()