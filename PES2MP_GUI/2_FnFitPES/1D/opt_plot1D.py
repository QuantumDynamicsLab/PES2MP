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
R_lim  = [2,6]   # R limit for plots in Angstroms (lower limit for 1D plot only)
#------------------------------------------------------------------------------#
########################### Optional Commands ##################################
#E_inf = -40.632795690775      # define E_infinity (Asymptotic Energy R@Inf)
################################################################################
################ Limited Availability (X axis = all plots) #####################
#plot_name  = 'xyz'                           # 1D/2D only
#plt_title  = 'Potential Energy Surface'      # 1D/2D only
#plt_x_axis = r'R $\mathrm{(\AA)}$'           # X label (in latex $...$ format)
#plt_y_axis = r'Energy $(\mathrm{cm}^{-1})$'  # Y label (in latex $...$ format)
#E_lim = [-200,100]    # Fix upper/lower energy limit for plots 
################################################################################
# By Deault the pes-data file is searched inside project name. For any other ###
# location, uncomment next line and  enter the location below within quotes. ###
################################################################################
# Default location if next line is commented is: /{Proj_name}/input_files -----#
Plot_folder = os.getcwd()+"/Projects/"+Proj_name+'/'  # Enter external location
#------------------------------------------------------------------------------#
