# ============================ Automated 4D ====================================
# MINIMAL 4D INPUT FILE for fitting PES, MP expansion and Vlam Coefficients
# ==============================================================================
import os        # Gettig project name from GUI interface ---------------------#
Proj_name        =  os.getenv("Proj_name", "automated_large") # Auto-set
FnFit_automated = True

# PES input information
filename = "psi4_PES_cm.dat"
sep = r"\s+"
PES_typ = "4D"
cutoff = 1000

def fnfit_custom(x, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17 \
                , a18, a19, a20, a21, a22, a23, a24, a25, a26, a27, a28, a29, a30, a31, a32, a33, a34 \
                , a35, a36, a37, a38, a39, a40, a41, a42, a43, a44, a45, a46, a47, a48, a49, a50):
    import numpy as np
    return a1*np.exp(-0.001000*x) + a2*np.exp(-0.103020*x) + a3*np.exp(-0.205041*x) + a4*np.exp(-0.307061*x) + \
           a5*np.exp(-0.409082*x) + a6*np.exp(-0.511102*x) + a7*np.exp(-0.613122*x) + a8*np.exp(-0.715143*x) + \
           a9*np.exp(-0.817163*x) + a10*np.exp(-0.919184*x) + a11*np.exp(-1.021204*x) + a12*np.exp(-1.123224*x) + \
           a13*np.exp(-1.225245*x) + a14*np.exp(-1.327265*x) + a15*np.exp(-1.429286*x) + a16*np.exp(-1.531306*x) + \
           a17*np.exp(-1.633327*x) + a18*np.exp(-1.735347*x) + a19*np.exp(-1.837367*x) + a20*np.exp(-1.939388*x) + \
           a21*np.exp(-2.041408*x) + a22*np.exp(-2.143429*x) + a23*np.exp(-2.245449*x) + a24*np.exp(-2.347469*x) + \
           a25*np.exp(-2.449490*x) + a26*np.exp(-2.551510*x) + a27*np.exp(-2.653531*x) + a28*np.exp(-2.755551*x) + \
           a29*np.exp(-2.857571*x) + a30*np.exp(-2.959592*x) + a31*np.exp(-3.061612*x) + a32*np.exp(-3.163633*x) + \
           a33*np.exp(-3.265653*x) + a34*np.exp(-3.367673*x) + a35*np.exp(-3.469694*x) + a36*np.exp(-3.571714*x) + \
           a37*np.exp(-3.673735*x) + a38*np.exp(-3.775755*x) + a39*np.exp(-3.877776*x) + a40*np.exp(-3.979796*x) + \
           a41*np.exp(-4.081816*x) + a42*np.exp(-4.183837*x) + a43*np.exp(-4.285857*x) + a44*np.exp(-4.387878*x) + \
           a45*np.exp(-4.489898*x) + a46*np.exp(-4.591918*x) + a47*np.exp(-4.693939*x) + a48*np.exp(-4.795959*x) + \
           a49*np.exp(-4.897980*x) + a50*np.exp(-5.000000*x)


initial_val = [1e4]*50
N_Vals = [-0.001, -0.10302, -0.205041, -0.307061, -0.409082, -0.511102, -0.613122, -0.715143, -0.817163, -0.919184, -1.021204, -1.123224, -1.225245, -1.327265, -1.429286, -1.531306, -1.633327, -1.735347, -1.837367, -1.939388, -2.041408, -2.143429, -2.245449, -2.347469, -2.44949, -2.55151, -2.653531, -2.755551, -2.857571, -2.959592, -3.061612, -3.163633, -3.265653, -3.367673, -3.469694, -3.571714, -3.673735, -3.775755, -3.877776, -3.979796, -4.081816, -4.183837, -4.285857, -4.387878, -4.489898, -4.591918, -4.693939, -4.795959, -4.89798, -5.0]

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
Y_lim = [-1, 1]      # E limit for residual plot (PES FnFit)

R_lim  = [3,10]      # R limit for 1D/2D plots in Angstroms for Vlam combined plot
E_lim = [-250, 100]      # E limit for Vlam combined plot
Ind_plot = True        # show individual plots for Vlam terms
ncol=4                 # number of columns for legend