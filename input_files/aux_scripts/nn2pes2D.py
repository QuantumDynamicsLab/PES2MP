''' Keep this file with .keras (NN_model_en) file and copy pes2mp.driver
file in the same folder. '''

import numpy as np
import os
import joblib
from tensorflow.keras.models import load_model
from pes2mp_driver import create_TrainableActivation, create_CustomDecayLayer

# ==========================
# USER OPTIONS:
# Set which predictions to run
# ==========================
DO_SINGLE = False    # Set to True to compute single-point prediction
DO_RANGE  = True    # Set to True to compute range/grid prediction

# ==========================
# Load scalers and model
# ==========================
feature_scaler = joblib.load(os.path.join('..', 'feature_scaler.pkl'))
target_scaler = joblib.load(os.path.join('..', 'target_scaler.pkl'))

TrainableActivation = create_TrainableActivation()
CustomDecayLayer = create_CustomDecayLayer()

model_name = 'NN_model_en.keras'
batch_size = 4096

model = load_model(model_name, custom_objects={
    'TrainableActivation': TrainableActivation,
    'CustomDecayLayer': CustomDecayLayer,
})

# ==========================
# Define input variable names
# ==========================
input_names = ['R', 'th']

# ==========================
# 1. Single-point input
# ==========================
num_outputs = 1
single_fmt = ["%.4f", "%.2f"] + ["%.4f"] * num_outputs

# ==========================
# 2. Grid/range input
# ==========================
ini_values = [1.0,     0]
fin_values = [50.1,   91]
step_sizes = [0.1,     5]

# ==========================
# Prediction: Single Point
# ==========================
if DO_SINGLE:
    single_input = np.array(single_point).reshape(1, -1)
    single_scaled = feature_scaler.transform(single_input)
    single_output_scaled = model.predict(single_scaled)
    single_output = target_scaler.inverse_transform(single_output_scaled)

    single_data = np.hstack((single_input, single_output))
    np.savetxt("NNp_single.dat", single_data, fmt=single_fmt,
               header=' '.join(input_names + ['Output']), comments='')

    print("✅ Single-point prediction saved as 'NNp_single.dat'.")

# ==========================
# Prediction: Grid Range
# ==========================
if DO_RANGE:
    input_ranges = [np.arange(start, stop, step)
                    for start, stop, step in zip(ini_values, fin_values, step_sizes)]

    mesh = np.meshgrid(*input_ranges, indexing='ij')
    grid_inputs = np.vstack([m.flatten() for m in mesh]).T
    grid_scaled = feature_scaler.transform(grid_inputs)

    grid_output_scaled = model.predict(grid_scaled, batch_size=batch_size)
    grid_output = target_scaler.inverse_transform(grid_output_scaled)

    grid_data = np.hstack((grid_inputs, grid_output))  # Assuming log(k)

    num_outputs = grid_output.shape[1] if grid_output.ndim > 1 else 1
    grid_fmt = single_fmt
    header = ' '.join(input_names + ([f'Output{i+1}' for i in range(num_outputs)] if num_outputs > 1 else ['Output']))

    np.savetxt("NNp.dat", grid_data, fmt=grid_fmt, header=header, comments='')

    print("✅ Range/grid prediction saved as 'NNp.dat'.")
#-----------------------------------------------------------------------------#
