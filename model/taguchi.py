import numpy as np
import pandas as pd
from itertools import product


def control_factors():
    """Prints control factors as stated by the authors."""

    return {
        'operating_temperature': [313, 323, 333, 338, 343, 353],  # 6 levels
        'fuel_flow_rate': [50, 65, 85, 0, 0, 0],  # 3 levels
        'air_flow_rate': [300, 400, 500, 0, 0, 0],  # 3 levels
        'fuel_supply_pressure': [1.5, 2.0, 2.5, 0, 0, 0],  # 3 levels
    }

# return {
#     '1': pd.Series([313, 50, 300, 1.5], index=['A', 'B', 'C', 'D']),
#     '2': pd.Series([323, 65, 400, 2], index=['A', 'B', 'C', 'D']),
#     '3': pd.Series([333, 85, 500, 2.5], index=['A', 'B', 'C', 'D']),
#     '4': pd.Series([338, None, None, None], index=['A', 'B', 'C', 'D']),
#     '5': pd.Series([343, None, None, None], index=['A', 'B', 'C', 'D']),
#     '6': pd.Series([353, None, None, None], index=['A', 'B', 'C', 'D']),
# }

# Generate all combinations of levels for the factors
def combinations():
    factors = control_factors()

    # list(product(*control_factors.values()))
    return list(product(
        factors['operating_temperature'],
        factors['fuel_flow_rate'],
        factors['air_flow_rate'],
        factors['fuel_supply_pressure']
    ))


if __name__ == '__main__':
    cf = control_factors()
    dataframe = pd.DataFrame(cf)

    dataframe.to_csv('control_factors.csv', index=False)

    # Generate all combinations of levels for the factors
    all_combinations = list(product(*cf.values()))

    # Convert to a DataFrame
    df_combinations = pd.DataFrame(all_combinations, columns=list(cf.keys()))
    df_combinations.to_csv('combinations.csv', index=False)

    # Randomly sample a subset of rows to create an orthogonal array
    np.random.seed(42)  # For reproducibility
    orthogonal_array = df_combinations.sample(n=18)  # Example: Select 18 trials

    print("Orthogonal Array (Subset of Combinations):")
    print(orthogonal_array)

    # Add a column to store experiment results
    orthogonal_array['Result'] = np.nan  # Placeholder for experimental data

    print("Orthogonal Array with Results Column:")
    print(orthogonal_array)

    orthogonal_array['S/N Ratio'] = 10 * np.log10(orthogonal_array['Result']**2 / len(orthogonal_array))

    # Analyze mean S/N ratio by factor
    mean_snr_by_factor = orthogonal_array.groupby(list(cf.keys()))['S/N Ratio'].mean()

    # Identify optimal levels
    optimal_levels = mean_snr_by_factor.idxmax()

    print("Optimal Levels for Factors:")
    print(optimal_levels)

