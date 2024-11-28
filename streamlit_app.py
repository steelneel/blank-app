import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate deflection
def calculate_deflection(r, L, F, E):
    I = (np.pi / 4) * (r**4)  # Moment of inertia
    return (F * L**3) / (3 * E * I)

# Cutting force coefficients for different materials
material_kc = {
    "Aluminum": 50000,
    "Medium Carbon Steel": 200000,
    "Hardened Steel": 300000,
    "Titanium Alloys": 400000,
    "Bearing Bronzes": 80000,  # Added Bearing Bronzes
}

# App layout
st.title("Tool Deflection Optimization App")

# Inputs
st.sidebar.header("Input Parameters")
material = st.sidebar.selectbox("Material", list(material_kc.keys()))
radius = st.sidebar.slider("Tool Radius (in)", min_value=0.008, max_value=0.062, value=0.031, step=0.001)
overhang_length = st.sidebar.slider("Overhang Length (in)", min_value=1.0, max_value=6.0, value=4.0, step=0.1)
depth_of_cut = st.sidebar.slider("Depth of Cut (in)", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
feed_rate = st.sidebar.slider("Feed Rate (in/rev)", min_value=0.002, max_value=0.02, value=0.01, step=0.001)
modulus_of_elasticity = 30e6  # Steel (psi)

# Select cutting force coefficient based on material
kc = material_kc[material]

# Calculate cutting force and deflection
cutting_force = kc * depth_of_cut * feed_rate
deflection = calculate_deflection(radius, overhang_length, cutting_force, modulus_of_elasticity)

# Display results
st.subheader("Results")
st.write(f"Selected Material: {material}")
st.write(f"Cutting Force Coefficient: {kc} psi")
st.write(f"Cutting Force: {cutting_force:.2f} lb")
st.write(f"Deflection: {deflection:.5f} in")

# Graph: Deflection vs Feed Rate for Fixed Radius
st.subheader("Deflection vs Feed Rate")
feed_rates = np.linspace(0.002, 0.02, 100)
deflections = [calculate_deflection(radius, overhang_length, kc * depth_of_cut * f, modulus_of_elasticity) for f in feed_rates]

fig, ax = plt.subplots()
ax.plot(feed_rates, deflections, label=f"Material: {material}")
ax.axhline(y=0.001, color="red", linestyle="--", label="Deflection Limit (0.001 in)")
ax.set_title("Deflection vs Feed Rate")
ax.set_xlabel("Feed Rate (in/rev)")
ax.set_ylabel("Deflection (in)")
ax.legend()
ax.grid(True)
st.pyplot(fig)
