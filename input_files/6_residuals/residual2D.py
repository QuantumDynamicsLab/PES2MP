#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
############################ MP Expansion of PES ##############################
###############################################################################
# Gives residual plot by recreating PES from V_lambda. Must use after FnFit.
# The raw V_lam will not give any error, but analytically fitted V_lams will!
# This provides an estimate for quality of fit for the PES.

# The PES must be located inside Projects/Proj_name
# The V_lam file must be inside Projects/Proj_name/MP_files
#-----------------------------------------------------------------------------#
MPExp = True              # Set job-type
Proj_name = 'test2D'      # Folder name inside "Projects" folder
Expansion_typ = '2D'      # 2D i.e. RR-atom collision PES expansion
Residuals = True
#-----------------------------------------------------------------------------#
# Reference PES (No Header)
PES_filename_cm  = "Fnfit_PES.dat"     # Enter Filename (Energies in cm-1)
sep = ','    # data separation: ',' comma, '\t' tab, '\s+' multiple spaces

# Read Legendre Coefficients
read_Legendre = True  # set read_Legendre to True to read existing file.

# Read V_lambda (No Headers)
V_lam_filename_cm = 'FnFitted_Vlam.dat'  # File contain radial terms
sep_vlam = ','    # data separation: ',' comma, '\t' tab, '\s+' multiple spaces

#-----------------------------------------------------------------------------#
symmetric = True     # Verify if rigid rotor is symmetric (else put False)
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Enter format for residual plot
fmt     = 'pdf'     # format for created plots, options = pdf, eps, png, etc.
scale_x = 'symlog'  # 'symlog' or 'linear'
scale_y = 'symlog'  # 'symlog' or 'linear'
Y_lim   = [-1,1]    # E (residual) Y limit for zoomed in plot
cutoff  = 100       # E (residual) X limit for zoomed in plot
########################### Optional Commands #################################
## If Energies are in Hartree, Enter E_inf below for conversion. (Optional)  ##
#E_inf = -188.31099452      # define E_infinity (Asymptotic Energy)
###############################################################################
