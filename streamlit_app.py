import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate deflection
def calculate_deflection(r, L, a, f, k_c, E):
    """
    Calculate tool deflection based on machining parameters.
    r: Tool radius (in)
    L: Tool overhang length (in)
    a: Depth of cut (in)
    f: Feed rate (in/rev)
    k_c: Cutting force coefficient (psi)
    E: Modulus of elasticity (psi)
    """
    # Cutting force
    F_c = k_c * a * f
    # Moment of inertia
    I = (np.pi / 4) * (r**4)
    # Deflection
    delta = (F_c * L**3) / (3 * E * I)
    return F_c, delta

# Metal and tool material properties dictionary
metal_data = {
    "Aluminum": {"k_c": 50000, "E": 10e6, "Machinability": "Excellent", "Uses": "Aircraft parts, automotive components"},
    "Medium Carbon Steel": {"k_c": 200000, "E": 30e6, "Machinability": "Good", "Uses": "Shafts, gears, bolts"},
    "Hardened Steel": {"k_c": 300000, "E": 30e6, "Machinability": "Poor", "Uses": "Tooling, dies, cutting edges"},
    "Titanium Alloys": {"k_c": 400000, "E": 16e6, "Machinability": "Fair", "Uses": "Aerospace, medical implants"},
    "Bearing Bronzes": {"k_c": 80000, "E": 12e6, "Machinability": "Excellent", "Uses": "Bearings, bushings, thrust washers"},
}

tool_material_data = {
    "Steel (HSK)": {"E": 30e6, "Description": "Standard steel, widely used in HSK tooling."},
    "Carbide Bar": {"E": 90e6, "Description": "High-stiffness material for demanding applications."},
}

# App layout
st.title("Enhanced Tool Deflection Optimization App")

# Inputs
st.sidebar.header("Input Parameters")
material = st.sidebar.selectbox("Workpiece Material", list(metal_data.keys()))
tool_material = st.sidebar.selectbox("Tool Material", list(tool_material_data.keys()))
radius = st.sidebar.number_input("Tool Radius (in)", min_value=0.001, max_value=0.5, value=0.031, step=0.001, format="%.3f")
overhang_length = st.sidebar.number_input("Overhang Length (in)", min_value=0.1, max_value=12.0, value=4.0, step=0.1, format="%.1f")
depth_of_cut = st.sidebar.number_input("Depth of Cut (in)", min_value=0.001, max_value=1.0, value=0.05, step=0.001, format="%.3f")
feed_rate = st.sidebar.number_input("Feed Rate (in/rev)", min_value=0.001, max_value=0.1, value=0.01, step=0.001, format="%.3f")

# Retrieve material and tool properties
selected_metal = metal_data[material]
selected_tool_material = tool_material_data[tool_material]
k_c = selected_metal["k_c"]
E = selected_tool_material["E"]

# Calculate cutting force and deflection
cutting_force, deflection = calculate_deflection(radius, overhang_length, depth_of_cut, feed_rate, k_c, E)

# Display material properties and results
st.subheader("Material Properties")
st.write(f"**Selected Material:** {material}")
st.write(f"**Cutting Force Coefficient (\(k_c\)):** {k_c} psi")
st.write(f"**Machinability:** {selected_metal['Machinability']}")
st.write(f"**Typical Uses:** {selected_metal['Uses']}")

st.subheader("Tool Material Properties")
st.write(f"**Selected Tool Material:** {tool_material}")
st.write(f"**Modulus of Elasticity (\(E\)):** {E:.1e} psi")
st.write(f"**Description:** {selected_tool_material['Description']}")

st.subheader("Results")
st.write(f"**Cutting Force:** {cutting_force:.2f} lb")
st.write(f"**Deflection:** {deflection:.5f} in")

# Graph: Deflection vs Feed Rate for Fixed Radius
st.subheader("Deflection vs Feed Rate")
feed_rates = np.linspace(0.002, 0.02, 100)
deflections = [
    calculate_deflection(radius, overhang_length, depth_of_cut, f, k_c, E)[1] for f in feed_rates
]

fig, ax = plt.subplots()
ax.plot(feed_rates, deflections, label=f"Material: {material}")
ax.axhline(y=0.001, color="red", linestyle="--", label="Deflection Limit (0.001 in)")
ax.set_title("Deflection vs Feed Rate")
ax.set_xlabel("Feed Rate (in/rev)")
ax.set_ylabel("Deflection (in)")
ax.legend()
ax.grid(True)
st.pyplot(fig)
