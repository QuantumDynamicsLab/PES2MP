#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################################
####################### Analytical radial fitting of V_lam ######################
#################################################################################
#-------------------------------------------------------------------------------#
Lmat = 'Lambda_ref.dat'               # for 4D enter file containing lambda terms
#-------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
# Use below code to define custom analytical function for radial fitting -------#
# Use same templates as FnFit_PES just use -inf for lower_bounds ---------------#
#-------------------------------------------------------------------------------#
def fnfit_custom(x, a1,a2,a3,a4,a5,a6):
    import numpy as np
    return  a1*np.exp(-6*x) + a2*np.exp(-5*x) + a3*np.exp(-4*x) + a4*np.exp(-3*x) + \
            a5*np.exp(-2*x) + a6*np.exp(-1*x)

initial_val  =  [1e8, -1e7]*3                   # Enter initial guess
#-------------------------------------------------------------------------------#
#------------------------ Optional Constraints ---------------------------------#
#lower_bounds = [-1e12]*3 + [0]*3                       # Lower bound
#upper_bounds = [ 1e12]*3 + [10]*3                     # Upper bound
#-------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#----------------- Enter data for printing MOLSCAT &POTL File ------------------#
#-------------------------------------------------------------------------------#
#import numpy as np                        # Use if needed ---------------------#
Exp_fns = 6                                # number of Exponential functions
A_sign  = [+1]*Exp_fns                     # Enter signs of coeffs A (in order)

N_Opt   = False                            # Are N values optimised (A.e^(-Nx))?
N_Vals  = [-6,-5,-4,-3,-2,-1]                          # If N_Opt=False, enter N coeffs 

Pair_fns = False		    # pair func = a1*(np.exp(-3.1*x)+np.exp(-3.0*x))...
Print_raw = True            # Raw coefficients for later formatting
#-------------------------------------------------------------------------------#
# ------------------------   Plot parameters   ---------------------------------#
# plot parameters
R_lim  = [0,12]    # R limit for 1D/2D plots in Angstroms
fmt    = 'pdf'     # format for created plots, options = pdf, eps, png, etc.
#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#
#----------------------------- OPTIONAL ----------------------------------------#
#scale_Energy = 1       # multiplies cm-1 energy to scale_Energy
#scale_R      = 1       # multiplies Ang. R diatance to scale_R
#------------------------ Optional Constraints ---------------------------------#
#lower_bounds = [-1e12]*16                        # Lower bound
#upper_bounds = [1e12]*16                         # Upper bound
#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#


#################################################################################
#################################################################################
#----------      Codes that probably don't need changes         ----------------#
#################################################################################
#################################################################################
#-------------------------------------------------------------------------------#
import os        # Gettig project name from GUI interface ----------------------#
FnFit = True     # Job type
Proj_name        =  os.getenv("Proj_name", "default_project_name") # Auto-set
Fnfit_type       = 'Vlam'    # Radial coefficients are located inside /MP_files/
#-------------------------------------------------------------------------------#
# Keep header for V_lam-default file (V_lam must be in Matrix format)
filename  = "4D_Vlam.dat"     # Enter Filename (inside Proj_name/MP_files/)
sep       = ','   # data separation: ',' comma, '\t' tab, '\s+' multiple spaces
#-------------------------------------------------------------------------------#
#################################################################################
coll_typ = '4D'            # Set '2D' or '4D'
#----------------------------- OPTIONAL ----------------------------------------#
# The below command supersedes cutoff (Use with caution) -----------------------#
# Fitting will start from n'th position for each lam regardless of min/max -----#
# start_pos are printed in log file and can be copied and changed as one wishes #
# eg. start_pos = [9,5,4,5,6,...] to force 9th start position for V0, and so on #
#-------------------------------------------------------------------------------#
# To forces 0 for all (recommended if PES is fitted using FnFit_PES) -----------#
start_pos = [0]*1000 # Use number greater than number of lambda terms (eg 1000)
#-------------------------------------------------------------------------------#
#cutoff   = 300    # Energy cutoff in cm-1. (Not used: Using start pos) 
#           # --> For attractive potental code automatically switches to -cutoff#
#-------------------------------------------------------------------------------#
#################################################################################
#################################################################################

