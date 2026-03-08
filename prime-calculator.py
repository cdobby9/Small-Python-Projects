import math

def is_prime(j):
    if j < 2:
        return 0
    for k in range(2, int(j**0.5) + 1):
        if j % k == 0:
            return 0
    return 1

def nth_prime(n):
    count_primes = 0
    i = 1
    while count_primes < n:
        i += 1
        if is_prime(i):
            count_primes += 1
    return i

def prime_position(p):
    if not is_prime(p):
        return None
    count_primes = 0
    i = 1
    while i <= p:
        i += 1
        if is_prime(i):
            count_primes += 1
        if i == p:
            return count_primes

mode = input("find nth prime \nor \nposition of a prime \n(enter n or p): ").strip().lower()

if mode == 'n':
    n = int(input("Enter n: "))
    print("The", n, "th prime is:", nth_prime(n))
elif mode == 'p':
    p = int(input("Enter a prime number: "))
    pos = prime_position(p)
    if pos is None:
        print(p, "is not prime")
    else:
        print(p, "is the", pos, "th prime.")
else:
    print("Invalid.")
