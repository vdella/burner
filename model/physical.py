import numpy as np
import taguchi


parameters = {
    'number_of_cells': 65,
    'nominal_operating_of_current': 133.3,  # A
    'nominal_operating_of_voltage': 45,  # V
    'operating_temperature': 338,  # K
    'nominal_air_flow_rate': 300,  # lpm
    'nominal_fuel_flow_rate': 50,  # lpm
    'fuel_supply_pressure': 1.5,  # bar
    'air_supply_concentration': 1  # bar
}


def nernst(P_h2, P_o2, T):
    """Calculates the reversible voltage of the cell using the Nernst equation.

    :param P_h2: partial pressure of hydrogen.
    :param P_o2: partial pressure of oxygen.
    :param T: operating temperature of the cell.

    :return: reversible voltage of the cell."""

    env_temperature = 298.15
    return 1.22 - 0.85e-3*(T - env_temperature) + 4.3085e-5*T*np.log(P_h2/P_o2)  # TODO review euler cte.


def activation_loss(epsilons: tuple, T, o2_concentration, i_cell):
    """Calculates the activation loss of the cell. Indicates
    how slow is the reaction on the electrode surface.

    :param epsilons: MUST be a tuple of FOUR values. Those are the
     semi-empirically obtained parametric coefficients.
    :param T: operating temperature of the cell.
    :param o2_concentration: concentration of oxygen at the cathode catalytic interface.
    :param i_cell: cell current."""

    return (epsilons[0]
            + epsilons[1]*T
            + epsilons[2]*T*np.log(o2_concentration)
            + epsilons[3]*T*np.log(i_cell))


def ohmic_loss(i, R_m, R_c):
    """Sum of the resistances against the flow of electrons and ions in the cell.

    :param i: current density. (A/m^2)
    :param R_m: electronic resistance of the cell.
    :param R_c: ionic resistance of the cell."""

    return i * (R_m + R_c)


def concentration_loss(b, J, J_max):
    """Mass transfer. Output voltage of the fuel cell decreases
    according to the amount of current drawn from the PEMFc
    with other physical parameters.

    :param b: parametric coefficient.
    :param J: actual current density of the cell.
    :param J_max: maximum current density of the cell.
    :return: the mass transfer, AKA concentration loss."""

    return -b*np.log(1 - (J / J_max))
