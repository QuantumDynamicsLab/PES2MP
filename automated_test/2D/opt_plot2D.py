#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
############################ Plot External PES #################################
################################################################################
import os                    # Gettig project name from GUI interface ---------#
Proj_name        =  os.getenv("Proj_name", "default_project_name") # Auto-set
Plot_PES         = True          # Job Type
PES_filename_cm  = "psi4_PES_cm.dat"     # Enter Filename (Energies in cm-1)
#------------------------------------------------------------------------------#
# plot parameters
sep    = '\s+'   # data separation: ',' comma, '\t' tab, '\s+' multiple spaces
fmt    = 'pdf'   # format for created plots, options = pdf, eps, png, etc.
#------------------------------------------------------------------------------#
# R limit for R vs E plots
R_lim  = [3,6]   # R limit for plots in Angstroms (lower limit for 1D plot only)
#------------------------------------------------------------------------------#
# 2D PES angles to be plotted! (Uncomment next line to use! )
thetax  = [0,30,60,90]       # Angles to be plotted (R vs E plot) 
#------------------------------------------------------------------------------#
########################### Optional Commands ##################################
#E_inf = -78.698190719292      # define E_infinity (Asymptotic Energy R@Inf)
################################################################################
# By default the energy levels are chosen automatically to preserve features ###
# and the default ste size is 0.1. This can be changed using below commands  ###
################################################################################
#####################  For 2D/4D Polar Plots Only  #############################
#E_lim = [-6,6]    # Fix upper/lower energy limit for plots (keep symmetric)
#E_stp = 0.2       # Step size for energy (default 0.1)

##################### Limited Availability (X axis = all plots) ################
#plot_name  = ''                              # 1D/2D only
#plt_title  = 'Potential Energy Surface'      # 1D/2D only
#plt_x_axis = r'R $\mathrm{(\AA)}$'           # X label (in latex $...$ format)
#plt_y_axis = r'Energy $(\mathrm{cm}^{-1})$'  # Y label (in latex $...$ format)
################################################################################
# By Deault the pes-data file is searched inside project name. For any other ###
# location, uncomment next line and  enter the location below within quotes. ###
################################################################################
# Default location if next line is commented is: /{Proj_name}/input_files -----#
#Plot_folder = os.getcwd()+"/Projects/"+Proj_name+'/'  # Enter external location
#------------------------------------------------------------------------------#
