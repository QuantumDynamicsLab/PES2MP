''' Keep this file with .keras (NN_model_en) file and copy pes2mp.driver
file in the same folder. '''


import numpy as np
import os
import joblib  # for loading scalers efficiently
from tensorflow.keras.models import load_model
from pes2mp_driver import create_TrainableActivation, create_CustomDecayLayer

# Load scalers from parent directory
feature_scaler_path = os.path.join('..', 'feature_scaler.pkl')
target_scaler_path = os.path.join('..', 'target_scaler.pkl')

feature_scaler = joblib.load(feature_scaler_path)
target_scaler = joblib.load(target_scaler_path)

# Re-create custom layers for loading model
TrainableActivation = create_TrainableActivation()
CustomDecayLayer = create_CustomDecayLayer()


######################### INPUT VARIABLES ###############################
ini_values = [2.5, 0, 0, 0]      
fin_values = [50.1, 91, 91, 181]
step_sizes = [0.1, 30, 30, 30]

input_names = ['R', 'Phi', 'Th2', 'Th1']

precision = 4

model_name = 'NN_model_en.keras'
########################################################################

# Load model with custom objects
model = load_model(model_name, custom_objects={
    'TrainableActivation': TrainableActivation,
    'CustomDecayLayer': CustomDecayLayer,
})


# Create input grids dynamically for any number of dimensions
input_ranges = [np.arange(start, stop + step, step) for start, stop, step in zip(ini_values, fin_values, step_sizes)]
mesh = np.meshgrid(*input_ranges, indexing='ij')

inputs = np.vstack([m.flatten() for m in mesh]).T

# Scale inputs before prediction
inputs_scaled = feature_scaler.transform(inputs)

# Predict with scaled inputs
outputs_scaled = model.predict(inputs_scaled, batch_size=512)

# Inverse-transform outputs to original scale
outputs = target_scaler.inverse_transform(outputs_scaled)

# Save results to .npz
np.savez('NN_predictions.npz', inputs=inputs, outputs=outputs)

# Prepare header
num_inputs = inputs.shape[1]
num_outputs = outputs.shape[1] if outputs.ndim > 1 else 1

if len(input_names) != num_inputs:
    input_names = [f'Input{i+1}' for i in range(num_inputs)]

header_cols = input_names.copy()
if num_outputs == 1:
    header_cols.append('Output')
else:
    header_cols.extend([f'Output{i+1}' for i in range(num_outputs)])

header = ' '.join(header_cols)

data_to_save = np.hstack((inputs, outputs))
fmt = ['%.{}f'.format(precision)] * data_to_save.shape[1]

np.savetxt('NNp.dat', data_to_save, fmt=fmt, delimiter=' ', header=header, comments='')

print("Prediction and saving complete.")
