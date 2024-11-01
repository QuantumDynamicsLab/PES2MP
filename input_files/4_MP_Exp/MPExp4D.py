#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
############################ MP Expansion of PES ##############################
###############################################################################
MPExp = True              # Set job-type
Proj_name = 'test4D'      # Folder name inside "Projects" folder
Expansion_typ = '4D'      # 2D i.e. RR-atom collision PES expansion
#-----------------------------------------------------------------------------#
# keep PES file inside Projects/Proj_name folder and provide data separation
# Do not use header and make sure that any R/theta coordinate is not missing
PES_filename_cm  = "Fnfit_PES.dat"     # Enter Filename (Energies in cm-1)
sep = ','    # data separation: ',' comma, '\t' tab, '\s+' multiple spaces
#-----------------------------------------------------------------------------#
L1max = 4                           # max order for first radial term (L1)
L2max = 2                           # max order for second radial term (L2)
Symm_1 = True                       # True if RR1 is symmetric, else False
Symm_2 = True                       # True if RR2 is symmetric, else False
#-----------------------------------------------------------------------------#
# If Spherical Harmonics are available for above angular coordinates, use the
# below command to ready existing numpy file, else the code will generate the
# same from scratch which will take a lot of time.
read_SH = False  # set read_SH to True to read existing file.

#-----------------------------------------------------------------------------#
# Enter a rough Estimate. Updated plots by --> read_Legendre = True --> new R/E
Ind_plot = False  # Each radial term is plotted individually (Full range/zoomed)
R_lim  = [0,10]   # R limit for R vs V_lambda plots in Angstroms
E_lim  = [-150,15]       # E limit for combined plot
fmt    = 'pdf'    # format for created plots, options = pdf, eps, png, etc.

########################### Optional Commands #################################
## If Energies are in Hartree, Enter E_inf below for conversion. (Optional)  ##
## Comment if Energies are in cm-1 (will result in wrong output)             ##
E_inf = -186.5889233299891146      # define E_infinity (Asymptotic Energy)
###############################################################################
