#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
####################### Analytical radial fitting of PES ######################
###############################################################################
FnFit = True          # Job type
Proj_name = '1d'  # Folder name inside "Projects" folder
Fnfit_type = 'PES'    # PES in cm-1 are located inside Proj_name folder

# Remove header for PES (also PES must be in R,A,E format)
# If PES is in Hartree convert to cm-1 using E_inf in optional commands below
filename  = "pes_cm.dat"     # Enter Filename @ /Proj_name/
sep    = ','      # data separation: ',' comma, '\t' tab, '\s+' multiple spaces

# If PES must be in R,A,E format
PES_typ = '2D'      # Set '2D' or '4D' (important for reading file)
cutoff = 500        # Energy cutoff in cm-1. Features are preserved till cutoff

# plot parameters
fmt     = 'pdf'     # format for created plots, options = pdf, eps, png, etc.
scale_x = 'symlog'  # 'symlog' or 'linear'
scale_y = 'symlog'  # 'symlog' or 'linear'
Y_lim   = [-2,2]    # E (residual) limit for zoomed in plot
#-----------------------------------------------------------------------------#
# Use below code to define custom analytical function for radial fitting
# Use templates for more functions

def fnfit_custom(x,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16):
    import numpy as np
    return  a1*np.exp(-0.25*x)+a2*np.exp(-0.5*x)+a3*np.exp(-0.75*x)+a4*np.exp(-1*x) + \
            a5*np.exp(-1.25*x)+a6*np.exp(-1.5*x)+a7*np.exp(-1.75*x)+a8*np.exp(-2*x) +\
            a9*np.exp(-2.25*x)+a10*np.exp(-2.5*x)+a11*np.exp(-2.75*x)+a12*np.exp(-3*x)+\
            a13*np.exp(-3.25*x)+a14*np.exp(-3.5*x)+a15*np.exp(-3.75*x)+a16*np.exp(-4*x) + \
            a13*np.exp(-4.25*x)+a14*np.exp(-4.5*x)+a15*np.exp(-4.75*x)+a16*np.exp(-5*x)
initial_val  =  [1e4]*16                   # Enter initial guess
#------------------------ Optional Constraints -------------------------------#
#lower_bounds = [0]*8                        # Lower bound
#upper_bounds = [1e12]*8                     # Upper bound

#----------------------------- OPTIONAL --------------------------------------#
#E_inf = -186.545562935966	# define E_infinity (Asymptotic Energy R@Inf)
#scale_Energy = 1       	# multiplies cm-1 energy to scale_Energy
#scale_R      = 1       	# multiplies Ang. R diatance to scale_R

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
#cutoff_pos = 4  # Fitting will start 4 (cutoff_pos) positions before minima.
#-----------------------------------------------------------------------------#
# New R range (Inter/Extrapolate R) for fitted PES
#New_R = np.arange(0,50.1,0.1) # New R range from 0 to 50 Ang | Step size = 0.1
#-----------------------------------------------------------------------------#
