# ============================ Automated 4D ====================================
# MINIMAL 4D INPUT FILE for fitting PES, MP expansion and Vlam Coefficients
# ==============================================================================
import os        # Gettig project name from GUI interface ---------------------#
Proj_name        =  os.getenv("Proj_name", "automated") # Auto-set
FnFit_automated = True

# PES input information
filename = "psi4_PES_cm.dat"
sep = r"\s+"
PES_typ = "4D"
cutoff = 200

def fnfit_custom(x, a1,a2,a3,a4):
    import numpy as np
    return  a1*np.exp(-4*x) + a2*np.exp(-3*x) + a3*np.exp(-2*x) + a4*np.exp(-1*x)

initial_val  =  [1e8, -1e7, 1e8, 1e-7]                  # Enter initial guess
N_Vals  = [-4,-3,-2,-1]                                 # Enter N coeffs 

# multipole expansion information
Expansion_typ = '4D'
L1max = 4                           # max order for first radial term (L1)
L2max = 2                           # max order for second radial term (L2)
Symm_1 = True                       # True if RR1 is symmetric, else False
Symm_2 = True                       # True if RR2 is symmetric, else False
read_SH = False                     # set read_SH to True to read existing file.

# plot parameters
fmt = 'pdf'
scale_x = 'symlog'
scale_y = 'symlog'
Y_lim = [-20, 20]      # E limit for residual plot (PES FnFit)

R_lim  = [3,10]      # R limit for 1D/2D plots in Angstroms for Vlam combined plot
E_lim = [-250, 100]      # E limit for Vlam combined plot
Ind_plot = True        # show individual plots for Vlam terms
ncol=4                 # number of columns for legend