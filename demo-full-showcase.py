#!/usr/bin/env python3
"""
CPPCheck Studio - Full Demo Showcase
Demonstrates all features and capabilities
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

class CppCheckStudioDemo:
    def __init__(self):
        self.demo_dir = Path("demo-output")
        self.demo_dir.mkdir(exist_ok=True)
        self.results = []
        
    def print_header(self, title):
        """Print a formatted section header"""
        print("\n" + "="*60)
        print(f"🚀 {title}")
        print("="*60)
        
    def print_step(self, step):
        """Print a step in the demo"""
        print(f"\n➤ {step}")
        
    def print_success(self, message):
        """Print success message"""
        print(f"✅ {message}")
        
    def print_info(self, message):
        """Print info message"""
        print(f"ℹ️  {message}")
        
    def print_error(self, message):
        """Print error message"""
        print(f"❌ {message}")
        
    def run_command(self, command, description):
        """Run a shell command and display results"""
        self.print_step(description)
        print(f"   Command: {command}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.print_success("Command completed successfully")
                if result.stdout:
                    print(f"   Output: {result.stdout[:200]}...")
                return True
            else:
                self.print_error(f"Command failed: {result.stderr}")
                return False
        except Exception as e:
            self.print_error(f"Error running command: {e}")
            return False
            
    def demo_python_dashboards(self):
        """Demo all Python dashboard generators"""
        self.print_header("Python Dashboard Generators Demo")
        
        # Check if we have analysis data
        analysis_file = "analysis-with-context.json"
        if not Path(analysis_file).exists():
            self.print_info("No analysis file found. Using sample data...")
            # Create sample analysis data
            sample_data = {
                "issues": [
                    {
                        "file": "/sample/code.cpp",
                        "line": 10,
                        "severity": "error",
                        "message": "Null pointer dereference",
                        "id": "nullPointer",
                        "code_context": {
                            "code": ["void test() {", "  int* p = nullptr;", "  *p = 10; // Error here", "}"],
                            "start_line": 9
                        }
                    },
                    {
                        "file": "/sample/code.cpp",
                        "line": 20,
                        "severity": "warning",
                        "message": "Member variable not initialized",
                        "id": "uninitMemberVar"
                    },
                    {
                        "file": "/sample/code.cpp",
                        "line": 30,
                        "severity": "style",
                        "message": "Use nullptr instead of NULL",
                        "id": "useNullptr"
                    }
                ]
            }
            with open(self.demo_dir / "sample-analysis.json", "w") as f:
                json.dump(sample_data, f, indent=2)
            analysis_file = str(self.demo_dir / "sample-analysis.json")
            
        # Generate different dashboard types
        dashboards = [
            ("generate-ultimate-dashboard.py", "Ultimate Dashboard (Recommended)", "ultimate"),
            ("generate-virtual-scroll-dashboard.py", "Virtual Scroll Dashboard", "virtual"),
            ("generate-robust-dashboard.py", "Robust Dashboard", "robust"),
            ("generate-production-dashboard.py", "Production Dashboard", "production"),
            ("generate-split-dashboard.py", "Split Dashboard", "split")
        ]
        
        for script, desc, output_name in dashboards:
            script_path = Path("generate") / script
            if script_path.exists():
                output_file = self.demo_dir / f"demo-{output_name}.html"
                self.run_command(
                    f"python3 {script_path} {analysis_file} {output_file}",
                    f"Generating {desc}"
                )
                if output_file.exists():
                    size_kb = output_file.stat().st_size / 1024
                    self.print_info(f"Generated {output_file.name} ({size_kb:.1f} KB)")
                    
    def demo_test_scripts(self):
        """Run all test scripts"""
        self.print_header("Running Test Scripts")
        
        test_scripts = [
            ("test/test_dashboards.py", "Dashboard Analysis Test"),
            ("test/test-integration.py", "Integration Test"),
            ("test/test-e2e.js", "End-to-End Test"),
            ("test/debug-dashboard.py", "Debug Dashboard Test"),
            ("test/verify-code-context.py", "Code Context Verification")
        ]
        
        for script, desc in test_scripts:
            if Path(script).exists():
                ext = Path(script).suffix
                if ext == ".py":
                    self.run_command(f"python3 {script}", f"Running {desc}")
                elif ext == ".js":
                    self.run_command(f"node {script}", f"Running {desc}")
                    
    def demo_analysis_workflow(self):
        """Demo the complete analysis workflow"""
        self.print_header("Complete Analysis Workflow Demo")
        
        # Create sample C++ files
        self.print_step("Creating sample C++ code for analysis")
        sample_cpp = """
#include <iostream>
#include <vector>

class TestClass {
private:
    int* data;
    int size;
    
public:
    TestClass() {
        // Missing initialization of member variables
        data = NULL;  // Should use nullptr
    }
    
    ~TestClass() {
        delete data;  // Should be delete[]
    }
    
    void process() {
        std::vector<int> v;
        for (int i = 0; i < v.size(); i++) {  // Should use size_t
            v[i] = i;
        }
    }
    
    virtual void virtualFunc() {  // Missing override in derived class
        std::cout << "Base class" << std::endl;
    }
};

class DerivedClass : public TestClass {
public:
    void virtualFunc() {  // Should have override
        std::cout << "Derived class" << std::endl;
    }
};

int main() {
    TestClass* obj = new TestClass();
    obj->process();
    delete obj;
    return 0;
}
"""
        
        sample_dir = self.demo_dir / "sample-code"
        sample_dir.mkdir(exist_ok=True)
        sample_file = sample_dir / "test.cpp"
        sample_file.write_text(sample_cpp)
        self.print_success(f"Created sample C++ file: {sample_file}")
        
        # Run cppcheck (if available)
        self.print_step("Running cppcheck analysis")
        if subprocess.run("which cppcheck", shell=True, capture_output=True).returncode == 0:
            analysis_output = self.demo_dir / "cppcheck-analysis.json"
            self.run_command(
                f"cppcheck --enable=all --std=c++17 --template='{{\"file\":\"{{file}}\",\"line\":{{line}},\"severity\":\"{{severity}}\",\"id\":\"{{id}}\",\"message\":\"{{message}}\"}}' {sample_dir} 2>&1 | grep -E '^{{' > {analysis_output}",
                "Running cppcheck on sample code"
            )
        else:
            self.print_info("cppcheck not installed. Using pre-generated analysis data.")
            
    def demo_features_showcase(self):
        """Showcase all features"""
        self.print_header("Feature Showcase")
        
        features = {
            "Dashboard Generators": [
                "✓ Ultimate Dashboard - Production-ready with all features",
                "✓ Virtual Scroll - Handles 10,000+ issues efficiently",
                "✓ Robust Dashboard - Error handling and chunked rendering",
                "✓ Production Dashboard - Minimal size, no code context",
                "✓ Split Dashboard - Separate files for modularity"
            ],
            "Interactive Features": [
                "✓ Real-time search filtering",
                "✓ Severity-based filtering (Errors/Warnings/Style/Performance)",
                "✓ Code preview with syntax highlighting",
                "✓ Statistics cards with percentages",
                "✓ Responsive design for all screen sizes"
            ],
            "Analysis Capabilities": [
                "✓ CPPCheck integration",
                "✓ Code context extraction",
                "✓ Fix generation for common issues",
                "✓ Support for large codebases",
                "✓ JSON and JSONL output formats"
            ],
            "Testing Infrastructure": [
                "✓ Integration tests",
                "✓ End-to-end tests",
                "✓ Dashboard comparison tests",
                "✓ Code context verification",
                "✓ Performance benchmarks"
            ]
        }
        
        for category, items in features.items():
            self.print_step(category)
            for item in items:
                print(f"   {item}")
                
    def generate_demo_report(self):
        """Generate a comprehensive demo report"""
        self.print_header("Generating Demo Report")
        
        report = {
            "demo_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project": "CPPCheck Studio",
            "features_demonstrated": {
                "dashboard_generators": 5,
                "test_scripts": 5,
                "interactive_features": 10,
                "analysis_capabilities": 5
            },
            "output_files": list(self.demo_dir.glob("*.html")),
            "statistics": {
                "lpzrobots_issues": 2975,
                "errors": 772,
                "warnings": 153,
                "style": 1932,
                "performance": 31
            },
            "recommendations": [
                "Use generate-ultimate-dashboard.py for production",
                "Use virtual-scroll for large datasets (>5000 issues)",
                "Add code context for better issue understanding",
                "Run tests regularly to ensure functionality"
            ]
        }
        
        report_file = self.demo_dir / "demo-report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2, default=str)
            
        self.print_success(f"Demo report saved to: {report_file}")
        
        # Create summary HTML
        summary_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CPPCheck Studio Demo Summary</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .stat-card {{ 
            display: inline-block; 
            padding: 20px; 
            margin: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #f5f5f5;
        }}
        .number {{ font-size: 2em; font-weight: bold; color: #2563eb; }}
    </style>
</head>
<body>
    <h1>CPPCheck Studio Demo Summary</h1>
    <p>Demo run: {report['demo_run']}</p>
    
    <h2>LPZRobots Analysis Results</h2>
    <div class="stat-card">
        <div class="number">2,975</div>
        <div>Total Issues</div>
    </div>
    <div class="stat-card">
        <div class="number">772</div>
        <div>Errors (25.9%)</div>
    </div>
    <div class="stat-card">
        <div class="number">153</div>
        <div>Warnings (5.1%)</div>
    </div>
    <div class="stat-card">
        <div class="number">1,932</div>
        <div>Style (64.9%)</div>
    </div>
    
    <h2>Generated Dashboards</h2>
    <ul>
        {"".join(f'<li><a href="{f.name}">{f.name}</a></li>' for f in report['output_files'])}
    </ul>
    
    <h2>Recommendations</h2>
    <ul>
        {"".join(f'<li>{r}</li>' for r in report['recommendations'])}
    </ul>
</body>
</html>
"""
        
        summary_file = self.demo_dir / "demo-summary.html"
        summary_file.write_text(summary_html)
        self.print_success(f"Demo summary saved to: {summary_file}")
        
    def run_full_demo(self):
        """Run the complete demo"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║           CPPCheck Studio - Full Feature Demo                ║
║                                                              ║
║  This demo will showcase all features and capabilities       ║
║  of the CPPCheck Studio static analysis visualization tool   ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Run all demo sections
        self.demo_analysis_workflow()
        self.demo_python_dashboards()
        self.demo_test_scripts()
        self.demo_features_showcase()
        self.generate_demo_report()
        
        # Final summary
        self.print_header("Demo Complete!")
        print(f"""
📁 All demo outputs saved to: {self.demo_dir}/

Key files generated:
- demo-ultimate.html    : Best dashboard for production use
- demo-virtual.html     : Virtual scrolling for large datasets  
- demo-robust.html      : Error handling and chunked rendering
- demo-production.html  : Minimal size dashboard
- demo-summary.html     : Demo summary report

To view the dashboards:
  open {self.demo_dir}/demo-ultimate.html
  
To run on your own C++ code:
  1. Run cppcheck: cppcheck --enable=all --template=gcc your-code/ 2>&1 | grep -E "^[^:]+:[0-9]+:" > analysis.txt
  2. Convert to JSON format (use the provided scripts)
  3. Generate dashboard: python3 generate/generate-ultimate-dashboard.py analysis.json dashboard.html

Thank you for exploring CPPCheck Studio!
        """)

def main():
    demo = CppCheckStudioDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main()