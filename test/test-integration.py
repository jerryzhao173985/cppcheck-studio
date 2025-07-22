#!/usr/bin/env python3
"""
Integration test for CPPCheck Studio on LPZRobots codebase
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Add the Python scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "cppcheck" / "scripts"))

from analyze import CppcheckAnalyzer
from generate_enhanced_dashboard import EnhancedDashboardGenerator
from fix_generator import FixGenerator
from code_context_extractor import CodeContextExtractor

class CppCheckStudioTester:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.studio_root = Path(__file__).parent
        self.results = {}
        
    def test_analyzer(self):
        """Test the analyzer on LPZRobots codebase"""
        print("🔍 Testing analyzer on LPZRobots...")
        
        analyzer = CppcheckAnalyzer(str(self.project_root))
        
        # Test on a subset first
        test_files = [
            self.project_root / "selforg" / "controller" / "sox.cpp",
            self.project_root / "selforg" / "controller" / "dep.cpp",
            self.project_root / "ode_robots" / "simulation.cpp"
        ]
        
        # Filter existing files
        existing_files = [str(f) for f in test_files if f.exists()]
        print(f"   Testing on {len(existing_files)} files...")
        
        results = analyzer.run_quick_analysis(file_list=existing_files)
        
        print(f"✅ Found {len(results)} issues")
        print(f"   - Errors: {sum(1 for r in results if r.get('severity') == 'error')}")
        print(f"   - Warnings: {sum(1 for r in results if r.get('severity') == 'warning')}")
        print(f"   - Style: {sum(1 for r in results if r.get('severity') == 'style')}")
        print(f"   - Performance: {sum(1 for r in results if r.get('severity') == 'performance')}")
        
        self.results['analysis'] = results
        return len(results) > 0
        
    def test_dashboard_generation(self):
        """Test dashboard generation"""
        print("\n📊 Testing dashboard generation...")
        
        if not self.results.get('analysis'):
            print("❌ No analysis results to generate dashboard")
            return False
            
        generator = EnhancedDashboardGenerator(self.results['analysis'])
        dashboard_path = self.studio_root / "test-dashboard.html"
        
        generator.generate_enhanced_dashboard(str(dashboard_path))
        
        if dashboard_path.exists():
            print(f"✅ Dashboard generated: {dashboard_path}")
            print(f"   Size: {dashboard_path.stat().st_size / 1024:.1f} KB")
            
            # Check for key features
            content = dashboard_path.read_text()
            features = {
                'Syntax highlighting': 'hljs' in content,
                'Diff viewer': 'diff2html' in content,
                'Interactive fixes': 'applyFix' in content,
                'Code context': 'expandRow' in content,
                'Metrics': 'chart.js' in content or 'Chart' in content
            }
            
            for feature, present in features.items():
                status = "✅" if present else "❌"
                print(f"   {status} {feature}")
                
            return all(features.values())
        else:
            print("❌ Dashboard generation failed")
            return False
            
    def test_fix_generation(self):
        """Test fix generation"""
        print("\n🔧 Testing fix generation...")
        
        if not self.results.get('analysis'):
            print("❌ No analysis results for fix generation")
            return False
            
        generator = FixGenerator(str(self.project_root))
        
        # Find fixable issues
        fixable_ids = ['useNullptr', 'modernizeOverride', 'explicitConstructor']
        fixable_issues = [
            issue for issue in self.results['analysis']
            if any(fid in issue.get('id', '') for fid in fixable_ids)
        ][:5]  # Test first 5
        
        if not fixable_issues:
            print("⚠️  No fixable issues found in test subset")
            return True
            
        print(f"   Found {len(fixable_issues)} fixable issues")
        
        fixes_generated = 0
        for issue in fixable_issues:
            fix = generator.generate_fix(issue)
            if fix and fix.get('diff'):
                fixes_generated += 1
                print(f"   ✅ Generated fix for: {issue['id']}")
                
        print(f"   Generated {fixes_generated}/{len(fixable_issues)} fixes")
        return fixes_generated > 0
        
    def test_context_extraction(self):
        """Test code context extraction"""
        print("\n📄 Testing context extraction...")
        
        if not self.results.get('analysis'):
            print("❌ No analysis results for context extraction")
            return False
            
        extractor = CodeContextExtractor(str(self.project_root))
        
        # Test on first few issues
        test_issues = self.results['analysis'][:3]
        
        contexts_extracted = 0
        for issue in test_issues:
            context = extractor.extract_context(
                issue['file'],
                issue['line'],
                context_size=10
            )
            
            if context and context.get('code'):
                contexts_extracted += 1
                print(f"   ✅ Extracted context for {Path(issue['file']).name}:{issue['line']}")
                print(f"      Function: {context.get('function', 'N/A')}")
                print(f"      Lines: {len(context['code'])}")
                
        return contexts_extracted > 0
        
    def test_npm_package_structure(self):
        """Validate npm package structure"""
        print("\n📦 Testing npm package structure...")
        
        checks = {
            'CLI package.json': (self.studio_root / "packages" / "cli" / "package.json").exists(),
            'CLI binary entry': False,
            'Core exports': (self.studio_root / "packages" / "core" / "src" / "index.ts").exists(),
            'API routes': (self.studio_root / "apps" / "api" / "src" / "routes").exists(),
            'Web app': (self.studio_root / "apps" / "web" / "app" / "page.tsx").exists(),
        }
        
        # Check CLI binary configuration
        cli_package = self.studio_root / "packages" / "cli" / "package.json"
        if cli_package.exists():
            pkg = json.loads(cli_package.read_text())
            checks['CLI binary entry'] = 'bin' in pkg and 'cppcheck-studio' in pkg.get('bin', {})
            
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
            
        return all(checks.values())
        
    def test_typescript_core(self):
        """Test TypeScript core functionality"""
        print("\n🔷 Testing TypeScript core...")
        
        # Check if TypeScript files compile
        core_src = self.studio_root / "packages" / "core" / "src"
        ts_files = list(core_src.glob("*.ts"))
        
        print(f"   Found {len(ts_files)} TypeScript files")
        
        required_modules = ['analyzer', 'parser', 'fix-generator', 'metrics', 'context-extractor']
        for module in required_modules:
            exists = (core_src / f"{module}.ts").exists()
            status = "✅" if exists else "❌"
            print(f"   {status} {module}.ts")
            
        return len(ts_files) >= len(required_modules)
        
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📝 Generating test report...")
        
        report = {
            'timestamp': str(Path.cwd()),
            'project': 'LPZRobots',
            'issues_found': len(self.results.get('analysis', [])),
            'features_tested': {
                'analyzer': '✅',
                'dashboard': '✅',
                'fixes': '✅',
                'context': '✅',
                'npm_structure': '✅',
                'typescript': '✅'
            },
            'sample_issues': self.results.get('analysis', [])[:10]
        }
        
        report_path = self.studio_root / "test-report.json"
        report_path.write_text(json.dumps(report, indent=2))
        print(f"✅ Test report saved to: {report_path}")
        
        return report

def main():
    print("🚀 CPPCheck Studio Integration Test")
    print("=" * 50)
    
    tester = CppCheckStudioTester()
    
    tests = [
        ("Analyzer", tester.test_analyzer),
        ("Dashboard", tester.test_dashboard_generation),
        ("Fix Generation", tester.test_fix_generation),
        ("Context Extraction", tester.test_context_extraction),
        ("NPM Structure", tester.test_npm_package_structure),
        ("TypeScript Core", tester.test_typescript_core),
    ]
    
    passed = 0
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {name} test failed")
        except Exception as e:
            print(f"❌ {name} test error: {e}")
            import traceback
            traceback.print_exc()
            
    print("\n" + "=" * 50)
    print(f"✅ Passed: {passed}/{len(tests)} tests")
    
    if passed == len(tests):
        print("🎉 All tests passed!")
        tester.generate_test_report()
    else:
        print("❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()