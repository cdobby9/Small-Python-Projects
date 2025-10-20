print("Binomial Expansion: (1 ± x)^n up to x^4")
print()

def parse_number(s):
    s = s.strip()
    if "/" in s:
        num, den = s.split("/")
        return float(num) / float(den)
    else:
        return float(s)

n_str = input("Enter n (can be a fraction or negative): ")
sign = input("Enter sign (+ or -): ")

n = parse_number(n_str)

if sign == "+":
    s = 1
elif sign == "-":
    s = -1
else:
    print("No sign, assuming +")
    s = 1



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
print(f"= {term1:.4f} + ({term2:.4f})x + ({term3:.4f})x² + ({term4:.4f})x³ + ({term5:.4f})x⁴")