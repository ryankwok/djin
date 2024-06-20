import pytest
from Specimens.second import is_palindrome


def test_empty_string():
    assert is_palindrome('') is True


def test_single_character():
    assert is_palindrome('a') is True
    assert is_palindrome('A') is True


def test_palindromic_strings():
    assert is_palindrome('racecar') is True
    assert is_palindrome('A man, a plan, a canal: Panama') is True
    assert is_palindrome('Was it a car or a cat I saw?') is True


def test_non_palindromic_strings():
    assert is_palindrome('hello') is False
    assert is_palindrome('Python') is False
    assert is_palindrome('not a palindrome') is False
