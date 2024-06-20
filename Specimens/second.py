# Generated at 2024-06-18 00:05:55.331145
# Query:
# Provide a python script that satisfies the following pytest unit test:
# 
# import pytest
# from Specimens.second import 
# import pytest
# from Specimens.second import is_palindrome
# 
# 
# def test_empty_string():
#     assert is_palindrome('') is True
# 
# 
# def test_single_character():
#     assert is_palindrome('a') is True
#     assert is_palindrome('A') is True
# 
# 
# def test_palindromic_strings():
#     assert is_palindrome('racecar') is True
#     assert is_palindrome('A man, a plan, a canal: Panama') is True
#     assert is_palindrome('Was it a car or a cat I saw?') is True
# 
# 
# def test_non_palindromic_strings():
#     assert is_palindrome('hello') is False
#     assert is_palindrome('Python') is False
#     assert is_palindrome('not a palindrome') is False
# 
#
# python
# Define the function to check if a string is a palindrome
def is_palindrome(s):
    # Remove non-alphanumeric characters and convert to lower case
    s = ''.join(e for e in s if e.isalnum()).lower()
    
    # Compare the string with its reverse, ignoring case sensitivity
    return s == s[::-1]
