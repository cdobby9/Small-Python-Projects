print("Binomial Expansion: (1 + or - x)^n up to x^4")
print()

def parse_number(s):
    s = s.strip()
    if "/" in s:
        num, den = s.split("/")
        return float(num) / float(den)
    else:
        return float(s)

def to_fraction(x, max_denom=1000):
    sign = "-" if x < 0 else ""
    x = abs(x)
    best_num = 0
    best_den = 1
    min_error = 1e9

    for d in range(1, max_denom + 1):
        n = round(x * d)
        error = abs(x - n/d)
        if error < min_error:
            min_error = error
            best_num = n
            best_den = d
    if best_den == 1:
        return sign + str(best_num)
    else:
        return sign + str(best_num) + "/" + str(best_den)

n_str = input("Enter n (can be a fraction like 1/2 or -3/4): ")
sign = input("Enter sign (+ or -): ")

n = parse_number(n_str)
s = 1 if sign == "+" else -1

# ^0
term1 = 1

# ^1
term2 = n * s

# ^2
term3 = n * (n - 1) / 2 * (s ** 2)

# ^3
term4 = n * (n - 1) * (n - 2) / 6 * (s ** 3)

# ^4
term5 = n * (n - 1) * (n - 2) * (n - 3) / 24 * (s ** 4)

print("\nExpansion:")
print("= " + to_fraction(term1)
      + " + (" + to_fraction(term2) + ")x"
      + " + (" + to_fraction(term3) + ")x^2"
      + " + (" + to_fraction(term4) + ")x^3"
      + " + (" + to_fraction(term5) + ")x^4")

