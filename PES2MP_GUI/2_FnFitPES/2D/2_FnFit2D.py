#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
####################### Analytical radial fitting of PES #######################
################################################################################
#------------------------------------------------------------------------------#
cutoff = 100    # Energy cutoff in cm-1. PES Features are preserved till cutoff
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# Use below code to define custom analytical function for radial fitting ------#
# Use templates for more functions. -------------------------------------------#

def fnfit_custom(x, a1,a2):
    import numpy as np
    return  a1*np.exp(-4*x) + a2*np.exp(-2*x)

initial_val  =  [1e8, -1e7]                  # Enter initial guess

#------------------------ Optional Constraints --------------------------------#
#lower_bounds = [0]*8                        # Lower bound
#upper_bounds = [1e12]*8                     # Upper bound
#------------------------------------------------------------------------------#
# ------------------------   Plot parameters   --------------------------------#
fmt     = 'pdf'     # format for created plots, options = pdf, eps, png, etc.
scale_x = 'symlog'  # 'symlog' or 'linear'
scale_y = 'symlog'  # 'symlog' or 'linear'
Y_lim   = [-10,10]    # E (residual) limit for zoomed in plot
#------------------------------------------------------------------------------#



################################################################################
################################################################################
#----------      Codes that probably don't need changes         ---------------#
################################################################################
################################################################################
#------------------------------------------------------------------------------#
import os        # Gettig project name from GUI interface ---------------------#
FnFit = True     # Job type
Proj_name        =  os.getenv("Proj_name", "default_project_name") # Auto-set
Fnfit_type       = 'PES'    # PES in cm-1 are located inside Proj_name folder
#------------------------------------------------------------------------------#
# Remove header for PES (also PES must be in R,A,E format) --------------------#
# If PES is in Hartree convert to cm-1 using E_inf in optional commands below -#

# testrun2
filename  = "psi4_PES_cm.dat"     # Enter Filename @ /Proj_name/
# testrun3
#filename  = "NN_Predicted_results.txt"     # Enter Filename @ /Proj_name/

sep       = '\s+'                 # data separation: ',' comma, '\t' tab, '\s+'
#------------------------------------------------------------------------------#
# If PES must be in R,A,E format
PES_typ = '2D'      # Set '2D' or '4D' (important for reading file)

################################################################################
#-----------------   (OPTIONAL) Short/Long Range Fit   ------------------------#
################################################################################
#------------------------------------------------------------------------------#
#he_fit = True			# To fit HIGH ENERGY REGION (Set True)
#he_cutoff = 10000		# end value: fit datapoints till he_cutoff
#he_min_offset = 4		# start value: fit from 4 position before minima
#------------------------------------------------------------------------------#
#def fnfit_he(x, he1,he2):             # Function for fitting high energy Region 
#    import numpy as np
#    return  he1*np.exp(-he2*x)
#he_initial_val  =  [1e4,1]            # Enter initial guess
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#lr_fit = True			# To fit Long Range Region (Set True)
#lr_min_offset = 10		# fit from 10 position after minima till end
#------------------------------------------------------------------------------#
#def fnfit_lr(x, lr1,lr2):           # Function for fitting LONG RANGE REGION   
#    import numpy as np
#    return  lr1*np.power(x,-lr2)
#lr_initial_val  =  [1e4,6]          # Enter initial guess
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
# Converting energy to cm-1 and scaling the same for fitting (Optional) -------#
#E_inf = -186.545562935966	# define E_infinity (Asymptotic Energy R@Inf)
#scale_Energy = 1       	# multiplies cm-1 energy to scale_Energy
#scale_R      = 1      	# multiplies Ang. R diatance to scale_R
#------------------------------------------------------------------------------#
#-------------------------------- More Options --------------------------------#
# The below command supersedes cutoff (Use with caution only if fitting fails)
#cutoff_pos = 4  # Fitting will start 4 (cutoff_pos) positions before minima.
#------------------------------------------------------------------------------#
# New R range (Inter/Extrapolate R) for fitted PES ----------------------------#
#New_R = np.arange(0,50.1,0.1) # New R range from 0 to 50 Ang | Step size = 0.1
#------------------------------------------------------------------------------#
################################################################################
################################################################################
