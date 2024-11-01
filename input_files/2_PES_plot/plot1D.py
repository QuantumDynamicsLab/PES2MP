#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
############################ Plot External PES #################################
################################################################################
Plot_PES = True
Proj_name = 'pesgen1D'  # Project name (Path:/current-folder/Projects/Proj_name)
PES_filename_cm  = "psi4_PES.dat"     # Enter Filename (Energies in cm-1)

# plot parameters
sep    = '\s+'   # data separation: ',' comma, '\t' tab, '\s+' multiple spaces
fmt    = 'pdf'   # format for created plots, options = pdf, eps, png, etc.

# R limit for R vs E plots
R_lim  = [0,8]   # R limit for plots in Angstroms (lower limit for 1D plot only)

########################### Optional Commands ##################################
################ Limited Availability (X axis = all plots) #####################
#plot_name  = 'xyz'                           # 1D/2D only
#plt_title  = 'Potential Energy Surface'      # 1D/2D only
#plt_x_axis = r'R $\mathrm{(\AA)}$'           # X label (in latex $...$ format)
#plt_y_axis = r'Energy $(\mathrm{cm}^{-1})$'  # Y label (in latex $...$ format)
################################################################################
# By Deault the pes-data file is searched inside project name. For any other ###
# location, uncomment next line and  enter the location below within quotes. ###
################################################################################
#Plot_folder = "/Volumes/xyz/Projects/H2_H2/"  # Enter external folder location

#-----------------------------------------------------------------------------#
