import pandas as pd

# Load the data
# Load the data
# Replace 'your_file.csv' with your actual filename and select separation
data = pd.read_csv('PES.dat', sep='\s+' , header=None)


data = data.apply(pd.to_numeric, errors='coerce')
data.dropna(inplace=True) #removing rows with na values
data.reset_index(drop=True, inplace=True) # reset index

# Adding column names
data.columns =['R', 'theta', 'E']

R_col = 'R'
theta_col = 'theta'
E_col = 'E'

# Sort by theta, then by R
data = data.sort_values(by=[theta_col, R_col])

# Find the maximum R for each theta
max_R_indices = data.groupby(theta_col)[R_col].idxmax()

# Extract E at maximum R for each theta
E_at_max_R = data.loc[max_R_indices, [theta_col, E_col]].set_index(theta_col)[E_col]

# Subtract E at max R from all E values for the corresponding theta
data['E_cm'] = data.apply(lambda row: (row[E_col] - E_at_max_R[row[theta_col]])*219474.63, axis=1)

data = data.drop('E', axis=1)

# Save and inspect the resulting data
# Replace 'output_file.csv' with your desired output filename
data.to_csv('PES_cm.dat', index=False)

print("PES converted successfully. File saved to 'PES_cm.dat'.")
