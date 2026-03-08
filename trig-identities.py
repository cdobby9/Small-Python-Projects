# Trig Identity Simplifier for MicroPython
# Supports common A-level style equations such as:
# 3sin^2(x) - cos^2(x) = 2
# sin^2(x) + cos^2(x) = 5
# 2sin^2(2x) + 3cos^2(2x) = 1
#
# Current supported identity:
#   sin^2(theta) + cos^2(theta) = 1
# used in rearranged form as either:
#   cos^2(theta) = 1 - sin^2(theta)
#   sin^2(theta) = 1 - cos^2(theta)

def clean_number(n):
    if abs(n - int(n)) < 1e-10:
        return str(int(n))
    return str(n)

def split_top_level(expr):
    # Splits an expression into signed terms at top-level + and -
    # Example: "3sin^2(x)-cos^2(x)+2" -> ["3sin^2(x)", "-cos^2(x)", "+2"]
    expr = expr.replace(" ", "")
    if not expr:
        return []

    parts = []
    bracket = 0
    current = ""

    for i, ch in enumerate(expr):
        if ch == "(":
            bracket += 1
        elif ch == ")":
            bracket -= 1

        if i > 0 and bracket == 0 and (ch == "+" or ch == "-"):
            parts.append(current)
            current = ch
        else:
            current += ch

    if current:
        parts.append(current)

    return parts

def parse_coefficient(s):
    if s == "" or s == "+":
        return 1.0
    if s == "-":
        return -1.0
    if s.endswith("*"):
        s = s[:-1]
    return float(s)

def parse_term(term):
    # Returns (kind, angle, coeff)
    # kind can be: "const", "sin2", "cos2"
    term = term.replace(" ", "")

    # find first letter
    first_letter = -1
    for i, ch in enumerate(term):
        if ch.isalpha():
            first_letter = i
            break

    if first_letter == -1:
        return ("const", None, float(term))

    coeff_str = term[:first_letter]
    func_str = term[first_letter:]

    coeff = parse_coefficient(coeff_str)

    if func_str.startswith("sin^2(") and func_str.endswith(")"):
        angle = func_str[6:-1]
        return ("sin2", angle, coeff)

    if func_str.startswith("cos^2(") and func_str.endswith(")"):
        angle = func_str[6:-1]
        return ("cos2", angle, coeff)

    raise ValueError("Unsupported term: " + term)

def parse_expression(expr):
    # Stores as dict with keys:
    # ("const", None), ("sin2", angle), ("cos2", angle)
    terms = {}
    for part in split_top_level(expr):
        kind, angle, coeff = parse_term(part)
        key = (kind, angle)
        terms[key] = terms.get(key, 0.0) + coeff

    remove_zero_terms(terms)
    return terms

def remove_zero_terms(terms):
    zeros = []
    for k, v in terms.items():
        if abs(v) < 1e-10:
            zeros.append(k)
    for k in zeros:
        del terms[k]

def subtract_expressions(lhs, rhs):
    result = dict(lhs)
    for k, v in rhs.items():
        result[k] = result.get(k, 0.0) - v
    remove_zero_terms(result)
    return result

def apply_pythag_identity_once(expr_terms):
    # Looks for a*sin^2(x) + b*cos^2(x) and removes one of the pair
    # using either:
    #   cos^2(x) = 1 - sin^2(x)
    # or
    #   sin^2(x) = 1 - cos^2(x)
    angles = set()
    for kind, angle in expr_terms:
        if kind in ("sin2", "cos2"):
            angles.add(angle)

    for angle in angles:
        sin_key = ("sin2", angle)
        cos_key = ("cos2", angle)

        a = expr_terms.get(sin_key, 0.0)
        b = expr_terms.get(cos_key, 0.0)

        if abs(a) > 1e-10 and abs(b) > 1e-10:
            # Keep whichever has larger absolute coefficient
            # Eliminate the other using the identity
            if abs(a) >= abs(b):
                # replace b*cos^2(angle) with b*(1 - sin^2(angle))
                expr_terms[("const", None)] = expr_terms.get(("const", None), 0.0) + b
                expr_terms[sin_key] = a - b
                del expr_terms[cos_key]
                remove_zero_terms(expr_terms)
                return "Used cos^2(θ) = 1 - sin^2(θ) with θ = " + angle
            else:
                # replace a*sin^2(angle) with a*(1 - cos^2(angle))
                expr_terms[("const", None)] = expr_terms.get(("const", None), 0.0) + a
                expr_terms[cos_key] = b - a
                del expr_terms[sin_key]
                remove_zero_terms(expr_terms)
                return "Used sin^2(θ) = 1 - cos^2(θ) with θ = " + angle

    return None

def simplify_expression(expr_terms):
    steps = []
    while True:
        step = apply_pythag_identity_once(expr_terms)
        if step is None:
            break
        steps.append(step)
    return steps

def format_single_term(kind, angle, coeff):
    coeff_str = ""
    abs_coeff = abs(coeff)

    if kind == "const":
        return clean_number(coeff)

    if abs(abs_coeff - 1.0) < 1e-10:
        coeff_str = "-" if coeff < 0 else ""
    else:
        coeff_str = ("-" if coeff < 0 else "") + clean_number(abs_coeff)

    if kind == "sin2":
        return coeff_str + "sin^2(" + angle + ")"
    if kind == "cos2":
        return coeff_str + "cos^2(" + angle + ")"

    return ""

def format_expression(expr_terms):
    if not expr_terms:
        return "0"

    trig_terms = []
    const_terms = []

    for (kind, angle), coeff in expr_terms.items():
        if kind == "const":
            const_terms.append((kind, angle, coeff))
        else:
            trig_terms.append((kind, angle, coeff))

    # Sort for consistent output
    trig_terms.sort(key=lambda t: (t[0], t[1]))
    const_terms.sort(key=lambda t: t[0])

    ordered = trig_terms + const_terms

    out = ""
    for i, (kind, angle, coeff) in enumerate(ordered):
        if abs(coeff) < 1e-10:
            continue

        term_str = format_single_term(kind, angle, coeff)

        if i == 0:
            out += term_str
        else:
            if coeff >= 0:
                out += " + " + term_str
            else:
                # remove leading minus because separator already shows it
                if term_str.startswith("-"):
                    term_str = term_str[1:]
                out += " - " + term_str

    return out if out else "0"

def isolate_if_possible(expr_terms):
    # expr_terms represents expression = 0
    # If there's exactly one trig term, isolate it
    trig_keys = []
    const_value = expr_terms.get(("const", None), 0.0)

    for k in expr_terms:
        if k[0] != "const":
            trig_keys.append(k)

    if len(trig_keys) == 1:
        k = trig_keys[0]
        coeff = expr_terms[k]
        rhs = -const_value

        left = format_single_term(k[0], k[1], coeff)
        right = clean_number(rhs)
        return left + " = " + right

    return format_expression(expr_terms) + " = 0"

def simplify_trig_equation(equation):
    equation = equation.replace(" ", "")
    if "=" not in equation:
        return "Error: equation must contain '='", []

    lhs_str, rhs_str = equation.split("=", 1)

    lhs = parse_expression(lhs_str)
    rhs = parse_expression(rhs_str)

    combined = subtract_expressions(lhs, rhs)   # now combined = 0
    steps = simplify_expression(combined)
    final_equation = isolate_if_possible(combined)

    return final_equation, steps

# ---------------------------
# Example interactive loop
# ---------------------------

def main():
    print("Trig Identity Simplifier")
    print("Supported forms: constants, sin^2(...), cos^2(...)")
    print("Example: 3sin^2(x)-cos^2(x)=2")
    print()

    while True:
        eq = input("Enter equation (or 'quit'): ")
        if eq.lower() == "quit":
            break

        try:
            result, steps = simplify_trig_equation(eq)
            print("Simplified:", result)

            if steps:
                print("Identities used:")
                for i, step in enumerate(steps, 1):
                    print(str(i) + ".", step)
            else:
                print("No supported trig identity was applied.")

        except Exception as e:
            print("Error:", e)

        print()

main()