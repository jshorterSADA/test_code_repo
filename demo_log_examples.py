#!/usr/bin/env python3
"""
Demo script to show log outputs for various edge cases in add_two_numbers function.
This will demonstrate what the application logs look like for different error scenarios.
"""

import sys
import os

# Add the parent directory to sys.path to import addNums
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from addNums import add_two_numbers

def demo_log_output(description, *args, **kwargs):
    """Helper function to demonstrate log output for different inputs."""
    print(f"\n{'='*60}")
    print(f"SCENARIO: {description}")
    print(f"{'='*60}")
    print(f"Input: add_two_numbers{args}")
    if kwargs:
        print(f"Kwargs: {kwargs}")
    print("Log Output:")
    print("-" * 40)
    
    result = add_two_numbers(*args, **kwargs)
    
    print("-" * 40)
    print(f"Return Value: {result}")
    print(f"{'='*60}")

if __name__ == "__main__":
    print("DEMONSTRATION: Application Log Outputs for Edge Cases")
    print("=" * 70)
    
    # 1. Normal successful case
    demo_log_output("Normal successful addition", 5, 10)
    
    # 2. Basic ValueError case
    demo_log_output("Basic ValueError - non-numeric string", "hello", 5)
    
    # 3. None inputs
    demo_log_output("None as first input", None, 5)
    demo_log_output("None as second input", 5, None)
    demo_log_output("Both inputs None", None, None)
    
    # 4. Empty string inputs
    demo_log_output("Empty string as first input", "", 5)
    demo_log_output("Empty string as second input", 5, "")
    
    # 5. Whitespace-only inputs
    demo_log_output("Whitespace-only first input", "   ", 5)
    demo_log_output("Tab and newline input", "\t\n", 5)
    
    # 6. Float string inputs (will cause ValueError)
    demo_log_output("Float string inputs", "3.14", "2.71")
    
    # 7. Scientific notation
    demo_log_output("Scientific notation", "1e5", "2e3")
    
    # 8. Unicode digits (full-width)
    demo_log_output("Unicode full-width digits", "５", "３")
    
    # 9. Hexadecimal strings
    demo_log_output("Hexadecimal strings", "0xFF", "0x10")
    
    # 10. Very large numbers (should work)
    demo_log_output("Very large numbers", "9" * 50, "1" * 50)
    
    # 11. Custom correlation ID with error
    demo_log_output("Custom correlation ID with error", "invalid", 5, corrID="custom-test-id-123")
    
    # 12. Empty correlation ID
    demo_log_output("Empty correlation ID", "invalid", 5, corrID="")
    
    # 13. Potential log injection attempt
    demo_log_output("Potential log injection", "5\nFAKE ERROR: correlation_ID:hacker-id Something bad", 5)
    
    # 14. Mixed valid and invalid
    demo_log_output("One valid, one invalid", 10, "not_a_number")