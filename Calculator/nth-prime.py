import math

def is_prime(j):
    if j < 2: return 0
    for k in range(2, int(j**0.5) + 1):
        if j % k == 0: return 0
    return 1

def nth_prime(n):
    total = 0
    for i in range(1, 2**n + 1):
        inner_sum = sum(is_prime(j) for j in range(1, i + 1))
        total += math.floor(n / (1 + inner_sum))
    return total + 1
