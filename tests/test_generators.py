#!/usr/bin/env python3
"""
Test suite for CPPCheck dashboard generators
"""

import unittest
import json
import tempfile
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'generate'))

# Test by running the generators directly as subprocesses to avoid import issues

class TestGenerators(unittest.TestCase):
    """Test all core dashboard generators"""
    
    @classmethod
    def setUpClass(cls):
        """Create test data files"""
        cls.test_dir = tempfile.mkdtemp()
        
        # Small test data
        cls.small_data = {
            "issues": [
                {
                    "id": "unreadVariable",
                    "severity": "style",
                    "message": "Variable 'x' is assigned a value that is never used.",
                    "file": "test.cpp",
                    "line": 10
                },
                {
                    "id": "uninitvar",
                    "severity": "error",
                    "message": "Uninitialized variable: y",
                    "file": "test.cpp",
                    "line": 20
                }
            ]
        }
        
        # Large test data
        cls.large_data = {
            "issues": [
                {
                    "id": f"issue{i}",
                    "severity": ["error", "warning", "style", "performance"][i % 4],
                    "message": f"Test issue {i}",
                    "file": f"file{i % 10}.cpp",
                    "line": i
                }
                for i in range(1000)
            ]
        }
        
        # Write test files
        cls.small_file = os.path.join(cls.test_dir, "small.json")
        with open(cls.small_file, 'w') as f:
            json.dump(cls.small_data, f)
            
        cls.large_file = os.path.join(cls.test_dir, "large.json")
        with open(cls.large_file, 'w') as f:
            json.dump(cls.large_data, f)
    
    def test_standalone_generator_small(self):
        """Test standalone generator with small dataset"""
        output_file = os.path.join(self.test_dir, "standalone_small.html")
        
        # Run generator
        result = os.system(f"python3 generate/generate-standalone-virtual-dashboard.py {self.small_file} {output_file}")
        
        # Check success
        self.assertEqual(result, 0, "Generator should exit successfully")
        self.assertTrue(os.path.exists(output_file), "Output file should exist")
        
        # Check content
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("CPPCheck", content)
            self.assertIn("Uninitialized variable", content)
            # Check for virtual scrolling functionality
            self.assertIn("class=\"virtual-table-container\"", content, "Should have virtual scrolling")
    
    def test_production_generator_small(self):
        """Test production generator with small dataset"""
        output_file = os.path.join(self.test_dir, "production_small.html")
        
        # Run generator
        result = os.system(f"python3 generate/generate-production-dashboard.py {self.small_file} {output_file}")
        
        # Check success
        self.assertEqual(result, 0, "Generator should exit successfully")
        self.assertTrue(os.path.exists(output_file), "Output file should exist")
        
        # Check content
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("CPPCheck Analysis Dashboard", content)
            self.assertIn("Uninitialized variable", content)
    
    def test_virtual_scroll_generator_large(self):
        """Test virtual scroll generator with large dataset"""
        output_file = os.path.join(self.test_dir, "virtual_large.html")
        
        # Run generator
        result = os.system(f"python3 generate/generate-virtual-scroll-dashboard.py {self.large_file} {output_file}")
        
        # Check success
        self.assertEqual(result, 0, "Generator should exit successfully")
        self.assertTrue(os.path.exists(output_file), "Output file should exist")
        
        # Check content
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("1000", content, "Should show 1000 issues")
            self.assertIn("virtualScroll", content, "Should have virtual scrolling")
    
    def test_empty_input(self):
        """Test generators with empty input"""
        empty_data = {"issues": []}
        empty_file = os.path.join(self.test_dir, "empty.json")
        with open(empty_file, 'w') as f:
            json.dump(empty_data, f)
        
        output_file = os.path.join(self.test_dir, "empty_output.html")
        
        # Test standalone generator
        result = os.system(f"python3 generate/generate-standalone-virtual-dashboard.py {empty_file} {output_file}")
        self.assertEqual(result, 0, "Should handle empty input")
        
        with open(output_file, 'r') as f:
            content = f.read()
            # Dashboard shows "0 issues" instead of "No issues found"
            self.assertIn("0 issues", content, "Should show 0 issues")
    
    def test_malformed_input(self):
        """Test generators with malformed input"""
        malformed_file = os.path.join(self.test_dir, "malformed.json")
        with open(malformed_file, 'w') as f:
            f.write('{"issues": [{"bad": "data"')  # Invalid JSON
        
        output_file = os.path.join(self.test_dir, "malformed_output.html")
        
        # Test should fail gracefully
        result = os.system(f"python3 generate/generate-standalone-virtual-dashboard.py {malformed_file} {output_file} 2>/dev/null")
        self.assertNotEqual(result, 0, "Should fail with malformed input")
    
    def test_code_context(self):
        """Test generator with code context"""
        context_data = {
            "issues": [{
                "id": "test",
                "severity": "error",
                "message": "Test issue",
                "file": "test.cpp",
                "line": 10,
                "context": {
                    "before": ["line 8", "line 9"],
                    "line": "line 10 with issue",
                    "after": ["line 11", "line 12"]
                }
            }]
        }
        
        context_file = os.path.join(self.test_dir, "context.json")
        with open(context_file, 'w') as f:
            json.dump(context_data, f)
        
        output_file = os.path.join(self.test_dir, "context_output.html")
        result = os.system(f"python3 generate/generate-standalone-virtual-dashboard.py {context_file} {output_file}")
        
        self.assertEqual(result, 0, "Should handle code context")
        
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("line 10 with issue", content, "Should include code context")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test files"""
        import shutil
        shutil.rmtree(cls.test_dir)


class TestGeneratorPerformance(unittest.TestCase):
    """Performance tests for generators"""
    
    def setUp(self):
        """Create performance test data"""
        self.test_dir = tempfile.mkdtemp()
        self.perf_data = {
            "issues": [
                {
                    "id": f"perf{i}",
                    "severity": "style",
                    "message": f"Performance test issue {i}",
                    "file": f"perf{i % 100}.cpp",
                    "line": i % 1000
                }
                for i in range(10000)
            ]
        }
        
        self.perf_file = os.path.join(self.test_dir, "perf.json")
        with open(self.perf_file, 'w') as f:
            json.dump(self.perf_data, f)
    
    def test_generation_time(self):
        """Test that generation completes in reasonable time"""
        import time
        
        output_file = os.path.join(self.test_dir, "perf_output.html")
        
        start_time = time.time()
        result = os.system(f"python3 generate/generate-standalone-virtual-dashboard.py {self.perf_file} {output_file}")
        end_time = time.time()
        
        self.assertEqual(result, 0, "Should complete successfully")
        self.assertLess(end_time - start_time, 5.0, "Should complete in under 5 seconds for 10k issues")
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.test_dir)


if __name__ == '__main__':
    unittest.main()