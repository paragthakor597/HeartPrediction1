---
name: syntax-checker
description: Use this skill whenever the user provides, writes, edits, or asks about programming code and wants code formatting, cleanup, syntax checking, error detection, spelling or typo checking, indentation checking, punctuation checking, or code quality checking. Detect missing colons, semicolons, commas, brackets, quotes, indentation errors, syntax errors, and obvious spelling mistakes. Always use this skill when the user asks to check or clean code.
---
# Syntax checker
When the user asks to format or clean code:
Read the code carefully.
Fix incorrect indentation.
Fix unnecessary spaces.
Fix inconsistent line breaks.
Fix formatting around brackets, commas, operators, and functions.
Keep the code's logic unchanged.
Do not change variable names or program behavior.
Format the code consistently, similar to what a code formatter would do.
After formatting, show the cleaned code.
Briefly explain what formatting was changed.
Additional Syntax and Error Checks
Check for common syntax errors:
Missing :
Missing or incorrect ; where the programming language requires it
Missing or incorrect ,
Missing or mismatched (), [], and {}
Unclosed quotes
Incorrect indentation
Invalid syntax
Check for obvious spelling mistakes and typos in:
Function names
Variable names
Class names
Imports
Keywords
Commonly misspelled identifiers
Do not change intentional project-specific names or identifiers just because they look unusual.
When an error is found, report:
File name
Line number, when available
What is wrong
Suggested correction
If an appropriate syntax checker or linter is available, run it after making changes.
Do not say that the code has no errors unless the available syntax/lint check actually passes.
Keep the original program logic and behavior unchanged while fixing formatting and syntax issues.