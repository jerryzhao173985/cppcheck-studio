#!/usr/bin/env python3
"""
Simplified test suite for CPPCheck dashboard generators
Focus on basic functionality and successful execution
"""

import unittest
import json
import tempfile
import os
import sys
from pathlib import Path

class TestGeneratorsSimple(unittest.TestCase):
    """Test all core dashboard generators can run successfully"""
    
    @classmethod
    def setUpClass(cls):
        """Create test data files"""
        cls.test_dir = tempfile.mkdtemp()
        
        # Small test data
        cls.small_data = {
            "issues": [
                {
                    "id": "uninitvar",
                    "severity": "error",
                    "message": "Uninitialized variable: x",
                    "file": "test.cpp",
                    "line": 42
                },
                {
                    "id": "unusedVariable",
                    "severity": "style",
                    "message": "Unused variable: temp",
                    "file": "test.cpp",
                    "line": 15
                }
            ]
        }
        
        # Empty data
        cls.empty_data = {"issues": []}
        
        # Write test files
        cls.small_file = os.path.join(cls.test_dir, "small.json")
        with open(cls.small_file, 'w') as f:
            json.dump(cls.small_data, f)
            
        cls.empty_file = os.path.join(cls.test_dir, "empty.json")
        with open(cls.empty_file, 'w') as f:
            json.dump(cls.empty_data, f)
    
    def test_standalone_generator(self):
        """Test standalone virtual dashboard generator"""
        output_file = os.path.join(self.test_dir, "standalone.html")
        result = os.system(f"python3 generate/generate-standalone-virtual-dashboard.py {self.small_file} {output_file} >/dev/null 2>&1")
        self.assertEqual(result, 0, "Standalone generator should exit successfully")
        self.assertTrue(os.path.exists(output_file), "Output file should exist")
        self.assertGreater(os.path.getsize(output_file), 1000, "Output should not be empty")
    
    def test_production_generator(self):
        """Test production dashboard generator"""
        output_file = os.path.join(self.test_dir, "production.html")
        result = os.system(f"python3 generate/generate-production-dashboard.py {self.small_file} {output_file} >/dev/null 2>&1")
        self.assertEqual(result, 0, "Production generator should exit successfully")
        self.assertTrue(os.path.exists(output_file), "Output file should exist")
        self.assertGreater(os.path.getsize(output_file), 1000, "Output should not be empty")
    
    def test_virtual_scroll_generator(self):
        """Test virtual scroll generator"""
        output_file = os.path.join(self.test_dir, "virtual.html")
        result = os.system(f"python3 generate/generate-virtual-scroll-dashboard.py {self.small_file} {output_file} >/dev/null 2>&1")
        self.assertEqual(result, 0, "Virtual scroll generator should exit successfully")
        self.assertTrue(os.path.exists(output_file), "Output file should exist")
        self.assertGreater(os.path.getsize(output_file), 1000, "Output should not be empty")
    
    def test_empty_input(self):
        """Test generators handle empty input gracefully"""
        output_file = os.path.join(self.test_dir, "empty_out.html")
        result = os.system(f"python3 generate/generate-standalone-virtual-dashboard.py {self.empty_file} {output_file} >/dev/null 2>&1")
        self.assertEqual(result, 0, "Should handle empty input")
        self.assertTrue(os.path.exists(output_file), "Output file should exist")
    
    def test_deprecation_notice(self):
        """Test that deprecation notice exists"""
        notice_path = "generate/DEPRECATION_NOTICE.md"
        self.assertTrue(os.path.exists(notice_path), "Deprecation notice should exist")
        self.assertGreater(os.path.getsize(notice_path), 1000, "Deprecation notice should have content")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test files"""
        import shutil
        shutil.rmtree(cls.test_dir)


if __name__ == '__main__':
    # Run with minimal verbosity for cleaner output
    unittest.main(verbosity=1)