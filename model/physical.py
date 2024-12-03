import numpy as np
import matplotlib.pyplot as plt

# Constants
R = 8.314  # Universal gas constant, J/(mol*K)
F = 96485  # Faraday's constant, C/mol
T = 298.15  # Temperature, K (25°C)
n = 2  # Number of electrons transferred (for H2/O2 fuel cells)
E0 = 1.23  # Theoretical Nernst voltage, V
i0 = 1e-4  # Exchange current density, A/cm² (activation losses)
R_ohmic = 0.1  # Ohmic resistance, ohm*cm²
i_limit = 1.5  # Limiting current density, A/cm² (concentration losses)

# Current density range
current_density = np.linspace(0.01, i_limit, 500)

# Loss calculations
# Activation loss (Tafel equation)
activation_loss = (R * T / (n * F)) * np.log(current_density / i0)

# Ohmic loss
ohmic_loss = R_ohmic * current_density

# Concentration loss
concentration_loss = -(R * T / (n * F)) * np.log(1 - current_density / i_limit)

# Total voltage
voltage = E0 - activation_loss - ohmic_loss - concentration_loss

# Avoid NaNs or unrealistic values at very high current densities
voltage = np.where(current_density < i_limit, voltage, np.nan)

# Plotting the polarization curve
plt.figure(figsize=(8, 6))
plt.plot(current_density, voltage, label="PEMFC Polarization Curve", linewidth=2)
plt.title("PEMFC Polarization Curve", fontsize=16)
plt.xlabel("Current Density (A/cm²)", fontsize=14)
plt.ylabel("Cell Voltage (V)", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
