# !usr/bin/env python3

"""An implementation of the Sieve of Atkin algorithm in Python.
How the algorithm works can be read in the references below. 

References:
    - https://en.wikipedia.org/wiki/Sieve_of_Atkin

Note: Iteration for the algorithm is currently very slow due
to the range iterators not having the optimized limits,
wasting lots of loop iterations.
"""

import cProfile
import doctest
import pstats
from itertools import product
from math import isqrt, sqrt


def sieve_of_atkin(limit: int) -> list[int]:
    """Returns the number of primes from 2 to a specified limit in a list.

    An algorithm for finding all primes less than or equal to the limit
    specified to the function.

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

    sieve = {}
    s = {1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59}
    results = [2, 3, 5]

    wset = range(0, limit + 1, 60)

    for w, x in product(wset, s):
        n = w + x
        if n > limit:
            break
        sieve[n] = False

    xset = range(1, isqrt((limit - 1) // 4) + 1)
    yset = range(1, isqrt(limit - 4) + 1, 2)

    for x, y in product(xset, yset):
        n = 4 * x ** 2 + y ** 2
        if n <= limit and n % 60 in {1, 13, 17, 29, 37, 41, 49, 53}:
            sieve[n] ^= True

    xset = range(1, isqrt((limit - 1) // 3) + 1)
    yset = range(2, isqrt(limit - 3) + 1, 2)

    for x, y in product(xset, yset):
        n = 3 * x ** 2 + y ** 2
        if n <= limit and n % 60 in {7, 19, 31, 43}:
            sieve[n] ^= True

    lim2 = int((sqrt(limit * 2 + 3) + 1) / 2)

    for x in range(2, lim2):
        for y in range(1, x):
            n = 3 * x ** 2 - y ** 2
            if n <= limit and n % 60 in {11, 23, 47, 59}:
                sieve[n] ^= True

    nwset = range(0, limit // 49 - 1, 60)

    for w, x in product(wset, s):
        n = w + x
        npow = n ** 2
        if n >= 7 and npow < limit and sieve[n]:
            for w, x in product(nwset, s):
                c = npow * (w + x)
                if c <= limit:
                    sieve[c] = False

    for w, x in product(wset, s):
        n = w + x
        if n > limit:
            break
        if sieve[n]:
            results.append(n)

    return results


def main(n: int = 10_000) -> None:
    with cProfile.Profile() as pr:
        print(len(sieve_of_atkin(n)))
        pr.print_stats(pstats.SortKey.TIME)


if __name__ == "__main__":
    # doctest.testmod()
    main()
