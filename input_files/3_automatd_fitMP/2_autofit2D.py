# ============================ Automated 2D ====================================
# MINIMAL 2D INPUT FILE fitting PES, MP expansion and Vlam Coefficients
# ==============================================================================
import os        # Gettig project name from GUI interface ---------------------#
Proj_name        =  os.getenv("Proj_name", "automated") # Auto-set by GUI or change "automated"
FnFit_automated = True

# PES input information
filename = "psi4_PES_cm.dat"
sep = r"\s+"
PES_typ = "2D"
cutoff = 100

# Exponential-Decay function for fitting PES anglewise
def fnfit_custom(x, a1, a2, a3, a4, a5):
    import numpy as np
    return (a1*np.exp(-4*x) + a2*np.exp(-3*x) + a3*np.exp(-2*x)
            + a4*np.exp(-1*x) + a5*np.exp(-0.2*x))

initial_val = [1e4]*5
N_Vals = [-4, -3, -2, -1, -0.2]

# multipole expansion information
Expansion_typ = '2D'
lam_max = 4            # Maximum expansion terms for lambda in V_lambda
symmetric = True       # Verify if rigid rotor is symmetric (else put False)
read_Legendre = False  # set read_Legendre to True to read existing file.

# plot parameters
fmt = 'pdf'
scale_x = 'symlog'
scale_y = 'symlog'
Y_lim = [-2, 2]      # E limit for residual plot (PES FnFit)

R_lim  = [2.5,6]      # R limit for 1D/2D plots in Angstroms for Vlam combined plot
E_lim = [-25, 25]      # E limit for Vlam combined plot
Ind_plot = True        # show individual plots for Vlam terms
ncol=4                 # number of columns for legend

