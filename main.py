import kagglehub
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch

# Download latest version
path = kagglehub.dataset_download("sepandhaghighi/proton-exchange-membrane-pem-fuel-cell-dataset")

# Define the base path to the extracted dataset # Replace with your extracted folder path
cycling_potential_folder = os.path.join(path, 'Activation Test MEA Cycling Potential')

print(cycling_potential_folder)

# Initialize a list to store data from all CSV files
all_data = []

# Load and stack data from all CSV files
for file in os.listdir(cycling_potential_folder):
    if file.endswith('.csv'):
        file_path = os.path.join(cycling_potential_folder, file)
        data = pd.read_csv(file_path)
        data['file_id'] = file  # Add file identifier
        all_data.append(data)

# Combine all the data into one DataFrame
stacked_data = pd.concat(all_data, ignore_index=True)

# Add a sequential time index for each test file
stacked_data['time_step'] = stacked_data.groupby('file_id').cumcount()
print(stacked_data)

# Features and target preparation
features = stacked_data[['time_step', 'applied_voltage']].values
targets = stacked_data[['z_real', 'z_img']].values

# Normalize the features and targets
scaler_features = StandardScaler()
scaler_targets = StandardScaler()

features_scaled = scaler_features.fit_transform(features)
targets_scaled = scaler_targets.fit_transform(targets)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(features_scaled, targets_scaled, test_size=0.2, random_state=42)

# Convert to PyTorch tensors for time-series modeling
X_train_tensor = torch.tensor(X_train, dtype=torch.float32).unsqueeze(1)  # Add sequence dimension
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32).unsqueeze(1)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

# Print shape of tensors to confirm successful preparation
print(f"Training Data Shape: {X_train_tensor.shape}, Target Shape: {y_train_tensor.shape}")
print(f"Testing Data Shape: {X_test_tensor.shape}, Target Shape: {y_test_tensor.shape}")
