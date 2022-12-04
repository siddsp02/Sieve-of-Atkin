import cProfile
import doctest
from itertools import compress, count, product
from math import isqrt
from operator import mul
import pstats


def sieve_of_atkin(n: int) -> list[int]:
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
    sieve = bytearray(n)
    lim = isqrt(n) + 1
    squares = map(mul, range(lim), range(lim))
    for x2, y2 in product(squares, repeat=2):
        r = 4 * x2 + y2
        if r < n and r % 60 in {1, 13, 17, 29, 37, 41, 49, 53}:
            sieve[r] ^= True
        r = 3 * x2 + y2
        if r < n and r % 60 in {7, 19, 31, 43}:
            sieve[r] ^= True
        if x2 > y2:
            r = 3 * x2 - y2
            if r < n and r % 60 in {11, 23, 47, 59}:
                sieve[r] ^= True
    sieve[:6] = 0, 0, 1, 1, 0, 1
    for i in compress(count(), sieve):
        sieve[i * i :: i * i] = bytearray(len(range(i * i, n, i * i)))
    return list(compress(count(), sieve))


def main(n: int = 10_000) -> None:
    with cProfile.Profile() as pr:
        print(len(sieve_of_atkin(n)))
        pr.print_stats(pstats.SortKey.TIME)


if __name__ == "__main__":
    doctest.testmod()
    main(250_000)
