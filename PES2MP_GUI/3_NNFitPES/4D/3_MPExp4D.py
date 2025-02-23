#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
############################ MP Expansion of PES ###############################
################################################################################
#------------------------------------------------------------------------------#
# The number of expansion terms should not exceed number of angles ------------#
L1max = 6                           # max order for first radial term (L1)
L2max = 4                           # max order for second radial term (L2)
Symm_1 = True                       # True if RR1 is symmetric, else False
Symm_2 = True                       # True if RR2 is symmetric, else False
#------------------------------------------------------------------------------#
################################################################################
#--------------------------- MP Expansion Plots -------------------------------#
################################################################################
#------------------------------------------------------------------------------#
# To (only) update plots for an existing expansion: ---------------------------#
# Set --> read_SH = True --> and enter new R/E_lim below ----------------------#

read_SH       = False       # set read_SH to True to read existing file.
R_lim         = [3,10]      # R limit for R vs V_lambda plots in Angstroms
E_lim         = [-250,100]    # E limit for combined plot
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
# If Spherical Harmonics are available for above angular coordinates, use -----#
# read_SH command to read existing numpy file, else the code will generate ----#
# the same from scratch which will take a lot of time. ------------------------#
#------------------------------------------------------------------------------#

################################################################################
################################################################################
#----------      Codes that probably don't need changes         ---------------#
################################################################################
################################################################################
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
import os                 # Gettig project name from GUI interface ------------#
MPExp         = True      # Set job-type
Proj_name     =  os.getenv("Proj_name", "default_project_name") # Auto-set
Expansion_typ = '4D'      # 2D i.e. RR-atom collision PES expansion
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#-------------------------- PES File for Expansion ----------------------------#
#------------------------------------------------------------------------------#
# keep PES file inside Projects/Proj_name folder and provide data separation
# Do not use header and make sure that any R/theta coordinate is not missing
PES_filename_cm  = "Fnfit_PES.dat"     # Enter Filename (Energies in cm-1)
sep = ','    # data separation: ',' comma, '\t' tab, '\s+' multiple spaces
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#-------------------------------Plot Options ----------------------------------#
#------------------------------------------------------------------------------#
Ind_plot = False  # Each radial term is plotted individually (Full range/zoomed)
fmt    = 'pdf'    # format for created plots, options = pdf, eps, png, etc.
#------------------------------------------------------------------------------#

########################### Optional Commands ##################################
## If Energies are in Hartree, Enter E_inf below for conversion. (Optional) ---#
## Comment if Energies are in cm-1 (will result in wrong output) --------------#
#E_inf = -186.5889233299891146      # define E_infinity (Asymptotic Energy)
################################################################################
################################################################################
