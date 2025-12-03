def nCr(n, r):
    if r < 0 or r > n:
        return 0
    num = 1
    den = 1
    for i in range(1, r + 1):
        num *= (n - i + 1)
        den *= i
    return num // den

def binom_pmf(n, p, x):
    return nCr(n, x) * (p ** x) * ((1 - p) ** (n - x))

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

def two_tailed_p(n, p, x):
    px = binom_pmf(n, p, x)
    total = 0
    for k in range(0, n + 1):
        if binom_pmf(n, p, k) <= px + 1e-12:
            total += binom_pmf(n, p, k)
    return total


#  Critical REgion

def critical_region_left(n, p, alpha):
    k = 0
    while k <= n and binom_cdf_lower(n, p, k) <= alpha:
        k += 1
    # The critical region is everything ≤ (k-1)
    return list(range(0, k))

def critical_region_right(n, p, alpha):
    k = n
    while k >= 0 and binom_cdf_upper(n, p, k) <= alpha:
        k -= 1
    # Critical region is everything ≥ (k+1)
    return list(range(k + 1, n + 1))

def critical_region_two_tailed(n, p, alpha):
    # Split α into two tails (A-level convention)
    left_alpha = alpha / 2
    right_alpha = alpha / 2

    left = critical_region_left(n, p, left_alpha)
    right = critical_region_right(n, p, right_alpha)
    return left, right




print("Binomial Hypothesis Testing")

n = int(input("Enter n (number of trials): "))
p0 = float(input("Enter p0 under H0: "))
x_obs = int(input("Observed successes: "))
test_type = input("Test type? (left/right/two): ").strip().lower()
alpha = float(input("Significance level (e.g., 0.05): "))

# p-value
if test_type == "left":
    p_value = binom_cdf_lower(n, p0, x_obs)
elif test_type == "right":
    p_value = binom_cdf_upper(n, p0, x_obs)
elif test_type == "two":
    p_value = two_tailed_p(n, p0, x_obs)
else:
    print("Invalid test type!")
    raise SystemExit

# Output 
print("\n===== RESULTS =====")
print("p-value =", p_value)

# Critical region calculation
print("\n===== CRITICAL REGION =====")
if test_type == "left":
    CR = critical_region_left(n, p0, alpha)
    print("Critical region:", CR)
    reject = x_obs in CR

elif test_type == "right":
    CR = critical_region_right(n, p0, alpha)
    print("Critical region:", CR)
    reject = x_obs in CR

elif test_type == "two":
    CR_left, CR_right = critical_region_two_tailed(n, p0, alpha)
    print("Left tail CR:", CR_left)
    print("Right tail CR:", CR_right)
    reject = (x_obs in CR_left) or (x_obs in CR_right)

# Conclusion
print("\n===== CONCLUSION =====")
if reject:
    print("Reject H0 at the", alpha, "level.")
else:
    print("Fail to reject H0 at the", alpha, "level.")
