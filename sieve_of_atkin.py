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
from collections import defaultdict
from itertools import product
from math import isqrt


def sieve_of_atkin(limit: int) -> list[int]:
    """Returns the number of primes from 2 to a specified limit in a list.

    An algorithm for finding all primes less than or equal to the limit
    specified to the function. The algorithm works by not only marking
    multiples of a number, but also multiples of its square, and checking
    modulus 60 remainders.

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

    wheel = {1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59}
    sieve, lim = defaultdict(bool), isqrt(limit) + 1
    xset, yset = range(1, isqrt(limit // 4) + 1), range(1, lim, 2)

    for x, y in product(xset, yset):
        n = 4*x*x + y*y
        if n <= limit and n % 60 in {1, 13, 17, 29, 37, 41, 49, 53}:
            sieve[n] ^= True

    xset, yset = range(1, isqrt(limit // 3) + 1), range(2, lim, 2)

    for x, y in product(xset, yset):
        n = 3*x*x + y*y
        if n <= limit and n % 60 in {7, 19, 31, 43}:
            sieve[n] ^= True

    lim = isqrt(limit * 2 + 3) // 2 + 1

    for x in range(2, lim):
        for y in range(1, x):
            n = 3*x*x - y*y
            if n <= limit and n % 60 in {11, 23, 47, 59}:
                sieve[n] ^= True

    wset, nwset = range(0, limit, 60), range(0, limit // 49, 60)

    for w, x in product(wset, wheel):
        npow = (n := w+x) * n
        if npow < limit and sieve[n]:
            for w, x in product(nwset, wheel):
                if (c := npow * (w + x)) <= limit:
                    sieve[c] = False

    results = [2, 3, 5]

    for w, x in product(wset, wheel):
        if (n := w+x) > limit:
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
    main(250000)
