#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
####################### Analytical radial fitting of V_lam ####################
###############################################################################
FnFit = True                  # Job type
Proj_name  = 'C2_H2'         # Folder name inside "Projects" folder
Fnfit_type = 'Vlam'  # Radial coefficients are located inside MP_files folder

# Keep header for V_lam-default file (V_lam must be in Matrix format)
filename  = "4D_Vlam.dat"     # Enter Filename (inside Proj_name/MP_files/)
sep       = ','   # data separation: ',' comma, '\t' tab, '\s+' multiple spaces

###############################################################################
coll_typ = '4D'            # Set '2D' or '4D'
#-------------------- Choose 2D/4D Collision Parameter -----------------------#
#Choose correct parameter based on 2D/4D RR collision and comment the other
#-------------------------------- 2D -----------------------------------------#
# If coll_typ = '2D' , uncomment 'symmetric =' and comment 'Lmat ='
#symmetric = True        # Verify if rigid rotor is symmetric (else put False)
#-------------------------------- 4D -----------------------------------------#
# If coll_typ = '4D' , uncomment 'Lmat =' and comment 'symmetric ='
Lmat = 'Lambda_ref.dat' # for 4D enter file containing lambda terms
###############################################################################

#cutoff   = 300    # Energy cutoff in cm-1.
           # --> For attractive potental code automatically switches to -cutoff
# plot parameters
R_lim  = [0,12]    # R limit for 1D/2D plots in Angstroms
fmt    = 'pdf'     # format for created plots, options = pdf, eps, png, etc.

#-----------------------------------------------------------------------------#
# Use below code to define custom analytical function for radial fitting
# Use same templates as FnFit_PES just use -inf for lower_bounds

def fnfit_custom(x,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16):
    import numpy as np
    return  a1*np.exp(-0.25*x)+a2*np.exp(-0.5*x)+a3*np.exp(-0.75*x)+a4*np.exp(-1*x) + \
            a5*np.exp(-1.25*x)+a6*np.exp(-1.5*x)+a7*np.exp(-1.75*x)+a8*np.exp(-2*x) +\
            a9*np.exp(-2.25*x)+a10*np.exp(-2.5*x)+a11*np.exp(-2.75*x)+a12*np.exp(-3*x)+\
            a13*np.exp(-3.25*x)+a14*np.exp(-3.5*x)+a15*np.exp(-3.75*x)+a16*np.exp(-4*x) + \
            a13*np.exp(-4.25*x)+a14*np.exp(-4.5*x)+a15*np.exp(-4.75*x)+a16*np.exp(-5*x)
initial_val  =  [1e4]*16                   # Enter initial guess

#----------------------------- OPTIONAL --------------------------------------#
#scale_Energy = 1       # multiplies cm-1 energy to scale_Energy
#scale_R      = 1       # multiplies Ang. R diatance to scale_R
#-----------------------------------------------------------------------------#
# Enter data about custom function for printing MOLSCAT &POTL File
import numpy as np

Exp_fns = 16                       # number of Exponential functions
N_Opt   = False                   # Are N values optimised (A.e^(-Nx))
N_Vals  = np.linspace(0.1, 5, Exp_fns)*(-1)           # If N_Opt=False, enter N coeffs (in order)
A_sign  = [+1]*Exp_fns             # Enter signs of coeffs A (in order)
Pair_fns = False		    # pair func = a1*(np.exp(-3.1*x)+np.exp(-3.0*x))...

Print_raw = True                 # Raw coefficients for later formatting

#----------------------------- OPTIONAL --------------------------------------#
# The below command supersedes cutoff (Use with caution)
# Fitting will start from n'th position for each lam regardless of min/max
# start_pos are printed in log file and can be copied and changed as one wishes
# eg. start_pos = [9,5,4,5,6,...] to force 9th start position for V0, and so on

# To forces 0 for all (recommended if PES is fitted using FnFit_PES)
start_pos = [0]*1000 # Use number greater than number of lambda terms (eg 1000)

#-----------------------------------------------------------------------------#
