"""
Basic tests for the LitPrinter package.
"""

import io
import sys
import builtins

import pytest

from litprinter import litprint, lit, cprint
from litprinter.colors import Colors


def test_litprint_basic():
    """Test basic functionality of litprint."""
    # Redirect stdout to capture output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        # Call litprint with a simple string
        litprint("Hello, world!")
        
        # Get the output
        output = captured_output.getvalue()
        
        # Check that the output contains our string
        assert "Hello, world!" in output
        
        # Check that it has the LIT prefix
        assert "LIT" in output
    finally:
        # Reset stdout
        sys.stdout = sys.__stdout__


def test_lit_basic():
    """Test basic functionality of lit."""
    # Redirect stdout to capture output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        # Call lit with a simple string
        lit("Hello, world!")
        
        # Get the output
        output = captured_output.getvalue()
        
        # Check that the output contains our string
        assert "Hello, world!" in output
        
        # Check that it has the LIT prefix
        assert "LIT" in output
    finally:
        # Reset stdout
        sys.stdout = sys.__stdout__


def test_cprint_markup():
    """Test the cprint function with simple markup."""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        cprint("[red]Error[/red] message")
        output = captured_output.getvalue()
        assert "Error" in output
        assert "\x1b[31m" in output  # red ANSI code
    finally:
        sys.stdout = sys.__stdout__


def test_color_synonyms_and_parse():
    """Ensure color synonyms and parsing work."""

    # grey/gray synonyms
    assert Colors.from_name("lightgrey") == Colors.from_name("lightgray")
    assert Colors.from_name("darkgrey") == Colors.from_name("darkgray")
    assert Colors.from_name("slategrey") == Colors.from_name("slategray")

    # Parsing of names and hex values should match explicit calls
    assert Colors.parse("red") == Colors.from_name("red")
    assert Colors.parse("#ff0000") == Colors.from_hex("ff0000")
    assert Colors.bg_parse("lightgrey") == Colors.bg_from_name("lightgrey")


def test_cprint_as_print():
    """cprint should work as a drop-in replacement for print."""

    captured_output = io.StringIO()
    original_print = builtins.print
    builtins.print = cprint
    sys.stdout = captured_output
    try:
        print("[green]OK[/green]", flush=True)
        assert captured_output.getvalue() == f"{Colors.GREEN}OK{Colors.RESET}\n"
    finally:
        builtins.print = original_print
        sys.stdout = sys.__stdout__
