import pandas as pd

# Load the data
# Replace 'your_file.csv' with your actual filename and select separation
data = pd.read_csv('PES.dat', sep='\s+' , header=None)


data = data.apply(pd.to_numeric, errors='coerce')
data.dropna(inplace=True) #removing rows with na values
data.reset_index(drop=True, inplace=True) # reset index

# Adding column names
data.columns =['R', 'phi', 'th2', 'th1', 'E']

R_col = 'R'
phi_col = 'phi'
th2_col = 'th2'
th1_col = 'th1'
E_col = 'E'

# Sort by th1, th2, phi, then by R
data = data.sort_values(by=[th1_col, th2_col, phi_col, R_col])

# Group by unique combinations of phi, th2 and th1,
group_cols = [phi_col, th2_col, th1_col]

# Find the index of maximum R for each group
max_R_indices = data.groupby(group_cols)[R_col].idxmax()

# Extract E at maximum R for each group
E_at_max_R = data.loc[max_R_indices, group_cols + [E_col]].set_index(group_cols)[E_col]

# Subtract E at max R from all E values for the corresponding group
data['E_cm'] = data.apply(
    lambda row: (row[E_col] - E_at_max_R[tuple(row[group_cols])])*219474.63,
    axis=1)

data = data.drop('E', axis=1)


# Save or inspect the resulting data
# Replace 'output_file.csv' with your desired output filename
data.to_csv('PES_cm.dat', index=False)

print("Processed data saved to 'PES_cm.dat'.")
