from Specimens.first import factorial


def test_factorial():
    # Test case 1: factorial of 0 should be 1
    assert factorial(0) == 1

    # Test case 2: factorial of 5 should be 120
    assert factorial(5) == 120

    # Test case 3: factorial of 10 should be 3628800
    assert factorial(10) == 3628800


# Run the test
if __name__ == "__main__":
    test_factorial()
    print("All tests passed!")
