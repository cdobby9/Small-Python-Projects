import math

def willans_prime(n):
    total = 0
    for i in range(1, 2**n + 1):
        inner_sum = 0
        for j in range(1, i + 1):
            value = ((math.factorial(j - 1) + 1) / j)
            cos_value = math.cos(math.pi * value)
            inner_sum += math.floor(cos_value ** 2)
        total += math.floor(n / (1 + inner_sum))
    return total + 1
