#
# Generated at 2024-06-17 01:07:57.397541
# Query:
# There was a problem running the code: ```
# def factorial(n):
#     """Compute the factorial of n"""
#     if n == 0:
#         return 1
#     else:
#         return n * factorial(n-1)
# 
# import pytest
# 
# @pytest.mark.parametrize("input_value, expected_output", [
#     (0, 1),
#     (5, 120),
#     (10, 3628800)
# ])
# def test_factorial(input_value, expected_output):
#     assert factorial(input_value) == expected_output
# 
# if __name__ == "__main__":
#     test_factorial()
#     print("All tests passed!")
# ```
# 
# The `error was: Traceback (most recent call last):
#   File "C:\Users\kwokd\Documents\1_PROJECTS\ai_game\Specimens\first.py", line 58, in <module>
#     test_factorial()
# TypeError: test_factorial() missing 2 required positional arguments: 'input_value' and 'expected_output'
# 
# 
# Please try again
#
# 
def factorial(n):
    '''Compute the factorial of n'''
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

import pytest

@pytest.mark.parametrize("n, expected_output", [
    (0, 1),
    (5, 120),
    (10, 3628800)
])
def test_factorial(n, expected_output):
    assert factorial(n) == expected_output

if __name__ == "__main__":
    pytest.main([__file__])
    print("All tests passed!")
