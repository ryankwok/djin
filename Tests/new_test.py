# Generated at 2024-06-18 01:12:01.908984
# Query:
# Please write a unit test in pytest that satisfies the following requirements:
# Please provide a description of the code to be written:returns a number between 1 and 6 with equal probability. please include tests to verify probability
# include this import at the top:
# from Specimens.{} import *
#
# Here is an example test using pytest: import pytest
from Specimens.new import *

@pytest.mark.parametrize("expected_count", [(1,2), (3,4), (5,6)])
def test_random_number_probability(expected_count):
    generator = random_number_generator()
    count_dict = {}
    
    for _ in range(10000):  # Run the test 10,000 times
        num = next(generator)
        if num not in count_dict:
            count_dict[num] = 1
        else:
            count_dict[num] += 1
    
    for expected, actual in zip(expected_count, list(count_dict.values())):
        assert abs(actual - (10000 / 6) * expected) < 50  # Allow a small margin of error due to randomness

@pytest.mark.parametrize("expected_range", [(1,6)])
def test_random_number_range(expected_range):
    generator = random_number_generator()
    numbers = [next(generator) for _ in range(10)]  # Run the test 10 times
    assert all(exp <= num <= sup for num, (exp, sup) in zip(numbers, [(expected_range[0], expected_range[1])] * 10))
