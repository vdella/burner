import numpy as np
import taguchi
import pandas as pd
import matplotlib.pyplot as plt


parameters = {
    'number_of_cells': 65,
    'activation_area': 56,  # cm^2
    'nominal_operating_of_current': 133.3,  # A
    'nominal_operating_of_voltage': 45,  # V
    'operating_temperature': 338,  # K
    'nominal_air_flow_rate': 300,  # lpm
    'nominal_fuel_flow_rate': 50,  # lpm
    'fuel_supply_pressure': 1.5,  # bar
    'air_supply_pressure': 1  # bar
}


def output_voltage(P_h2, P_o2, T, epsilons, o2_concentration, i_cell, i_density, R_m, R_c, b, J_max):
    return (nernst(P_h2, P_o2, T)
            - activation_loss(epsilons, T, o2_concentration, i_cell)
            - ohmic_loss(i_density, R_m, R_c)
            - concentration_loss(b, i_density, J_max))


def nernst(P_h2, P_o2, T):
    """Calculates the reversible voltage of the cell using the Nernst equation.

    :param P_h2: partial pressure of hydrogen (atm).
    :param P_o2: partial pressure of oxygen (atm).
    :param T: operating temperature of the cell (K).  # TODO review units.

    :return: reversible voltage of the cell (V)."""

    env_temperature = 298.15
    return 1.22 - 0.85e-3*(T - env_temperature) + 4.3085e-5*T*np.log(P_h2 + 0.5*P_o2)  # TODO review euler cte.


def activation_loss(epsilons: tuple, T, o2_concentration, i_cell):
    """Calculates the activation loss of the cell. Indicates
    how slow is the reaction on the electrode surface.

    :param epsilons: MUST be a tuple of FOUR values. Those are the
     semi-empirically obtained parametric coefficients.
    :param T: operating temperature of the cell (K).
    :param o2_concentration: concentration of oxygen at the cathode catalytic interface (mol/cm^3).
    :param i_cell: cell current (A)."""

    return (epsilons[0]
            + epsilons[1]*T
            + epsilons[2]*T*np.log(o2_concentration)
            + epsilons[3]*T*np.log(i_cell))


def ohmic_loss(i_density, R_m, R_c):
    """Sum of the resistances against the flow of electrons and ions in the cell.

    :param i_density: current density. (A/m^2)
    :param R_m: electronic resistance of the cell (ohm.cm^2).
    :param R_c: ionic resistance of the cell (ohm.cm^2)."""

    return i_density * (R_m + R_c)


def concentration_loss(b, J, J_max):
    """Mass transfer. Output voltage of the fuel cell decreases
    according to the amount of current drawn from the PEMFC
    with other physical parameters.

    :param b: parametric coefficient (V).
    :param J: actual current density of the cell (A/cm^2).
    :param J_max: maximum current density of the cell (A/cm^2).
    :return: the mass transfer, AKA concentration loss."""

    return -b*np.log(1 - (J / J_max))


def actual_current_density_from(current):
    """Calculates the current density from the current and the area.

    :param current: current (A).
    :return: current density (A/cm^2)."""

    return current / parameters.get('activation_area')


def max_current_density():
    """Calculates the maximum current density of the cell.

    :return: maximum current density (A/cm^2)."""

    return parameters.get('nominal_operating_of_current') / parameters.get('activation_area')


def o2_concentration(P_air, T):
    """
    Calculates the O2 concentration at the cathode catalytic interface.

    :param P_air: Total pressure of air supply (atm or bar).
    :param T: Operating temperature (K).
    :return: Concentration of O2 (mol/cm^3).
    """
    # Air composition: 21% O2 by volume
    P_o2 = 0.21 * P_air  # Partial pressure of O2 in air
    R = 0.0821  # Universal gas constant (L·atm/(mol·K))

    # Convert concentration to mol/cm³ (1 L = 1000 cm³)
    C_o2 = (P_o2 / (R * T)) * (1 / 1000)  # Convert from mol/L to mol/cm³
    return C_o2


# Example Usage
if __name__ == "__main__":
    # Example current
    current = 100  # Replace with your desired current value (A)

    # Compute actual current density
    actual_i_density = actual_current_density_from(current)
    print(f"Actual Current Density: {actual_i_density} A/cm^2")

    # Compute O2 concentration
    o2_concentration = o2_concentration(parameters.get('air_supply_pressure'), parameters.get('operating_temperature'))
    print(f"O2 Concentration: {o2_concentration} mol/cm^3")

    results = list()
    for temp in taguchi.control_factors()['operating_temperature']:
        for fuel_rate in taguchi.control_factors()['fuel_flow_rate']:
            for air_rate in taguchi.control_factors()['air_flow_rate']:
                for fuel_p in taguchi.control_factors()['fuel_supply_pressure']:
                    P_H2 = fuel_p
                    P_O2 = parameters.get('air_supply_pressure') / (parameters.get('air_supply_pressure') + fuel_p)
                    E_nernst = nernst(P_H2, P_O2, temp)

                    V_a = activation_loss((0.2, 0.003, -0.001, 0.01), temp, o2_concentration, current)
                    V_ohm = ohmic_loss(actual_i_density, 0.003, 0.002)
                    V_c = concentration_loss(0.05, actual_i_density, max_current_density())

                    V_cell = E_nernst - V_a - V_ohm - V_c
                    print(f"Temperature: {temp}, Fuel Flow Rate: {fuel_rate}, Air Flow Rate: {air_rate}, Fuel Pressure: {fuel_p}, Cell Voltage: {V_cell}")

                    results.append((temp, fuel_rate, air_rate, fuel_p, V_cell))


    # Convert results to a structured array
    df = pd.DataFrame(results, columns=['Temperature (K)', 'Fuel Flow Rate (lpm)', 'Air Flow Rate (lpm)', 'Fuel Pressure (bar)', 'Cell Voltage (V)'])
    df.to_csv("PEMFC_simulation_results.csv", index=False)

    # Visualize data (example)
    plt.plot(taguchi.control_factors()['operating_temperature'], [res[4] for res in results if res[1] == 50 and res[2] == 300 and res[3] == 1.5], label='Fuel Rate 50 lpm, Air Rate 300 lpm, Pressure 1.5 bar')
    plt.xlabel("Temperature (K)")
    plt.ylabel("Cell Voltage (V)")
    plt.legend()
    plt.show()
