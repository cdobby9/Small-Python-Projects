import math

def is_prime(j):
    if j < 2: return 0
    for k in range(2, int(j**0.5) + 1):
        if j % k == 0: return 0
    return 1

def nth_prime(n):
    count_primes = 0
    i = 1
    while count_primes < n:
        i += 1
        if is_prime(i):
            count_primes += 1
    return i