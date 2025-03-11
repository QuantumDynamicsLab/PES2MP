import numpy as np
import pandas as pd

############################## INPUT PARAMETERS ################################
#------------------------------------------------------------------------------#
# Enter custom function below
def fnfit_custom(x, a1,a2,a3,a4):
    import numpy as np
    return  a1*np.exp(-4*x) + a2*np.exp(-3*x) + a3*np.exp(-2*x) + a4*np.exp(-1*x)
    
Num_coeff = 4                    # number of coefficients
R1        = np.arange(1,20,0.1)  # range of R
R2        = np.arange(20,51,5)  # range of R
R_range = np.concatenate((R1, R2))

#------------------------------------------------------------------------------#
# Define input & output files
input_filename = "4dpes_fn.txt"         # filename having pes coefficients
output_dataframe = "4dpes_fngen.dat"    # filename for PES in dataframe format
output_matrix = "4dpesmat_fngen.dat"    # filename for PES in matrix format (2D/4D)
#------------------------------------------------------------------------------#

################################## MAIN CODE ###################################


# Load file
with open(input_filename, "r") as f:
    lines = [line.strip() for line in f if line.strip()]  # Remove blank lines

# Read dimensionality (second line)
dimensionality = lines[0]
if dimensionality not in {"1D", "2D", "4D"}:
    raise ValueError(f"Invalid dimensionality: {dimensionality}. Must be '1D', '2D', or '4D'.")

# Read coefficients (starting from line 2)
data_lines = lines[1:]

if dimensionality == "1D":
    # ----- 1D CASE -----
    if len(data_lines) != 1:
        raise ValueError("1D case: Expected exactly 1 line of coefficients.")

    # Parse coefficients
    coeffs = list(map(float, data_lines[0].split(",")))
    if len(coeffs) != Num_coeff:
        raise ValueError(f"1D case: Expected {Num_coeff} coefficients but got {len(coeffs)}.")

    # Compute E(R)
    E_values = fnfit_custom(R_range, *coeffs)

    # Save output
    df = pd.DataFrame({"R": R_range, "E": E_values})
    df["R"] = df["R"].map(lambda x: f"{x:.2f}")  # Format col1 to 2 decimal places
    df["E"] = df["E"].map(lambda x: f"{x:.16g}") # Format col2 to 16 significant digits
    df.to_csv(output_dataframe, index=False, sep="\t")
    print(f"1D case: Output saved to {output_dataframe}")

elif dimensionality in {"2D", "4D"}:
    # ----- 2D / 4D CASE -----
    if len(data_lines) % 2 != 0:
        raise ValueError(f"{dimensionality} case: Data lines must be in pairs (angles, coefficients).")

    angles_list = []
    coeffs_list = []
    
    for i in range(0, len(data_lines), 2):
        angles = list(map(float, data_lines[i].split(",")))  # Read angle(s)
        coeffs = list(map(float, data_lines[i + 1].split(",")))  # Read coefficients
        if len(coeffs) != Num_coeff:
            raise ValueError(f"{dimensionality} case: Expected {Num_coeff} coefficients but got {len(coeffs)}.")

        angles_list.append(angles)
        coeffs_list.append(coeffs)

    # Compute results for each angle set
    matrix_list = []
    df_list = []

    for angles, coeffs in zip(angles_list, coeffs_list):
        E_values = fnfit_custom(R_range, *coeffs)  # Compute function output

        # Store in dataframe format
        if dimensionality == "2D":
            df_temp = pd.DataFrame({"R": R_range, "Theta": angles[0], "E": E_values})
        else:  # 4D case
            df_temp = pd.DataFrame({"R": R_range, "Phi": angles[0], "Theta2": angles[1], "Theta1": angles[2], "E": E_values})

        df_list.append(df_temp)
        matrix_list.append(E_values)

    # Combine all results
    df_final = pd.concat(df_list, ignore_index=True)
    #matrix_final = np.column_stack(matrix_list)
    matrix_final = np.column_stack((R_range, np.column_stack(matrix_list)))

    # Save outputs
    if dimensionality == "2D":
        df_final["R"] = df_final["R"].map(lambda x: f"{x:.2f}")  # Format R to 2 decimal places
        df_final["Theta"] = df_final["Theta"].map(lambda x: f"{x:.2f}") # Format Th to 2 significant digits
        df_final["E"] = df_final["E"].map(lambda x: f"{x:.16g}") # Format E to 16 significant digits
        
    else:
        df_final["R"] = df_final["R"].map(lambda x: f"{x:.2f}")  # Format R to 2 decimal places
        df_final["Phi"] = df_final["Phi"].map(lambda x: f"{x:.2f}") # Format phi to 16 significant digits
        df_final["Theta2"] = df_final["Theta2"].map(lambda x: f"{x:.2f}") # Format Th2 to 16 significant digits
        df_final["Theta1"] = df_final["Theta1"].map(lambda x: f"{x:.2f}") # Format Th1 to 16 significant digits
        df_final["E"] = df_final["E"].map(lambda x: f"{x:.16g}") # Format E to 16 significant digits
        
    df_final.to_csv(output_dataframe, index=False, sep="\t")
    print(f"{dimensionality} case: Output saved to {output_dataframe}")
    
    # Create header for the matrix file
    if dimensionality == "2D":
        header_matrix = "R," + ",".join([f"{angles[0]:.2f}" for angles in angles_list])
    elif dimensionality == "4D":
        header_matrix = "R," + ",".join([" ".join(f"{a:.2f}" for a in angles) for angles in angles_list])
    
    # Save matrix output with headers
    np.savetxt(output_matrix, matrix_final, delimiter=",", fmt="%.6f", header=header_matrix, comments="")
    print(f"{dimensionality} case: Matrix output saved to {output_matrix}")



else:
    raise ValueError("Unexpected dimensionality header.")
    
################################## MAIN CODE ###################################
