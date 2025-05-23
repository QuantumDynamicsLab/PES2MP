#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
############################ Plot External PES #################################
################################################################################
import os                    # Gettig project name from GUI interface ---------#
Proj_name        =  os.getenv("Proj_name", "default_project_name") # Auto-set
Plot_PES         = True          # Job Type
PES_filename_cm  = "NN_Predicted_results.txt"     # Enter Filename (Energies in cm-1)
#------------------------------------------------------------------------------#
# plot parameters
sep    = '\s+'   # data separation: ',' comma, '\t' tab, '\s+' multiple spaces
fmt    = 'jpeg'   # format for created plots, options = pdf, eps, png, etc.
#------------------------------------------------------------------------------#
# R limit for R vs E plots
R_lim  = [2,10]  # R limit for plots in Angstroms (lower limit for 1D plot only)
#------------------------------------------------------------------------------#
# 4D PES angle combinations to be plotted! (# R vs E plot)
#        [ [phi,th2,th1] , [phi,th2,th1] ]
thetax = [[0,0,0],[0,45,30],[0,90,90],[0,45,0],[0,90,0],[45,45,60],[90,90,90]]
#------------------------------------------------------------------------------#
# Angle combinations for polar Plots
phix               = [0,30,90]          # phi angles
theta2x            = [0,30,90]          # theta2 angles
theta1x            = [0,60,180]         # theta1 angles
#------------------------------------------------------------------------------#

########################### Optional Commands ##################################
# By default the energy levels are chosen automatically to preserve features ###
# and the default ste size is 0.1. This can be changed using below commands  ###
################################################################################
#E_inf = -76.971917082028      # define E_infinity (Asymptotic Energy R@Inf)
################################################################################
#####################  For 2D/4D Polar Plots Only   ############################
E_lim = [-120,120]    # Fix upper/lower energy limit for plots (keep symmetric)
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
Plot_folder = os.getcwd()+"/Projects/"+Proj_name+'/'  # Enter external location
#------------------------------------------------------------------------------#
