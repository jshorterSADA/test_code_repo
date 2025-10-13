This is Repo is used to test the Jira_bug_agent the following are examples that can be used to test the code fix suggestions from the gemini-2.5-pro llm:

DEMONSTRATION: Application Log Outputs for Edge Cases
============================================================ SCENARIO: Normal successful addition
Input: add_two_numbers(5, 10) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=5, num2=10. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. 41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 5 and 10. Result: 15
Return Value: 15
============================================================ SCENARIO: Basic ValueError - non-numeric string
Input: add_two_numbers('hello', 5) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=hello, num2=5. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: None as first input
Input: add_two_numbers(None, 5) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=None, num2=5. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 An unexpected error occurred: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
Return Value: None
============================================================ SCENARIO: None as second input
Input: add_two_numbers(5, None) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=5, num2=None. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 An unexpected error occurred: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
Return Value: None
============================================================ SCENARIO: Both inputs None
Input: add_two_numbers(None, None) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=None, num2=None. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 An unexpected error occurred: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
Return Value: None
============================================================ SCENARIO: Empty string as first input
Input: add_two_numbers('', 5) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=, num2=5. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Empty string as second input
Input: add_two_numbers(5, '') Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=5, num2=. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Whitespace-only first input
Input: add_two_numbers(' ', 5) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1= , num2=5. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Tab and newline input
Input: add_two_numbers('\t\n', 5) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1= , num2=5. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Float string inputs
Input: add_two_numbers('3.14', '2.71') Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=3.14, num2=2.71. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Scientific notation
Input: add_two_numbers('1e5', '2e3') Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=1e5, num2=2e3. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Unicode full-width digits
Input: add_two_numbers('５', '３') Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=５, num2=３. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. 41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 5 and 3. Result: 8
Return Value: 8
============================================================ SCENARIO: Hexadecimal strings
Input: add_two_numbers('0xFF', '0x10') Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=0xFF, num2=0x10. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Very large numbers
Input: add_two_numbers('99999999999999999999999999999999999999999999999999', '11111111111111111111111111111111111111111111111111') Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=99999999999999999999999999999999999999999999999999, num2=11111111111111111111111111111111111111111111111111. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. 41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 99999999999999999999999999999999999999999999999999 and 11111111111111111111111111111111111111111111111111. Result: 111111111111111111111111111111111111111111111111110
Return Value: 111111111111111111111111111111111111111111111111110
============================================================ SCENARIO: Custom correlation ID with error
Input: add_two_numbers('invalid', 5) Kwargs: {'corrID': 'custom-test-id-123'} Log Output:
custom-test-id-123 - Function add_two_numbers called with num1=invalid, num2=5. custom-test-id-123 - Attempting to convert inputs to integers. correlation_ID:custom-test-id-123 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Empty correlation ID
Input: add_two_numbers('invalid', 5) Kwargs: {'corrID': ''} Log Output:
Function add_two_numbers called with num1=invalid, num2=5. Attempting to convert inputs to integers. Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: Potential log injection
Input: add_two_numbers('5\nFAKE ERROR: correlation_ID:hacker-id Something bad', 5) Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=5 FAKE ERROR: correlation_ID:hacker-id Something bad, num2=5. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
============================================================ SCENARIO: One valid, one invalid
Input: add_two_numbers(10, 'not_a_number') Log Output:
41131d34-334c-488a-bce2-a7642b27cf35 - Function add_two_numbers called with num1=10, num2=not_a_number. 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers. correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers.
Return Value: None
