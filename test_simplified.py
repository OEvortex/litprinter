#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script to verify the simplified litprinter functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from litprinter import lit, litprint
from litprinter.core import LitPrintDebugger

def test_basic_functionality():
    print("Testing basic lit() functionality...")
    
    # Test 1: Simple string
    result = lit("Hello world")
    assert result == "Hello world", f"Expected 'Hello world', got {result}"
    
    # Test 2: Multiple arguments
    result = lit("arg1", "arg2", 123)
    assert result == ("arg1", "arg2", 123), f"Expected tuple, got {result}"
    
    # Test 3: Single non-string argument
    result = lit(42)
    assert result == 42, f"Expected 42, got {result}"
    
    # Test 4: No arguments
    result = lit()
    assert result is None, f"Expected None, got {result}"
    
    print("✓ Basic lit() functionality works")

def test_litprint_functionality():
    print("Testing basic litprint() functionality...")
    
    # Test 1: Simple string
    result = litprint("Hello from litprint")
    assert result == "Hello from litprint", f"Expected 'Hello from litprint', got {result}"
    
    print("✓ Basic litprint() functionality works")

def test_debugger_configuration():
    print("Testing debugger configuration...")
    
    # Test enable/disable
    debugger = LitPrintDebugger()
    debugger.disable()
    result = debugger("Should not print")
    assert result == "Should not print", "Return value should work even when disabled"
    
    debugger.enable()
    result = debugger("Should print")
    assert result == "Should print", "Return value should work when enabled"
    
    print("✓ Debugger configuration works")

def test_format_method():
    print("Testing format method...")
    
    debugger = LitPrintDebugger()
    formatted = debugger.format("test")
    assert isinstance(formatted, str), "Format should return a string"
    assert "test" in formatted, "Formatted string should contain the argument"
    
    print("✓ Format method works")

if __name__ == "__main__":
    print("Running simplified litprinter tests...\n")
    
    test_basic_functionality()
    test_litprint_functionality()
    test_debugger_configuration()
    test_format_method()
    
    print("\n✅ All tests passed! The simplified litprinter is working correctly.")