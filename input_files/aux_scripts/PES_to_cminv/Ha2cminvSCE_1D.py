import pandas as pd

# Load the data
# Replace 'your_file.csv' with your actual filename
data = pd.read_csv('PES.dat', sep='\s+' , header=None)


data = data.apply(pd.to_numeric, errors='coerce')
data.dropna(inplace=True) #removing rows with na values
data.reset_index(drop=True, inplace=True) # reset index

# Adding column names
data.columns =['R', 'E']

R_col = 'R'
E_col = 'E'

# Find the maximum R and the corresponding E value
max_R_index = data[R_col].idxmax()
E_at_max_R = data.loc[max_R_index, E_col]

# Subtract E at max R from all E values
data['E_cm'] = (data[E_col] - E_at_max_R)*219474.63

data = data.drop('E', axis=1)

# Save and inspect the resulting data
# Replace 'output_file.csv' with your desired output filename
data.to_csv('PES_cm.dat', index=False)

print("PES converted successfully. File saved to 'PES_cm.dat'.")
