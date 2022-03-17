# !usr/bin/env python3

"""An implementation of the Sieve of Atkin algorithm in Python.
How the algorithm works can be read in the references below.

References:
    - https://en.wikipedia.org/wiki/Sieve_of_Atkin
"""

import cProfile
import doctest
from itertools import product
import math
import pstats


def square(x: int) -> int:
    return x*x


def sieve_of_atkin(limit: int):
    """Returns the number of primes from 2 to a specified limit in a list.
    
    An algorithm for finding all primes less than or equal to the limit
    specified to the function. The algorithm works by not only marking
    multiples of a number, but also multiples of its square, and checking
    modulo 60 remainders.

    :param limit: The maximum value for a prime number.
    :type limit: int
    :return: All prime numbers less than or equal to the limit specified.
    :rtype: list[int]

    Examples:
    >>> sieve_of_atkin(5)
    [2, 3, 5]
    >>> sieve_of_atkin(10)
    [2, 3, 5, 7]
    >>> sieve_of_atkin(20)
    [2, 3, 5, 7, 11, 13, 17, 19]
    >>> sieve_of_atkin(40)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    For a very large limit, the number of primes can be tested by taking
    the length of the sequence or list returned by the function:
    >>> len(sieve_of_atkin(100_000))
    9592
    >>> len(sieve_of_atkin(200_000))
    17984
    """
    sieve = [False] * limit
    root = math.isqrt(limit) + 1
    squares = map(square, range(root))
    for x2, y2 in product(squares, repeat=2):
        n = 4*x2 + y2
        if n < limit and n % 60 in {1, 13, 17, 29, 37, 41, 49, 53}:
            sieve[n] ^= True
        n = 3*x2 + y2
        if n < limit and n % 60 in {7, 19, 31, 43}:
            sieve[n] ^= True
        if x2 > y2:
            n = 3*x2 - y2
            if n < limit and n % 60 in {11, 23, 47, 59}:
                sieve[n] ^= True
    results = [2, 3, 5]
    for i, prime in enumerate(sieve):
        if i > 1 and prime:
            results.append(i)
            for x in range(i*i, limit, i*i):
                sieve[x] = False
    return results


def main(n: int = 10_000) -> None:
    with cProfile.Profile() as pr:
        print(len(sieve_of_atkin(n)))
        pr.print_stats(pstats.SortKey.TIME)


if __name__ == "__main__":
    doctest.testmod()
    main(250_000)
