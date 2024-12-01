import numpy as np
import pandas as pd

# Constants
R = 8.314  # Universal gas constant (J/mol·K)
F = 96485  # Faraday's constant (C/mol)
E0 = 1.229  # Standard reversible potential (V)
alpha = 0.5  # Charge transfer coefficient
i0_ref = 0.1  # Reference exchange current density (A/cm²) at 25°C
T_ref = 298.15  # Reference temperature in Kelvin (25°C)
activation_energy = 40000  # Activation energy for i0 (J/mol)


# Temperature-dependent exchange current density
def exchange_current_density(T):
    return i0_ref * np.exp((activation_energy / R) * (1 / T_ref - 1 / T))


# Temperature-dependent ohmic resistance
def ohmic_resistance(T, r_membrane_ref):
    return r_membrane_ref * (T_ref / T)


# PEMFC Voltage Model
def pemfc_voltage_expanded(i, T, i_max, r_membrane_ref):
    """Calculate expanded PEMFC voltage model."""
    i0 = exchange_current_density(T)
    R_ohmic = ohmic_resistance(T, r_membrane_ref)

    # Activation overpotential (Tafel equation)
    eta_activation = (R * T / (alpha * F)) * np.log(i / i0)

    # Ohmic overpotential
    eta_ohmic = i * R_ohmic

    # Concentration overpotential
    eta_concentration = - (R * T / F) * np.log(1 - i / i_max)

    # Cell voltage
    V = E0 - eta_activation - eta_ohmic + eta_concentration
    return V


# Define parameter ranges
current_density = np.linspace(0.01, 1.4, 100)  # Current density (A/cm²)
temperatures = np.linspace(298.15, 353.15, 10)  # Temperatures (K)
r_membrane_values = np.linspace(0.1, 0.3, 5)  # Membrane resistance (ohms·cm²)
i_max_values = np.linspace(1.0, 2.0, 5)  # Maximum current density (A/cm²)

# Generate data
data = []
for T in temperatures:
    for r_membrane in r_membrane_values:
        for i_max in i_max_values:
            for i in current_density:
                voltage = pemfc_voltage_expanded(i, T, i_max, r_membrane)
                data.append([i, T, i_max, r_membrane, voltage])

# Convert data to a pandas DataFrame
df = pd.DataFrame(data, columns=['current_density', 'temperature', 'i_max', 'r_membrane', 'voltage'])

# Save the data to a CSV file
df.to_csv("pemfc_simulation_data.csv", index=False)
print("Data saved to 'pemfc_simulation_data.csv'.")
