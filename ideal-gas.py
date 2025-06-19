import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# --- Constants ---
# Ideal Gas Constant (R) in L·atm/(mol·K)
# This value is commonly used in AP Chemistry
R = 0.0821

# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="Gas & KMT Simulator")

st.title("🧪 Gases & Kinetic Molecular Theory Simulator")
st.markdown("---")

# --- Ideal Gas Law Calculator Section ---
st.header("💡 Ideal Gas Law Calculator ($PV = nRT$)")
st.write("Enter any three values to calculate the fourth.")

col1_calc, col2_calc, col3_calc, col4_calc = st.columns(4)

with col1_calc:
    P_calc = st.number_input("Pressure (atm)", value=1.0, format="%.3f", key="P_calc")
with col2_calc:
    V_calc = st.number_input("Volume (L)", value=22.4, format="%.3f", key="V_calc")
with col3_calc:
    n_calc = st.number_input("Moles (mol)", value=1.0, format="%.3f", key="n_calc")
with col4_calc:
    T_calc = st.number_input("Temperature (K)", value=273.15, format="%.2f", key="T_calc")

# Option to select which variable to calculate
calc_option = st.radio(
    "Calculate which variable?",
    ("Pressure (P)", "Volume (V)", "Moles (n)", "Temperature (T)"),
    index=0,  # Default to calculating Pressure
    horizontal=True
)

st.markdown("---")

# Calculation logic
if st.button("Calculate"):
    try:
        if calc_option == "Pressure (P)":
            if V_calc == 0:
                st.error("Volume cannot be zero for calculation.")
            else:
                P_result = (n_calc * R * T_calc) / V_calc
                st.success(f"Calculated Pressure (P): **{P_result:.3f} atm**")
        elif calc_option == "Volume (V)":
            if P_calc == 0:
                st.error("Pressure cannot be zero for calculation.")
            else:
                V_result = (n_calc * R * T_calc) / P_calc
                st.success(f"Calculated Volume (V): **{V_result:.3f} L**")
        elif calc_option == "Moles (n)":
            if R * T_calc == 0:
                st.error("R or Temperature cannot be zero for calculation.")
            else:
                n_result = (P_calc * V_calc) / (R * T_calc)
                st.success(f"Calculated Moles (n): **{n_result:.3f} mol**")
        elif calc_option == "Temperature (T)":
            if n_calc * R == 0:
                st.error("Moles or R cannot be zero for calculation.")
            else:
                T_result = (P_calc * V_calc) / (n_calc * R)
                st.success(f"Calculated Temperature (T): **{T_result:.2f} K**")
    except Exception as e:
        st.error(f"Error during calculation: {e}. Please ensure inputs are valid (e.g., no division by zero).")

st.markdown("---")

# --- Kinetic Molecular Theory Simulator Section ---
st.header("💨 Kinetic Molecular Theory Visualizer")
st.write("Explore how temperature affects particle movement and pressure.")

# Simulator parameters
sim_volume_L = st.slider("Container Volume (L)", 1.0, 100.0, 50.0, 0.5)
sim_moles = st.slider("Number of Moles (mol)", 0.1, 5.0, 1.0, 0.1)
sim_temperature_K = st.slider(
    "Temperature (K)",
    100.0, 1000.0, 300.0, 10.0,
    help="Higher temperature means higher kinetic energy and faster particles."
)

num_particles = 100 # Fixed number of particles for visual consistency

# Calculate pressure based on current simulator parameters
sim_pressure_atm = (sim_moles * R * sim_temperature_K) / sim_volume_L

st.metric(label="Calculated Pressure (atm)", value=f"{sim_pressure_atm:.3f}")

# Visualizer
st.subheader("Gas Particle Visualization")
st.write(f"Showing {num_particles} conceptual particles in a {sim_volume_L:.1f} L container.")

# Create a figure and an axes for the plot
fig, ax = plt.subplots(figsize=(6, 6))

# Particle positions are random within a square representing the volume.
# For simplicity, we represent volume as a 2D area for visual.
# Particle "speed" or "agitation" can be represented by size or slight offset from center
# or even just by the conceptual text explanation.
# Let's use a subtle visual effect: a larger marker size for higher temperature.
base_marker_size = 50
max_marker_size = 300
marker_size = base_marker_size + (sim_temperature_K - 100) / (1000 - 100) * (max_marker_size - base_marker_size)

# Generate random particle positions within a normalized 0-1 range for the visual box
np.random.seed(42) # for reproducible particle positions
x_coords = np.random.rand(num_particles)
y_coords = np.random.rand(num_particles)

ax.scatter(x_coords, y_coords, s=marker_size, alpha=0.6, color='skyblue', edgecolors='blue')

# Set plot limits and labels
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([]) # Hide x-axis ticks
ax.set_yticks([]) # Hide y-axis ticks
ax.set_aspect('equal', adjustable='box')
ax.set_title(f"Temperature: {sim_temperature_K:.1f} K")
ax.text(0.05, 0.95, f"Volume: {sim_volume_L:.1f} L\nMoles: {sim_moles:.1f} mol",
        transform=ax.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=0.5, alpha=0.7))


st.pyplot(fig) # Display the plot

st.subheader("Kinetic Molecular Theory Explanation:")
st.markdown(f"""
* **Temperature and Kinetic Energy:** At higher temperatures ({sim_temperature_K:.1f} K), gas particles have higher average kinetic energy. This means they move faster and collide with the container walls more frequently and with greater force.
* **Pressure:** The pressure exerted by a gas is a result of these collisions with the container walls. As shown above, when temperature increases (and volume/moles are constant), the calculated pressure also increases ({sim_pressure_atm:.3f} atm).
* **Particle Representation:** The particles in the visualization are shown with a size that conceptually represents their increased agitation/kinetic energy at higher temperatures.
""")

st.markdown("---")
st.info("💡 Remember: This visualization is a simplified model. Real gas particles are much smaller and numerous!")


