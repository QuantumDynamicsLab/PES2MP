#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
############################ Plot External PES #################################
################################################################################
Plot_PES = True
Proj_name = 'pesgen4D'  # Project name (Path:/current-folder/Projects/Proj_name)
PES_filename_cm  = "psi4_PES.dat"     # Enter Filename (Energies in cm-1)

# plot parameters
sep    = '\s+'   # data separation: ',' comma, '\t' tab, '\s+' multiple spaces
fmt    = 'pdf'   # format for created plots, options = pdf, eps, png, etc.

# R limit for R vs E plots
R_lim  = [2,10]  # R limit for plots in Angstroms (lower limit for 1D plot only)

# 4D PES angle combinations to be plotted! (# R vs E plot)
#        [ [phi,th2,th1] , [phi,th2,th1] ]
thetax = [[0,0,0],[0,90,0],[90,90,0],[30,60,120]]

# Angle combinations for polar Plots
phix    = [0,45,90]            # 4D (phi between RR1 and RR2)
theta2x = [0,45,90]            # 4D (theta 2 for RR2)
theta1x = [0,45,90,135,180]    # 4D (theta 1 for RR1)


########################### Optional Commands ##################################
# By default the energy levels are chosen automatically to preserve features ###
# and the default ste size is 0.1. This can be changed using below commands  ###
################################################################################
#####################  For 2D/4D Polar Plots Only   ############################
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
#Plot_folder = "/Volumes/xyz/Projects/H2_H2/"  # Enter external folder location

#-----------------------------------------------------------------------------#
