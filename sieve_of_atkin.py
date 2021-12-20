# !usr/bin/env python3

"""An implementation of the Sieve of Atkin algorithm in Python.
How the algorithm works can be read in the references below. 

References:
    - https://en.wikipedia.org/wiki/Sieve_of_Atkin

Note: Iteration for the algorithm is currently very slow due
to the range iterators not having the optimized limits,
wasting lots of loop iterations.
"""

from itertools import product


def sieve_of_atkin(limit: int) -> list[int]:
    """Returns the number of primes from 2 to a specified limit in a list.

    An algorithm for finding all primes less than or equal to the limit
    specified to the function.

    :param limit: The maximum value for a prime number.
    :type limit: int
    :return: The prime numbers less than or equal to the limit specified.
    :rtype: list[int]
    """

    sieve = {}
    results = [2, 3, 5]
    s = {1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59}

    # Iteration for ranges has to be improved to reduce the number
    # of computations performed by the algorithm.

    set_w = range(limit // 60 + 1)

    for w, x in product(set_w, s):
        n = 60 * w + x
        sieve[n] = False

    set_x, set_y = range(1, limit + 1), range(1, limit + 1, 2)

    for x, y in product(set_x, set_y):
        n = 4 * x ** 2 + y ** 2
        if n > limit:
            continue
        if n % 60 in {1, 13, 17, 29, 37, 41, 49, 53}:
            sieve[n] ^= True

    set_x, set_y = set_y, range(2, limit + 1, 2)

    for x, y in product(set_x, set_y):
        n = 3 * x ** 2 + y ** 2
        if n > limit:
            continue
        if n % 60 in {7, 19, 31, 43}:
            sieve[n] ^= True

    set_x, set_y = range(2, limit + 1), range(1, limit + 1)

    for x, y in product(set_x, set_y):
        if x <= y:
            continue
        n = 3 * x ** 2 - y ** 2
        if n > limit:
            continue
        if n % 60 in {11, 23, 47, 59}:
            sieve[n] ^= True

    for w, x in product(set_w, s):
        n = 60 * w + x
        if n < 7 or n ** 2 > limit:
            continue
        if sieve[n]:
            for w, x in product(set_w, s):
                c = n ** 2 * (60 * w + x)
                if c > limit:
                    continue
                sieve[c] = False

    for w, x in product(set_w, s):
        n = 60 * w + x
        if n < 7:
            continue
        if n > limit:
            break
        if sieve[n]:
            results.append(n)

    return results


def main(n: int) -> None:
    length = len(sieve_of_atkin(n))
    print(f"primes <= {n}: {length}")


if __name__ == "__main__":
    main(100)
