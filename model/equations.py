import numpy as np
import matplotlib.pyplot as plt

# Constants
R = 8.314  # Universal gas constant (J/mol K)
F = 96485  # Faraday's constant (C/mol)
E0 = 1.229  # Nernst potential (V)
alpha = 0.5  # Charge transfer coefficient
P_H2 = 1.0  # Partial pressure of H2 (atm)
P_O2 = 1.0  # Partial pressure of O2 (atm)
P_ref = 1.0  # Reference pressure (atm)
I0 = 1e-3  # Exchange current density (A/cm^2)
R_ohm = 0.1  # Ohmic resistance (Ohm cm^2)
I_lim = 1.5  # Limiting current density (A/cm^2)
current_density = np.linspace(0.01, I_lim, 200)  # Range of current densities (A/cm^2)

# Temperature profiles (K)
temperatures = [313, 323, 333, 338, 343, 353]

# Function to calculate polarization curve
def calculate_voltage(T, current_density):
    b = 2.3 * (R * T / (alpha * F))
    E = E0 + (R * T / (2 * F)) * np.log(P_ref / (P_H2 * np.sqrt(P_O2)))
    eta_act = b * np.log(current_density / I0)
    eta_ohm = current_density * R_ohm
    eta_conc = (R * T / (2 * F)) * np.log(1 - (current_density / I_lim))
    voltage = E - eta_act - eta_ohm - eta_conc
    return voltage

if __name__ == '__main__':
    # Plotting polarization curves
    plt.figure(figsize=(10, 6))

    for T in temperatures:
        voltage = calculate_voltage(T, current_density)
        plt.plot(current_density, voltage, label=f'T = {T} K')

    plt.title('PEMFC Polarization Curves at Different Temperatures')
    plt.xlabel('Current Density (A/cm²)')
    plt.ylabel('Cell Voltage (V)')
    plt.grid(True)
    plt.legend()
    plt.show()
