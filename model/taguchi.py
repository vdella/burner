import numpy as np
import pandas as pd
from itertools import product
from physical import *


def control_factors():
    """Retrieves control factors as stated by the authors."""

    return {
        "operating_temperature": [('1', 313), ('2', 323), ('3', 333), ('4', 338), ('5', 343), ('6', 353)],  # 6 levels
        "fuel_flow_rate": [('1', 50), ('2', 65), ('3', 85), ('4', None), ('5', None), ('6', None)],  # 3 levels
        "air_flow_rate": [('1', 300), ('2', 400), ('3', 500), ('4', None), ('5', None), ('6', None)],  # 3 levels
        "fuel_supply_pressure": [('1', 1.5), ('2', 2.0), ('3', 2.5), ('4', None), ('5', None), ('6', None)],  # 3 levels
    }


def combinations():
    """Generate all possible combinations of control factors, without
    using null objects. MUST return 162 possibilities."""
    factors = control_factors()

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


def orthogonal_array():
    """
    Builds an orthogonal array by sampling from all combinations.
    Outputs 18 rows with placeholders for observed values and S/N ratios.
    """
    # Generate all possible combinations
    all_combs = combinations()
    all_combs_df = pd.DataFrame(all_combs, columns=['A', 'B', 'C', 'D'])  # Convert to DataFrame

    # Randomly sample 18 rows for the orthogonal array
    np.random.seed(42)  # Set seed for reproducibility
    orthogonal_sample = all_combs_df.sample(n=18).reset_index(drop=True)

    # Add columns for observed values and S/N ratios (initially placeholders)
    orthogonal_sample['Observed values'] = np.nan  # Placeholder for experimental results
    orthogonal_sample['S/N Ratio'] = np.nan  # Placeholder for S/N ratio

    # Return the constructed orthogonal array
    return orthogonal_sample


if __name__ == '__main__':
    # Generate all combinations
    print("\nAll Combinations:")
    all_combs = combinations()
    df_combinations = pd.DataFrame(all_combs, columns=['A', 'B', 'C', 'D'])
    print(df_combinations)
    df_combinations.to_csv('all_combinations.csv', index=False)

    # Update the orthogonal array with results
    oa = orthogonal_array()
    df_combinations = pd.DataFrame(oa, columns=['A', 'B', 'C', 'D', 'Observed values'])
    df_combinations.to_csv('orthogonal_array.csv', index=False)