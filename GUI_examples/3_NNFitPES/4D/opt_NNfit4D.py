#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:28:43 2023
This is main input for creating ensemble of NN models with tensorflow.

#-----------------------------------------------------------------------------#
# Uses Functional API to learn multiple outputs simultaneously!

# Enter % data points for
 testing dataset: Training model
 validation data: Testing model when model is learning/training.
 testing data   : Testing model after model is created.

# Split ratio for NN models

training : Testing : Validation Split for NN models
 Model (a) 50: 45: 05
 Model (b) 70: 25: 05
 Model (c) 90: 05: 05
#-----------------------------------------------------------------------------#
"""
############################ Global Options #####################################
#-------------------------------------------------------------------------------#
#------------------------NN model Parameters------------------------------------#
#-------------------------------------------------------------------------------#
# NN model parameters (Program uses remaing data points for validation dataset)
train_dataset   = [80]*4      # % of data points used for training model
testing_dataset = [5]*4       # % of data ponts for testing model
#-------------------------------------------------------------------------------#
#----------------- Augmented dimentions for NN prediction ----------------------#
ini_values = [1,     0,   0,   0]      # Initial values for each input dimension
fin_values = [50.1, 91,  91, 181]      # Final values for each input dimension
step_sizes = [0.1,  15,  15,  30]      # Step sizes for each input dimension
#################################################################################





#################################################################################
#################################################################################
#----------      Codes that probably don't need changes         ----------------#
#################################################################################
#################################################################################
#-------------------------------------------------------------------------------#
import os                    # Gettig project name from GUI interface ----------#
Create_NN_model = True       # Job type
Proj_name        =  os.getenv("Proj_name", "default_project_name") # Auto-set
#-------------------------------------------------------------------------------#

#------------------------Input File Parameters----------------------------------#
# Data Separation: '\t' for tab, '\s+' for multiple spaces, ',' for comma, etc. #
#-------------------------------------------------------------------------------#
file_name = 'psi4_PES_cm.dat'   # input file name for PES file
sep = '\s+'                     # Data Separation: | '\t' | '\s+' | ',' |  etc..
#-------------------------------------------------------------------------------#
num_X = 4                     # the number of  input columns (descriptors)
num_Y = 1                     # the number of output columns (descriptors)
#-------------------------------------------------------------------------------#
#------------------------Partition commands-------------------------------------#
#-------------------------------------------------------------------------------#
# The minima region will be learnt separately from High Energy (HE) region!! ---#
partition_req = True       # partition data -> High Energy(HE) and minima region
High_E_cutoff = 300        # E in cm-1 ---> Model Energies lower than this cutoff
reference_output = 4       # Column number for sorting and separating minima/HE
                           # Column numbering starts from 0
#-------------------------------------------------------------------------------#
# Enter your choice for dataset Split (Refer FAQs)? ----------------------------#
# 1 = Randomized (Default) OR Stratified : 2 = Input (Recommended) 3 = Output --#
Split_type = 1                 # Randomized/Stratified (Input or Output) 
#-------------------------------------------------------------------------------#
#-----------------------------  Plot options  ----------------------------------#
#-------------------------------------------------------------------------------#
yscale = f'cm$\mathrm(^{-1})$' # yscale is in cm-1
fmt = 'pdf'                    # output format for plots
#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#

#################################################################################
##########################  Optional Commands ###################################
#################################################################################
# Commands to rearrange/scale and remove columns in dataset (Uncomment to Use) -#
# Default values 0: Uncomment and set variables to 1: follow on screen commands-#

#rearrange_columns = 1     # rearrange position of columns in dataframe
#drop_columns = 1          # drop any non-required column
#scale_columns = 1         # scale R, theta and energy into different units

##########################  Advanced commands ###################################

#--------------------------     Plot Scale   -----------------------------------#
# for +ive logarithmic scale: "log" | for both +ive and -ive log scale: "symlog"
# Default values are provided as given below

# Sorted Partitioned/Unpartitioned plot ----------------------------------------#
#plt_srt_yscale = 'symlog'          # 'linear' | 'log' | 'symlog'| etc...
#plt_srt_xscale = 'linear'          # 'linear' | 'log' | 'symlog'| etc...

# Boundary Partitioned/Unpartitioned plot --------------------------------------#
#plt_bnd_yscale = 'linear'          # 'linear' | 'log' | 'symlog'| etc...
#plt_bnd_xscale = 'linear'          # 'linear' | 'log' | 'symlog'| etc...

#--------------------------  Partition  ----------------------------------------#

#partition_req = 0     # partition the data into high energy and minima region
                       # by default 1
#auto_cutoff = False   # if False, follow on screen commands,
                       # if True, give High_E_cutoff in input file
#reference_output = 3  # reference column for sorting, partitioning and plotting
                       # default: first output column for multiple output data

#--------------------------   NN model  ----------------------------------------#

#generic_model = True  # use generic model insted of default model (R/theta PES)
                       # The genaric model does not constraint R

#HE_train = False      # combine HE data in NN model (provide HE_epochs below)
#HE_epochs = 100       # (50-200) WARNING: Large epochs will degrade minima
#################################################################################

