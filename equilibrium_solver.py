import cmath
import math

def solve_quadratic(a, b, c):
    discriminant = (b**2) - 4*(a*c)
    if discriminant < 0:
        return None
    sol1 = (-b - math.sqrt(discriminant)) / (2*a)
    sol2 = (-b + math.sqrt(discriminant)) / (2*a)
    if sol1 > 0 and sol2 <= 0:
        return sol1
    elif sol2 > 0 and sol1 <= 0:
        return sol2
    elif sol1 > 0 and sol2 > 0:
        return min(sol1, sol2)
    else:
        return None

def calculate_weak_acid_ph(initial_ha_conc, ka_value):
    results = {
        "initial_ha_conc": initial_ha_conc,
        "ka_value": ka_value,
        "pH": None,
        "h_plus_eq": None,
        "approximation_used": False,
        "steps": [],
        "error": None
    }

    if not (initial_ha_conc > 0 and ka_value > 0):
        results["error"] = "Initial concentration and Ka value must be positive."
        return results

    steps = results["steps"]

    steps.append(f"**1. Write the Dissociation Reaction and ICE Table:**")
    steps.append(f"   For a weak acid HA, the dissociation is:")
    steps.append(f"   HA(aq) + H₂O(l) ⇌ H₃O⁺(aq) + A⁻(aq)")
    steps.append(f"   ")
    steps.append(f"   | Species    | Initial (M)      | Change (M) | Equilibrium (M) |")
    steps.append(f"   |------------|------------------|------------|-----------------|")
    steps.append(f"   | HA         | {initial_ha_conc:.4f}     | -x         | {initial_ha_conc:.4f} - x |")
    steps.append(f"   | H₃O⁺       | 0                | +x         | x               |")
    steps.append(f"   | A⁻         | 0                | +x         | x               |")
    steps.append(f"   ")

    steps.append(f"**2. Write the Acid Dissociation Constant (Ka) Expression:**")
    steps.append(r"   $K_a = \frac{[H_3O^+][A^-]}{[HA]}$")
    steps.append(f"   Substituting the equilibrium concentrations:")
    steps.append(fr"   ${ka_value:.2e} = \frac{{(x)(x)}}{{({initial_ha_conc:.4f} - x)}}$")
    steps.append(f"   ")

    # Attempt the small x approximation
    steps.append(f"**3. Attempt the Small 'x' Approximation:**")
    steps.append(f"   If 'x' is much smaller than the initial concentration of HA (typically if the initial concentration / $K_a$ > 100), we can approximate $({initial_ha_conc:.4f} - x) \\approx {initial_ha_conc:.4f}$.")

    approximation_ratio = initial_ha_conc / ka_value
    steps.append(fr"   Ratio (Initial Conc / $K_a$) = ${initial_ha_conc:.4f} / {ka_value:.2e} = {approximation_ratio:.2f}$")

    # Initialize h_plus_eq to None so it's defined before conditional blocks
    h_plus_eq = None
    x_approx = 0.0 # Initialize x_approx to prevent NameError in string formatting if ratio is low
    percent_dissociation = 0.0 # Initialize percent_dissociation to prevent NameError

    if approximation_ratio > 100:
        steps.append(f"   Since the ratio ({approximation_ratio:.2f}) is greater than 100, the approximation is likely valid.")
        x_approx = math.sqrt(ka_value * initial_ha_conc)

        # Calculate percent_dissociation only if approximation is attempted
        percent_dissociation = (x_approx / initial_ha_conc) * 100

        steps.append(fr"   Using the approximation: ${ka_value:.2e} = \frac{{x^2}}{{{initial_ha_conc:.4f}}}$")
        steps.append(fr"   $x^2 = {ka_value:.2e} \times {initial_ha_conc:.4f} = {(ka_value * initial_ha_conc):.2e}$")
        steps.append(fr"   $x = \sqrt{{{(ka_value * initial_ha_conc):.2e}}} = {x_approx:.4e}$ M")
        steps.append(f"   ")
        steps.append(f"   **Check Approximation Validity:**")
        # Corrected: Raw f-string fr"" for `\%` and double braces for `\text{...}`
        steps.append(fr"   Percent dissociation = $(x / \text{{Initial HA Conc}}) \times 100\% = ({x_approx:.4e} / {initial_ha_conc:.4f}) \times 100\% = {percent_dissociation:.2f}\%$")

        if percent_dissociation <= 5:
            results["approximation_used"] = True
            h_plus_eq = x_approx
            # Corrected: Use fr-string and ensure proper backslashes for LaTeX
            steps.append(fr"   Since the percent dissociation is {percent_dissociation:.2f}% (which is $\le 5\%$), the approximation is valid.")
        else:
            # Corrected: Use fr-string and ensure proper backslashes for LaTeX
            steps.append(fr"   Since the percent dissociation is {percent_dissociation:.2f}% (which is $> 5\%$), the approximation is **NOT** valid. We must use the quadratic formula.")
            # Fall through to quadratic solution
            h_plus_eq = None # Ensure it falls to quadratic if approximation is invalid
    else:
        steps.append(f"   Since the ratio ({approximation_ratio:.2f}) is less than or equal to 100, the approximation is likely **NOT** valid.")
        # h_plus_eq is already None from initialization, ready for quadratic
        # No percent_dissociation message needed here as approximation wasn't even attempted as primary method.


    # If h_plus_eq is still None, it means approximation was not used or failed, so use quadratic
    if h_plus_eq is None:
        steps.append(f"**4. Solve using the Quadratic Formula:**")
        steps.append(fr"   Rearrange the Ka expression: $x^2 = {ka_value:.2e} ({initial_ha_conc:.4f} - x)$")
        steps.append(fr"   $x^2 = {ka_value * initial_ha_conc:.2e} - {ka_value:.2e}x$")
        steps.append(fr"   $x^2 + {ka_value:.2e}x - {ka_value * initial_ha_conc:.2e} = 0$")

        a_quad = 1
        b_quad = ka_value
        c_quad = -ka_value * initial_ha_conc

        steps.append(f"   This is in the form $ax^2 + bx + c = 0$, where:")
        steps.append(f"   $a = {a_quad}$")
        steps.append(fr"   $b = {b_quad:.2e}$")
        steps.append(fr"   $c = {c_quad:.2e}$")

        steps.append(fr"   Using the quadratic formula: $x = \frac{{-b \pm \sqrt{{b^2 - 4ac}}}}{{2a}}$")

        x_quad = solve_quadratic(a_quad, b_quad, c_quad)

        if x_quad is None:
            results["error"] = "Could not find a valid positive concentration for H+ from quadratic equation."
            return results

        h_plus_eq = x_quad
        steps.append(fr"   $x = {x_quad:.4e}$ M")
        steps.append(f"   ")

    # Final pH calculation and conclusion
    if h_plus_eq is not None and h_plus_eq > 0:
        results["h_plus_eq"] = h_plus_eq
        results["pH"] = -math.log10(h_plus_eq)

        steps.append(f"**5. Calculate pH:**")
        steps.append(fr"   At equilibrium, $[H_3O^+] = x = {results['h_plus_eq']:.4e}$ M")
        steps.append(fr"   $pH = -log_{{10}}[H_3O^+] = -log_{{10}}({results['h_plus_eq']:.4e})$")
        steps.append(fr"   **$pH = {results['pH']:.2f}$**")
        steps.append(f"   ")
        steps.append(f"**Conclusion:** The pH of a {initial_ha_conc:.4f} M solution of a weak acid with $K_a = {ka_value:.2e}$ is **{results['pH']:.2f}**.")
    else:
        results["error"] = "Calculated H+ concentration was not positive. Check inputs."

    return results

if __name__ == '__main__':
    # --- Test Cases (You can run this file directly to test the logic) ---
    print("--- Test Case 1: Acetic Acid (Small x should be valid) ---")
    results1 = calculate_weak_acid_ph(0.10, 1.8e-5)
    if results1["error"]:
        print(f"Error: {results1['error']}")
    else:
        print(f"pH: {results1['pH']:.2f}")
        for step in results1['steps']:
            print(step)
    print("\n" + "="*50 + "\n")

    print("--- Test Case 2: Stronger Weak Acid (Small x might not be valid) ---")
    results2 = calculate_weak_acid_ph(0.010, 1.0e-3)
    if results2["error"]:
        print(f"Error: {results2['error']}")
    else:
        print(f"pH: {results2['pH']:.2f}")
        for step in results2['steps']:
            print(step)
    print("\n" + "="*50 + "\n")

    print("--- Test Case 3: Very Dilute Weak Acid (Quadratic almost certainly needed) ---")
    results3 = calculate_weak_acid_ph(0.0001, 1.8e-5)
    if results3["error"]:
        print(f"Error: {results3['error']}")
    else:
        print(f"pH: {results3['pH']:.2f}")
        for step in results3['steps']:
            print(f"{step}")
    print("\n" + "="*50 + "\n")

    print("--- Test Case 4: Invalid Input ---")
    results4 = calculate_weak_acid_ph(-0.1, 1.8e-5)
    if results4["error"]:
        print(f"Error: {results4['error']}")
    else:
        print(f"pH: {results4['pH']:.2f}")

