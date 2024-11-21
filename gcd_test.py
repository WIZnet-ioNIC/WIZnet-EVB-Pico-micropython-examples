import math
import timeit
from collections import Counter


def gcd_euclidean(a, b):
    while b:
        a, b = b, a % b
    return a


def gcd_binary(a, b):
    if a == 0:
        return b
    if b == 0:
        return a

    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1

    while (a & 1) == 0:
        a >>= 1

    while b != 0:
        while (b & 1) == 0:
            b >>= 1
        if a > b:
            a, b = b, a
        b -= a

    return a << shift


def prime_factors(n):
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors


def prime_factors2(n):
    factors = []
    # Handle smallest prime factor (2) separately to allow incrementing d by 2 later
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # Use 6k +/- 1 optimization to reduce the number of iterations
    d = 3
    while d * d <= n:
        if n % d == 0:
            while n % d == 0:
                factors.append(d)
                n //= d
        d += 2
    if n > 1:
        factors.append(n)
    return factors


def gcd_prime_factors(a, b, func=prime_factors2):
    fa = Counter(func(a))
    fb = Counter(func(b))
    return math.prod(k ** min(fa[k], fb[k]) for k in set(fa) & set(fb))


# 테스트할 숫자 쌍
numbers = [(48, 18), (100, 75), (3918848, 1653264), (28871271685163, 17461204521323)]

# 각 방법에 대한 실행 시간 측정
for a, b in numbers:
    print(f"\nTesting GCD for {a} and {b}:")

    euclidean_time = timeit.timeit(lambda: gcd_euclidean(a, b), number=10000)
    print(f"Euclidean: {euclidean_time:.6f} seconds")

    math_gcd_time = timeit.timeit(lambda: math.gcd(a, b), number=10000)
    print(f"math.gcd: {math_gcd_time:.6f} seconds")

    binary_time = timeit.timeit(lambda: gcd_binary(a, b), number=10000)
    print(f"Binary GCD: {binary_time:.6f} seconds")

    prime_factors_time = timeit.timeit(lambda: gcd_prime_factors(a, b), number=10000)
    print(f"Prime factors: {prime_factors_time:.6f} seconds")
