# nCx function (exact)
def nCr(n, r):
    if r < 0 or r > n:
        return 0
    num = 1
    den = 1
    for i in range(1, r + 1):
        num *= (n - (i - 1))
        den *= i
    return num // den  # integer combination

# Binomial PMF
def binom_pmf(n, p, x):
    return nCr(n, x) * (p ** x) * ((1 - p) ** (n - x))

# Cumulative sums
def binom_cdf_lower(n, p, x):
    total = 0
    for k in range(0, x + 1):
        total += binom_pmf(n, p, k)
    return total

def binom_cdf_upper(n, p, x):
    total = 0
    for k in range(x, n + 1):
        total += binom_pmf(n, p, k)
    return total

# Two-tailed p-value method used at A-level
def two_tailed_p(n, p, x):
    # probability of the observed outcome or anything equally/extremely unlikely
    px = binom_pmf(n, p, x)

    total = 0
    for k in range(0, n + 1):
        if binom_pmf(n, p, k) <= px + 1e-12:  # tiny tolerance
            total += binom_pmf(n, p, k)
    return total

# MAIN PROGRAM
print("BINOMIAL HYPOTHESIS TEST")

# Inputs
n = int(input("Enter n (number of trials): "))
p0 = float(input("Enter p0 under H0: "))
x_obs = int(input("Observed number of successes: "))
test_type = input("Test type? (less/greater/two): ").strip().lower()
alpha = float(input("Significance level (e.g., 0.05): "))

# Compute p-value
if test_type == "l":
    p_value = binom_cdf_lower(n, p0, x_obs)
elif test_type == "g":
    p_value = binom_cdf_upper(n, p0, x_obs)
elif test_type == "t":
    p_value = two_tailed_p(n, p0, x_obs)
else:
    print("Invalid test type!")
    raise SystemExit

print("\n===== RESULTS =====")
print("p-value =", p_value)

if p_value < alpha:
    print("Reject H0 at the", alpha, "level.")
else:
    print("Fail to reject H0 at the", alpha, "level.")
