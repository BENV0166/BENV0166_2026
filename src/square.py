def square(x):
    """
    Return the square of a value x
    """
    return x**2

def slow_square(x):
    """
    Return the square of a value x after doing a bunch of needless calculations
    """

    # Perform needless calculations
    A = 1
    for i in range(200):
        A += 1

    return x**2