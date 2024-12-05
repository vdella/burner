import numpy as np
import pandas as pd
from itertools import product
from equations import *
from factors import control_factors


def combinations():
    """Generate all possible combinations of control factors, without
    using null objects. MUST return 162 possibilities."""
    factors = control_factors.copy()

    alpha_keys = {
        'operating_temperature': 'A',
        'fuel_flow_rate': 'B',
        'air_flow_rate': 'C',
        'fuel_supply_pressure': 'D'
    }

    total = {
        "A": [],
        "B": [],
        "C": [],
        "D": [],
    }


    for key in factors.keys():
        total[alpha_keys[key]] = [x for x in factors[key] if x[1] is not None]

    return list(product(*total.values()))


def calculate_result(temp, fuel_flow, air_flow, pressure):
    """
    Calculate the polarization curve result based on input parameters.
    Modify as needed for your exact calculation logic.
    """
    # Example: Adjust these calculations based on your mapping
    R_ohmic = pressure / 2  # Example adjustment
    i_limit = fuel_flow / 100  # Example adjustment
    voltage = E0 - activation_loss() - ohmic_loss() - concentration_loss()
    # Return a single representative value, e.g., max voltage or voltage at a specific current density
    return np.nanmax(voltage)


def results():
    # Generate all possible combinations
    all_combs = combinations()
    combination_dataframe = pd.DataFrame(all_combs, columns=['A', 'B', 'C', 'D'])  # Convert to DataFrame

    # Add columns for observed values
    combination_dataframe['Observed values'] = np.nan  # Placeholder for experimental results

    # Iterate through the combinations and calculate the observed values
    for index, row in combination_dataframe.iterrows():
        temp = row['A'][1]  # Extract the value of temperature
        fuel_flow = row['B'][1]  # Extract the value of fuel flow rate
        air_flow = row['C'][1]  # Extract the value of air flow rate
        pressure = row['D'][1]  # Extract the value of fuel supply pressure

        # Calculate the result using the calculate_result function
        result = calculate_result(temp, fuel_flow, air_flow, pressure)
        combination_dataframe.at[index, 'Observed values'] = result  # Assign the result

    # Return the updated DataFrame
    return combination_dataframe


if __name__ == '__main__':
    # Generate the orthogonal array
    print("Orthogonal Array:")
    result_df = results()
    print(result_df)
    result_df.to_csv('results-array.csv', index=False)