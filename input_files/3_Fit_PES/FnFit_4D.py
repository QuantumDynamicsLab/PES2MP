#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
####################### Analytical radial fitting of PES ######################
###############################################################################
FnFit = True          # Job type
Proj_name = 'chp'  # Folder name inside "Projects" folder
Fnfit_type = 'PES'    # PES in cm-1 are located inside Proj_name folder

# Remove header for PES (also PES must be in R,A,E format)
# If PES is in Hartree convert to cm-1 using E_inf in optional commands below
filename  = "abinitio_cm.dat"     # Enter Filename @ /Proj_name/
sep    = ','      # data separation: ',' comma, '\t' tab, '\s+' multiple spaces

# If PES must be in R,A,E format
PES_typ = '4D'      # Set '2D' or '4D' (important for reading file)
#cutoff = 5000        # Energy cutoff in cm-1. Features are preserved till cutoff

# plot parameters
fmt     = 'pdf'     # format for created plots, options = pdf, eps, png, etc.
scale_x = 'symlog'  # 'symlog' or 'linear'
scale_y = 'symlog'  # 'symlog' or 'linear'
Y_lim   = [-1,1]    # E (residual) limit for zoomed in plot
#-----------------------------------------------------------------------------#
# Cleaning the data (fitting high energy region)

he_fit = False
he_cutoff = 10000
he_min_offset = 0

def fnfit_he(x, he1,he2):                     # High Energy Region fit
    import numpy as np
    return  he1*np.exp(-he2*x)
he_initial_val  =  [1e4,1]                    # Enter initial guess ()
#-----------------------------------------------------------------------------#
# Cleaning the data (fitting long range region)

lr_fit = False
lr_cutoff = -1.0
lr_min_offset = 8

def fnfit_lr(x, lr1,lr2):                     # Long Range Region fit
    import numpy as np
    return  lr1*np.power(x,-lr2)
lr_initial_val  =  [1e4,3]                    # Enter initial guess
#-----------------------------------------------------------------------------#
# Use below code to define custom analytical function for radial fitting
# Use templates and fn_generator.py for more functions

def fnfit_custom(x ,a1,a2,a3,a4):
    import numpy as np
    return a1*np.exp(-0.5*x) +  a2*np.exp(-1.75*x) +  a3*np.exp(-3.5*x) +  a4*np.exp(-5.0*x)

initial_val  = [1e4]*4
#----------------------------- OPTIONAL --------------------------------------#
#E_inf = -186.545562935966      # define E_infinity (Asymptotic Energy R@Inf)
#scale_Energy = 1       # multiplies cm-1 energy to scale_Energy
#scale_R      = 1       # multiplies Ang. R diatance to scale_R
#-----------------------------------------------------------------------------#
#------------------------ Optional Constraints -------------------------------#
#lower_bounds = [0]*8                        # Lower bound
#upper_bounds = [1e12]*8                     # Upper bound

#----------------------------- OPTIONAL --------------------------------------#
#E_inf = -186.545562935966      # define E_infinity (Asymptotic Energy R@Inf)

#------------------ Optional High Energy and long-range fit ------------------#

#he_fit = True			# To fit high Energy region (Set True)
#he_cutoff = 10000		# end value: fit datapoints till he_cutoff
#he_min_offset = 4		# start value: fit from 4 position before minima

#def fnfit_he(x, he1,he2):             # Function for fitting high energy Region 
#    import numpy as np
#    return  he1*np.exp(-he2*x)
#he_initial_val  =  [1e4,1]            # Enter initial guess

#-----------------------------------------------------------------------------#

#lr_fit = True			# To fit Long Range Region (Set True)
#lr_min_offset = 10		# fit from 10 position after minima till end

#def fnfit_lr(x, lr1,lr2):              # Function for fitting Long Range Region   
#    import numpy as np
#    return  lr1*np.power(x,-lr2)
#lr_initial_val  =  [1e4,6]             # Enter initial guess
#-----------------------------------------------------------------------------#

#-------------------------------- More Options -------------------------------#
# The below command supersedes cutoff (Use with caution only if fitting fails)
cutoff_pos = 4  # Fitting will start 4 (cutoff_pos) positions before minima.
#-----------------------------------------------------------------------------#
# New R range (Inter/Extrapolate R) for fitted PES
#New_R = np.arange(0,50.1,0.1) # New R range from 0 to 50 Ang | Step size = 0.1
#-----------------------------------------------------------------------------#
