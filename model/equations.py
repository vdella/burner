import numpy as np
import matplotlib.pyplot as plt

# Constants
R = 8.314  # Universal gas constant, J/(mol*K)
F = 96485  # Faraday's constant, C/mol
T = 298.15  # Temperature, K (25°C)
n = 2  # Number of electrons transferred (for H2/O2 fuel cells)
E0 = 1.219  # Theoretical Nernst voltage, V
i0 = 1e-4  # Exchange current density, A/cm² (activation losses)
R_ohmic = 0.1  # Ohmic resistance, ohm*cm²
i_limit = 1.5  # Limiting current density, A/cm² (concentration losses)

# Current density range
def current_density():
    return np.linspace(0.01, i_limit, 500)

# Loss calculations
# Activation loss (Tafel equation)

def activation_loss():
    return (R * T / (n * F)) * np.log(current_density() / i0)

# Ohmic loss
def ohmic_loss():
    return R_ohmic * current_density()

# Concentration loss
def concentration_loss():
    return -(R * T / (n * F)) * np.log(1 - current_density() / i_limit)

# Total voltage

def output_voltage():
    voltage = E0 - activation_loss() - ohmic_loss() - concentration_loss()

    # Avoid NaNs or unrealistic values at very high current densities
    return np.where(current_density() < i_limit, voltage, np.nan)


if __name__ == "__main__":
    # Plotting the polarization curve
    plt.figure(figsize=(8, 6))
    plt.plot(current_density(), output_voltage(), label="PEMFC Polarization Curve", linewidth=2)
    plt.title("PEMFC Polarization Curve", fontsize=16)
    plt.xlabel("Current Density (A/cm²)", fontsize=14)
    plt.ylabel("Cell Voltage (V)", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
#
# # Constants
# R = 8.314  # Universal gas constant, J/(mol*K)
# F = 96485  # Faraday's constant, C/mol
# T = 313  # Operating temperature in K (adjust as per your conditions)
# n = 2  # Number of electrons per reaction
# PH2 = 1.5  # Partial pressure of hydrogen, atm
# PO2 = 1.0  # Partial pressure of oxygen, atm
# J_max = 1.5  # Maximum current density, A/cm²
# Rm = 0.01  # Membrane resistance, ohm*cm²
# Rc = 0.02  # Ionic resistance, ohm*cm²
#
# # Semi-empirical coefficients for activation losses
# epsilon_1 = -0.948
# epsilon_2 = 0.0034
# epsilon_3 = -0.0002
# epsilon_4 = 0.2
#
# # Nernst voltage calculation
# def nernst_voltage(PH2, PO2, T):
#     return 1.229 - 8.5e-4 * (T - 298.15) + 4.3085e-5 * T * np.log(PH2 * np.sqrt(PO2))
#
# # Activation losses
# def activation_loss(J):
#     CO2 = PO2 / (0.0821 * T)  # Oxygen concentration (ideal gas law)
#     icell = J  # Assuming current density is proportional to cell current
#     Va = (epsilon_1 + epsilon_2 * T + epsilon_3 * T * np.log(CO2) + epsilon_4 * T * np.log(icell))
#     return Va
#
# # Ohmic losses
# def ohmic_loss(J):
#     return J * (Rm + Rc)
#
# # Concentration losses
# def concentration_loss(J, J_max):
#     return -0.1 * np.log(1 - J / J_max)  # -b*ln(1 - J/J_max), with b=0.1 as an example
#
# # Overall voltage calculation
# def cell_voltage(J):
#     E = nernst_voltage(PH2, PO2, T)
#     Va = activation_loss(J)
#     Vohm = ohmic_loss(J)
#     Vc = concentration_loss(J, J_max)
#     V = E - Va - Vohm - Vc
#     return V
#
# # Current density range
# J = np.linspace(0.01, J_max, 500)
#
# # Compute voltage for each current density
# V = []
# for j in J:
#     try:
#         voltage = cell_voltage(j)
#         if voltage > 0:  # Avoid invalid values
#             V.append(voltage)
#         else:
#             V.append(np.nan)
#     except ValueError:
#         V.append(np.nan)  # Handle math domain errors for log(0)
#
# # Plot polarization curve
# plt.figure(figsize=(10, 6))
# plt.plot(J, V, label="Polarization Curve", linewidth=2)
# plt.title("PEMFC Polarization Curve", fontsize=16)
# plt.xlabel("Current Density (A/cm²)", fontsize=14)
# plt.ylabel("Cell Voltage (V)", fontsize=14)
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.legend(fontsize=12)
# plt.tight_layout()
# plt.show()
