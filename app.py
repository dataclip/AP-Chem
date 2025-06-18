import streamlit as st
from equilibrium_solver import calculate_weak_acid_ph # Import your solver function

st.set_page_config(
    page_title="AP Chem Weak Acid pH Solver & Explainer",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🔬 AP Chem Weak Acid pH Solver & Explainer")
st.markdown("---")

st.write("""
This tool helps you understand and calculate the pH of a weak acid solution.
Enter the initial concentration of the weak acid and its $K_a$ value below.
""")

st.header("1. Enter Your Weak Acid Data")

col1, col2 = st.columns(2)

with col1:
    acid_formula = st.text_input(
        "Weak Acid Formula (e.g., HA, CH₃COOH)",
        value="HA",
        help="This is for display purposes in the explanation."
    )

with col2:
    initial_conc_str = st.text_input(
        "Initial Concentration [HA] (M)",
        value="0.10",
        help="Enter the initial molarity of the weak acid."
    )
    
ka_value_str = st.text_input(
    "Ka Value (e.g., 1.8e-5, 6.3e-5)",
    value="1.8e-5",
    help="Enter the acid dissociation constant in scientific notation if preferred."
)


submit_button = st.button("Calculate pH & Explain!")

if submit_button:
    try:
        initial_ha_conc = float(initial_conc_str)
        ka_value = float(ka_value_str)

        if initial_ha_conc <= 0 or ka_value <= 0:
            st.error("Please enter positive values for concentration and Ka.")
        else:
            st.markdown("---")
            st.header("2. Detailed Solution & Explanation")
            
            results = calculate_weak_acid_ph(initial_ha_conc, ka_value)

            if results["error"]:
                st.error(f"Calculation Error: {results['error']}")
            else:
                st.subheader(f"Results for {acid_formula} Solution:")
                st.write(f"**Initial [{acid_formula}]:** {results['initial_ha_conc']:.4f} M")
                st.write(f"**Ka Value:** {results['ka_value']:.2e}")
                st.write(f"**Equilibrium [H₃O⁺]:** {results['h_plus_eq']:.4e} M")
                st.write(f"**Calculated pH:** **{results['pH']:.2f}**")
                
                if results["approximation_used"]:
                    st.success("The 'small x' approximation was valid for this calculation.")
                else:
                    st.warning("The 'small x' approximation was NOT valid. The quadratic formula was used.")
                
                st.markdown("---")
                st.subheader("Step-by-Step Breakdown:")
                for step in results['steps']:
                    st.markdown(step) # Use st.markdown to render LaTeX, bold text etc.
                
    except ValueError:
        st.error("Invalid input. Please ensure concentration and Ka are valid numbers.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

st.markdown("---")
st.markdown("### How to Use:")
st.markdown("""
1.  Enter the initial molar concentration of your weak acid.
2.  Enter the $K_a$ value for that acid.
3.  Click "Calculate pH & Explain!" to get the full solution.

*Need help with other equilibrium problems? Stay tuned for more features!*
""")

st.markdown("---")
st.markdown("Created with ❤️ by your friendly Chemistry & Programming Coach.")
