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

@author: Apoorv Kushwaha & Dr. T. J. Dhilip Kumar
"""
############################ Global Options ####################################
Create_NN_model = True     # jobtype
Proj_name = 'NN_E1'           # Folder name inside "Projects" folder
file_name = 'Fnfit_PES.dat'   # input file name for PES file

#------------------------Input File Parameters---------------------------------#
# Data Separation: '\t' for tab, '\s+' for multiple spaces, ',' for comma, etc.
# for the input file "file_name" provided above
sep = ','                # Data Separation: | '\t' | '\s+' | ',' |  etc..
num_X = 4                  # the number of  input columns (descriptors)
num_Y = 1                  # the number of output columns (descriptors)

#------------------------Partition commands------------------------------------#
# The minima region will be learnt separately from High Energy (HE) region!!
partition_req = True       # partition data -> High Energy(HE) and minima region

High_E_cutoff = 300        # E in cm-1 ---> Energies lower than this cutoff
                           # will be used for primary NN model. Higher energies
                           # in repulsive region will be modelled separetely!

reference_output = 4       # Column number for sorting and separating minima/HE
                           # Column numbering starts from 0

#------------------------Train/Test/Validation Split---------------------------#
# Enter your choice for dataset Split (Refer FAQs)?
# 1 = Randomized (Default) OR Stratified : 2 = Input (Recommended) 3 = Output
Split_type = 1             # Randomized/Stratified (Input or Output): See above
#-----------------------------  Plot options  ---------------------------------#
yscale = f'cm$\mathrm(^{-1})$' # yscale is in cm-1
fmt = 'pdf'                    # output format for plots

# Augmented dimentions for NN prediction
ini_values = [1,     0,   0,   0]      # Initial values for each input dimension
fin_values = [50.1, 91,  91, 181]      # Final values for each input dimension
step_sizes = [0.1,  15,  15,  15]      # Step sizes for each input dimension

#------------------------NN model Parameters-----------------------------------#
# NN model parameters (Program uses remaing data points for validation dataset)
train_dataset   = [85]*16       # % of data points used for training model
testing_dataset = [5]*16       # % of data ponts for testing model

# See auxillary files to use previously built NN model
# NN model search hyper-parameters 

NN_hyperpara = {
    'Max_trial'   : 20,           # number of trials for architecture search 
    'NN_nodes'    : [128,64,32],      # search space for NN nodes per layer
    'NN_layers'   : [2,4,6,8],      # search space for NN layers 
    'NN_branches' : [2,4],        # search space for NN Branches: even only
    'maxit_trial' : 250,          # max iterations during trial (100-500)
    'maxit_base'  : 1000,         # max iterations: base model (500-5000)
    'maxit_ensemble' : 10000      # max iterations: ensemble model (5-10K)
}
Ensemble_Model_Train = False

# NN model early stopping hyper-parameters 
early_stop_para =  {
    'start_after_cycle_base' :  20,   # 20-50% of max iterations: base
    'patience_step_base'     :   5,   # 5-10% of max iterations: base
    'start_after_cycle_en'   :  50,   # 50% of max iterations: ensemble 
    'patience_step_en'       :  10   # 10% of max iterations: ensemble
}

##########################  Optional Commands ##################################
# Commands to rearrange/scale and remove columns in dataset (Uncomment to Use)
# Default values 0: Uncomment and set variables to 1: follow on screen commands

#rearrange_columns = 1     # rearrange position of columns in dataframe
#drop_columns = 1          # drop any non-required column
#scale_columns = 1         # scale R, theta and energy into different units

##########################  Advanced commands ##################################

#--------------------------     Plot Scale   ----------------------------------#
# for +ive logarithmic scale: "log" | for both +ive and -ive log scale: "symlog"
# Default values are provided as given below

# Sorted Partitioned/Unpartitioned plot
#plt_srt_yscale = 'symlog'          # 'linear' | 'log' | 'symlog'| etc...
#plt_srt_xscale = 'linear'          # 'linear' | 'log' | 'symlog'| etc...

# Boundary Partitioned/Unpartitioned plot
#plt_bnd_yscale = 'linear'          # 'linear' | 'log' | 'symlog'| etc...
#plt_bnd_xscale = 'linear'          # 'linear' | 'log' | 'symlog'| etc...

#--------------------------  Partition  ---------------------------------------#

#partition_req = 0     # partition the data into high energy and minima region
                       # by default 1
#auto_cutoff = False   # if False, follow on screen commands,
                       # if True, give High_E_cutoff in input file
#reference_output = 3  # reference column for sorting, partitioning and plotting
                       # default: first output column for multiple output data

#--------------------------   NN model  ---------------------------------------#

#generic_model = True  # use generic model insted of default model (R/theta PES)
                       # The genaric model does not constraint R

#HE_train = False      # combine HE data in NN model (provide HE_epochs below)
#HE_epochs = 100       # (50-200) WARNING: Large epochs will degrade minima
###############################################################################
