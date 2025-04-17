#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:28:43 2023

@author: Apoorv Kushwaha, Pooja Chahal, Habit Tatin & Prof. T. J. Dhilip Kumar

main file for PES2MP package (to debug/modify --> refer manual)
This program:
 (*) imports necessary libraries
 (*) creates required folders
 (*) PESGen:
     (*) calculates and moves respective Rigid Rotor(s) (RR) to COM.
     (*) generates PES using Psi4 internally (for rough estimation)
     (*) generates input files by transforming Jacobi coordinates (R, θ_n) to XYZ
     (*) auxillary scripts are provided for external calculations (Molpro/Gaussian) and collecting results
 (*) PESPlot:
     (*) Plots 1D/2D and 4D PES using (a) R vs E plots and (b) polar plots
 (*) NNGen:
     (*) Can generate NN model for augmenting PES2MP
     (*) Can handle N inputs and M outputs with PES and non-PES data
 (*) MPExp:
     (*) Does Multipole expansion of 2D and 4D PES
     (*) 2D PES is expanded using Legendre polynomials and 4D using Spherical Harmonics
     (*) Also performs inverse fitting after analytical fitting to print residual errors.
 (*) AnaFit:
     (*) Uses analytical expressions for fitting either PES or V Lambda terms.
"""

# general libraries
import numpy as np
import pandas as pd
# importing driver.py
import pes2mp_driver as driver
import os
from tqdm import tqdm 
#import re

import shutil
import sys
import importlib
from datetime import datetime

import time
import subprocess

# Start the timer.
start_time = time.time()

# uncomment the fllowing two linesto catch segmentation error!!
# import faulthandler
# faulthandler.enable()

# defining current directory for creating new directories
input_dir = os.getcwd()+'/'

# the fllowing two lines define input file for pes2mp
inputfile = sys.argv[1]
sys.path.append(input_dir)
inp = importlib.import_module(inputfile)

# original_stdout = sys.stdout # Save a reference to the original standard output
driver.varerr(inp, inp.Proj_name)
Proj_name = inp.Proj_name

out_data = input_dir + 'Projects/' + Proj_name + '/'   # directory for psi4 data
if not os.path.exists(out_data):
    os.makedirs(out_data)

input_files_data = out_data + 'input_files/' # directory for Gaussian/Molpro input files
if not os.path.exists(input_files_data):
    os.makedirs(input_files_data)

log_filex = inp.Proj_name  + '.log'      # Set a project name (Important)
f = open(out_data+log_filex, 'a+')

num_bars = 60

print("#####################################################################")
print("--- Date {} ---".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
print("#####################################################################")
print("#####################    PES2MP Initiated    ########################")
print("#####################################################################")
print('Necessary files Created')

f.write("#####################################################################")
f.write("\n--- Date {} ---".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
f.write("\n#####################################################################")
f.write("\n#####################    PES2MP Initiated    ########################")
f.write("\n#####################################################################")
f.write('\n \n /data and /project folders created. \n\n')

# with open(out_data+log_filex, 'w+') as f:
#     sys.stdout = f # Change the standard output to the file we created.
#     print('/data/ ; /psi4_PES_data/ ; /scratch/ folders created.')
#     sys.stdout = original_stdout # Reset the standard output to its original value

# The program checks for job type in the input file uses series of if-else
# commands to execute the task inside the jobtype.

try:
    inp.Create_PES_input
except:
    print("Create_PES_input not provided! Skipping PESGen module!")
    PESGen =False
    direct_plot = False
else:
    PESGen = inp.Create_PES_input


###############################################################################
###############################################################################
########################## PES Generation #####################################
###############################################################################
###############################################################################


if PESGen == True:
    print("#-------------------------------------------------------------------#")
    print("#-------------------#    Using PESGen module    #-------------------#")
    print("#-------------------------------------------------------------------#")
    
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n#-------------------#    Using PESGen module    #-------------------#")
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n\n")

    #print("Using PESGen module!")
    import psi4
    coll_1D = False
    coll_2D = False
    coll_4D = False
    # determining nature of collision (1D/2D/4D)
    f.write("\nIdentifying collision type !!!: ")
    if (len(inp.RR1_atoms) == 1 and len(inp.RR2_atoms) == 1):
        coll_1D = True
        print("\n \t atom-atom collision: Using 1D template for PES")
        f.write("\n \t atom-atom collision: Using 1D template for PES")
        driver.PES_handler(inp, 1)

    elif (len(inp.RR1_atoms) > 1 and len(inp.RR2_atoms) == 1):
        coll_2D = True
        print("\n \t RR1 has >1 atoms and RR2 has 1 atom: Using 2D Template for PES")
        f.write("\n \t RR1 has >1 atoms and RR2 has 1 atom: Using 2D Template for PES")
        driver.PES_handler(inp, 2)

    elif (len(inp.RR1_atoms) > 1 and len(inp.RR2_atoms) > 1):
        coll_4D = True
        print("\n \t Both RR1 and RR2 have >1 atoms: Using 4D Template for PES")
        f.write("\n \t Both RR1 and RR2 have >1 atoms: Using 4D Template for PES")
        driver.PES_handler(inp, 4)

    else:
        print("\n Something wrong with the input atoms.\n")
        print("\n For 1D collision, make sure that the num of atoms in the lists: RR1 = 1 and RR2 = 1")
        print("\n For 2D collision, make sure that the num of atoms in the lists: RR1 > 1 and RR2 = 1")
        print("\n For 2D collision, make sure that the num of atoms in the lists: RR1 > 1 and RR2 > 1")

        f.write("\n Something wrong with the input atoms.\n")
        f.write("\n For 1D collision, make sure that the num of atoms in the lists: RR1 = 1 and RR2 = 1")
        f.write("\n For 2D collision, make sure that the num of atoms in the lists: RR1 > 1 and RR2 = 1")
        f.write("\n For 2D collision, make sure that the num of atoms in the lists: RR1 > 1 and RR2 > 1")
        driver.exit_program()

    R = np.empty(0)
    for i in range (len(inp.R_i)):
        R_1 = np.arange(inp.R_i[i],  inp.R_f[i], inp.R_stp[i])    # R_1 from  R_i to R_f Ang with step size R_stp Ang
        R = np.concatenate((R,R_1),axis=None)         # merging R columns
    r_n = len(R)                                      # saving number of R data points
    print("\n The R coodinates are: \n", R)
    print("\n Total number of data points in R coordinates are: ", r_n)
    r4 = np.atleast_2d(R).T                              # Converting R from row to column vector
    f.write("\n \n The R coodinates are: \n")
    f.write(str(R))
    f.write("\n\n Total number of data points in R coordinates are: {} \n\n".format (r_n))

    if coll_1D:
        np.savetxt(out_data + "1D_input_coordinates.dat", R,fmt='%.2f')
        # saving input coordinates
        print("Saving input coordinates in 'Projects/{}/1D_input_coordinates.dat'".format(Proj_name))
        f.write("\n\nSaving input coordinates in 'Projects/{}/1D_input_coordinates.dat'".format(Proj_name))

    elif coll_2D:
        # creating matrix for 2D collision coordinates
        ang_i= inp.theta

        A_nr = np.ndarray(shape=(1,2))   # R, theta array initialization
        for i_gamma in tqdm(range (ang_i[0], ang_i[1], ang_i[2])):
                    b = np.array([i_gamma])                  # defining array with angle
                    c = np.tile(b,(r_n,1))                   # creating angles as columns
                    d = np.c_[ r4, c ]                       # joining r and columns
                    A_nr = np.vstack([A_nr, d])              # repeating for different geoms and joining
        A_nr = np.delete(A_nr, 0, 0)                         # deleting first row (empty)
        # sorting coordinates by theta and then R
        keys = (A_nr[:, 1], A_nr[:, 0])
        # creating matrix for 2D collision coordinates
        sorted_indices = np.lexsort(keys)
        A = A_nr[sorted_indices]
        f.write("\nCreating matrix for 2D collision coordinates")
        #f.write("\nTQDM LOOP FINISHED:\n {'|' * num_bars} 100% |\n\n")
        f.write(f"\nTQDM LOOP FINISHED:\n {'|' * num_bars} 100% |\n\n")

    # creating matrix for 4D collision coordinates
    elif coll_4D:
        phi= inp.phi
        th2= inp.theta2
        th1 = inp.theta1
        A_nr = np.ndarray(shape=(1,4))   # internal coordinates array initialization
        # to include final value in python, step size is added to it.
        for i_phi in tqdm(range (phi[0],phi[1],phi[2])):
            for j_theta2 in range (th2[0],th2[1],th2[2]):
                for k_theta1 in range (th1[0],th1[1],th1[2]):
                    b = np.array([i_phi,j_theta2,k_theta1])  # defining array with angle
                    c = np.tile(b,(r_n,1))                   # creating angles as columns
                    d = np.c_[ r4, c ]                       # joining r and columns
                    A_nr = np.vstack([A_nr, d])              # repeating for different geoms and joining
        A_nr = np.delete(A_nr, 0, 0)                         # deleting first row (empty)
        # sorting coordinates by phi, th2, th1 and then R
        keys = (A_nr[:, 3], A_nr[:, 2], A_nr[:, 1], A_nr[:, 0])
        # creating matrix for 4D collision coordinates
        sorted_indices = np.lexsort(keys)
        A = A_nr[sorted_indices]
        f.write("\nCreating matrix for 4D collision coordinates")
        f.write(f"\nTQDM LOOP FINISHED:\n {'|' * num_bars} 100% |\n\n")
    else:
        # this condition is non viable
        pass

    # checking if isotopic substitution is requested!
    try:
        inp.Use_isotope
    except:
        Use_isotope = False
        print('\n Not using isotopic substitution! \n')
    else:
        Use_isotope = inp.Use_isotope

    if Use_isotope:
        print('\n Using isotopic substitution! \n')
        f.write('\n Using isotopic substitution! \n')
        RR1_isotope_mass = inp.RR1_isotope_mass
        RR2_isotope_mass = inp.RR2_isotope_mass
        #RR1_isotope_G = inp.RR1_isotope_G
        #RR2_isotope_G = inp.RR2_isotope_G
    else:
        RR1_isotope_mass = [0] * len(inp.RR1_atoms)
        RR2_isotope_mass = [0] * len(inp.RR2_atoms)
        #RR1_isotope_G = [0] * len(inp.RR1_atoms)
        #RR2_isotope_G = [0] * len(inp.RR1_atoms)

# Printing coordinates for 2D/4D rigid rotors and extracting COM coordinates
    if coll_1D:
        pass
    else:
        # if 2D/4D collision
        print('\n Input coordinates (first 5, mid and last 5)\n')
        print(A[:5]) # prints first 5 coordinates of R, gamma
        print('---')
        half_c = int(len(A)/2)
        print(A[half_c-3:half_c+2]) # prints mid coordinates of R, gamma
        print('---')
        print(A[-5:]) # prints last 5 coordinates of R, gamma
        print("\nTotal number of input coordinates : ",len(A))

        f.write('\n Input coordinates (first 5, mid and last 5)\n')
        f.write('\n' + str(A[:5]) + '\n') # prints first 5 coordinates of R, gamma
        f.write('---')
        f.write('\n' + str(A[half_c-3:half_c+2]) + '\n' ) # prints mid coordinates of R, gamma
        f.write('---')
        f.write('\n' + str(A[-5:]) + '\n' ) # prints last 5 coordinates of R, gamma
        f.write("\nTotal number of input coordinates : {}".format(len(A)))

        # Creating rigid rotor 1 (RR1) coordinates below and extracting COM coordinates
        RR1_psi4, RR1_COM_len = driver.RR_com(f, inp.RR1_atoms, inp.RR1_bond_len,
                                              inp.Charge[0], inp.Multiplicity[0],
                                              RR1_isotope_mass)

        if coll_2D:
            np.savetxt(out_data + "2D_input_coordinates.dat", A,fmt='%.2f\t%d')
            # saving input coordinates
            print("Saving input coordinates in 'Projects/{}/2D_input_coordinates.dat'".format(Proj_name))
            f.write("\n\nSaving input coordinates in 'Projects/{}/2D_input_coordinates.dat'".format(Proj_name))

        elif coll_4D:
            np.savetxt(out_data + "4D_input_coordinates.dat", A,fmt='%.2f\t%d\t%d\t%d')
            print("Saving input coordinates in '/{}/4D_input_coordinates.dat'".format(Proj_name))
            f.write("\n\nSaving input coordinates in '/{}/4D_input_coordinates.dat'".format(Proj_name))
            # Creating RR2 input file with XYZ coordinates below and extracting COM coordinates
            RR2_psi4, RR2_COM_len = driver.RR_com(f, inp.RR2_atoms, inp.RR2_bond_len,
                                                  inp.Charge[1], inp.Multiplicity[1],
                                                  RR2_isotope_mass)

        else:
            pass

###############################################################################
#-----------------------Gaussian Input Parameters-----------------------------#
###############################################################################
    try:
        inp.Create_GAUSSIAN_input_files
    except:
        Create_GAUSSIAN_input_files = False
    else:
        Create_GAUSSIAN_input_files = inp.Create_GAUSSIAN_input_files
        print("\nCreating Gaussian Input files!\n")
        f.write("\nCreating Gaussian Input files!\n")
        
    # creating input files for Gaussian (CP corrected) ########################
    if Create_GAUSSIAN_input_files:
        gaussian_data = input_files_data + 'Gaussian_CP/'           # directory for Gaussian data
        # creating gaussian directory
        if not os.path.exists(gaussian_data):
            os.makedirs(gaussian_data)
        # appending gaussian template with charge spin and other info!
        Gaussian_input_template  = "%nprocshared={}".format(inp.proc_g)
        Gaussian_input_template += "\n%mem={}".format(inp.mem_g)
        Gaussian_input_template += "\n%chk={}.chk\n".format(inp.chk_g)
        Gaussian_input_template += inp.cmd_g

# Creating input files by calling appropriate function in driver file.
#-------------------------------# Gaussian 1D #-------------------------------#
        if coll_1D:
            FxD_geom_G = driver.gaussian_files_1D(f, Gaussian_input_template,
                                                  inp.RR1_atoms, inp.RR2_atoms,
                                                  inp.Charge, inp.Multiplicity,
                                                  R, gaussian_data)
#-------------------------------# Gaussian 2D #-------------------------------#
        elif coll_2D :
            FxD_geom_G = driver.gaussian_files_2D(f, Gaussian_input_template,
                                                  inp.RR1_atoms, inp.RR2_atoms,
                                                  inp.Charge, inp.Multiplicity,
                                                  R, gaussian_data, RR1_COM_len,A)
#-------------------------------# Gaussian 4D #-------------------------------#
        elif coll_4D:
            FxD_geom_G = driver.gaussian_files_4D(f, Gaussian_input_template,
                                                  inp.RR1_atoms, inp.RR2_atoms,
                                                  inp.Charge, inp.Multiplicity,
                                                  R, gaussian_data, RR1_COM_len,
                                                  RR2_COM_len, A)
        else:
            print('ID: 260 --> All coll_1D, coll_2D and coll_4D are False. Check for error!')

        f.write("\n---- Gaussian input file template : see Template_Gaussian_CP.dat .")
        template_filex = 'Template_Gaussian_CP.log'
        f2 = open(input_files_data+template_filex, 'a+')
        f2.write(str(FxD_geom_G))
        f2.close()
        f.write(f"\n TQDM LOOP: Gaussian input files created:\n {'|' * num_bars} 100% |\n\n")

        print(" \n Gaussian (CP) Input files Created! Check: 'Projects/{}/input_files/Gaussian_CP/' \n".format(Proj_name))
        f.write(" \n Gaussian (CP) Input files Created! Check: 'Projects/{}/input_files/Gaussian_CP/' \n".format(Proj_name))

    else:
        print(" \n Create_GAUSSIAN_input_files = False : Skipping Gaussian (CP) Input! \n")
        f.write('\n Create_GAUSSIAN_input_files = False : Skipping Gaussian (CP) Input! \n ')


###############################################################################
#-----------------------Molpro Input Parameters (CP)--------------------------#
###############################################################################
    try:
        inp.Create_MOLPRO_CP_input_files
    except:
        Create_MOLPRO_CP_input_files = False
    else:
        Create_MOLPRO_CP_input_files = inp.Create_MOLPRO_CP_input_files
        print("\nCreating molpro (CP) Input files!\n")
        f.write("\nCreating molpro (CP) Input files!\n")

    # creating input files for Molpro (CP corrected)   ########################
    if Create_MOLPRO_CP_input_files:
        molpro_data = input_files_data + 'Molpro_CP/'           # directory for psi4 data
        if not os.path.exists(molpro_data):
            os.makedirs(molpro_data)

        Molpro_input_template  = "***,single point energies \n"
        Molpro_input_template += "memory,{}\n".format(inp.mem_m)
        Molpro_input_template += "basis= {}\n".format(inp.basis_cp)
        Molpro_input_template += "run_method={}\n".format(inp.run_method)

        # converting RR atoms with label eg. C1, C2, etc.
        RR1_name = [f'{name}{ii}' for ii, name in enumerate(inp.RR1_atoms, 1)]
        RR2_name = [f'{name}{iii}' for iii, name in enumerate(inp.RR2_atoms, len(inp.RR1_atoms)+1)]

        #print(psi4.core.Molecule.mass(RR1_psi4))
#-----------------------------# Molpro 1D (CP) #------------------------------#
        if coll_1D:
            FxD_geom_M = driver.molpro_files_CP_1D(f, Molpro_input_template, RR1_name, RR2_name,
                                                   inp.Charge, inp.Multiplicity, R, molpro_data)
#-------------------------------# Molpro 2D #-------------------------------#
        elif coll_2D :
            FxD_geom_M = driver.molpro_files_CP_2D(f, Molpro_input_template, RR1_name, RR2_name,
                                                   inp.Charge, inp.Multiplicity, R, molpro_data,
                                                   RR1_COM_len, A)
#-------------------------------# Molpro 4D #-------------------------------#
        elif coll_4D:
            FxD_geom_M = driver.molpro_files_CP_4D(f, Molpro_input_template, RR1_name, RR2_name,
                                                   inp.Charge, inp.Multiplicity, R, molpro_data,
                                                   RR1_COM_len, RR2_COM_len, A)
        else:
            print('ID: 317 --> All coll_1D, coll_2D and coll_4D are False. Check for error!')

        f.write("\n---- Molpro input file template : see Template_Molpro_CP.dat.")
        template_filex = 'Template_Molpro_CP.log'
        f3 = open(input_files_data+template_filex, 'a+')
        f3.write(str(FxD_geom_M))
        f3.close()
        f.write(f"\n TQDM LOOP: Molpro (CP) input files created:\n {'|' * num_bars} 100% |\n\n")

        print(" \n Molpro (CP) Input files Created! Check: 'Projects/{}/input_files/Molpro_CP/' \n".format(Proj_name))
        f.write(" \n Molpro (CP) Input files Created! Check: 'Projects/{}/input_files/Molpro_CP/' \n".format(Proj_name))

    else:
        print(" \n Create_MOLPRO_input_files = False : Skipping Molpro (CP) Input! \n")
        f.write('\n Create_MOLPRO_input_files = False : Skipping Molpro (CP) Input! \n ')



###############################################################################
#----------------------Molpro Input Parameters (CBS)--------------------------#
###############################################################################
    try:
        inp.Create_MOLPRO_CBS_input_files
    except:
        Create_MOLPRO_CBS_input_files = False
    else:
        Create_MOLPRO_CBS_input_files = inp.Create_MOLPRO_CBS_input_files
        print("\nCreating molpro (CBS) Input files!\n")
        f.write("\nCreating molpro (CBS) Input files!\n")

    # creating input files for Molpro (CBS extrapolated energies) #############
    if Create_MOLPRO_CBS_input_files:
        molpro_cbs_data = input_files_data + 'Molpro_CBS/'           # directory for psi4 data
        if not os.path.exists(molpro_cbs_data):
            os.makedirs(molpro_cbs_data)

        Molpro_cbs_template  = "***,single point energies \n"
        Molpro_cbs_template += "memory,{} \n".format(inp.mem_m)
        Molpro_cbs_template += "run_method={} \n".format(inp.run_method)

        # converting RR atoms with label eg. C1, C2, etc.
        RR1_name = [f'{name}{ii}' for ii, name in enumerate(inp.RR1_atoms, 1)]
        RR2_name = [f'{name}{iii}' for iii, name in enumerate(inp.RR2_atoms, len(inp.RR1_atoms)+1)]

#-----------------------------# Molpro 1D (CBS) #------------------------------#
        if coll_1D:
            FxD_geom_M_cbs = driver.molpro_files_CBS_1D(f, Molpro_cbs_template, RR1_name, RR2_name,
                                                        inp.Charge, inp.Multiplicity, R, molpro_cbs_data,
                                                        inp.basis_ref,inp.basis_cbs)
#-------------------------------# Molpro 2D #-------------------------------#
        elif coll_2D :
            FxD_geom_M_cbs = driver.molpro_files_CBS_2D(f, Molpro_cbs_template, RR1_name, RR2_name,
                                                        inp.Charge, inp.Multiplicity, R, molpro_cbs_data,
                                                        RR1_COM_len, A, inp.basis_ref,inp.basis_cbs)
#-------------------------------# Molpro 4D #-------------------------------#
        elif coll_4D:
            FxD_geom_M_cbs = driver.molpro_files_CBS_4D(f, Molpro_cbs_template, RR1_name, RR2_name,
                                                        inp.Charge, inp.Multiplicity, R, molpro_cbs_data,
                                                        RR1_COM_len, RR2_COM_len, A,
                                                        inp.basis_ref,inp.basis_cbs)
        else:
            print('ID: 375 --> All coll_1D, coll_2D and coll_4D are False. Check for error!')

        f.write("\n---- Molpro input file template : see Template_Molpro_CBS.dat.")
        template_filex = 'Template_Molpro_CBS.log'
        f4 = open(input_files_data+template_filex, 'a+')
        f4.write(str(FxD_geom_M_cbs))
        f4.close()
        f.write(f"\n TQDM LOOP: Molpro(CBS) input files created:\n {'|' * num_bars} 100% |\n\n")

        print(" \n Molpro (CBS) Input files Created! Check: 'Projects/{}/input_files/Molpro_CBS/' \n".format(Proj_name))
        f.write(" \n Molpro (CBS) Input files Created! Check: 'Projects/{}/input_files/Molpro_CBS/' \n".format(Proj_name))

    else:
        print(" \n Create_MOLPRO_CBS_input_files = False : Skipping Molpro (CBS) Input! \n")
        f.write('\n Create_MOLPRO_CBS_input_files = False : Skipping Molpro (CBS) Input! \n ')

###############################################################################
#----------------------Molpro Input Parameters (Custom)-----------------------#
###############################################################################
    try:
        inp.Create_MOLPRO_custom_input_files
    except:
        Create_MOLPRO_custom_input_files = False
    else:
        Create_MOLPRO_custom_input_files = inp.Create_MOLPRO_custom_input_files
        print("\nCreating molpro (custom) Input files!\n")
        f.write("\nCreating molpro (custom) Input files!\n")

    # creating input files for Molpro (custom input) #############
    if Create_MOLPRO_custom_input_files:
        molpro_custom_data = input_files_data + 'Molpro_custom/'           # directory for psi4 data
        if not os.path.exists(molpro_custom_data):
            os.makedirs(molpro_custom_data)

        Molpro_custom_template  = "***,single point energies \n"
        Molpro_custom_template += "memory,{} \n".format(inp.mem_m)

        # converting RR atoms with label eg. C1, C2, etc.
        RR1_name = [f'{name}{ii}' for ii, name in enumerate(inp.RR1_atoms, 1)]
        RR2_name = [f'{name}{iii}' for iii, name in enumerate(inp.RR2_atoms, len(inp.RR1_atoms)+1)]

#-----------------------------# Molpro 1D (CBS) #------------------------------#
        if coll_1D:
            FxD_geom_M_ext = driver.molpro_files_custom_1D(f, Molpro_custom_template, RR1_name, RR2_name,
                                                           inp.Charge, inp.Multiplicity, R, molpro_custom_data,
                                                           inp.molpro_ext)
#-------------------------------# Molpro 2D #-------------------------------#
        elif coll_2D :
            FxD_geom_M_ext = driver.molpro_files_custom_2D(f, Molpro_custom_template, RR1_name, RR2_name,
                                                           inp.Charge, inp.Multiplicity, R, molpro_custom_data,
                                                           RR1_COM_len, A, inp.molpro_ext)
#-------------------------------# Molpro 4D #-------------------------------#
        elif coll_4D:
            FxD_geom_M_ext = driver.molpro_files_custom_4D(f, Molpro_custom_template, RR1_name, RR2_name,
                                                           inp.Charge, inp.Multiplicity, R, molpro_custom_data,
                                                           RR1_COM_len, RR2_COM_len, A, inp.molpro_ext)
        else:
            print('ID: 428 --> All coll_1D, coll_2D and coll_4D are False. Check for error!')

        f.write("\n---- Molpro input file template : see Template_Molpro_custom.dat.")
        template_filex = 'Template_Molpro_custom.log'
        f5 = open(input_files_data+template_filex, 'a+')
        f5.write(str(FxD_geom_M_ext))
        f5.close()
        f.write(f"\n TQDM LOOP: Molpro (custom)  input files created:\n {'|' * num_bars} 100% |\n\n")

        print(" \n Molpro (custom) Input files Created! Check: 'Projects/{}/input_files/Molpro_custom/' \n".format(Proj_name))
        f.write(" \n Molpro (custom) Input files Created! Check: 'Projects/{}/input_files/Molpro_custom/' \n".format(Proj_name))
    else:
        print(" \n Create_MOLPRO_custom_input_files = False : Skipping Molpro (custom) Input! \n")
        f.write('\n Create_MOLPRO_custom_input_files = False : Skipping Molpro (custom) Input! \n ')

###############################################################################
#--------- Psi4 Input Parameters (Custom for external calculation) -----------#
###############################################################################
    try:
        inp.Create_Psi4_custom_input_files
    except:
        Create_Psi4_custom_input_files = False
    else:
        Create_Psi4_custom_input_files = inp.Create_Psi4_custom_input_files
        print("\nCreating Psi4 (custom) Input files!\n")
        f.write("\nCreating Psi4 (custom) Input files!\n")

    # creating input files for Psi4 (Custom Template) #############
    if Create_Psi4_custom_input_files:
        psi4_custom_data = input_files_data + 'psi4_custom/'           # directory for psi4 data
        if not os.path.exists(psi4_custom_data):
            os.makedirs(psi4_custom_data)

        Psi4_custom_template = 'molecule {{'
#-----------------------------# Psi4 1D (Custom) #------------------------------#
        if coll_1D:
            FxD_geom_psi4 = driver.psi4_input_1D(inp)
            Psi4_custom_template += FxD_geom_psi4
            Psi4_custom_template += '}}'
            Psi4_custom_template += '\nR = {:.4f}\n'
            Psi4_custom_template += inp.psi4_ext
            for j in tqdm(range (len(R))):    # python loop to generate PES
                R_ii     = R[j]               # radial  coordinate
                inp_file = open(psi4_custom_data + '{:d}.inp'.format(int(j)), "w")  # open input file
                inp_file.write(Psi4_custom_template.format(R_ii,R_ii))   # write string to file
                inp_file.close()              # close file
            f.write(f"\n TQDM LOOP: Psi4 1D input files created:\n {'|' * num_bars} 100% |\n\n")
#-----------------------------# Psi4 2D (Custom) #------------------------------#
        elif coll_2D :
            FxD_geom_psi4 = driver.psi4_input_2D(inp,RR1_psi4)
            Psi4_custom_template += FxD_geom_psi4
            Psi4_custom_template += '}}'
            Psi4_custom_template += '\nR = {:.4f} \nTheta = {:.4f}\n'
            Psi4_custom_template += inp.psi4_ext
            for j in tqdm(range (len(A))):    # python loop to generate PES
                R     = A[j,0]     # radial  coordinate
                gamma = A[j,1]     # angular coordinate
                # Rigid rotor (RR) lies on Z axis (no rotation of RR : no projection)
                R_x, R_z = driver.proj2D (R, gamma)
                inp_file = open(psi4_custom_data + '{:d}.inp'.format(int(j)), "w")  # open input file
                inp_file.write(Psi4_custom_template.format(R_x, R_z,R, gamma))
                inp_file.close()              # close file
            f.write(f"\n TQDM LOOP: Psi4 2D input files created:\n {'|' * num_bars} 100% |\n\n")

#-----------------------------# Psi4 4D (Custom) #------------------------------#
        elif coll_4D:
            FxD_geom_psi4 = driver.psi4_input_4D(inp,RR1_COM_len,RR2_COM_len)
            Psi4_custom_template += FxD_geom_psi4
            Psi4_custom_template += '}}'
            Psi4_custom_template += '\nR = {:.4f} \nPhi = {:.4f} \nTheta2 = {:.4f} \nTheta1 = {:.4f}'
            Psi4_custom_template += inp.psi4_ext
            for j in tqdm(range (len(A))):    # python loop to generate PES
                R      = A[j,0]                        # radial  coordinate
                phi    = A[j,1]                        # angular coordinate phi
                theta2 = A[j,2]                        # angular coordinate theta2
                theta1 = A[j,3]                        # angular coordinate theta1
                RR_mat = driver.proj4D (R, phi, theta2, theta1, RR1_COM_len, RR2_COM_len)   # calling 4D projection function
                inp_file = open(psi4_custom_data + '{:d}.inp'.format(int(j)), "w")  # open input file
                inp_file.write(Psi4_custom_template.format(*RR_mat,R, phi, theta2, theta1))
                inp_file.close()              # close file
            f.write(f"\n TQDM LOOP: Psi4 4D input files created:\n {'|' * num_bars} 100% |\n\n")

        else:
            print('ID: 475 --> All coll_1D, coll_2D and coll_4D are False. Check for error!')

        template_filex = 'Template_psi4_custom.log'
        f5 = open(input_files_data+template_filex, 'a+')
        f5.write(str(Psi4_custom_template))
        f5.close()

        print(" \n Psi4 (custom) Input files Created! Check: 'Projects/{}/input_files/psi4_custom/' \n".format(Proj_name))
        f.write("\n Psi4 (custom) Input files Created! Check: 'Projects/{}/input_files/psi4_custom/' \n".format(Proj_name))
    else:
        print(" \n Create_Psi4_custom_input_files = False : Skipping Psi4 (custom) Input! \n")
        f.write('\n Create_Psi4_custom_input_files = False : Skipping Psi4 (custom) Input! \n ')

################################################################################
#----------------- Running Psi4 calculations internally------------------------#
################################################################################
#Important:

#Try/Except/Finally block (in Psi4 - for rough PES calculation):
#Use 'pass' to ignore failed calculations (only store data points that converge)
#Use 'raise' to show error ! --> to debug code
################################################################################
    try:
        inp.Run_psi4
    except:
        Run_psi4 = False
    else:
        Run_psi4 = inp.Run_psi4

    if Run_psi4:
        direct_plot = True
        psi4_int = out_data + 'psi4_PES_data/'           # directory for psi4 data
        psi4_data = psi4_int + 'data/'           # directory for psi4 data
        if not os.path.exists(psi4_data):
            os.makedirs(psi4_data)

        scratch_dir = psi4_int + 'scratch/'      # scratch directory for Psi4
        if not os.path.exists(scratch_dir):
            os.makedirs(scratch_dir)
        f1 = open(psi4_int+'psi4_failed_coordinates', 'a+')
        psi4_io = psi4.core.IOManager.shared_object()
        psi4_io.set_default_path(scratch_dir)
        psi4.set_memory(inp.psi4_mem)
        psi4.set_num_threads(inp.psi4_proc)
        print("Generating Psi4 PES!")
        f.write("Generating Psi4 PES!")
        # 1D PES calculation using psi4
        if coll_1D:
            # geometry specifications
            ecp = {}     # dictionary for energies
            F1D_geom = driver.psi4_input_1D(inp)
            # print(" \n Psi4 Input : \n ")
            # print(F1D_geom)
            f.write(" \n Psi4 Input : \n ")
            f.write('-x'*30 + '\n')
            f.write(str(F1D_geom))
            f.write('-x'*30 + '\n')
            print(F1D_geom)
            for fx in os.listdir(scratch_dir):        # removing any previous scratch files
                os.remove(os.path.join(scratch_dir, fx))

            for j in tqdm(range (len(R))):      # python loop to generate PES (using try and except to suppress error)
                try:
                    R_ii = R[j]     # radial  coordinate
                    # Rigid rotor (RR) lies on Z axis (no rotation of RR : no projection)
                    psi4.core.set_output_file(psi4_data+'{:.2f}.out'.format(R_ii), False) # sets output file location
                    F1D_mol = psi4.geometry(F1D_geom.format(R_ii))
                    psi4_inp = psi4.core.Molecule.create_psi4_string_from_molecule(F1D_mol)

                    psi4.set_options({'reference': inp.psi4_reference,'freeze_core': inp.psi4_Frozen_Core})
                    if inp.psi4_bsse == None:
                        ecp[j] = psi4.energy(inp.psi4_method_basis, molecule=F1D_mol)
                    else:
                        ecp[j] = psi4.energy(inp.psi4_method_basis, bsse_type= inp.psi4_bsse,
                                             return_total_data=True, molecule=F1D_mol)
                except:
                    print("\n\n")
                    print ("Failed coordinate : (R = %.2f) \n" % (R_ii) )
                    f1.write("Failed coordinate : (R = %.2f) \n" % (R_ii) )
                    # replace 'pass' with 'raise' to show error ! to debug code
                    pass
                finally:
                    psi4.core.close_outfile()
                    try:
                        os.remove(psi4_data+'{:.2f}.log'.format(R_ii)) # removing log file (too large)
                    except:
                        pass
                    psi4.core.clean()
                    psi4.core.clean_variables()
                    psi4.core.clean_options()
                    psi4.core.clean_timers()
                    for fx in os.listdir(scratch_dir):        # removing remaining files after psi4 clean()
                        os.remove(os.path.join(scratch_dir, fx))
            f.write(f"\n TQDM LOOP: Psi4 1D PES created:\n {'|' * num_bars} 100% |\n\n")
            #####################################################################################################################
            # coordinates for calculating E_inf ( to convert energies to cm-1 )
            R_inf         = inp.R_inf
            #####################################################################################################################

            # Section 4.0.2 : Calculating E infinity (200 Angstroms) at 90 degrees (BSSE approx. 0 at infinity)
            # print("\n Geometry at infinity: \n ", F1D_geom.format(R_inf))
            f.write("\n Geometry at infinity: \n ")
            f.write("R = {}".format(R_inf))
            psi4.core.set_output_file(psi4_data+'E_Inf.out',False) # sets output file location
            F1D_mol_inf = psi4.geometry(F1D_geom.format(R_inf))
            psi4.set_options({'reference': inp.psi4_reference,'freeze_core': inp.psi4_Frozen_Core})
            try:
                if inp.psi4_bsse == None:
                    ecp_inf = psi4.energy(inp.psi4_method_basis, molecule=F1D_mol_inf)
                else:
                    ecp_inf = psi4.energy(inp.psi4_method_basis, bsse_type= inp.psi4_bsse,
                                          return_total_data=True, molecule=F1D_mol_inf)
                #os.remove(psi4_data+'E_Inf.log') # removing log file
                psi4.core.clean()
            except:
                print('E infinity convergence failed! using last converged energy')
                f.write('\n E infinity convergence failed! using last converged energy \n')
                ecp_inf = list(ecp.values())[-1]
                print(list(ecp.values())[-1])
                pass
            print("\n Energy at inifinity (Hartree): ", ecp_inf)
            f.write("\n Energy at inifinity (Hartree): {}"  .format(ecp_inf) )
            # converting ecp diectionary into dataframe
            df_ecp = pd.DataFrame.from_dict([ecp]).T
            df_ecp.columns = ['E'] # giving suitable name for header
            # converting coordinates to dataframe with suitable names
            df_A = pd.DataFrame({'R': R })

            # merging coordinate and energy dataframes
            # The coordinates for which calculations have failed are dropped automatically
            merged_df = pd.merge(df_A, df_ecp, left_index=True, right_index=True)
            # set precision of each column
            merged_df['R']     = merged_df['R'].apply(lambda x: format(x,".2f"))
            merged_df['E']  = merged_df['E'].apply(lambda x: round(x,12))

            # saving csv file
            merged_df.to_csv(psi4_int + inp.PES_filename, index=None, header=True,sep='\t')

            # converting energies in cm-1 and saving file
            merged_df['E'] = (merged_df['E']-ecp_inf)*219474.6
            merged_df['E'] = merged_df['E'].apply(lambda x: round(x,6))
            merged_df.to_csv(out_data + inp.PES_filename_cm, index=None, header=True,sep='\t')
            print("All required files are saved ! Check folder --> ", out_data)
            try:
                shutil.rmtree(scratch_dir) # removing scratch directory (residual files)
                print("Scratch Directory Removed!")
            except:
                print("Most probably the scratch directory is already deleted! \n To see error replace 'pass' with 'raise' in the code.")
                pass

        # 2D PES calculation using psi4
        elif coll_2D:
            # geometry specifications
            ecp = {}     # dictionary for energies
            F2D_geom = driver.psi4_input_2D(inp, RR1_psi4)
            # print(" \n Psi4 Input : \n ")
            #print(F2D_geom)
            f.write(" \n Psi4 Input : \n ")
            f.write(str(F2D_geom))

            for fx in os.listdir(scratch_dir):        # removing any previous scratch files
                os.remove(os.path.join(scratch_dir, fx))

            for j in tqdm(range (len(A))):      # python loop to generate PES (using try and except to suppress error)
                try:
                    R     = A[j,0]     # radial  coordinate
                    gamma = A[j,1]     # angular coordinate
                    # Rigid rotor (RR) lies on Z axis (no rotation of RR : no projection)
                    R_x, R_z = driver.proj2D (R, gamma)
                    psi4.core.set_output_file(psi4_data+'{:.2f}_{:d}.out'.format(R,int(gamma)), False) # sets output file location

                    F2D_mol = psi4.geometry(F2D_geom.format(R_x, R_z))
                    psi4.set_options({'reference': inp.psi4_reference,'freeze_core': inp.psi4_Frozen_Core})
                    if inp.psi4_bsse == None:
                        ecp[j] = psi4.energy(inp.psi4_method_basis, molecule=F2D_mol)
                    else:
                        ecp[j] = psi4.energy(inp.psi4_method_basis, bsse_type= inp.psi4_bsse,
                                             return_total_data=True, molecule=F2D_mol)
                except:
                    print ("Failed coordinate : (R = %.2f, theta = %d ) \n" % (A[j,0], A[j,1]) )
                    f1.write("Failed coordinate : (R = %.2f, theta = %d ) \n" % (A[j,0], A[j,1]) )
                    # replace 'pass' with 'raise' to show error ! to debug code
                    pass
                finally:
                    psi4.core.close_outfile()
                    try:
                        os.remove(psi4_data+'{:.2f}_{:d}.log'.format(R,int(gamma))) # removing log file
                    except:
                        pass
                    psi4.core.clean()
                    psi4.core.clean_variables()
                    psi4.core.clean_options()
                    psi4.core.clean_timers()
                    for fx in os.listdir(scratch_dir):        # removing remaining files after psi4 clean()
                        os.remove(os.path.join(scratch_dir, fx))
            
            f.write(f"\n TQDM LOOP: Psi4 2D PES created:\n {'|' * num_bars} 100% |\n\n")
            #####################################################################################################################
            # coordinates for calculating E_inf ( to convert energies to cm-1 )
            R_inf         = inp.R_inf
            ang_inf       = inp.theta_2D_inf
            #####################################################################################################################

            # Section 4.0.2 : Calculating E infinity (200 Angstroms) at 90 degrees (BSSE approx. 0 at infinity)
            R_x_inf, R_z_inf = driver.proj2D (R_inf, ang_inf)
            # print("\n Geometry at infinity: \n ", F2D_geom.format(R_x_inf, R_z_inf))
            f.write("\n Geometry at infinity: \n ")
            f.write("R = {}\n Theta = {}\n".format(R_inf,ang_inf))
            psi4.core.set_output_file(psi4_data+'E_Inf.out',False) # sets output file location
            F2D_mol_inf = psi4.geometry(F2D_geom.format(R_x, R_z))
            psi4.set_options({'reference': inp.psi4_reference,'freeze_core': inp.psi4_Frozen_Core})
            try:
                if inp.psi4_bsse == None:
                    ecp_inf = psi4.energy(inp.psi4_method_basis, molecule=F2D_mol_inf)
                else:
                    ecp_inf = psi4.energy(inp.psi4_method_basis, bsse_type= inp.psi4_bsse,
                                          return_total_data=True, molecule=F2D_mol_inf)
                #os.remove(psi4_data+'E_Inf.log') # removing log file
                psi4.core.clean()
            except:
                print('E infinity convergence failed! using last converged energy')
                f.write('E infinity convergence failed! using last converged energy \n ')
                ecp_inf = list(ecp.values())[-1]
                print(list(ecp.values())[-1])
                pass

            print("\n Energy at inifinity (Hartree): ", ecp_inf)
            f.write("\n Energy at inifinity (Hartree): " )
            f.write(str(ecp_inf))
            # converting ecp diectionary into dataframe
            df_ecp = pd.DataFrame.from_dict([ecp]).T
            df_ecp.columns = ['E'] # giving suitable name for header
            # converting coordinates to dataframe with suitable names
            df_A = pd.DataFrame({'R': A[:, 0], 'Gamma': A[:, 1]})

            # merging coordinate and energy dataframes
            # The coordinates for which calculations have failed are dropped automatically
            merged_df = pd.merge(df_A, df_ecp, left_index=True, right_index=True)
            # set precision of each column
            merged_df['R']     = merged_df['R'].apply(lambda x: format(x,".2f"))
            merged_df['Gamma'] = merged_df['Gamma'].apply(lambda x: format(x,".0f"))
            merged_df['E']  = merged_df['E'].apply(lambda x: round(x,12))

            # saving csv file
            merged_df.to_csv(psi4_int + inp.PES_filename, index=None, header=True,sep='\t')

            # converting energies in cm-1 and saving file
            merged_df['E'] = (merged_df['E']-ecp_inf)*219474.6
            merged_df['E'] = merged_df['E'].apply(lambda x: round(x,6))
            merged_df.to_csv(out_data + inp.PES_filename_cm, index=None, header=True,sep='\t')
            print("All required files are saved ! Check folder --> ", out_data)
            try:
                shutil.rmtree(scratch_dir) # removing scratch directory (residual files)
                print("Scratch Directory Removed!")
            except:
                print("Most probably the scratch directory is already deleted! \n To see error replace 'pass' with 'raise' in the code.")
                pass

        # 4D PES calculation using psi4
        elif coll_4D:
            ecp = {}     # dictionary for energies
            F4D_geom = driver.psi4_input_4D(inp,RR1_COM_len,RR2_COM_len)
            # print(" \n Psi4 Input : \n ")
            # print(F4D_geom)
            f.write(" \n Psi4 Input : \n ")
            f.write(str(F4D_geom))

            for fx in os.listdir(scratch_dir):        # removing any previous scratch files
                os.remove(os.path.join(scratch_dir, fx))
            for j in tqdm(range (len(A))):      # python loop to generate PES (using try and except to suppress convergence error)
                try:
                    R      = A[j,0]                        # radial  coordinate
                    phi    = A[j,1]                        # angular coordinate phi
                    theta2 = A[j,2]                        # angular coordinate theta2
                    theta1 = A[j,3]                        # angular coordinate theta1
                    RR_mat = driver.proj4D (R, phi, theta2, theta1, RR1_COM_len, RR2_COM_len)   # calling 4D projection function
                    psi4.core.set_output_file(psi4_data+'{:.2f}_{:d}_{:d}_{:d}.out'.format(R,int(phi),int(theta2),int(theta1)),
                                         False) # sets output file location
                    F4D_mol = psi4.geometry(F4D_geom.format(*RR_mat))
                    psi4.set_options({'reference': inp.psi4_reference,'freeze_core': inp.psi4_Frozen_Core})
                    if inp.psi4_bsse == None:
                        ecp[j] = psi4.energy(inp.psi4_method_basis, molecule=F4D_mol)
                    else:
                        ecp[j] = psi4.energy(inp.psi4_method_basis, bsse_type= inp.psi4_bsse,
                                             return_total_data=True, molecule=F4D_mol)
                except:
                    print ("Failed coordinate : (R = %.2f, phi = %d, theta2= %d, theta1= %d ) \n" % (A[j,0], A[j,1], A[j,2], A[j,3]) )
                    f1.write("Failed coordinate : (R = %.2f, phi = %d, theta2= %d, theta1= %d ) \n" % (A[j,0], A[j,1], A[j,2], A[j,3]) )
                    # replace 'pass' with 'raise' to show error ! to debug code
                    pass
                finally:
                    psi4.core.close_outfile()
                    try:
                        os.remove(psi4_data+'{:.2f}_{:d}_{:d}_{:d}.log'.format(R,int(phi),int(theta2),int(theta1))) # removing log file
                    except:
                        pass
                    psi4.core.clean()
                    psi4.core.clean_variables()
                    psi4.core.clean_options()
                    psi4.core.clean_timers()
                    for fx in os.listdir(scratch_dir):        # removing remaining files after psi4 clean()
                        os.remove(os.path.join(scratch_dir, fx))

            f.write(f"\n TQDM LOOP: Psi4 4D PES created:\n {'|' * num_bars} 100% |\n\n")

            #####################################################################################################################
            # coordinates for calculating E_inf ( to convert energies to cm-1 )
            R_inf         = inp.R_inf
            phi_inf       = inp.phi_4D_inf
            theta2_inf    = inp.theta2_4D_inf
            theta1_inf    = inp.theta1_4D_inf
            #####################################################################################################################

            # Section 4.0.2 : Calculating E infinity (200 Angstroms) at 90 degrees (BSSE approx. 0 at infinity)
            RR_mat_inf = driver.proj4D ( R_inf, phi_inf, theta2_inf, theta1_inf, RR1_COM_len, RR2_COM_len)   # calling 4D projection function
            F4D_mol_inf = psi4.geometry(F4D_geom.format(*RR_mat_inf))
            # print("\n Geometry at infinity: \n ", F4D_geom.format(*RR_mat_inf))
            f.write("\n Geometry at infinity: \n ")
            f.write(" R = {}\n Phi = {}\n Theta 2 = {}\n Theta 1 = {}\n".format(R_inf,phi_inf, theta2_inf, theta1_inf))
            psi4.core.set_output_file(psi4_data+'E_Inf.out',False) # sets output file location
            psi4.set_options({'reference': inp.psi4_reference,'freeze_core': inp.psi4_Frozen_Core})
            try:
                if inp.psi4_bsse == None:
                    ecp_inf = psi4.energy(inp.psi4_method_basis, molecule=F4D_mol_inf)
                else:
                    ecp_inf = psi4.energy(inp.psi4_method_basis, bsse_type= inp.psi4_bsse,
                                          return_total_data=True, molecule=F4D_mol_inf)
                #os.remove(psi4_data+'E_Inf.log') # removing log file
                psi4.core.clean()
            except:
                print('E infinity convergence failed! using last converged energy')
                f.write('\n E infinity convergence failed! using last converged energy \n')
                ecp_inf = list(ecp.values())[-1]
                print(list(ecp.values())[-1])
                pass

            print("\n Energy at inifinity (Hartree): ", ecp_inf)
            f.write("\n Energy at inifinity (Hartree): ")
            f.write(str(ecp_inf))
            #####################################################################################################################
            # converting ecp diectionary into dataframe
            df_ecp = pd.DataFrame.from_dict([ecp]).T
            df_ecp.columns = ['E'] # giving suitable name for header
            # converting coordinates to dataframe with suitable names
            df_A = pd.DataFrame({'R': A[:, 0], 'phi': A[:, 1], 'theta2': A[:, 2], 'theta1': A[:, 3]})

            # merging coordinate and energy dataframes
            # The coordinates for which calculations have failed are dropped automatically
            merged_df = pd.merge(df_A, df_ecp, left_index=True, right_index=True)
            # set precision of each column
            merged_df['R']     = merged_df['R'].apply(lambda x: format(x,".2f"))
            merged_df['phi'] = merged_df['phi'].apply(lambda x: format(x,".0f"))
            merged_df['theta2'] = merged_df['theta2'].apply(lambda x: format(x,".0f"))
            merged_df['theta1'] = merged_df['theta1'].apply(lambda x: format(x,".0f"))
            merged_df['E']  = merged_df['E'].apply(lambda x: round(x,12))

            # saving csv file
            merged_df.to_csv(psi4_int + inp.PES_filename, index=None, header=True,sep='\t')

            # converting energies in cm-1 and saving file
            merged_df['E'] = (merged_df['E']-ecp_inf)*219474.6
            merged_df['E'] = merged_df['E'].apply(lambda x: round(x,6))
            merged_df.to_csv(out_data + inp.PES_filename_cm, index=None, header=True,sep='\t')
            print("All required files are saved ! \n  Check folder : \n ", out_data)
            try:
                shutil.rmtree(scratch_dir)                    # removing scratch directory (along with residual files)
                print("Scratch Directory Removed!")
            except:
                print("Most probably the scratch directory is already deleted! \n To see error replace 'pass' with 'raise' in the code.")
        else:
            print('ID: 235 --> All coll_1D, coll_2D and coll_4D are False. Check for error!')

        print(" \n Psi4 calculations finished! \n")
        f.write('\n Psi4 calculations finished! \n ')
        f1.close()
    else:
        direct_plot = False
        print(" \n Run_psi4 = False : Skipping Psi4 calculations! \n")
        f.write('\n Run_psi4 = False : Skipping Psi4 calculations! \n ')

    print("#-------------------------------------------------------------------#")
    print("#--------------#    PES Files Created Successfully    #-------------#")
    print("#-------------------------------------------------------------------#")

    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n#--------------#    PES Files Created Successfully    #-------------#")
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n\n")

else:
    print(" \n Create_PES_input = False : Checking input for external Plots \n")
    f.write('\n Create_PES_input = False : Checking input for external Plots! \n ')


###############################################################################
###############################################################################
############################# PES Plot ########################################
###############################################################################
###############################################################################


try:
    inp.Plot_PES
except:
    print("Plot_PES not defined! Skipping PES plots!")
    Plot_PES =False
else:
    Plot_PES = inp.Plot_PES

# plotting psi4 or any other dataframe in required format
if (direct_plot == True or Plot_PES == True):
    print("#-------------------------------------------------------------------#")
    print("#------------------#    Using PES Plot module    #------------------#")
    print("#-------------------------------------------------------------------#")
    
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n#------------------#    Using PES Plot module    #------------------#")
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n\n")

    #print("Using Plot module!")
    if direct_plot:
        print('\nPlotting PES from Psi4 output.')
        f.write('\nPlotting PES from Psi4 output.\n')
        print("The energies at very small R distance don't usually converge (may give : -inf ) and ruin the plots !")
        print("Check and remove unconverged coordinates/energies in : ",out_data+inp.PES_filename_cm)
        df_out1 = pd.read_csv(out_data+inp.PES_filename_cm,sep='\s+')
        print(df_out1.head(5))
        print("\n If you have missed unconverged points, EXIT and replot PES using PESPlot input file! \n")
        f.write("\nIf you have unconverged points, remove them, and replot PES using PESPlot input file! \n\n ")
        input("Satisfied! Press Enter to continue...")
        f.write(str(df_out1.head(5)))
    else:
        print('\nPlotting PES from external output. ')
        f.write('\n Plotting PES from external output. ')
        try:
            Plot_folder = inp.Plot_folder
        except:
            print('\nUsing default path and project name')
            f.write('\n Using default path and project name')
            Plot_folder = out_data #+ 'input_files/'
        else:
            print('\nExternal folder path provided!')
            f.write('\n External folder path provided!')
        df_out1 = pd.read_csv(Plot_folder+inp.PES_filename_cm,sep=inp.sep,header=None)
        df_out1 = df_out1.apply(pd.to_numeric, errors='coerce')
        df_out1.dropna(inplace=True) #removing rows with na values

        print(df_out1.head(5))
        print("\n If your input dataframe contain non-numeric 'HEADER' like R, theta, E, etc, it will be removed. \n")
        print("\n Also verify if data separator is correct ! If incorrect separator is used, only single columns will appear. \n")
        sep_change = int(input("Satisfied! Enter 0 to continue or 1 to change separator (\s+, \\t, ',', etc.)..."))
        if (sep_change == 1):
            new_sep = input("Enter new separator (\s+ (multiple spaces), \\t (tab space), ',', etc.)...")
            df_out1 = pd.read_csv(Plot_folder+inp.PES_filename_cm,sep=new_sep,header=None)
            df_out1 = df_out1.apply(pd.to_numeric, errors='coerce')
            df_out1.dropna(inplace=True) #removing rows with na values
            print(df_out1.head(5))
            f.write("\n")
            f.write("\nThe loaded PES: --> \n")
            f.write(str(df_out1.head(5)))
        else:
            f.write("\n")
            f.write("\nThe loaded PES: --> \n")
            f.write(str(df_out1.head(5)))
            
        #print("\n If your input dataframe contain 'HEADER' like R, theta, E, etc, it should be visible on 1st row and must be removed. \n")

        #df_choice2 = int(input("\n Do you want to remove 1st row ! (0= No, 1= Yes) : "))
        #if (df_choice2 == 1):
        #    df_out1.drop(index=df_out1.index[0], axis=0, inplace=True)
        #    print("Header column removed! The new dataframe is: \n")
        #    print(df_out1.head(5))
        #else:
        #    print("No header input. The dataframe remains same: \n ")

        try:
            inp.E_inf
        except:
            E_Hartree = False
            E_inf = 0.00
        else:
            E_Hartree = True
            E_inf = inp.E_inf

        coll_1D = False
        coll_2D = False
        coll_4D = False
        print(len(df_out1.axes[1]))
        if len(df_out1.axes[1]) == 2:
            print('\n 1D coll. Columns must be in order: R and E')
            coll_1D = True
            if E_Hartree == True:
                df_out1[1] = (df_out1[1] - E_inf)*219474.63             # convert to cm-1
                df_out1.to_csv(out_data+'pes_cm_1D.dat', index=None, header=None,sep=',')    # save V_lam coefficients to file separated by comma
            df_out1.columns = ['R', 'E']

        elif len(df_out1.axes[1]) == 3:
            print('\n 2D coll. Columns must be in order: R, theta and E')
            coll_2D = True
            if E_Hartree == True:
                df_out1[2] = (df_out1[2] - E_inf)*219474.63             # convert to cm-1
                df_out1.to_csv(out_data+'pes_cm_2D.dat', index=None, header=None,sep=',')    # save V_lam coefficients to file separated by comma
            df_out1.columns = ['R', 'theta', 'E']

        elif len(df_out1.axes[1]) == 5:
            print('\n 4D coll. Columns must be in order R, phi, th2, th1 and E')
            coll_4D = True
            if E_Hartree == True:
                df_out1[4] = (df_out1[4] - E_inf)*219474.63             # convert to cm-1
                df_out1.to_csv(out_data+'pes_cm_4D.dat', index=None, header=None,sep=',')    # save V_lam coefficients to file separated by comma
            df_out1.columns = ['R', 'phi', 'theta_2', 'theta_1', 'E']

        else:
            print('Invalid dataframe column number: Must be 2, 3 or 5.')
            print('Current dataframe has {} columns'.format(df_out1.axes[1]))
            print(df_out1.head(5))
            driver.exit_program()

    #print(df_out1.head(5))
    #f.write ('\nInput file read! \nPrinting first 5 values of dataframe! \n\n')
    #f.write(str(df_out1.head(5)))

    out_plots = out_data + 'plots/'                   # directory for plots
    if not os.path.exists(out_plots):
        os.makedirs(out_plots)
    if coll_1D:
        driver.plot_1D(df_out1,df_out1,out_plots, inp, 1)

    elif coll_2D:
        df_res = df_out1.loc[(df_out1[df_out1.columns[1]].isin(inp.thetax))]
        z1_3d = df_res.pivot(index=df_res.columns[0], columns=df_res.columns[1], values=df_res.columns[2])
        z1_3d.to_csv(out_data + '2D_PES_psi4_cm_matrix.dat', header=True,sep='\t')
        driver.plot_1D(df_out1,z1_3d,out_plots, inp, 2)
        z1_3d = driver.mirror(df_out1,df_out1.columns[1],z1_3d)              # mirroring to 360 degrees
        driver.plot_2D_proj(df_out1, z1_3d, out_data, out_plots, inp)

    elif coll_4D:
        # 4D PES need 2D slices for ploar plots
        out_data_plots = out_data + 'plots_data_2D/'
        if not os.path.exists(out_data_plots):
            os.makedirs(out_data_plots)

        #1D plots
        # R vs E plots (1D) provided by thetax in input file
        for i in range(len(inp.thetax)):
            if i == 0:
                df_res = df_out1.loc[(df_out1[df_out1.columns[1]] == inp.thetax[i][0]) & \
                (df_out1[df_out1.columns[2]] == inp.thetax[i][1]) & \
                (df_out1[df_out1.columns[3]] == inp.thetax[i][2])]
            else:
                df_res1 = df_out1.loc[(df_out1[df_out1.columns[1]] == inp.thetax[i][0]) & \
                (df_out1[df_out1.columns[2]] == inp.thetax[i][1]) & \
                (df_out1[df_out1.columns[3]] == inp.thetax[i][2])]
                frames = [df_res, df_res1]
                df_res = pd.concat(frames)
        # df_res = df_out1.loc[(df_out1[df_out1.columns[1]].isin(inp.thetax[:][0])) & \
        # (df_out1[df_out1.columns[2]].isin(inp.thetax[:][1])) & \
        # (df_out1[df_out1.columns[3]].isin(inp.thetax[:][2]))]
        z4_3d = df_res.pivot(index=df_res.columns[0], columns=[df_res.columns[1],df_res.columns[2],df_res.columns[3]], values=df_res.columns[4])
        z4_3d.to_csv(out_data + '4D_PES_psi4_cm_matrix.dat', header=True,sep='\t')
        driver.plot_1D(df_out1,z4_3d,out_plots, inp, 4)

        # uncomment code below to plot all angles in R vs E format
        # z4_3d = df_out1.pivot(index=df_out1.columns[0],
        #                       columns=[df_out1.columns[1],df_out1.columns[2],df_out1.columns[3]],
        #                       values=df_out1.columns[4])
        # driver.plot_1D(df_out1,z4_3d,out_plots, inp, 4)

        # Polar plots for theta1 vs R at various phi, theta2
        for i in inp.phix:
            for j in inp.theta2x:
                driver.plot_4D_proj(df_out1, df_out1.columns[3], df_out1.columns[1],
                                    i, df_out1.columns[2], j, out_data_plots, out_plots, inp)
        # Polar plots for theta2 vs R at various phi, theta1
        for i in inp.phix:
            for j in inp.theta1x:
                driver.plot_4D_proj(df_out1, df_out1.columns[2], df_out1.columns[1],
                                    i, df_out1.columns[3], j, out_data_plots, out_plots, inp)
        # Polar plots for phi vs R at various theta1, theta2
        for i in inp.theta1x:
            for j in inp.theta2x:
                driver.plot_4D_proj(df_out1, df_out1.columns[1], df_out1.columns[3],
                                    i, df_out1.columns[2], j, out_data_plots, out_plots, inp)

    print("#-------------------------------------------------------------------#")
    print("#--------------------#    PES Plots Updated    #--------------------#")
    print("#-------------------------------------------------------------------#")

    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n#--------------------#    PES Plots Updated    #--------------------#")
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n\n")

else:
    print('No plots created. Create_PES_input / Run_psi4 and Plot_PES are False')
    f.write(' \n No plots created. Create_PES_input / Run_psi4 and Plot_PES are False \n')



###############################################################################
###############################################################################
############################# Neural Networks #################################
###############################################################################
###############################################################################




try:
    inp.Create_NN_model
except:
    print("Create_NN_model not provided! Skipping NN module!")
    NNGen =False
else:
    NNGen = inp.Create_NN_model

if NNGen:
    NN_data = out_data + 'NN_files/' # directory for TF NN model and other files
    if not os.path.exists(NN_data):
        os.makedirs(NN_data)
    print("#-------------------------------------------------------------------#")
    print("#--------------------#    Using NNGen module    #-------------------#")
    print("#-------------------------------------------------------------------#")
    
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n#--------------------#    Using NNGen module    #-------------------#")
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n\n")

    #print("Using NNGen module!")
#    from keras.layers import Dropout
    from importlib import reload
    import matplotlib.pyplot as plt

    df = pd.read_csv(out_data+inp.file_name, sep=inp.sep, header=None)
    df = df.apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True) #removing rows with na values
    df.reset_index(drop=True, inplace=True) # reset index
    print("The code designates columns by number 0, 1, 2 etc. ")
    print('\n and omits headers by default OR places them as first row! ')
    print(df.head(5))
    print("\n If your input dataframe contain non-numeric 'HEADER' like R, theta, E, etc, it will be removed. \n")
    print("\n Also verify if data separator is correct ! If incorrect separator is used, only single columns will appear. \n")
    sep_change = int(input("Satisfied! Enter 0 to continue or 1 to change separator (\s+, \\t, ',', etc.)..."))
    if (sep_change == 1):
        new_sep = input("Enter new separator (\s+ (multiple spaces), \\t (tab space), ',', etc.)...")
        df = pd.read_csv(out_data+inp.file_name, sep=new_sep, header=None)
        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True) #removing rows with na values
        print(df.head(5))
        f.write("\n")
        f.write("\nThe loaded PES: --> \n")
        f.write(str(df.head(5)))
    else:
        f.write("\n")
        f.write("\nThe loaded PES: --> \n")
        f.write(str(df.head(5)))

    #print("\n If your input dataframe contain 'HEADER' like R, theta, E, etc, it should be visible on 1st row and must be removed. \n")
    #df_choice2 = int(input("\n Do you want to remove 1st row ! (0= No, 1= Yes) : "))
    #if (df_choice2 == 1):
    #    df.drop(index=df.index[0], axis=0, inplace=True)
    #    print("Header column removed! The new dataframe is: \n")
    #    print(df.head(5))
    #else:
    #    print("No header input. The dataframe remains same: \n ")
    print("\n Number of rows: ",len(df))
    print("\n")

    f.write('''\n\nImportant Notice:
    (a) The first Num_X molumns must be input coordinates and last Num_Y columns must be output descriptors.
    (b) The first column must be R i.e. the radial coordinate (Needed for seperating boundary elements.
    Unless you are familiar with modifying the code or have some other application, keep the first column as R! \n\n''')

    try:
        inp.rearrange_columns
    except:
        df_rearrange = 0
    else:
        df_rearrange = inp.rearrange_columns

    try:
        inp.drop_columns
    except:
        drop_columns = 0
    else:
        drop_columns = inp.drop_columns

    #df_rearrange = int(input("\n Do you want to rearrange dataframe (0 = No, 1 = Yes) : "))
    if (df_rearrange == 1):
        rearrange = 1
        while (rearrange == 1):
            rearrange_1 = int(input("\n Enter column number you want to move to first position (enter 999 if no rearrangement is required): "))
            if (rearrange_1 != 999):
                first_column = df.pop(rearrange_1)
                df.insert(0, rearrange_1 , first_column)
            rearrange_2 = int(input("\n Enter column number you want to move to last position (enter 999 if no rearrangement is required): "))
            if (rearrange_2 != 999):
                last_column = df.pop(rearrange_2)
                df.insert(df.shape[1], rearrange_2 , last_column)
            print("\n Reindexing columns: \n ")
            df = df.set_axis(np.arange(df.shape[1]), axis=1)
            print(df.head(5))
            rearrange = int(input("\n Further changes needed? (0= No, 1= Yes) : "))
        new_df_name = str(input("\n Enter name for saving updated file: "))
        df.to_csv(NN_data+new_df_name, sep='\t', header=None, index=False)
        print("Updated file saved")
        f.write("\n Columns rearranged internally! Check out new file. \n")
        f.write("\n at 'Projects/{}/NN_files/' \n".format(Proj_name))
        f.write(str(new_df_name))
    # drop columns
    elif drop_columns == 1:
        df_drop = 1
        while (df_drop == 1):
            df_drop1 = int(input("\n Enter column number you want to move to remove (enter 999 if no rearrangement is required): "))
            if (df_drop1 != 999):
                rm_column = df.pop(df_drop1)
            df = df.set_axis(np.arange(df.shape[1]), axis=1)
            print(df.head(5))
            df_drop = int(input("\n Further changes needed? (0= No, 1= Yes) : "))
        new_df_name = str(input("\n Enter name for saving updated file: "))
        df.to_csv(NN_data+new_df_name, sep='\t', header=None, index=False)
        print("Updated file saved")
        f.write("\n Columns rearranged internally! Check out new file. \n")
        f.write("\n at 'Projects/{}/NN_files/' \n".format(Proj_name))
        f.write(str(new_df_name))
    else:
        print("\n Final Dataframe \n ")
        print(df.head(5))
        f.write(str(df.head(5)))
    # define input and output columns in dataframe
    if ( inp.num_Y == 1 ):
        Functional_API_output = False
    else:
        Functional_API_output = True

    print("\n In case you have columns that are neither input nor output, please remove them and rereun the code from begining!")

    num_XY = inp.num_X + inp.num_Y
    if (num_XY == len(df.columns)):
        num_Y = inp.num_Y
        num_X = inp.num_X

    else:
        print("\n Incorrect X / Y column lengths (See Below)! ")
        print("X \t Y \t X+Y \t Dataframe columns (starts from 0)")
        print(inp.num_Y, '\t',  inp.num_Y, '\t', inp.num_X + inp.num_Y,  '\t', len(df.columns))
        print("\n X+Y must be equal to dataframe columns in the Input file")
        print('\n If dimentions are correct. Check separation (sep)')
        driver.exit_program()

    if (Functional_API_output==False):
        print("Assuming last column as Output variable")
        num_XY = len(df.columns)
        num_Y = int(1)
        num_X = int(num_XY-num_Y)
        x = df.values[:,:-1]
        y = df.values[:,-1]
        print("X shape:", x.shape)
        print("Y shape:", y.shape)
    else:
        num_XY = len(df.columns)
        print("Total no of columns: ", num_XY, "\n \n  Input columns: ", inp.num_X, "\n \n Remaining columns -> Outputs: ")
        num_Y = int(num_XY-inp.num_X)
        x = df.values[:, :num_X]
        y = df.values[:, -num_Y:]
        print("X shape:", x.shape)
        print("Y shape:", y.shape)
        print("\n")

    print("Check for NaN Values.")
    #f.write("Check for NaN Values.\n")
    if (df.isnull().sum().sum() == 0):
        print("\n No NaN values found !!! \n ")
    else:
        nan_rows = df.isnull().sum()
        print(nan_rows)
        f.write(str(nan_rows))
        print("\n If any columns show number > 0 --> find and remove NaN values!!!")
## SCALING PARAMETERS for Energies (from NIST)

#################################################################################
    try:
        inp.scale_columns
    except:
        Scaling_req = 0
        print("\n No scaling done. Remember to give output energies in cm-1 (or other appropriate unit) \n ")
    else:
        Scaling_req = inp.scale_columns

    #Scaling_req = int(input("\n Is scaling required? (0=No, 1=Yes): "))
    if (Scaling_req == 1):
        print("\n Review dataframe header (column) number before proceeding")
        print(df.head(5))
        print ("\n For each column select the type of scaling as needed. If no scaling is needed enter 0 for that particular column")
        for i in range(num_XY):
            print("\n For elements in column %d" %(i))
            Scaling_req_2 = int(input("\n Type of scaling required (0) No Scaling (1) Radial (2) Anglular (3) Energy : "))
            if (Scaling_req_2 == 1):
                df = driver.R_Scale(df, i)
            elif (Scaling_req_2 == 2):
                df = driver.theta_Scale(df, i)
            elif (Scaling_req_2 == 3):
                df, y_scale_name = driver.E_Scale(df, i)
            else:
                print ("No Scaling Done")
        new_df_name = str(input("\n Enter name for saving updated file: "))
        df.to_csv(NN_data+new_df_name, sep='\t', header=None, index=False)
        print("Updated file saved")
        f.write("\n Columns rearranged internally! Check out new file. \n")
        f.write("\n at 'Projects/{}/NN_files/' \n".format(Proj_name))
        f.write(str(new_df_name))
    else :
        print("No Scaling required")
        y_scale_name = inp.yscale
    # print(" This the final dataframe that shall be used for creating NN models. Verify before proceeding! \n ", df)

    # f.write(""" The code will sort the dataframe based on the output column (provided by the user)
    #             and will give multiple trials till required partition is achieved! (Refer Manual)
    #             In case the data does not need partition. For applications like dipole moment, classification, etc. Use partition = 0
    #             For partitioning required:
    #             The code will first plot full dataset so that users can visualize at which point partition is required!
    #             Use a value well suited to seperate (minima + asymptotic) region from high energy data points. (Any guess < total data points
    #             In case of multiple outputs: ")
    #             The code will plot partitioned data of all output columns. Continue with guess value till required separation is achieved !")

    # Read Carefully if your input file requires learning multiple output simultaneously:
    # The code assumes dataframe to contain multiple output columns.
    # The partition will be done assuming that all output columns are closely related to both input coordinates and each other!.
    # If the dataframe contains multiple outputs which do not share close resemblance, it is better to create separate models for each rather than learning them simultaneously!
    # """)

    print("Dataframe for reference: \n ")
    print(df.head(5))
    # col_out = int(input("\n Enter the column number for output (to be used for sorting): "))
    try:
        inp.reference_output
    except:
        col_out = num_X      # defaults to first output column
    else:
        col_out = inp.reference_output

    if ((col_out < num_X) or (col_out >= num_XY)):
        print("Invalid input for output column! \n Defaulting to 1st output column")
        col_out = num_X # change to 2/3/4 (column number containing energy/output)

    #################################################################################
    # SORTING BY ENERGY (Needed for Visualization)
    NN_plots = NN_data + 'NN_plots/' # directory for TF NN model and other files
    if not os.path.exists(NN_plots):
        os.makedirs(NN_plots)

    print("Check plot of dataframe sorted by reference column at ",NN_plots)
    df_pl = df.sort_values(by=col_out)
    driver.pl_trim_vis_full(df_pl, num_XY, num_X, x.shape[0], NN_plots, inp)

    try:
        inp.partition_req
    except:
        partition = False
    else:
        partition = inp.partition_req

    try:
        inp.auto_cutoff
    except:
        auto_cutoff = 1
    else:
        auto_cutoff = inp.auto_cutoff

    #partition = int(input("\n Is partitioned required? (0 = No, 1=Yes) : \n"))
    if (partition == True):
        NN_part_data = NN_plots + 'partition_data/' # directory for TF NN model and other files
        if not os.path.exists(NN_part_data):
            os.makedirs(NN_part_data)

        if (auto_cutoff == 0):
            print('Manually partitioning data! Use Full_Dataset_E_sorted plot file for reference. ')
            f.write("\n Manually partitioning data!. \n")
            rerun = 1
            trim = int(input("\n Enter the number of points to be retained in minima region (Any guess < total data points) : \n "))
            df_pl_minima, df_pl_HE = driver.pl_trim_part(df_pl, num_XY, num_X, x.shape[0], trim, NN_plots, inp)
            print('\n Check the plot folder to see if required partition is achieved!')
            while (rerun == 1): # loop till required partition is achieved
                print('The program will loop untill required partition is achieved!')
                guess_2 = int(input("\n Do you want to make another guess (0=No, 1=Yes) :  \n"))
                if (guess_2 == 0):
                    print(" Final partition achieved! ")
                    f.write("\n Manual Partition Done! \n")
                    rerun = 0
                else:
                    trim = int(input("\n Another guess for number of points to be retained in minima region: \n "))
                    plt = reload(plt) # reloading the libraries to counter any error caused by running of cells multiple times
                    df_pl_minima, df_pl_HE = driver.pl_trim_part(df_pl, num_XY, num_X, x.shape[0], trim, NN_plots, inp)

        #else:
        #    print("Partioned data not saved !")
        else:
            print('\n Energy partitioning based on input value (High_E_cutoff) entered in input file! ')
            f.write('\n Energy partitioning based on input value (High_E_cutoff) entered in input file! ')
            diff_abs = np.abs(df_pl[col_out] - inp.High_E_cutoff)
            trim = np.argmin(diff_abs, axis=0)
            df_pl_minima, df_pl_HE = driver.pl_trim_part(df_pl, num_XY, num_X, x.shape[0], trim, NN_plots, inp)


        print("Num of data points in minima region = ", trim)
        print("Num of data points in high energy region = ", x.shape[0]-trim)

        f.write("Num of data points in minima region = {} \n".format(trim))
        f.write("\n Num of data points in high energy region = {} \n".format(x.shape[0]-trim))

        #print_part = int(input("\n Do you want to save the partitioned data (0=No, 1 = Yes) : \n "))
        #if (print_part == 1):
        df_pl_minima.to_csv(NN_part_data+"minima_partition.dat", sep='\t', float_format='%.10f')
        df_pl_HE.to_csv(NN_part_data+"high_E_partition.dat, minima_partition.dat and high_E_partition.dat", sep='\t', float_format='%.10f')
        print("\n Partitioned data Saved ! Check", NN_data)
        f.write("\n Partitioned data Saved ! Check -> \n")
        f.write(str(NN_data))
        f.write("\n \n")
    else:
        print("\n Data not partioned!")
        f.write("\n Data not partioned!")


#################################################################################
    # creating boundary and non boundary elements for full dataset

    NN_boundary_data = NN_plots + 'boundary_data/' # directory for TF NN model and other files
    if not os.path.exists(NN_boundary_data):
        os.makedirs(NN_boundary_data)

    # creating boundary and non boundary elements of minima and high energy regions
    if (partition == True):
        boundary_df_pl_minima = driver.extract_boundary_elements(df_pl_minima, num_X)
        non_boundary_df_pl_minima = df_pl_minima[~df_pl_minima.isin(boundary_df_pl_minima)].dropna()
        boundary_df_pl_HE = driver.extract_boundary_elements(df_pl_HE, num_X)
        non_boundary_df_pl_HE = df_pl_HE[~df_pl_HE.isin(boundary_df_pl_HE)].dropna()
        boundary_df_all = driver.extract_boundary_elements(df_pl, num_X)
        non_boundary_all = df_pl[~df_pl.isin(boundary_df_all)].dropna()
    else:
        boundary_df_all = driver.extract_boundary_elements(df_pl, num_X)
        non_boundary_all = df_pl[~df_pl.isin(boundary_df_all)].dropna()


    if (num_X==1):
        print('Input dimentions must be 2 or higher for using boundary extraction/plotting feature!')
    # plot BE of the partitioned data
    #elif (num_X==2):
    #  driver.plot_boundary(boundary_df_all, 0, 1, out_plots, inp)
    #  if (partition == 1):
    #    driver.plot_boundary_partition(boundary_df_pl_minima, boundary_df_pl_HE, 0, 1, out_plots, inp)
    else:
      print("The given code plots boundaries for data with only 2 input descriptors at a time (for better visualization).")
      print("The dataset has: ", num_X, " input Descriptors. The code is taking 1st column (Preferably R) as reference for plots")
      for j in range (1, num_X):
        print("\n")
        print("Extracting boundary elements for 0 vs ", j)
        driver.plot_boundary(boundary_df_all, 0, j, NN_plots, inp)
        if (partition == True):
          driver.plot_boundary_partition(boundary_df_pl_minima, boundary_df_pl_HE, 0, j, NN_plots, inp)

    # Saving partitioned data (High Energy and minimum) into BE and NBE.

    if (partition == True):
        #Save_partitioned_data = int(input("\n Do you want to save partitioned data into separate files? (0=No, 1=Yes): \n"))
        #Save_partitioned_data = 1
        #if (Save_partitioned_data == 1):
        boundary_df_pl_minima.to_csv(NN_boundary_data+"boundary_minima.dat", sep='\t', float_format='%.10f')
        non_boundary_df_pl_minima.to_csv(NN_boundary_data+"non_boundary_minima.dat", sep='\t', float_format='%.10f')
        boundary_df_pl_HE.to_csv(NN_boundary_data+"boundary_high_E.dat", sep='\t', float_format='%.10f')
        non_boundary_df_pl_HE.to_csv(NN_boundary_data+"non_boundary_high_E.dat", sep='\t', float_format='%.10f')
        boundary_df_all.to_csv(NN_boundary_data+"boundary_full.dat", sep='\t', float_format='%.10f')
        non_boundary_all.to_csv(NN_boundary_data+"non_boundary_full.dat", sep='\t', float_format='%.10f')
        print("Partioned dataframes saved to files!")
        #else:
        #print("Partioned data not saved!")
        print ("\n Length of partitioned dataframes (row, columns): ")
        print ("\n boundary_minima = {} \n non_boundary_minima = {} \n boundary_HE = {} \n non_boundary_HE = {}".format( \
        boundary_df_pl_minima.shape, non_boundary_df_pl_minima.shape, boundary_df_pl_HE.shape, non_boundary_df_pl_HE.shape))
    else:
        boundary_df_all.to_csv(NN_boundary_data+"boundary_full.dat", sep='\t', float_format='%.10f')
        non_boundary_all.to_csv(NN_boundary_data+"non_boundary_full.dat", sep='\t', float_format='%.10f')
        print ("\n Length of full dataframe (row, columns): ")
        print ("\n boundary_elements = {} \n non_boundary_elements = {}".format(boundary_df_all.shape, non_boundary_all.shape))

    print("\n Boundary elements of dataframes (based on input coordinates) are exteacted, plotted, and saved to files!")
    f.write("\n Boundary elements of dataframes (based on input coordinates) are exteacted, plotted, and saved to files!")
    f.write("\n Check Out -> \n")
    f.write(str(NN_boundary_data))
    f.write("\n \n")
#################################################################################
    # Creating several split for training, validation and testing datasets that shall be used to create ensemble models (Type 1a)
    # Function to split the dataset based on Euclidean distance and return the sorted datasets

    print("\n Splitting training trainig and testing data points ")

    f.write("Various Split Ratios: \n")
    f.write("\n Training {}".format(inp.train_dataset))
    f.write("\n Testing {}".format(inp.testing_dataset))
    val_dataset = [100]*len(inp.train_dataset)-(np.array(inp.train_dataset)+np.array(inp.testing_dataset))
    f.write("\n Validation {} \n\n".format(val_dataset))

    print("Various Split Ratios: \n")
    print("\n Training {}".format(inp.train_dataset))
    print("\n Testing {}".format(inp.testing_dataset))
    val_dataset = [100]*len(inp.train_dataset)-(np.array(inp.train_dataset)+np.array(inp.testing_dataset))
    print("\n Validation {} \n\n".format(val_dataset))

    # calculating % data points required in skitlearn to sepatate training and testing datasets
    train_ratio = inp.train_dataset
    sum_val_test = val_dataset+np.array(inp.testing_dataset)
    val_test_ratio = ((val_dataset)/sum_val_test)*100
    #print(train_ratio)
    #print(val_dataset)
    #print(inp.testing_dataset)
    #print(val_test_ratio)
    #val_test_ratio = [int(x) for x in input("Enter the three % for Testing : Validation Split separated by comma: ").split(",")]

    # Call the function to split the dataset
    #Split_Choice_minima = int(input("Enter your choice for dataset Split for minima region (Refer FAQs)? \
    #       \n 1 = Randomized (Default) \n 2 = Input Stratified (Recommended) \n 3 = Output Stratified: "))
    print("\n In case of Error for stratification: Reduce number of bins or use random split! \n")
    Split_Choice_minima = inp.Split_type

    if Split_Choice_minima == 1:
        num_bins = 0
        seed_inp = int(input("Enter seed number?: "))
        f.write('Seed for random skitlearn split of training, testing and validation dataset: {} \n'.format(seed_inp))
        stratify_val = 1
    elif Split_Choice_minima == 2 or 3:
        if Split_Choice_minima == 2:
            num_bins = int(input("Enter number of bins for split (Suggestion: 3-5 [4-5(2D); 2-3(4D)] : "))
        else:
            num_bins = int(input("Enter number of bins for split (Suggestion: 5+) : "))
        seed_inp = None
        if (Split_Choice_minima == 2):
          stratify_val = 2
        else:
          stratify_val = 3
    else:
      print("Incorrect input: Taking Default Parameters (seed = 0) ! \n")
      num_bins = 0
      seed_inp = 0
      stratify_val = 1

    ########## make default unless given in input file #############
    try:
        inp.HE_train
    except:
        HE_train = False
    else:
        HE_train = inp.HE_train
        HE_epochs = inp.HE_epochs

    if (partition == False and HE_train == True):
        print("\n partition_req = False and HE_train = True are incompitable conditions! ")
        print("\n Set partition_req = True to use HE region. ")

        driver.exit_program()
    else:
        pass

    ##############################################################

    model_num_f = len(inp.train_dataset)
    ##Splitting dataset for minima_asymptotic region
    if (partition == True):
        print("\n Data partitioning is used: Splitting high energy/minima dataframes \n ")
        print("\n All models will have same binning (histograms) as Model 0. \n")
        for i in range (model_num_f):
            globals()[f'X_train_{i}'], globals()[f'X_val_{i}'], globals()[f'X_test_{i}'], globals()[f'Y_train_{i}'],   \
            globals()[f'Y_val_{i}'], globals()[f'Y_test_{i}'] = driver.split_dataframe(non_boundary_df_pl_minima, \
                                    boundary_df_pl_minima, num_X, num_Y, train_ratio[i],val_test_ratio[i], \
                                    stratify_val, num_bins, seed_inp, i, NN_plots, inp)

            if HE_train == True:
                print("\n !!! HE_train == True : High energy points will be trained! This can degrade quality of minima \n")
                f.write("\n !!! HE_train == True : High energy points will be trained! This can degrade quality of minima \n")
                globals()[f'X_train_HE_{i}'], globals()[f'X_val_HE_{i}'], globals()[f'X_test_HE_{i}'], globals()[f'Y_train_HE_{i}'],   \
                globals()[f'Y_val_HE_{i}'], globals()[f'Y_test_HE_{i}'] = driver.split_dataframe(non_boundary_df_pl_HE, \
                                            boundary_df_pl_HE, num_X, num_Y, train_ratio[i],val_test_ratio[i],  \
                                            stratify_val,num_bins, seed_inp, 99+i, NN_plots, inp)
            else:
                pass

    else:
        print("\n All models will have same binning (histograms) as Model 0. \n")
        for i in range (model_num_f):
            globals()[f'X_train_{i}'], globals()[f'X_val_{i}'], globals()[f'X_test_{i}'], globals()[f'Y_train_{i}'],   \
            globals()[f'Y_val_{i}'], globals()[f'Y_test_{i}'] = driver.split_dataframe(non_boundary_all, \
                                  boundary_df_all, num_X, num_Y, train_ratio[i],val_test_ratio[i],  \
                                  stratify_val, num_bins, seed_inp, i, NN_plots, inp)

        print("\n Train:Val:Test split for the NN models done! \n ")
        f.write("\n Train:Val:Test split for the NN models done! \n ")
        print('Check required plots at : {}'.format(NN_plots))
        f.write('\n Check required plots at :-> \n ')
        f.write(str(NN_plots))

    # Scaling features
    from sklearn.preprocessing import StandardScaler
    feature_scaler =  StandardScaler(with_mean=False, with_std=True)
    target_scaler =  StandardScaler(with_mean=False, with_std=True)
    feature_scaler.fit(np.concatenate((X_train_0, X_val_0, X_test_0), axis=0))
    target_scaler.fit(np.concatenate((Y_train_0, Y_val_0, Y_test_0), axis=0))

    # code to print out normalized value at specific coordinate
    #new_data = np.array([[1.9, 0, 0, 0]])  # Make sure to keep it input dimentional
    #normalized_values = feature_scaler.transform(new_data)
    #normalized_x1_value = normalized_values[0][0]
    #print("\nNormalized x1:", normalized_x1_value)
    #print("\nNormalized all:", normalized_values)

    tuner_folder = str(input("\n Enter name for NN folder (where keras-tuner and NN data will be saved) : "))
    f.write("\n Folder where keras-tuner (trial) data will be saved : --> \n")
    f.write("Projects/{}/NN_files/NN_trial_models/{}/' \n\n".format(Proj_name,tuner_folder))
    
    f.write("\n Folder where final NN data will be saved : --> \n")
    f.write("Projects/{}/NN_files/NN_final_models/{}/' \n\n".format(Proj_name,tuner_folder))

    f.write("\n Plot for NN architecture will be saved inside respective folders for base and ensemble models! \n\n")

    final_NN_data = NN_data + 'NN_final_model/'+tuner_folder+'/' # directory for TF NN model and other files
    if not os.path.exists(final_NN_data):
        os.makedirs(final_NN_data)

    import pickle
    with open(final_NN_data+'feature_scaler.pkl', 'wb') as file:
        pickle.dump(feature_scaler, file)
    with open(final_NN_data+'target_scaler.pkl', 'wb') as file:
        pickle.dump(target_scaler, file)
    print("\n Saved feature and target scaling at " + final_NN_data)
    f.write("\n Feature and target scaling are saved as pickle files: --> \n")
    f.write(str(tuner_folder))
    f.write("\n\n")

    for i in range (model_num_f):
        # Standardize features
        globals()[f'X_train_s{i}'] = feature_scaler.transform(globals()[f'X_train_{i}'])
        globals()[f'X_val_s{i}'] = feature_scaler.transform(globals()[f'X_val_{i}'])
        globals()[f'X_test_s{i}'] = feature_scaler.transform(globals()[f'X_test_{i}'])

        # Standardize targets
        globals()[f'Y_train_s{i}'] = target_scaler.transform(globals()[f'Y_train_{i}'])
        globals()[f'Y_val_s{i}'] = target_scaler.transform(globals()[f'Y_val_{i}'])
        globals()[f'Y_test_s{i}'] = target_scaler.transform(globals()[f'Y_test_{i}'])

        if (partition == True and HE_train == True):
            # Standardize features for HE region
            globals()[f'X_train_HE_s{i}'] = feature_scaler.transform(globals()[f'X_train_HE_{i}'])
            globals()[f'X_val_HE_s{i}'] = feature_scaler.transform(globals()[f'X_val_HE_{i}'])
            globals()[f'X_test_HE_s{i}'] = feature_scaler.transform(globals()[f'X_test_HE_{i}'])

            # Standardize targets for HE region
            globals()[f'Y_train_HE_s{i}'] = target_scaler.transform(globals()[f'Y_train_HE_{i}'])
            globals()[f'Y_val_HE_s{i}'] = target_scaler.transform(globals()[f'Y_val_HE_{i}'])
            globals()[f'Y_test_HE_s{i}'] = target_scaler.transform(globals()[f'Y_test_HE_{i}'])
    #else:
        #pass

    # Function to create n-dimensional array for predicting new output
    def create_n_dimensional_array(init_values, final_values, step_sizes):
        ranges = [np.arange(init_values[i], final_values[i], step_sizes[i]) for i in range(len(init_values))]
        mesh = np.meshgrid(*ranges, indexing='ij')
        return np.stack(mesh, axis=-1)

    # Reshape the n-dimensional array to 2D format where each row is a coordinate
    def n_dim_array_to_dataframe(n_dim_array, len_init):
        reshaped_array = n_dim_array.reshape(-1, n_dim_array.shape[-1]) # np and tf cuasing issues with tqdmcallback
        #reshaped_array = tf.reshape(n_dim_array, [-1, n_dim_array.shape[-1]])
        for col in range(len_init):
            reshaped_array = reshaped_array[reshaped_array[:, col].argsort(kind='mergesort')]
        return reshaped_array

    # Create a ND array
    n_dim_array = create_n_dimensional_array(inp.ini_values, inp.fin_values, inp.step_sizes)
    # Convert ND array to 2D DataFrame
    X_augmented = n_dim_array_to_dataframe(n_dim_array, len(inp.ini_values))

#################################################################################
    # NN model
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress all logs except errors
    import tensorflow as tf
    from tensorflow.keras.utils import plot_model

    tf.random.set_seed(1)

    # Define the tuner
    for mod_i in range (model_num_f):
        X_train = globals()[f'X_train_s{mod_i}']
        X_val   = globals()[f'X_val_s{mod_i}']
        X_test  = globals()[f'X_test_s{mod_i}']
        Y_train = globals()[f'Y_train_s{mod_i}']
        Y_val   = globals()[f'Y_val_s{mod_i}']
        Y_test  = globals()[f'Y_test_s{mod_i}']

        batch_size_input = len(X_train)

        if HE_train == True:
            X_train_he = np.concatenate([ globals()[f'X_train_s{mod_i}'], globals()[f'X_train_HE_s{mod_i}'] ], axis=0)
            X_val_he   = np.concatenate([ globals()[f'X_val_s{mod_i}'], globals()[f'X_val_HE_s{mod_i}']  ], axis=0)
            X_test_he  = np.concatenate([ globals()[f'X_test_s{mod_i}'], globals()[f'X_test_HE_s{mod_i}'] ], axis=0)
            Y_train_he = np.concatenate([ globals()[f'Y_train_s{mod_i}'], globals()[f'Y_train_HE_s{mod_i}'] ], axis=0)
            Y_val_he   = np.concatenate([ globals()[f'Y_val_s{mod_i}'], globals()[f'Y_val_HE_s{mod_i}'] ], axis=0)
            Y_test_he  = np.concatenate([ globals()[f'Y_test_s{mod_i}'], globals()[f'Y_test_HE_s{mod_i}'] ], axis=0)

            batch_size_input_he = len(X_train_he)

        else:
            pass

        ###################   check what model to use  #########################
        try:
            inp.generic_model
        except:
            use_generic_model = False
        else:
            use_generic_model = inp.generic_model

        # Default values for NN hyperparameters
        DEFAULT_NN_HYPERPARA = {
            'Max_trial'   : 10,           # number of trials for architecture search 
            'NN_nodes'    : [64,32],      # search space for NN nodes per layer
            'NN_layers'   : [2,3,4],      # search space for NN layers 
            'NN_branches' : [2,4],        # search space for NN Branches: even only
            'maxit_trial' : 500,          # max iterations during trial (100-500)
            'maxit_base'  : 10000,         # max iterations: base model (500-5000)
            'maxit_ensemble' : 10000      # max iterations: ensemble model (5-10K)
        }
        
        # NN model early stopping hyper-parameters 
        DEFAULT_EARLY_STOP_PARA =  {
            'start_after_cycle_base' :  20,   # 20-50% of max iterations: base
            'patience_step_base'     :   5,   # 5-10% of max iterations: base
            'start_after_cycle_en'   :  50,   # 50% of max iterations: ensemble 
            'patience_step_en'       :  10   # 10% of max iterations: ensemble
        }

        # Safely merge user input with defaults
        if hasattr(inp, "NN_hyperpara"):
            NN_hyperpara = {**DEFAULT_NN_HYPERPARA, **inp.NN_hyperpara}
        else:
            NN_hyperpara = DEFAULT_NN_HYPERPARA
            
        if hasattr(inp, "early_stop_para"):
            early_stop_para = {**DEFAULT_EARLY_STOP_PARA, **inp.early_stop_para}
        else:
            early_stop_para = DEFAULT_EARLY_STOP_PARA

        print("\n NN HyperParameters loaded!  ")
        f.write("\n NN HyperParameters loaded! \n")

        if use_generic_model == True:
            print("\n Using Generic NN Model!  ")
            f.write("\n Using Generic NN Model! \n")
            def model_builder(hp):
                return driver.create_generic_model(hp, num_X, num_Y, NN_hyperpara)
        else:
            print("\n Using PES specific NN Model!  ")
            f.write("\n Using PES specific NN Model! \n")
            def model_builder(hp):
                return driver.create_ND_model(hp, num_X, num_Y, NN_hyperpara)

        ########################################################################
        SilentBayesianOptimization = driver.create_silent_bayesian_optimization()
        tuner = SilentBayesianOptimization(model_builder,
                objective='val_loss',
                max_trials=NN_hyperpara['Max_trial'],
                executions_per_trial=1,
                project_name=NN_data + 'NN_trial_models/'+tuner_folder+'/mod_{}'.format(mod_i))

        print("Finding optimum architecture for model {}!".format(mod_i))
        f.write("\n Finding optimum architecture for model {}!".format(mod_i))
        #print(X_train, Y_train)
        tuner.search(X_train, Y_train,                      # Running tuner
                     epochs=NN_hyperpara['maxit_trial'], # Fixed number of epochs for tuning
                     batch_size=batch_size_input,  # Fixed batch size for tuning
                     validation_data = (X_val, Y_val))

        print("\n Optimum architecture found! Optimising weights and biases! ")
        f.write("\n Optimum architecture found! Optimising weights and biases! ")
        best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
        #print(best_hps)

        # Build model with best HP
        model = tuner.hypermodel.build(best_hps)

        # Saving Final model
        final_NN_data_modi = final_NN_data + '/{}/'.format(mod_i) # directory for TF NN model and other files
        if not os.path.exists(final_NN_data_modi):
            os.makedirs(final_NN_data_modi)

        # plot graph
        plot_model(model, to_file=final_NN_data_modi+f'multilayer_perceptron_graph.{inp.fmt}', \
                    show_shapes=True,show_layer_names=False,
                    show_layer_activations=True)    # Define ReduceLROnPlateau callback

        ##fit the model
        if HE_train == True:
            print("HE region fit!")
            f.write("\n Fitting High Energy region! \n")
            from tqdm.keras import TqdmCallback
            tqdm_prog = TqdmCallback(verbose=1)
            history_he = model.fit(X_train_he, Y_train_he,
                                   validation_data = (X_val_he, Y_val_he),
                                   epochs=HE_epochs, verbose=0,
                                   callbacks=[tqdm_prog],
                                   batch_size=batch_size_input_he)
            f.write(f"\n TQDM LOOP (Base NN Model): HE region fitted:\n {'|' * num_bars} 100% |\n\n")

        else:
            pass
        start_from_epoch_base = int(early_stop_para['start_after_cycle_base']*NN_hyperpara['maxit_base']/100)
        patience_base = int(early_stop_para['patience_step_base']*NN_hyperpara['maxit_base']/100)
        
        early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_mae', mode='min', \
                                        verbose=1, patience=patience_base, restore_best_weights=True,\
                                        start_from_epoch=start_from_epoch_base)
        print("minima region fit!")
        f.write("\n Fitting Minima region! \n")
        from tqdm.keras import TqdmCallback
        tqdm_prog = TqdmCallback(verbose=1)
        history_f = model.fit(X_train, Y_train,
                              validation_data = (X_val, Y_val),
                              epochs=NN_hyperpara['maxit_base'], verbose=0,
                              callbacks=[tqdm_prog, early_stop],
                              batch_size=batch_size_input)

        f.write(f"\n TQDM LOOP (Base NN Model): Minima region fitted:\n {'|' * num_bars} 100% |\n\n")

        
        model.save(final_NN_data_modi+'NN_model_{}.keras'.format(mod_i))
        print("\n Saved final model at " + final_NN_data_modi)
        
        f.write("\n Base model {} training complete ".format(mod_i))
        f.write("\n Final model saved!!")

        globals()[f'model_e{mod_i}'] = model

        # plot metrics # Loss/MAE
        driver.plot_loss_and_mae(history_f.history, final_NN_data_modi, 'loss', inp.fmt)
        driver.plot_loss_and_mae(history_f.history, final_NN_data_modi, 'mae', inp.fmt)

        # Save metrics ! Test, Val, Combined
        test_loss, test_mae = model.evaluate(X_test, Y_test)
        print("test_loss = {:.4f} , test_mae = {:.4f} \n".format(test_loss, test_mae))
        #f.write("Model {} : test_loss = {:.4f} , test_mae = {:.4f} \n".format(mod_i, test_loss, test_mae))

        # Make predictions with residual plot for test dataset.
        predict_batch = 4096
        predictions_scaled = model.predict(X_test, batch_size=predict_batch)
        # Inverse transform to original scale
        predictions = target_scaler.inverse_transform(predictions_scaled)
        y_original = target_scaler.inverse_transform(Y_test)
        driver.plot_residuals(y_original, predictions, final_NN_data_modi, 'Residuals_test', fmt=inp.fmt)

        # Make predictions with residual plot for minimum E dataset.
        X_min  = np.concatenate([X_train_s0,  X_test_s0, X_val_s0],  axis=0)
        Y_min  = np.concatenate([Y_train_s0,  Y_test_s0, Y_val_s0],  axis=0)
        predictions_scaled = model.predict(X_min, batch_size=predict_batch)
        predictions = target_scaler.inverse_transform(predictions_scaled)
        y_original = target_scaler.inverse_transform(Y_min)
        # Save metrics ! Test, Val, Combined
        full_loss, full_mae = model.evaluate(X_min, X_min)
        print("full_loss = {:.4f} , full_mae = {:.4f} \n".format(full_loss, full_mae))
        f.write("\n Base model {} Prediction Matrics : \n".format(mod_i))
        f.write("Model {} : full_loss = {:.4f} , full_mae = {:.4f} \n\n ".format(mod_i, full_loss, full_mae))

        driver.plot_residuals(y_original, predictions, final_NN_data_modi,'Residuals_min', fmt=inp.fmt)

        if HE_train == True:
            # Make predictions with residual plot for whole (minimum+HE) dataset.
            X_all  = np.concatenate([X_min, X_train_HE_s0, X_test_HE_s0, X_val_HE_s0],  axis=0)
            Y_all  = np.concatenate([Y_min, Y_train_HE_s0, Y_test_HE_s0, Y_val_HE_s0],  axis=0)
            predictions_scaled = model.predict(X_all, batch_size=predict_batch)
            predictions = target_scaler.inverse_transform(predictions_scaled)
            y_original = target_scaler.inverse_transform(Y_all)
            driver.plot_residuals(y_original, predictions, final_NN_data_modi,'Residuals_all', fmt=inp.fmt)
        else:
            pass

        print("\n Predicting PES based on input coordinates for base model {}! \n".format(mod_i))
        f.write("\n Predicting PES based on input coordinates for base model {}! \n".format(mod_i))
        # save predicted value!
        X_aug_s = feature_scaler.transform(X_augmented)
        Y_aug_s = model.predict(X_aug_s, batch_size=predict_batch)
        Y_augmented = target_scaler.inverse_transform(Y_aug_s)
        # Combining input features and prediction
        AugmentedXY = np.c_[X_augmented,Y_augmented]
        np.savetxt(final_NN_data_modi + 'Predicted_results.txt' , AugmentedXY, delimiter='\t', fmt='%.4f')

    ################### test saved model (Aux script) #########################
    # loaded_model = keras.saving.load_model("model.keras")
    #
    # with open('feature_scaler.pkl', 'rb') as file:
    #     l_feature_scaler = pickle.load(file)
    # with open('target_scaler.pkl', 'rb') as file:
    #     l_target_scaler = pickle.load(file)
    #
    # X_scaled = l_feature_scaler.transform(X)
    #
    # l_predictions_scaled = loaded_model.predict(X_scaled)
    # l_predictions = l_target_scaler.inverse_transform(l_predictions_scaled)
    #
    ##############################################################

    # ####################################################################################
    # ###################### High Energy Model and Ensemble ##############################
    # ####################################################################################

    # if (partition == True and HE_train == True):
    #     X_train_he = np.concatenate([X_train_s0, X_train_HE_s0], axis=0)
    #     X_val_he   = np.concatenate([X_val_s0,   X_val_HE_s0],   axis=0)
    #     X_test_he  = np.concatenate([X_test_s0,  X_test_HE_s0],  axis=0)
    #     Y_train_he = np.concatenate([Y_train_s0, Y_train_HE_s0], axis=0)
    #     Y_val_he   = np.concatenate([Y_val_s0,   Y_val_HE_s0],   axis=0)
    #     Y_test_he  = np.concatenate([Y_test_s0,  Y_test_HE_s0],  axis=0)
    #     print("Fine Tuning weights and biases with HE region! ")
    # else:

    print("Fine Tuning weights and biases in Ensemble Model (uses minima region only)! ")
    f.write("\n Fine Tuning weights and biases in Ensemble Model (uses minima region only)! \n")

    X_train_en = X_train_s0
    X_val_en   = X_val_s0
    X_test_en  = X_test_s0
    Y_train_en = Y_train_s0
    Y_val_en   = Y_val_s0
    Y_test_en  = Y_test_s0

    batch_size_input = len(X_train_en)

    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense, Concatenate, Average
    from tensorflow.keras.constraints import NonNeg
    
    try:
        inp.Ensemble_Model_Train
    except:
        Ensemble_Model_Train = True
    else:
        Ensemble_Model_Train = inp.Ensemble_Model_Train
    
    if (Ensemble_Model_Train == True):
        print("\n The Enseble NN model will ALLOW for base model to be RETRAINED !")
        print(" !!! Make sure that the number of models are not too large as it may slow down training considerably! \n")
        f.write("\n\n The Enseble NN model will ALLOW for base model to be RETRAINED!")
        f.write("\n Make sure that the number of models are not too large as it may slow down training considerably! \n\n")

    else:
        print("\n The Enseble NN model will NOT allow for base model to be RETRAINED!")
        print(" !!! Make sure that base model have enough epochs to be trained! \n")
        f.write("\n\n The Enseble NN model will NOT allow for base model to be RETRAINED!")
        f.write("\n Make sure that base model have enough epochs to be trained! \n\n")

    def finetuning_model_ensemble(input_shape, output_shape, base_models, Ensemble_Model_Train):
        # Create a new model with the same architecture as the base model
        inputs = Input(shape=(input_shape,))
        for base_model in base_models:
            base_model.trainable = Ensemble_Model_Train

        base_outputs = [base_model(inputs) for base_model in base_models]
        concatenated_output = Concatenate()(base_outputs)
        averaged_output = Average()(base_outputs)
        concatenated_output = Concatenate()([concatenated_output,averaged_output])
        output = Dense(output_shape, activation='linear', use_bias=False, kernel_constraint=NonNeg())(concatenated_output)
        model = Model(inputs, output)
        optimizer_instance = tf.keras.optimizers.Adam(amsgrad=True) # learning_rate=1e-4 (include if deviations)
        model.compile(optimizer=optimizer_instance, loss='huber', metrics=['mae'])
        return model

    ## Create the fine-tuning model with the same architecture (HE)
    base_models = [globals()[f'model_e{i}'] for i in range(model_num_f)]
    model_en = finetuning_model_ensemble(num_X, num_Y, base_models, Ensemble_Model_Train)

    #fit the model
    start_from_epoch_en = int(early_stop_para['start_after_cycle_en']*NN_hyperpara['maxit_ensemble']/100)
    patience_en = int(early_stop_para['patience_step_en']*NN_hyperpara['maxit_ensemble']/100)
        
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_mae', mode='min', \
                                    verbose=1, patience=patience_en, restore_best_weights=True, \
                                    start_from_epoch=start_from_epoch_en)

    from tqdm.keras import TqdmCallback
    tqdm_prog = TqdmCallback(verbose=1)
    history_f_en = model_en.fit(X_train_en, Y_train_en,
                          validation_data = (X_val_en, Y_val_en),
                          epochs=NN_hyperpara['maxit_ensemble'], verbose=0,
                          callbacks=[tqdm_prog,early_stop],
                          batch_size=batch_size_input) #batch_size_input

    f.write(f"\n TQDM LOOP (Ensemble NN Model fitted) :\n {'|' * num_bars} 100% |\n\n")

    test_loss_en, test_mae_en = model_en.evaluate(X_test_en, Y_test_en)
    print("test_loss = {:.4f} , test_mae = {:.4f} \n".format(test_loss_en, test_mae_en))
    #f.write("Fine Tuning: test_loss = {:.4f} , test_mae = {:.4f} \n".format(full_loss, full_mae))

    # Saving Final model
    final_NN_data_en = final_NN_data + 'Ensemble_tuned/' # directory for TF NN model and other files
    if not os.path.exists(final_NN_data_en):
        os.makedirs(final_NN_data_en)

    f.write("\n Ensemble model training complete ")
    f.write("\n Final model saved!!")
    # plot graph
    plot_model(model_en, to_file=final_NN_data_en+f'ensemble_model_architecture.{inp.fmt}', \
                show_shapes=True,show_layer_names=False,
                show_layer_activations=True)

    driver.plot_loss_and_mae(history_f_en.history, final_NN_data_en, 'loss', inp.fmt)
    driver.plot_loss_and_mae(history_f_en.history, final_NN_data_en, 'mae', inp.fmt)

    model_en.save(final_NN_data_en+'NN_model_en.keras')
    print("\n Saved final model at " + final_NN_data_en)
    
    f.write("\n Folder where Ensemble NN data will be saved : --> \n")
    f.write(" 'Projects/{}/NN_files/NN_final_models/{}/Ensemble_tuned/' \n\n".format(Proj_name,tuner_folder))
    # Make predictions
    predictions_scaled_en = model_en.predict(X_test_en, batch_size=predict_batch)
    # Inverse transform to original scale
    predictions_en = target_scaler.inverse_transform(predictions_scaled_en)
    y_test_original_en = target_scaler.inverse_transform(Y_test_en)
    driver.plot_residuals(y_test_original_en, predictions_en, final_NN_data_en, 'Residuals_test_en', fmt=inp.fmt)

    predictions_scaled = model_en.predict(X_min, batch_size=predict_batch)
    predictions = target_scaler.inverse_transform(predictions_scaled)
    y_original = target_scaler.inverse_transform(Y_min)
    # Save metrics ! Test, Val, Combined
    full_loss, full_mae = model_en.evaluate(X_min, X_min)

    print("full_loss = {:.4f} , full_mae = {:.4f} \n".format(full_loss, full_mae))
    f.write("\n Ensemble Prediction Matrics : \n")
    f.write("Fine Tuning: full_loss = {:.4f} , full_mae = {:.4f} \n".format(full_loss, full_mae))

    #updated_weights = model_en.get_layer('ensemble_weights').weights[0].numpy()
    #print("Final ensemble weights:", updated_weights)
    #f.write("Final ensemble weights:\n")
    #f.write(", ".join(map(str, updated_weights)))
    #f.write("\n")


    driver.plot_residuals(y_original, predictions, final_NN_data_en,'Residuals_min_en', fmt=inp.fmt)

    if HE_train == True:
        predictions_scaled = model_en.predict(X_all, batch_size=predict_batch)
        predictions = target_scaler.inverse_transform(predictions_scaled)
        y_original = target_scaler.inverse_transform(Y_all)
        driver.plot_residuals(y_original, predictions, final_NN_data_en,'Residuals_all_en', fmt=inp.fmt)
    else:
        pass

    print("\n Predicting PES based on input coordinates using ensemble model! \n")
    f.write("\n Predicting PES based on input coordinates using ensemble model! \n")

    X_aug_s = feature_scaler.transform(X_augmented)
    Y_aug_s = model_en.predict(X_aug_s, batch_size=predict_batch)
    Y_augmented = target_scaler.inverse_transform(Y_aug_s)

    AugmentedXY = np.c_[X_augmented,Y_augmented]
    np.savetxt(final_NN_data_en + 'Predicted_results.txt' , AugmentedXY, delimiter='\t', fmt='%.4f')
    np.savetxt(out_data + 'NN_Predicted_results.txt' , AugmentedXY, delimiter='\t', fmt='%.4f')
    print("\n Saving final NN model at parent directory : -->  Projects/{}/' \n\n".format(Proj_name))
    
    f.write("\n\nSaving final NN model at parent directory : --> \n")
    f.write("Projects/{}/' \n\n".format(Proj_name))

    print("#-------------------------------------------------------------------#")
    print("#---------------------#    NN Model Created    #--------------------#")
    print("#-------------------------------------------------------------------#")

    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n#---------------------#    NN Model Created    #--------------------#")
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n\n")

else:
    print(" \n NNGen = False : Skipping NN Model \n")
    f.write('\n NNGen = False : Skipping NN Model! \n ')



###############################################################################
###############################################################################
############################ Multipole Expansion ##############################
###############################################################################
###############################################################################

try:
    inp.MPExp
except:
    MPExp =False
else:
    MPExp = inp.MPExp
    MP_data = out_data + 'MP_files/' # directory for TF NN model and other files
    if not os.path.exists(MP_data):
        os.makedirs(MP_data)
    MP_plots = MP_data + 'MP_plots/' # directory for TF NN model and other files
    if not os.path.exists(MP_plots):
        os.makedirs(MP_plots)

if MPExp:
    print("#-------------------------------------------------------------------#")
    print("#----------------#    Using MP Expansion module    #----------------#")
    print("#-------------------------------------------------------------------#")
    
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n#----------------#    Using MP Expansion module    #----------------#")
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n\n")

    import math
    import scipy
    from scipy.special import legendre

    try:
        inp.Expansion_typ
    except:
        print("Error: Set Expansion_typ as '2D' or '4D'.")
        driver.exit_program()
    else:
        Expansion_typ = inp.Expansion_typ

    try:
        inp.Residuals
    except:
        Residuals = False
    else:
        Residuals = inp.Residuals

    # 2D multipole expansion code for a rigid rotor-atom collision PES:
    # Uses Legendre functions from scipy library of python
    if Expansion_typ == '2D':
        ########################################################
        #                2D Multipole Expansion
        ########################################################
        if Residuals == False :
            # read input file (PES) give separation (remove header such as r, theta, phi, etc)
            # The code assumes first column to be R (Radial Coordinate), 2nd to be theta (Angular coordinate)
            # and 3rd column to be E(Potentials)

            lm = inp.lam_max  # lambda max
            df_inp = pd.read_csv(out_data+inp.PES_filename_cm,header=None,sep=inp.sep)
            df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
            df_inp.dropna(inplace=True) #removing rows with na values
            print(df_inp.head(5))

            print("\n If your input dataframe contain non-numeric 'HEADER' like R, theta, E, etc, it will be removed. \n")
            print("\n Also verify if data separator is correct ! If incorrect separator is used, only single columns will appear. \n")
            sep_change = int(input("Satisfied! Enter 0 to continue or 1 to change separator (\s+, \\t, ',', etc.)..."))
            if (sep_change == 1):
                new_sep = input("Enter new separator (\s+ (multiple spaces), \\t (tab space), ',', etc.)...")
                df_inp = pd.read_csv(out_data+inp.PES_filename_cm,header=None,sep=new_sep)
                df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
                df_inp.dropna(inplace=True) #removing rows with na values
                print(df_inp.head(5))
                f.write("\n")
                f.write("\nThe loaded PES: --> \n")
                        
                f.write(str(df_inp.head(5)))
            else:
                f.write("\n")
                f.write("\nThe loaded PES: --> \n")
                f.write(str(df_inp.head(5)))

            try:
                inp.E_inf
            except:
                E_Hartree = False
                E_inf = 0.00
            else:
                E_Hartree = True
                E_inf = inp.E_inf

            if E_Hartree == True:
                df_inp[2] = (df_inp[2] - E_inf)*219474.63             # convert to cm-1
                df_inp.to_csv(out_data+'psi4_PESMP_cm.dat', index=None, header=None,sep=',')    # save V_lam coefficients to file separated by comma

            df_inp.sort_values(by = [0,1], inplace=True, ascending = True)
            df_inp.reset_index(inplace=True, drop = True)
            print(df_inp)
            #f.write(str(df_inp))

            # Declare Variables

            R_arr = df_inp[0].unique()       # extracting unique values of R (sorted)
            gm_arr = df_inp[1].unique()      # extracting unique values of theta (sorted)
            nc = len(df_inp[0].unique())     # number of Radial coordinates (Must be same for all angles)
            ngm = len(df_inp[1].unique())    # number of angular coordinates

            px = np.zeros((ngm,lm))     # stores legendre polynomial
            fx = np.zeros(ngm)          # Ab initio energy
            R = np.zeros(nc)            # distance R
            E = np.zeros(nc)            # multipole expanded potentials
            df_out = pd.DataFrame()     # dataframe stores V lambda

            V_nf = np.zeros((nc,lm))      # Numpy 2D array to store V_lambdas as they are calculated for each radial term
            #V_n = np.zeros(lm)           # Stores V_lambda for one radial term (Depreciated part of code no longer used!)
            if inp.symmetric:
                sym = 2
            else:
                sym = 1

            try:
                inp.read_Legendre
            except:
                read_Legendre = False
            else:
                read_Legendre = inp.read_Legendre

            # Calculate legendre coeff and take pseudo-inverse

            if read_Legendre == False:
                print("Generating new legendre coefficient from scratch and saving 2D_L_coeff.npy in \n")
                print(str(MP_data))
                print("\n")
                f.write("\n Generating new legendre coefficient from scratch and saving 2D_L_coeff.npy in --> \n")
                f.write(str(MP_data))
                f.write("\n")

                for j2 in range (ngm):                 # loop over anglular terms (goes from 0 to ngm-1)
                    j2_ang = gm_arr[j2]                # angles go from 0-90 with 15 degree interval saved in gm_arr array
                    for j3 in range (lm):              # loop over legendre terms (goes from 0 to lm-1)
                        pxc = legendre(j3*sym)         # Uses j3*2 for symmetric molecule (only even V_lambdas); and *1 otherwise
                        ang = math.radians(j2_ang)     # convert angles to radians
                        px[j2,j3]= pxc(math.cos(ang))  # store legendre coefficient for corrosponding angle and lambda (2D)
                np.save(MP_data+"2D_L_coeff.npy", px)    # save Legendre coefficients to numpy readable file for future use
            else:
                px = np.load(MP_data+"2D_L_coeff.npy")

            A_inv = np.linalg.pinv(px)             # take pseudo-inverse of px matrix (equivalent to least squares fit)

            # Calculate V_lambda
            for i in range (nc):           # loop over all R
                ct = i*ngm                 # extract start point. Since input dataframe is sorted by R and theta,
                fx = df_inp[2][ct:ct+ngm]  # potentials (V) are extracting for each R value at a time
                V_n1 = A_inv.dot(fx)       # A-inv * V gives Radial coefficients
                V_nf[i,:] = V_n1           # radial coefficients stored in 2D matrix

            a12 = np.arange(lm)*sym                     # creates header for lambda terms
            df_Vnf = pd.DataFrame(V_nf, columns = a12)  # saves final matrix into dataframe with appropriate header
            df_Vnf.insert(0, 'R', R_arr)                # adding R column

            print("\n A preview of radial terms: \n ")        # printing radial dataframe
            print(df_Vnf.head(5))
            
            f.write("\n\n A preview of radial terms: \n ")        # printing radial dataframe
            f.write(str(df_Vnf.head(5)))

            print("Saving final radial terms file 2D_Vlam.dat in above folder! \n")
            f.write("\n\nSaving final radial terms file 2D_Vlam.dat in above folder! \n")
            
            df_Vnf.to_csv(MP_data+'2D_Vlam.dat', index=None, header=True,sep=',')    # save V_lam coefficients to file separated by comma
            print("Radial terms plots are available in above folder/MP_plots. \n")
            f.write("\n Radial terms plots are available in above folder/MP_plots. \n")

            try:
                inp.Ind_plot
            except:
                Ind_plot = False
            else:
                Ind_plot = inp.Ind_plot
            if Ind_plot == True:
                driver.plot_MP(lm, sym, R_arr, df_Vnf, MP_plots, inp)
            driver.plot_MP_combined(lm, sym, R_arr, df_Vnf, MP_plots, inp)

            print("#-------------------------------------------------------------------#")
            print("#---------------#    2D Mutipole Expansion Done!    #---------------#")
            print("#-------------------------------------------------------------------#")

            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n#---------------#    2D Mutipole Expansion Done!    #---------------#")
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n\n")

        else:
            ########################################################
            #        2D Inverse Multipole Expansion (for Residuals)
            ########################################################
            # read original PES
            MP_dataR = MP_data + 'Residuals_Inv_Fit/' # directory for fitted Vlam residual files
            if not os.path.exists(MP_dataR):
                os.makedirs(MP_dataR)
            df_inp = pd.read_csv(out_data+inp.PES_filename_cm,header=None,sep=inp.sep)
            df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
            df_inp.dropna(inplace=True) #removing rows with na values
            print(df_inp.head(5))
            
            print("\n If your input dataframe contain non-numeric 'HEADER' like R, theta, E, etc, it will be removed. \n")
            print("\n Also verify if data separator is correct ! If incorrect separator is used, only single columns will appear. \n")
            sep_change = int(input("Satisfied! Enter 0 to continue or 1 to change separator (\s+, \\t, ',', etc.)..."))
            if (sep_change == 1):
                new_sep = input("Enter new separator (\s+ (multiple spaces), \\t (tab space), ',', etc.)...")
                df_inp = pd.read_csv(out_data+inp.PES_filename_cm,header=None,sep=new_sep)
                df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
                df_inp.dropna(inplace=True) #removing rows with na values
                print(df_inp.head(5))
                f.write("\n")
                f.write("\nThe loaded PES: --> \n")
                f.write(str(df_inp.head(5)))
            else:
                f.write("\n")
                f.write("\nThe loaded PES: --> \n")
                f.write(str(df_inp.head(5)))
                
                
            df_inp.sort_values(by = [0,1], inplace=True, ascending = True)
            df_inp.reset_index(inplace=True, drop = True)

            # importing 2D radial terms
            df_Vn = pd.read_csv(MP_data+inp.V_lam_filename_cm,sep=inp.sep_vlam,header=None)

            df_Vn = df_Vn.apply(pd.to_numeric, errors='coerce')
            df_Vn.dropna(inplace=True) #removing rows with na values
            print(df_Vn.head(5))

            df_R = df_Vn.pop(0)                              # removing R column from df_Vn and saving to df_R
            
            if inp.read_Legendre :
                px = np.load(MP_data+"2D_L_coeff.npy")         # importing legendre coefficients
            else:
                print("Error! 2D_L_coeff.npy must be read from MPExp2D calculation")
                print("Make sure file exists at {} and set read_Legendre = True".format(MP_data))
                f.write("\n Error! 2D_L_coeff.npy must be read from MPExp2D calculation \n")
                f.write("Make sure file exists at {} and set read_Legendre = True \n".format(MP_data))
                driver.exit_program()
            #print("Radial coordinates are: \n ", df_R)        # Optional: prints radial coordinates
            print("The radial terms imported are: \n ")        # printing radial dataframe
            print(df_Vn.head(5))
            f.write("\n The radial terms imported are: \n ")        # printing radial dataframe
            f.write(str(df_Vn.head(5)))
            
            lm  = len(px.T)                    # Radial terms
            nc  = len(df_Vn)                   # number of Radial coordinates
            ngm = len(px)                      # number of angular coordinates
            R_arr = df_inp[0].unique()       # extracting unique values of R (sorted)

            #V_nf  = np.zeros((nc,lm))          # Numpy 2D array to store generated potentials
            #V_nf2 = np.zeros((ngm,nc))         # Numpy 2D array to store ab_initio potentials

            V_n1 = px.dot(df_Vn.T)                 # save regenerated potentials
            a12 = np.arange(ngm)            # creates header for angles
            df_Vnf = pd.DataFrame(V_n1.T, columns = a12) # saves final matrix into dataframe with appropriate header
            df_Vnf.insert(0, 'R', R_arr)                              # adding R column
            # converting PES from matrix format to R,A,E format
            df_Vnf2 = pd.melt(df_Vnf, id_vars='R', value_vars=list(df_Vnf.columns[1:]), var_name='th', value_name='E',ignore_index=True)
            df_inp.sort_values(by = [1,0], inplace=True, ascending = True,ignore_index=True) # sorting input data by theta and then R
            Origi_E = df_inp.values[:, -1].reshape(-1,1)  # original Energies
            Regen_E = df_Vnf2.values[:, -1].reshape(-1,1)  # regenerated Energies
            df_inp[3] = Regen_E.flatten()
            residuals = Regen_E - Origi_E

            print("\nSaving regenerated PES data from analytically fitted V_lamda terms and its residual at location --> \n")
            print(str(MP_dataR))
            print("\n")

            f.write("\n\nSaving regenerated PES data from analytically fitted V_lamda terms and its residual at location --> \n")
            f.write(str(MP_dataR))
            f.write("\n")

            np.savetxt(MP_dataR +'residual_Vlam2E.dat', np.array([Origi_E.flatten(), Regen_E.flatten(), residuals.flatten()]).T, delimiter='\t')
            df_Vnf2.to_csv(MP_dataR + 'regenerated_PES_data.dat', index=None, header=False,sep=',')  # save V_lam coefficients to file separated by comma
            #print("\nSaving V_lam2PES analytically fitted residual plot at location: {} ".format(MP_dataR))
            #f.write("\nSaving V_lam2PES analytically fitted residual plot at location: {} ".format(MP_dataR))
            driver.residual_plot(Origi_E,residuals,MP_dataR,inp)

            print("#-------------------------------------------------------------------#")
            print("#-----------------#    2D Inverse Fitting Done!    #----------------#")
            print("#-------------------------------------------------------------------#")

            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n#-----------------#    2D Inverse Fitting Done!    #----------------#")
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n\n")

    elif Expansion_typ == '4D':
        ########################################################
        #        4D Multipole Expansion
        ########################################################
        import scipy as sp
        import time
        if Residuals == False :
            df_inp = pd.read_csv(out_data+inp.PES_filename_cm,header=None,sep=inp.sep)
            df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
            df_inp.dropna(inplace=True) #removing rows with na values
            print(df_inp.head(5))
            
            print("\n If your input dataframe contain non-numeric 'HEADER' like R, theta, E, etc, it will be removed. \n")
            print("\n Also verify if data separator is correct ! If incorrect separator is used, only single columns will appear. \n")
            sep_change = int(input("Satisfied! Enter 0 to continue or 1 to change separator (\s+, \\t, ',', etc.)..."))
            if (sep_change == 1):
                new_sep = input("Enter new separator (\s+ (multiple spaces), \\t (tab space), ',', etc.)...")
                df_inp = pd.read_csv(out_data+inp.PES_filename_cm,header=None,sep=new_sep)
                df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
                df_inp.dropna(inplace=True) #removing rows with na values
                print(df_inp.head(5))
                f.write("\n")
                f.write("\nThe loaded PES: --> \n")
                f.write(str(df_inp.head(5)))
            else:
                f.write("\n")
                f.write("\nThe loaded PES: --> \n")
                f.write(str(df_inp.head(5)))
 
            df_inp.columns = ['R','phi','th2','th1','E']
            try:
                inp.E_inf
            except:
                E_Hartree = False
                E_inf = 0.00
            else:
                E_Hartree = True
                E_inf = inp.E_inf

            if E_Hartree == True:
                df_inp['E'] = (df_inp['E'] - E_inf)*219474.63             # convert to cm-1
                df_inp.to_csv(out_data+'psi4_PESMP_cm.dat', index=None, header=None,sep=',')    # save V_lam coefficients to file separated by comma

            df_inp.sort_values(by = [ 'R','phi','th2','th1'], inplace=True, ascending = True)
            df_inp.reset_index(inplace=True, drop = True)  # sorting by R, phi, th2 and th1 and reindexing
            print(df_inp)
            #f.write(str(df_inp))
            angmat = df_inp[['phi','th2','th1']].drop_duplicates().to_numpy() # extracting unique angular coordinates
            
            print("Number of angular terms: ", len(angmat))
            f.write("\n\nNumber of angular terms: \n {} \n".format(len(angmat)))
            f.write("\n\n List of angular terms: \n {} \n".format(angmat))            
            #print("Angular terms will be saved in {} Ang_Mat.dat".format(MP_data))
            #f.write("Angular terms will be saved in {} Ang_Mat.dat \n".format(MP_data))

            print("Angular terms will be saved in Ang_Mat.dat at : --> \n")
            print(str(MP_data))
            print("\n")
            f.write("\nAngular terms will be saved in Ang_Mat.dat at --> \n")
            f.write(str(MP_data))
            f.write("\n")

            np.savetxt(MP_data +"Ang_Mat.dat",angmat,fmt='%.2f\t%.2f\t%.2f')
            #print(angmat)
            #f.write(str(angmat))

            Lmat = np.zeros((1,3))
            L1max  = inp.L1max                           # max order for first radial term (NCCN)
            L2max  = inp.L2max                           # max order for second radial term (H_2)
            if inp.Symm_1 == True:                  # 1 for non symm, 2 for symmetric
                Symm_1 = 2
            else:
                Symm_1 = 1
            if inp.Symm_2 == True:                  # 1 for non symm, 2 for symmetric
                Symm_2 = 2
            else:
                Symm_2 = 1
            Symm   = max(Symm_1,Symm_2)          # If both Symm_1 and Symm_2 are 2 (symmetric), use 2 else 1.

            for i in range(0,L1max+1,Symm_1):        # loop for Lambda_1
                for j in range(0,L2max+1,Symm_2):    # loop for Lambda_2
                    for k in range(abs(i-j),abs(i+j)+1,Symm):    # loop for Lambda
                        Lc = np.matrix([i,j,k])
                        Lmat = np.append(Lmat,Lc,axis=0)
            Lmat = np.delete(Lmat,0,0)
            Lmat = Lmat.astype(int)
            print("Number of radial terms: ", len(Lmat))

            # appending Lambda matrix with integers that will point to specific radial coefficient.
            num   = np.arange(len(Lmat))
            num2  = np.reshape(num, (-1, 1))
            Lmat1 = np.append(num2,Lmat,axis=1)
            #Lmat1   # Vlam along with their numbering
            #print("Lambda terms will be saved in {} Lambda_ref.dat".format(MP_data))
            #f.write("Lambda terms will be saved in {} Lambda_ref.dat \n".format(MP_data))
            
            print("The list of Lambda terms will be saved in Lambda_ref.dat at \n")
            print(str(MP_data))
            print("\n")
            
            f.write("\nThe list of Lambda terms will be saved in Lambda_ref.dat at --> \n")
            f.write(str(MP_data))
            f.write("\n")

            print(Lmat1)
            f.write("\n\n Number of Lambda terms are: \n")
            f.write(str(len(Lmat1)))
            f.write("\n\nThe list of Lambda terms are: \n")
            f.write(str(Lmat1))
            # saving radial coefficients for future reference (The final data does not contain V_lambda terms but the pointer in the first column)
            np.savetxt(MP_data +"Lambda_ref.dat",Lmat1,fmt='%i\t%i\t%i\t%i')
            # Declare Variables

            lm = len(Lmat)               # number of lambda (radial) terms
            ngm = len(angmat)            # number of angular terms
            px = np.zeros((ngm,lm))      # initializing matrix to store BiSp coefficients
            R_arr = df_inp['R'].unique()   # extracting unique values of R (sorted)
            Rpt = len(R_arr)             # number of radial (R) terms
            fx = np.zeros(ngm)           # 1D matrix to store energies
            V_nf = np.zeros((Rpt,lm))    # 1D matrix to store least sq. fit terms

            try:
                inp.read_SH
            except:
                read_SH = False
            else:
                read_SH = inp.read_SH

            # Calculate legendre coeff and take pseudo-inverse
            if read_SH == False:
                print("Generating new Spherical Harmonics coefficient from scratch and saving 4D_BiSp_coeff.npy in \n")
                print(str(MP_data))
                print("\n")
                f.write("\n\nGenerating new Spherical Harmonics coefficient from scratch and saving 4D_BiSp_coeff.npy in --> \n")
                f.write(str(MP_data))
                f.write("\n")
                
                for j2 in tqdm(range (ngm)):
                    phi, th2, th1 = angmat[j2,0],angmat[j2,1],angmat[j2,2]
                    for j3 in range (lm):
                        L1,L2,L = Lmat[j3,0],Lmat[j3,1],Lmat[j3,2]
                        pxc = driver.Bispher_SF(L1,L2,L, phi, th2, th1)
                        px[j2,j3]=pxc
                np.save(MP_data + "4D_BiSp_coeff.npy", px)    # save Bispherical Harmonics coefficients to numpy readable file for future use
                f.write(f"\n TQDM LOOP (BiSpherical Harmonics calculated!) :\n {'|' * num_bars} 100% |\n\n")
            else:
                px = np.load(MP_data+"4D_BiSp_coeff.npy")

            C_inv = np.linalg.pinv(px)             # take pseudo-inverse of px matrix (equivalent to least squares fit)
            for i in range (Rpt):           # loop over all R
                ct = i*ngm                  # counter
                fx = df_inp.E[ct:ct+ngm]
                V_n1 = C_inv@(fx)
                V_nf[i,:] = V_n1

            a12 = np.arange(lm)             # a12 has same ordering as Lmat1
            df_Vnf = pd.DataFrame(V_nf, columns = a12)
            df_Vnf.insert(0, 'R', R_arr)                              # adding R column

            #print("The 15th to 30th terms are: \n ", df_Vnf[15:30])    # prints first few terms
            print("\n A preview of radial terms: \n ")        # printing radial dataframe
            print(df_Vnf.head(5))
            
            f.write("\n\n A preview of radial terms: \n ")        # printing radial dataframe
            f.write(str(df_Vnf.head(5)))
            
            
            print("Saving final radial terms file 4D_Vlam.dat in above folder")
            f.write("\n\nSaving final radial terms file 4D_Vlam.dat in above folder \n")
            df_Vnf.to_csv(MP_data + '4D_Vlam.dat', index=None, header=True,sep=',')  # save V_lam coefficients to file separated by comma
            print("Plotting radial terms at :--> ")
            print(MP_plots)
            
            f.write("\n Plotting radial terms at :--> \n ")
            f.write(str(MP_plots))
            f.write("\n")
 
            try:
                inp.Ind_plot
            except:
                Ind_plot = False
            else:
                Ind_plot = inp.Ind_plot
            if Ind_plot == True:
                driver.plot_MP(lm, 1, R_arr, df_Vnf, MP_plots, inp)
            driver.plot_MP_combined(lm, 1, R_arr, df_Vnf, MP_plots, inp)

            print("#-------------------------------------------------------------------#")
            print("#---------------#    4D Mutipole Expansion Done!    #---------------#")
            print("#-------------------------------------------------------------------#")

            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n#---------------#    4D Mutipole Expansion Done!    #---------------#")
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n\n")

        else:
            ########################################################
            #        4D Inverse Multipole Expansion (for Residuals)
            ########################################################
            # read original PES
            MP_dataR = MP_data + 'Residuals_Inv_Fit/' # directory for TF NN model and other files
            if not os.path.exists(MP_dataR):
                os.makedirs(MP_dataR)
            df_inp = pd.read_csv(out_data+inp.PES_filename_cm,header=None,sep=inp.sep)
            df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
            df_inp.dropna(inplace=True) #removing rows with na values
            print(df_inp.head(5))

            print("\n If your input dataframe contain non-numeric 'HEADER' like R, theta, E, etc, it will be removed. \n")
            print("\n Also verify if data separator is correct ! If incorrect separator is used, only single columns will appear. \n")
            sep_change = int(input("Satisfied! Enter 0 to continue or 1 to change separator (\s+, \\t, ',', etc.)..."))
            if (sep_change == 1):
                new_sep = input("Enter new separator (\s+ (multiple spaces), \\t (tab space), ',', etc.)...")
                df_inp = pd.read_csv(out_data+inp.PES_filename_cm,header=None,sep=new_sep)
                df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
                df_inp.dropna(inplace=True) #removing rows with na values
                print(df_inp.head(5))
                f.write("\n")
                f.write("\nThe loaded PES: --> \n")
                f.write(str(df_inp.head(5)))
            else:
                f.write("\n")
                f.write("\nThe loaded PES: --> \n")
                f.write(str(df_inp.head(5)))
            

            df_inp.columns =['R','phi','th2','th1','E']
            df_inp.sort_values(by = [ 'R','phi','th2','th1'], inplace=True, ascending = True)
            df_inp.reset_index(inplace=True, drop = True)  # sorting by R, phi, th2 and th1 and reindexing

            # importing 2D radial terms
            df_Vn = pd.read_csv(MP_data+inp.V_lam_filename_cm,sep=inp.sep_vlam,header=None)

            df_Vn = df_Vn.apply(pd.to_numeric, errors='coerce')
            df_Vn.dropna(inplace=True) #removing rows with na values
            print(df_Vn.head(5))

            df_R = df_Vn.pop(0)                              # removing R column from df_Vn and saving to df_R
            #df_R = df_Vn.pop('R')                              # removing R column from df_Vn and saving to df_R
            if inp.read_SH :
                px = np.load(MP_data+"4D_BiSp_coeff.npy")         # importing legendre coefficients
            else:
                print("Error! 4D_BiSp_coeff.npy must be read from MPExp2D calculation")
                print("Make sure file exists at {} and set read_Legendre = True".format(MP_data))
                f.write("Error! 4D_BiSp_coeff.npy must be read from MPExp2D calculation\n")
                f.write("Make sure file exists at {} and set read_Legendre = True \n".format(MP_data))
                driver.exit_program()
            #print("Radial coordinates are: \n ", df_R)        # Optional: prints radial coordinates

            print("The radial terms imported are: \n ")        # printing radial dataframe
            print(df_Vn.head(5))
            f.write("\n The radial terms imported are: \n ")        # printing radial dataframe
            f.write(str(df_Vn.head(5)))

            lm  = len(px.T)                    # Radial terms
            nc  = len(df_Vn)                   # number of Radial coordinates
            ngm = len(px)                      # number of angular coordinates
            R_arr = df_inp.R.unique()       # extracting unique values of R (sorted)

            V_n1 = px.dot(df_Vn.T)                 # save regenerated potentials
            a12 = np.arange(ngm)            # creates header for angles
            df_Vnf = pd.DataFrame(V_n1.T, columns = a12) # saves final matrix into dataframe with appropriate header
            df_Vnf.insert(0, 'R', R_arr)                              # adding R column
            # converting PES from matrix format to R,A,E format
            df_Vnf2 = pd.melt(df_Vnf, id_vars='R', value_vars=list(df_Vnf.columns[1:]), var_name='th_bin', value_name='E',ignore_index=True)
            #df_Vnf2.to_csv(MP_data + 'Regenerated_PES.dat', index=None, header=True,sep=',')  # save V_lam coefficients to file separated by comma
            df_inp.sort_values(by = ['phi','th2','th1','R'], inplace=True, ascending = True,ignore_index =True)
            #print(df_inp,df_Vnf2)
            Origi_E = df_inp.values[:, -1].reshape(-1,1)  # original Energies
            Regen_E = df_Vnf2.values[:, -1].reshape(-1,1)  # regenerated Energies
            residuals = Regen_E - Origi_E

            print("\nSaving regenerated PES data from analytically fitted V_lamda terms and its residual at location --> \n")
            print(str(MP_dataR))
            print("\n")

            f.write("\n\nSaving regenerated PES data from analytically fitted V_lamda terms and its residual at location --> \n")
            f.write(str(MP_dataR))
            f.write("\n")

            np.savetxt(MP_dataR +'residual_Vlam2E.dat', np.array([Origi_E.flatten(), Regen_E.flatten(), residuals.flatten()]).T, delimiter='\t')
            df_Vnf2.to_csv(MP_dataR + 'regenerated_PES_data.dat', index=None, header=False,sep=',')  # save V_lam coefficients to file separated by comma
            df_inp.to_csv(MP_dataR + 'original_PES_data.dat', index=None, header=False,sep=',')  # save V_lam coefficients to file separated by comma

            #print("\nSaving V_lam2PES analytically fitted residuals at location: {} ".format(MP_dataR))
            #f.write("\nSaving V_lam2PES analytically fitted residuals at location: {} ".format(MP_dataR))
            driver.residual_plot(Origi_E,residuals,MP_dataR,inp)

            print("#-------------------------------------------------------------------#")
            print("#-----------------#    4D Inverse Fitting Done!    #----------------#")
            print("#-------------------------------------------------------------------#")

            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n#-----------------#    4D Inverse Fitting Done!    #----------------#")
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n\n")

    else:
        print("Error: Unknwon Expansion_typ. Set as '2D' or '4D'.")
else:
    print(" \n MPExp = False : Skipping Multipole Expansion \n")
    f.write('\n MPExp = False : Skipping Multipole Expansion! \n ')

###############################################################################
###############################################################################
############################ Analytical Fitting ###############################
###############################################################################
###############################################################################

try:
    inp.FnFit
except:
    FnFit =False
else:
    FnFit = inp.FnFit

if FnFit:

    print("#-------------------------------------------------------------------#")
    print("#----------------#    Using Function Fit module    #----------------#")
    print("#-------------------------------------------------------------------#")
    
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n#----------------#    Using Function Fit module    #----------------#")
    f.write("\n#-------------------------------------------------------------------#")
    f.write("\n\n")
    
    from scipy.optimize import curve_fit
    from lmfit import Model
    #FnFit_data = out_data + 'FnFit_files/' # directory for TF NN model and other files
    #if not os.path.exists(FnFit_data):
    #    os.makedirs(FnFit_data)
    # FnFit_plots = FnFit_data + 'FnFit_plots/' # directory for TF NN model and other files
    # if not os.path.exists(FnFit_plots):
    #     os.makedirs(FnFit_plots)

    # Verifying input for optional features!
    try:
        inp.scale_Energy
    except:
        scale_Energy = 1
    else:
        scale_Energy = inp.scale_Energy

    try:
        inp.scale_R
    except:
        scale_R = 1
    else:
        scale_R = inp.scale_R

    try:
        inp.E_inf
    except:
        E_Hartree = False
        E_inf = 0.00
    else:
        E_Hartree = True
        E_inf = inp.E_inf

    if inp.Fnfit_type == 'Vlam':
        print("Fitting Radial coefficients obtained after multipole expansion!\n")
        f.write("Fitting Radial coefficients obtained after multipole expansion!\n")
        
        MP_data = out_data + 'MP_files/'
        FnFit_data = MP_data + 'VlamFnFit/' # directory for TF NN model and other files
        if not os.path.exists(FnFit_data):
            os.makedirs(FnFit_data)
        FnFit_plots = FnFit_data + 'Plots/' # directory for TF NN model and other files
        if not os.path.exists(FnFit_plots):
            os.makedirs(FnFit_plots)
        df_z = pd.read_csv(MP_data+inp.filename,sep=inp.sep)
        df_R = df_z.pop('R')                              # removing R column from df_Vn and saving to df_R
        df_z.columns = range(df_z.shape[1])
        lm = len(df_z.columns) # lm contains lambda terms
        x_dummy =df_R.to_numpy()
        #print(x_dummy)
        #print(df_z)

        Error_MP_fit0 = np.zeros(lm)
        Mp_coeff_E0 = np.zeros(shape=(lm,len(inp.initial_val)))
        Fitted_VlamE0 = x_dummy
        #FnFit_custom = FnFit_plots + 'custom_custom/' # directory for TF NN model and other files
        # if not os.path.exists(FnFit_custom):
        #     os.makedirs(FnFit_custom)
        strt_i = np.zeros(lm)
        for i in range(lm):
            y_dummy = df_z[i]
            try:
                inp.start_pos
            except:
                strt1, strt_val1 = driver.find_nearest(y_dummy, value=inp.cutoff) # datapoint with cutoff (repulsive potential)
                strt2, strt_val2 = driver.find_nearest(y_dummy, value=-inp.cutoff) # datapoint with -cutoff (attracive potential)
                strt = min(strt1,strt2)
                strt_i[i] = strt
                print("Minima Fit:{} | Start position: {} | Value (cm-1) {}".format(i,strt, y_dummy[strt]))
                f.write("\n\nMinima Fit:{} | Start position: {} | Value (cm-1) {} \n".format(i,strt, y_dummy[strt]))
            else:
                strt = inp.start_pos[i]
                strt_i[i] = strt
                print("Minima Fit:{} | Start position: {} | Value (cm-1) {}".format(i,strt, y_dummy[strt]))
                f.write("\n\nMinima Fit:{} | Start position: {} | Value (cm-1) {} \n\n".format(i,strt, y_dummy[strt]))

            gmodel = Model(inp.fnfit_custom) # using lmfit

            params = gmodel.make_params()
            for keyi in range (len(params.keys())):
                params.add(list(params.keys())[keyi], value=inp.initial_val[keyi])

            result = gmodel.fit(y_dummy[strt:]*scale_Energy, params, x=x_dummy[strt:]*scale_R) # Final Optimization

            best_vals = np.array(list(result.best_values.values()))

            Mp_coeff_E0[i] = best_vals

            new_lam0 = inp.fnfit_custom(x_dummy*scale_R, *best_vals)/scale_Energy
            Fitted_VlamE0 = np.c_[Fitted_VlamE0,new_lam0]
            Error_MP_fit0[i] = driver.plot_Vlam(x_dummy, y_dummy, best_vals, strt, i, inp, FnFit_plots,0, scale_R, scale_Energy)
            f.write( 'RMSE {} | {} \n'.format(i, Error_MP_fit0[i]))
            #print(result.best_values)
            #print('\n')

        #print("The new Function Fitted V_lam data is stored in {} ! ")
        #f.write("The new Function Fitted V_lam data is stored in {} ! ")

        f.write ("\n Start position for fitting each radial term : \n")
        f.write("start_pos = \n {} \n".format(strt_i))

        f.write('\n Mean RMS Error | {} \n'.format(np.mean(Error_MP_fit0)))
        
        print("\nSaving analytically fitted V_lam data (FnFitted_Vlam.dat) at locations: \n ")
        print(" {} \n and \n {} \n".format(MP_data,FnFit_data))
        f.write("\n\nSaving analytically fitted V_lam data (FnFitted_Vlam.dat) at locations: \n ")
        f.write(" {} \n and \n {} \n".format(MP_data,FnFit_data))

        np.savetxt(MP_data+"FnFitted_Vlam.dat", Fitted_VlamE0, delimiter=",")
        np.savetxt(FnFit_data+"FnFitted_Vlam.dat", Fitted_VlamE0, delimiter=",")

        print("\nThe coefficients for custom functions are saved in Raw format in Proj_name folder. The same can be converted manually!")
        f.write("\nThe coefficients for custom functions are saved in Raw format in Proj_name folder. The same can be converted manually!")

        if inp.coll_typ == '2D' :
            if inp.symmetric:
                sym = 2
            else:
                sym = 1
        elif inp.coll_typ == '4D' :
            L_mat = np.loadtxt(MP_data+inp.Lmat, dtype = int)
        else:
            print("Error! coll_typ must be either '2D' or '4D'. ")
            driver.exit_program()

        print("\nSaving V_lam raw coefficients at location: \n {} ".format(out_data))
        f.write("\n\nSaving V_lam raw coefficients at location: \n {} ".format(out_data))

        try:
            inp.Pair_fns
        except:
            Pair_fns = False
        else:
            Pair_fns = inp.Pair_fns

        try:
            inp.N_Opt
        except:
            N_Opt = False
        else:
            N_Opt = inp.N_Opt

        if inp.Print_raw:
            mol_file0 = open(out_data+"RAW_POT_custom.txt", "w")
            mol_file0.write(str(Mp_coeff_E0))
            mol_file0.close()
        N_Efn = inp.Exp_fns
        A_sgn = inp.A_sign
        Str3 = 'LAMBDA = '
        if inp.coll_typ == '2D' :
            L_map = list(range(0,(lm*sym),sym))
            L_map_str = ','.join(map(str, L_map))
            Str3 += L_map_str+ ','
        else:
            Str3 += '\n'
            for j in range (lm):
                Str3 += str(L_mat[j,1]) + ',' + str(L_mat[j,2]) + ',' + str(L_mat[j,3]) + ','
                Str3 += '\n'
        Str3 += '\nNTERM  = ' + '{},'.format(N_Efn)*(lm)
        Str3 += '\nNPOWER = ' + '0,'*N_Efn*lm
        Str3 += '\nA = \n'
        if N_Opt == True:
            for i in range (lm):
                Strlm3 = ''
                for k in range (N_Efn):
                    Strlm3 += str(Mp_coeff_E0[i][k+N_Efn]*A_sgn[k]) + ','
                Str3 += Strlm3 +'\n'
            Str3 += '\nE = \n'
            for i in range (lm):
                Strlm3 = ''
                for k in range (N_Efn):
                    Strlm3 += str(Mp_coeff_E0[i][k]) + ','
                    Str3 += Strlm3 +'\n'
        else:
            for i in range (lm):
                Strlm3 = ''
                for k in range (N_Efn):
                    if Pair_fns == False:
                        Strlm3 += str(Mp_coeff_E0[i][k]*A_sgn[k]) + ','
                    else:
                        Strlm3 += str(Mp_coeff_E0[i][k]) + ','
                        Strlm3 += str(Mp_coeff_E0[i][k] * -1) + ','
                Str3 += Strlm3 +'\n'
            Str3 += '\nE = \n'
            Strlm3 = ','.join(map(str, inp.N_Vals))+', \n'
            Str3 += Strlm3*lm +'\n'

        print("\nSaving MOLSCAT &POTL (MOLSCAT_POT.txt) at location: \n {} ".format(out_data))
        f.write("\n\nSaving MOLSCAT &POTL (MOLSCAT_POT.txt) at location: \n {} \n".format(out_data))

        mol_file3 = open(out_data+"MOLSCAT_POT.txt", "w")
        mol_file3.write(Str3)
        mol_file3.close()

        print("#-------------------------------------------------------------------#")
        print("#-----------------#    MOLSCAT &POTL Generated    #-----------------#")
        print("#-------------------------------------------------------------------#")

        f.write("\n#-------------------------------------------------------------------#")
        f.write("\n#-----------------#    MOLSCAT &POTL Generated    #-----------------#")
        f.write("\n#-------------------------------------------------------------------#")
        f.write("\n\n")

    elif inp.Fnfit_type == 'PES':

        try:
            inp.he_fit
        except:
            he_fit = False
            #he_cutoff = 0.00
        else:
            he_fit = inp.he_fit
            he_cutoff = inp.he_cutoff

        try:
            inp.lr_fit
        except:
            lr_fit = False
            #lr_cutoff = 0.00
        else:
            lr_fit = inp.lr_fit
            #lr_cutoff = inp.lr_cutoff

        if (lr_fit == True or he_fit == True):
            HELR_Fit = True
        else:
            HELR_Fit = False

        print("Fitting PES data into analytical function!\n")
        f.write("\n Fitting PES data into analytical function! \n")
        
        FnFit_data = out_data + 'PESFnFit/' # directory for TF NN model and other files

        if not os.path.exists(FnFit_data):
            os.makedirs(FnFit_data)
        FnFit_plots = FnFit_data + 'Plots/' # directory for TF NN model and other files
        if not os.path.exists(FnFit_plots):
            os.makedirs(FnFit_plots)

        if HELR_Fit == False:
            f_fnout = open(FnFit_data+"pes_fn.txt", "a+")
     
        #df_res = pd.read_csv(out_data+inp.filename,sep=inp.sep)
        #if Matrix_convert:
        #    if PES_typ == '2D':
        #        df_z = df_res.pivot(index=df_res.columns[0], columns=df_res.columns[1], values=df_res.columns[2])
        #    elif PES_typ == '4D':
        #        df_z = df_res.pivot(index=df_res.columns[0], columns=[df_res.columns[1],df_res.columns[2],df_res.columns[3]], values=df_res.columns[4])
        #    else:
        #        print("Incorrect PES_typ. Must be either '2D' or '4D'.")

        df_inp = pd.read_csv(out_data+inp.filename,header=None,sep=inp.sep)
        df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
        df_inp.dropna(inplace=True) #removing rows with na values

        print("Loaded PES! \n ")
        print(df_inp.head(5))
        
        print("\n If your input dataframe contain non-numeric 'HEADER' like R, theta, E, etc, it will be removed. \n")
        print("\n Also verify if data separator is correct ! If incorrect separator is used, only single columns will appear. \n")
        sep_change = int(input("Satisfied! Enter 0 to continue or 1 to change separator (\s+, \\t, ',', etc.)..."))
        if (sep_change == 1):
            new_sep = input("Enter new separator (\s+ (multiple spaces), \\t (tab space), ',', etc.)...")
            df_inp = pd.read_csv(out_data+inp.filename,header=None,sep=new_sep)
            df_inp = df_inp.apply(pd.to_numeric, errors='coerce')
            df_inp.dropna(inplace=True) #removing rows with na values
            print(df_inp.head(5))
            f.write("\n")
            f.write("\nThe loaded PES: --> \n")
            f.write(str(df_inp.head(5)))
        else:
            f.write("\n")
            f.write("\nThe loaded PES: --> \n")
            f.write(str(df_inp.head(5)))

        if inp.PES_typ == '1D':
            df_inp.columns = ['R', 'E']

            if HELR_Fit == False:
                f_fnout.write('1D \n')

            if E_Hartree == True:
                df_inp['E'] = (df_inp['E'] - E_inf)*219474.63             # convert to cm-1
                #df_inp.to_csv(FnFit_data+'psi4_FnFit_cm.dat', index=None, header=None,sep=',')
            print(df_inp)
            df_inp.to_csv(FnFit_data+'Original_PES_sort_cm.dat', index=None, header=None,sep=',')    # save sorted PES
            #f.write(str(df_inp))

            # dummy variables containing original data
            x_dummy = df_inp['R'].copy()
            y_dummy = df_inp['E'].copy()
            # Variable for carrying fitted PES (no extrapolation)
            Fitted_E = df_inp['E'].copy()

            # R_arr is either new R or unique R depending on input file
            # Variable for carrying fitted PES (with full extrapolation)
            try:
                inp.New_R
            except:
                R_arr = np.sort(df_inp['R'].unique())     # extracting unique values of R (sorted)
            else:
                R_arr = inp.New_R                     # R is provided in input file

            predicted_energies = np.zeros(len(R_arr))         # final terms
            predicted_energiesHELR = np.zeros(len(R_arr))       # final terms
            predicted_energiesR = np.zeros(len(df_inp))     # final terms

            # Determining cutoff position for HE/Minima region
            try:
                inp.cutoff_pos
            except:
                strt, strt_val = driver.find_nearest(y_dummy, value=inp.cutoff) # datapoint with cutoff
                print("Start position: {} | Value (cm-1) {} \n".format(strt, strt_val))
                f.write("Start position: {} | Value (cm-1) {} \n\n".format(strt, strt_val))
            else:
                strt=np.argmin(y_dummy)-inp.cutoff_pos

            #------------- High energy region fitting ---------------#

            if he_fit == True:
                print('High Energy region fitting!')
                f.write('\n High Energy region fitting!')
                pos_minima=np.argmin(y_dummy)
                strtHE, strt_valHe = driver.find_nearest(y_dummy, value=he_cutoff) # datapoint with cutoff
                gmodel = Model(inp.fnfit_he) # using lmfit
                params = gmodel.make_params()
                for keyi in range (len(params.keys())):
                    params.add(list(params.keys())[keyi], value=inp.he_initial_val[keyi])
                print('Fitting from :', strtHE, 'to', pos_minima-inp.he_min_offset)
                f.write('\n Fitting from: {} to {} \n'.format(strtHE, (pos_minima-inp.he_min_offset)))

                result = gmodel.fit(y_dummy[strtHE:pos_minima-inp.he_min_offset], params, x=x_dummy[strtHE:pos_minima-inp.he_min_offset]) # Final Optimization
                best_vals = np.array(list(result.best_values.values()))
                print('\n Optimised Coefficients for High Energy (HE) : \n ',best_vals)
                f.write(' \n Optimised Coefficients for High Energy (HE): \n  {} \n\n'.format(best_vals))

                Fitted_E[:strt] = inp.fnfit_he(x_dummy[:strt], *best_vals)
                R_arr_HE, R_arr_val_HE = driver.find_nearest(R_arr, value=x_dummy[strt]) # datapoint with cutoff
                predicted_energiesHELR[:R_arr_HE] = inp.fnfit_he(R_arr[:R_arr_HE], *best_vals)
            else:
                R_arr_HE = 0
                print('No High Energy fitting!')
                f.write('\n No High Energy fitting!')

            # ------------- Long range region fitting ---------------#

            if lr_fit == True:

                print('Long range fitting!')
                f.write('\n Long range fitting! \n')

                endLR = len(x_dummy)-inp.lr_min_offset # datapoint with cutoff
                gmodel = Model(inp.fnfit_lr) # using lmfit
                params = gmodel.make_params()
                for keyi in range (len(params.keys())):
                    params.add(list(params.keys())[keyi], value=inp.lr_initial_val[keyi])
                print('\n Fitting from :', endLR, 'to', len(x_dummy))
                f.write('\n Fitting from: {} to {} \n'.format(endLR, len(x_dummy)))

                result = gmodel.fit(y_dummy[endLR:], params, x=x_dummy[endLR:]) # Final Optimization
                best_vals = np.array(list(result.best_values.values()))
                print('\n Optimised Coefficients for Long Range (LR) : \n ',best_vals)
                f.write(' \n Optimised Coefficients for Long Range (LR): \n {} \n\n'.format(best_vals))
                Fitted_E[endLR:] = inp.fnfit_lr(x_dummy[endLR:], *best_vals)
                R_arr_LR, R_arr_val_LR = driver.find_nearest(R_arr, value=x_dummy[endLR]) # datapoint with cutoff
                predicted_energiesHELR[R_arr_LR:] = inp.fnfit_lr(R_arr[R_arr_LR:], *best_vals)
            else:
                print('No Long Range fitting!')
                f.write('\n No Long Range fitting! \n')
                R_arr_LR = len(R_arr)

            # --------------------------- Full range fitting ------------------------#

            print('\n Using Custom Function for full range fitting!')
            f.write('\n\n Using Custom Function for full range fitting!')

            gmodel = Model(inp.fnfit_custom) # using lmfit
            params = gmodel.make_params()

            try:
                inp.lower_bounds
                inp.upper_bounds
            except:
                for keyi in range (len(params.keys())):
                    params.add(list(params.keys())[keyi], value=inp.initial_val[keyi])
            else:
                for keyi in range(len(params.keys())):
                    params.add(list(params.keys())[keyi], value=inp.initial_val[keyi], \
                                min=inp.lower_bounds[keyi], max=inp.upper_bounds[keyi])

            result = gmodel.fit(y_dummy[strt:]*scale_Energy, params, x=x_dummy[strt:]*scale_R) # Final Optimization

            best_vals = np.array(list(result.best_values.values()))

            # predicted energies in new or unique range (for MP Expansion)
            predicted_energies = inp.fnfit_custom(R_arr*scale_R, *best_vals)/scale_Energy

            # predicted energies in original range (for Residual Plots)
            predicted_energiesR = inp.fnfit_custom(x_dummy*scale_R, *best_vals)/scale_Energy

            print("Potential at initial R value: ", predicted_energies[0])
            f.write("\n Potential at initial R value: {}".format(predicted_energies[0]))

            print(result.best_values)
            f.write("\n Fitting Coefficients for full region fit : \n")
            f.write(str(best_vals))

            if HELR_Fit == False:
                #f_fnout.write(str(",".join(best_vals) + "\n"))
                np.savetxt(f_fnout, best_vals.reshape(1, -1), delimiter=',', fmt='%.16g')


            final_data = np.c_[ R_arr, predicted_energies ]
            residuals = predicted_energiesR - y_dummy.to_numpy()
            residuals_data = np.c_[ y_dummy.to_numpy(), residuals ]
            if HELR_Fit == True:
                predicted_energiesHELR[R_arr_HE:R_arr_LR] = inp.fnfit_custom(R_arr[R_arr_HE:R_arr_LR]*scale_R, *best_vals)/scale_Energy

            print("\nSaving fitted PES (Fnfit_PES.dat) and residuals (residuals_Fnfit_PES.dat) to : \n {}".format(FnFit_data))
            f.write("\n\nSaving fitted PES (Fnfit_PES.dat) and residuals (residuals_Fnfit_PES.dat) to : \n {} \n\n".format(FnFit_data))
            np.savetxt(FnFit_data+"Fnfit_PES.dat", final_data, delimiter=",",fmt='%.2f,%.16f')
            np.savetxt(FnFit_data+"residuals_Fnfit_PES.dat", residuals_data, delimiter=",",fmt='%.16f,%.16f')

            print("\nPlotting E fit (R) at location: \n {} ".format(FnFit_plots))
            f.write("\n\nPlotting E fit (R) at location: \n {} \n\n".format(FnFit_plots))
            driver.residual_plot_E(y_dummy.to_numpy(),residuals,FnFit_plots,inp,'custom')

            if HELR_Fit == True:
                driver.C_fit1D_Plot(y_dummy,predicted_energies,predicted_energiesHELR,R_arr,x_dummy,FnFit_plots,inp)
                HELR_Fit_PES = np.c_[ x_dummy, predicted_energiesHELR ]
                print("\nSaving Only High Energy and Long Range region fitted PES (HELR_Fit_PES.dat) to : \n {}".format(FnFit_data))
                f.write("\n\nSaving Only High Energy and Long Range region fitted PES (HELR_Fit_PES.dat) to : \n {} \n\n".format(FnFit_data))

                np.savetxt(FnFit_data+"HELR_Fit_PES.dat", HELR_Fit_PES, delimiter=",",fmt='%.2f,%.16f')
                driver.fit1D_Plot(y_dummy,predicted_energiesHELR,'HELR',x_dummy,x_dummy,FnFit_plots,inp)
                driver.fit1D_Plot(y_dummy,predicted_energies,'CustomFn_fit',R_arr,x_dummy,FnFit_plots,inp)
            else:
                driver.fit1D_Plot(y_dummy,predicted_energies,'CustomFn_fit',R_arr,x_dummy,FnFit_plots,inp)
                f_fnout.close()

            # saving data and plots!

            f.write("\n\nSaving a copy of fitted PES (Fnfit_PES.dat) to : \n {} \n\n".format(out_data))
            np.savetxt(out_data+"Fnfit_PES.dat", final_data, delimiter=",",fmt='%.2f,%.16f')

            print("#-------------------------------------------------------------------#")
            print("#-------#    1D PES Fitted into analytical expression!    #---------#")
            print("#-------------------------------------------------------------------#")
    
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n#-------#    1D PES Fitted into analytical expression!    #---------#")
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n\n")


        elif inp.PES_typ == '2D':
            df_inp.columns = ['R', 'th', 'E']

            if HELR_Fit == False:
                f_fnout.write('2D \n')

            if E_Hartree == True:
                df_inp['E'] = (df_inp['E'] - E_inf)*219474.63             # convert to cm-1
                #df_inp.to_csv(FnFit_data+'psi4_FnFit_cm.dat', index=None, header=None,sep=',')

            df_inp.sort_values(by = ['th','R'], inplace=True, ascending = True)
            df_inp.reset_index(inplace=True, drop = True)  # sorting by R, phi, th2 and th1 and reindexing
            print(df_inp)
            df_inp.to_csv(FnFit_data+'Original_PES_sort_cm.dat', index=None, header=None,sep=',')    # save sorted PES
            #f.write(str(df_inp))
            angmat = df_inp['th'].drop_duplicates().to_numpy() # extracting unique angular coordinates

            try:
                inp.New_R
            except:
                R_arr = np.sort(df_inp['R'].unique())     # extracting unique values of R (sorted)
            else:
                R_arr = inp.New_R                     # R is provided in input file

            nc = len(R_arr)                           # number of Radial coordinates (Must be same for all angles)
            ngm = len(angmat)                         # number of angular coordinates

            # extract start and end values for each angular coordinate
            start = np.zeros(ngm,dtype=int)
            end   = np.zeros(ngm,dtype=int)
            ct = 0                      # counter
            print("Extracting end and start radial positions for each angular term : ")
            f.write("\n 2D Collision: Extracting end and start radial positions for each angular term: \n")
            for i in tqdm(range (len(df_inp))):
                if (i == 0):
                    R_st = df_inp['R'][i]
                    start[ct] = i
                    ct+=1
                elif (i == (len(df_inp)-1)):
                    end[ct-1] = i+1
                else:
                    if (df_inp['R'][i] > R_st):
                        R_st = df_inp['R'][i]
                    elif (df_inp['R'][i] < R_st):
                        end[ct-1] = i
                        start[ct] = i
                        R_st = df_inp['R'][i]
                        ct+=1
            f.write(f"\n TQDM LOOP (end and start radial positions extracted from PES!) :\n {'|' * num_bars} 100% |\n\n")

            #print("1922: Match these two numbers: ct = {} | ngm = {}".format(ct,ngm))
            print("Start End Positions for each angle: ")
            print("Start Positions: \n {}".format(start))
            print("End Positions: \n {}".format(end))
            f.write("Start End Positions: \n")
            f.write("Start Positions: \n {} \n".format(start))
            f.write("End Positions: \n {} \n \n".format(end))
            #if (ct!=ngm):
            #    driver.exit_program()
            # All R end and start positions extracted!

            # Generating R/Theta(s) coordinates (Full)
            A = np.ndarray(shape=(1,2)) # array initialization
            for i in tqdm (range (ngm)):
                b = angmat[i]              # getting angular coordinatees
                c = np.tile(b,(len(R_arr),1))  # creating angles as columns
                d = np.c_[ R_arr, c ]        # joining r and columns
                A = np.vstack([A, d]) # repeating for different geoms and joining
            A = np.delete(A, 0, 0) # deleting first row
            #A_Residuals = df_inp.pop('E')   # Coordinates for residuals
            A_Residuals = df_inp.drop('E', axis=1)
            AR = A_Residuals.to_numpy()

            f.write(f"\n TQDM LOOP (R/Theta coordinates Generated!) :\n {'|' * num_bars} 100% |\n\n")

            #print(len(df_inp))

            # Fitting PES
            print("Fitting PES each angle at a time: ")
            f.write("\n Fitting PES each angle at a time: \n")
            predicted_energies = np.zeros(ngm*nc)           # final terms
            predicted_energiesR = np.zeros(len(df_inp))     # final terms
            predicted_energiesHELR = np.zeros(ngm*nc)       # final terms

            for i in tqdm(range (ngm)):
                st, en = start[i], end[i]
                df_fit = df_inp.iloc[st:en,:].reset_index(drop=True)
                #print(df_fit)
                df_fit.columns=['a','b','e']

                # dummy variables containing original data
                y_dummy = df_fit['e'].copy()
                x_dummy = df_fit['a'].copy()
                # Variable for carrying fitted PES (no extrapolation)
                Fitted_E = df_fit['e'].copy()

                # Extracting location of minima in PES

                try:
                    inp.cutoff_pos
                except:
                    strt, strt_val = driver.find_nearest(y_dummy, value=inp.cutoff) # datapoint with cutoff
                    print("Minima Fit:{} | Start position: {} | Value (cm-1) {} \n".format(i,strt, strt_val))
                    f.write("\n\nMinima Fit:{} | Start position: {} | Value (cm-1) {} \n\n".format(i,strt, strt_val))
                else:
                    strt=np.argmin(y_dummy)-inp.cutoff_pos

                print("Coefficients for Angular coordinate: {} \n".format(angmat[i]))
                f.write("\n Coefficients for Angular coordinate: {} \n".format(angmat[i]))

                #------------- High energy region fitting ---------------#

                if he_fit == True:
                    print('High Energy region fitting!')
                    f.write('\n High Energy region fitting!')
                    pos_minima=np.argmin(y_dummy)
                    strtHE, strt_valHe = driver.find_nearest(y_dummy, value=he_cutoff) # datapoint with cutoff
                    gmodel = Model(inp.fnfit_he) # using lmfit
                    params = gmodel.make_params()
                    for keyi in range (len(params.keys())):
                        params.add(list(params.keys())[keyi], value=inp.he_initial_val[keyi])
                    print('Fitting from :', strtHE, 'to', pos_minima-inp.he_min_offset)
                    f.write('\n Fitting from: {} to {} \n'.format(strtHE, (pos_minima-inp.he_min_offset)))
                    result = gmodel.fit(y_dummy[strtHE:pos_minima-inp.he_min_offset], params, x=x_dummy[strtHE:pos_minima-inp.he_min_offset]) # Final Optimization
                    best_vals = np.array(list(result.best_values.values()))
                    print('Optimised Coefficients for High Energy (HE) : ',best_vals)
                    f.write(' \n Optimised Coefficients for High Energy (HE): \n  {} \n\n'.format(best_vals))
                    Fitted_E[:strt] = inp.fnfit_he(x_dummy[:strt], *best_vals)
                    R_arr_HE, R_arr_val_HE = driver.find_nearest(R_arr, value=x_dummy[strt]) # datapoint with cutoff
                    predicted_energiesHELR[i*nc:i*nc+R_arr_HE] = inp.fnfit_he(R_arr[:R_arr_HE], *best_vals)
                else:
                    R_arr_HE = 0
                    print('No High Energy fitting!')
                    f.write('\n No High Energy fitting! \n')
                # ------------- Long range region fitting ---------------#

                if lr_fit == True:
                    print('Long range fitting!')
                    f.write('\n Long range fitting! \n')
                    
                    endLR = len(x_dummy)-inp.lr_min_offset # datapoint with cutoff
                    gmodel = Model(inp.fnfit_lr) # using lmfit
                    params = gmodel.make_params()
                    for keyi in range (len(params.keys())):
                        params.add(list(params.keys())[keyi], value=inp.lr_initial_val[keyi])
                    print('\n Fitting from :', endLR, 'to', len(x_dummy))
                    f.write('\n Fitting from: {} to {} \n'.format(endLR, len(x_dummy)))
                    result = gmodel.fit(y_dummy[endLR:], params, x=x_dummy[endLR:]) # Final Optimization
                    best_vals = np.array(list(result.best_values.values()))
                    print('\n Optimised Coefficients for Long Range (LR)',best_vals)
                    f.write(' \n Optimised Coefficients for Long Range (LR): \n {} \n\n'.format(best_vals))
                    Fitted_E[endLR:] = inp.fnfit_lr(x_dummy[endLR:], *best_vals)
                    R_arr_LR, R_arr_val_LR = driver.find_nearest(R_arr, value=x_dummy[endLR]) # datapoint with cutoff
                    predicted_energiesHELR[i*nc+R_arr_LR:(i+1)*nc] = inp.fnfit_lr(R_arr[R_arr_LR:], *best_vals)

                else:
                    print('No Long Range fitting!')
                    f.write('\n No Long Range fitting! \n')
                    R_arr_LR = len(R_arr)

                    # ------------- Full range fitting ---------------#

                print('\n Using Custom Function for full range fitting!')
                f.write('\n\n Using Custom Function for full range fitting!')

                #y_dummy = Fitted_E

                gmodel = Model(inp.fnfit_custom)  # using lmfit
                #print(f'parameter names: {gmodel.param_names}')
                #print(f'independent variables: {gmodel.independent_vars}')

                params = gmodel.make_params()
                #print(type(list(params.keys())[0]))
                try:
                    inp.lower_bounds
                    inp.upper_bounds
                except:
                    for keyi in range (len(params.keys())):
                        params.add(list(params.keys())[keyi], value=inp.initial_val[keyi])
                else:
                    for keyi in range(len(params.keys())):
                        params.add(list(params.keys())[keyi], value=inp.initial_val[keyi], \
                                    min=inp.lower_bounds[keyi], max=inp.upper_bounds[keyi])
                #print(params)
                #y_eval = gmodel.eval(params, x=x_dummy[strt:])

                # To use LR fitted data for minima region fit, replace 'y_dummy' with 'Fitted_E'
                result = gmodel.fit(y_dummy[strt:]*scale_Energy, params, x=x_dummy[strt:]*scale_R) # Final Optimization

                best_vals = np.array(list(result.best_values.values()))

                # predicted energies in new or unique range (for MP Expansion)
                E = inp.fnfit_custom(R_arr*scale_R, *best_vals)/scale_Energy
                # predicted energies in original range (for Residual Plots)
                ER = inp.fnfit_custom(x_dummy*scale_R, *best_vals)/scale_Energy

                print("Potential at initial R value: ", E[0])
                f.write("\n Potential at initial R value: {}".format(E[0]))

                print(result.best_values)
                f.write("\n Fitting Coefficients for full region fit : \n")
                f.write(str(best_vals))
    
                if HELR_Fit == False:
                    np.savetxt(f_fnout, angmat[i].reshape(1, -1), delimiter=',', fmt='%.6g')
                    np.savetxt(f_fnout, best_vals.reshape(1, -1), delimiter=',', fmt='%.16g')

                predicted_energies[i*nc:(i+1)*nc] = E
                predicted_energiesR[st:en] = ER
                if HELR_Fit == True:
                    predicted_energiesHELR[i*nc+R_arr_HE:i*nc+R_arr_LR] = inp.fnfit_custom(R_arr[R_arr_HE:R_arr_LR]*scale_R, *best_vals)/scale_Energy
                #predicted_energiesHELR[st:en] = Fitted_E

            f.write(f"\n TQDM LOOP (Function Fitting Done!) :\n {'|' * num_bars} 100% |\n\n")

            Origi_E_df = df_inp['E']
            Origi_E = Origi_E_df.to_numpy()
            final_data = np.c_[ A, predicted_energies ]
            if HELR_Fit == True:
                HELR_Fit_PES = np.c_[ A, predicted_energiesHELR ]
            residuals = predicted_energiesR - Origi_E

            residuals_data = np.c_[Origi_E, residuals ]
            print("\nSaving fitted PES (Fnfit_PES.dat) and residuals (residuals_Fnfit_PES.dat) to: \n {}".format(FnFit_data))
            f.write("\n\nSaving fitted PES (Fnfit_PES.dat) and residuals (residuals_Fnfit_PES.dat) to: \n {} \n\n".format(FnFit_data))
            np.savetxt(FnFit_data+"Fnfit_PES.dat", final_data, delimiter=",",fmt='%.2f,%.2f,%.16f')
            if HELR_Fit == True:
                np.savetxt(FnFit_data+"HELRfit_PES.dat", HELR_Fit_PES, delimiter=",",fmt='%.2f,%.2f,%.16f')
                print("\nSaving Only High Energy and Long Range region fitted PES (HELR_Fit_PES.dat) to : \n {}".format(FnFit_data))
                f.write("\n\nSaving Only High Energy and Long Range region fitted PES (HELR_Fit_PES.dat) to : \n {} \n\n".format(FnFit_data))
            else:
                f_fnout.close()


            np.savetxt(FnFit_data+"residuals_Fnfit_PES.dat", residuals_data, delimiter=",",fmt='%.16f,%.16f')

            print("\nPlotting residuals for E fit (R) at location: \n {} ".format(FnFit_plots))
            f.write("\nPlotting residuals for E fit (R) at location: \n {} \n\n".format(FnFit_plots))
            driver.residual_plot_E(Origi_E,residuals,FnFit_plots,inp,'custom')

            f.write("\n\nSaving a copy of fitted PES (Fnfit_PES.dat) to: \n {} \n\n".format(out_data))
            np.savetxt(out_data+"Fnfit_PES.dat", final_data, delimiter=",",fmt='%.2f,%.2f,%.16f')

            print("#-------------------------------------------------------------------#")
            print("#-------#    2D PES Fitted into analytical expression!    #---------#")
            print("#-------------------------------------------------------------------#")
    
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n#-------#    2D PES Fitted into analytical expression!    #---------#")
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n\n")

        elif inp.PES_typ == '4D':
            df_inp.columns = ['R', 'phi', 'th2', 'th1', 'E']

            if HELR_Fit == False:
                f_fnout.write('4D \n')

            if E_Hartree == True:
                df_inp['E'] = (df_inp['E'] - E_inf)*219474.63             # convert to cm-1
                #df_inp.to_csv(FnFit_data+'psi4_FnFit_cm.dat', index=None, header=None,sep=',')

            df_inp.sort_values(by = [ 'th1','th2','phi','R'], inplace=True, ascending = True)
            df_inp.reset_index(inplace=True, drop = True)  # sorting by R, phi, th2 and th1 and reindexing
            print(df_inp)
            df_inp.to_csv(FnFit_data+'Original_PES_sort_cm.dat', index=None, header=None,sep=',')    # save sorted PES
            #f.write(str(df_inp))
            angmat = df_inp[['phi','th2','th1']].drop_duplicates().to_numpy() # extracting unique angular coordinates
            try:
                inp.New_R
            except:
                R_arr = np.sort(df_inp['R'].unique())     # extracting unique values of R (sorted)
            else:
                R_arr = inp.New_R                     # R is provided in input file

            nc = len(R_arr)                           # number of Radial coordinates (Must be same for all angles)
            ngm = len(angmat)                         # number of angular coordinates

            # extract start and end values for each angular coordinate
            start = np.zeros(ngm,dtype=int)
            end   = np.zeros(ngm,dtype=int)
            ct = 0                      # counter
            print("Extracting end and start radial positions for each angular term : ")
            f.write("\n 4D Collision: Extracting end and start radial positions for each angular term : \n")
            for i in tqdm(range (len(df_inp))):
                if (i == 0):
                    R_st = df_inp['R'][i]
                    start[ct] = i
                    ct+=1
                elif (i == (len(df_inp)-1)):
                    end[ct-1] = i+1
                else:
                    if (df_inp['R'][i] > R_st):
                        R_st = df_inp['R'][i]
                    elif (df_inp['R'][i] < R_st):
                        end[ct-1] = i
                        start[ct] = i
                        R_st = df_inp['R'][i]
                        ct+=1
            f.write(f"\n TQDM LOOP (end and start radial positions extracted!) :\n {'|' * num_bars} 100% |\n\n")

            #print("1951: Match these two numbers: i = {} | ngm = {}".format(i,ngm))
            print("Start End Positions for each angle: ")
            print("Start Positions: \n {}".format(start))
            print("End Positions: \n {}".format(end))
            f.write("Start End Positions: \n")
            f.write("Start Positions: \n {} \n".format(start))
            f.write("End Positions: \n {} \n".format(end))
            #if (ct!=ngm):
            #    driver.exit_program()
            # All R end and start positions extracted!

            # Generating R/Theta(s) coordinates (Full)
            A = np.ndarray(shape=(1,4)) # array initialization
            for i in tqdm (range (ngm)):
                b = angmat[i]              # getting angular coordinatees
                c = np.tile(b,(len(R_arr),1))  # creating angles as columns
                d = np.c_[ R_arr, c ]        # joining r and columns
                A = np.vstack([A, d]) # repeating for different geoms and joining
            f.write(f"\n TQDM LOOP (R/Phi/Theta2/Theta1 coordinates generated!) :\n {'|' * num_bars} 100% |\n\n")

            A = np.delete(A, 0, 0) # deleting first row
            A_Residuals = df_inp.drop('E', axis=1)
            AR = A_Residuals.to_numpy()
            # Fitting PES
            print("\nFitting PES each angle at a time: ")
            f.write("\n Fitting PES each angle at a time: \n")
            predicted_energies = np.zeros(ngm*nc)     # final terms
            predicted_energiesR = np.zeros(len(df_inp))     # final terms
            predicted_energiesHELR = np.zeros(len(df_inp))  # final terms

            for i in tqdm(range (ngm)):
                st, en = start[i], end[i]
                df_fit = df_inp.iloc[st:en,:].reset_index(drop=True)
                df_fit.columns=['a','b','c','d','e']

                # dummy variables containing original data
                y_dummy = df_fit['e'].copy()
                x_dummy = df_fit['a'].copy()
                # Variable for carrying fitted PES (no extrapolation)
                Fitted_E = df_fit['e'].copy()

                # Extracting location of minima in PES

                try:
                    inp.cutoff_pos
                except:
                    strt, strt_val = driver.find_nearest(y_dummy, value=inp.cutoff) # datapoint with cutoff
                    print("Minima Fit:{} | Start position: {} | Value (cm-1) {} \n".format(i,strt, strt_val))
                    f.write("\n\nMinima Fit:{} | Start position: {} | Value (cm-1) {} \n\n".format(i,strt, strt_val))
                else:
                    strt=np.argmin(y_dummy)-inp.cutoff_pos

                print("Coefficients for Angular coordinate: {} \n".format(angmat[i]))
                f.write("\n Coefficients for Angular coordinate: {} \n".format(angmat[i]))

                #------------- High energy region fitting ---------------#

                if he_fit == True:
                    print('High Energy region fitting!')
                    f.write('\n High Energy region fitting!')
                    pos_minima=np.argmin(y_dummy)
                    strtHE, strt_valHe = driver.find_nearest(y_dummy, value=he_cutoff) # datapoint with cutoff
                    gmodel = Model(inp.fnfit_he) # using lmfit
                    params = gmodel.make_params()
                    for keyi in range (len(params.keys())):
                        params.add(list(params.keys())[keyi], value=inp.he_initial_val[keyi])
                    print('Fitting from :', strtHE, 'to', pos_minima-inp.he_min_offset)
                    f.write('\n Fitting from: {} to {} \n'.format(strtHE, (pos_minima-inp.he_min_offset)))
                    result = gmodel.fit(y_dummy[strtHE:pos_minima-inp.he_min_offset], params, x=x_dummy[strtHE:pos_minima-inp.he_min_offset]) # Final Optimization
                    best_vals = np.array(list(result.best_values.values()))
                    print('Optimised Coefficients for High Energy (HE): \n ',best_vals)
                    f.write(' \n Optimised Coefficients for High Energy (HE): \n  {} \n\n'.format(best_vals))
                    Fitted_E[:strt] = inp.fnfit_he(x_dummy[:strt], *best_vals)
                    # ! Test and Uncomment
                    R_arr_HE, R_arr_val_HE = driver.find_nearest(R_arr, value=x_dummy[strt]) # datapoint with cutoff
                    predicted_energiesHELR[i*nc:i*nc+R_arr_HE] = inp.fnfit_he(R_arr[:R_arr_HE], *best_vals)
                else:
                    R_arr_HE = 0 # ! Test and Uncomment
                    print('No High Energy fitting!')
                    f.write('\n No High Energy fitting! \n')
                # ------------- Long range region fitting ---------------#

                if lr_fit == True:
                    print('Long range fitting!')
                    f.write('\n Long range fitting! \n')

                    endLR = len(x_dummy)-inp.lr_min_offset # datapoint with cutoff
                    gmodel = Model(inp.fnfit_lr) # using lmfit
                    params = gmodel.make_params()
                    for keyi in range (len(params.keys())):
                        params.add(list(params.keys())[keyi], value=inp.lr_initial_val[keyi])
                    print('\n Fitting from :', endLR, 'to', len(x_dummy))
                    f.write('\n Fitting from: {} to {} \n'.format(endLR, len(x_dummy)))
                    result = gmodel.fit(y_dummy[endLR:], params, x=x_dummy[endLR:]) # Final Optimization
                    best_vals = np.array(list(result.best_values.values()))
                    print('\n Optimised Coefficients for Long Range (LR)',best_vals)
                    f.write(' \n Optimised Coefficients for Long Range (LR): \n {} \n\n'.format(best_vals))
                    Fitted_E[endLR:] = inp.fnfit_lr(x_dummy[endLR:], *best_vals)
                    # ! Test and Uncomment
                    R_arr_LR, R_arr_val_LR = driver.find_nearest(R_arr, value=x_dummy[endLR]) # datapoint with cutoff
                    predicted_energiesHELR[i*nc+R_arr_LR:(i+1)*nc] = inp.fnfit_lr(R_arr[R_arr_LR:], *best_vals)
                else:
                    print('No Long Range fitting!')
                    f.write('\n No Long Range fitting! \n')
                    R_arr_LR = len(R_arr) # ! Test and Uncomment

                # ------------- Full range fitting ---------------#


                print('\n Using Custom Function for full range fitting!')
                f.write('\n\n Using Custom Function for full range fitting!')

                gmodel = Model(inp.fnfit_custom) # using lmfit

                params = gmodel.make_params()
                try:
                    inp.lower_bounds
                    inp.upper_bounds
                except:
                    for keyi in range (len(params.keys())):
                        params.add(list(params.keys())[keyi], value=inp.initial_val[keyi])
                else:
                    for keyi in range(len(params.keys())):
                        params.add(list(params.keys())[keyi], value=inp.initial_val[keyi], \
                                    min=inp.lower_bounds[keyi], max=inp.upper_bounds[keyi])

                result = gmodel.fit(y_dummy[strt:]*scale_Energy, params, x=x_dummy[strt:]*scale_R) # Final Optimization

                best_vals = np.array(list(result.best_values.values()))

                E = inp.fnfit_custom(R_arr*scale_R, *best_vals)/scale_Energy
                ER = inp.fnfit_custom(x_dummy*scale_R, *best_vals)/scale_Energy
                print("Potential at initial R value: ", E[0])
                f.write("\n Potential at initial R value: {}".format(E[0]))

                print(result.best_values)
                f.write("\n Fitting Coefficients for full region fit : \n")
                f.write(str(best_vals))

                if HELR_Fit == False:
                    np.savetxt(f_fnout, angmat[i].reshape(1, -1), delimiter=',', fmt='%.6g')
                    np.savetxt(f_fnout, best_vals.reshape(1, -1), delimiter=',', fmt='%.16g')

                predicted_energies[i*nc:(i+1)*nc] = E
                predicted_energiesR[st:en] = ER
                if HELR_Fit == True:
                    predicted_energiesHELR[i*nc+R_arr_HE:i*nc+R_arr_LR] = inp.fnfit_custom(R_arr[R_arr_HE:R_arr_LR]*scale_R, *best_vals)/scale_Energy

            f.write(f"\n TQDM LOOP (Function Fitting Done!) :\n {'|' * num_bars} 100% |\n\n")

            Origi_E_df = df_inp['E']
            Origi_E = Origi_E_df.to_numpy()
            final_data = np.c_[ A, predicted_energies ]
            if HELR_Fit == True:
                HELR_Fit_PES = np.c_[ A, predicted_energiesHELR ]
            residuals = predicted_energiesR - Origi_E

            residuals_data = np.c_[Origi_E, residuals ]
            print("\nSaving fitted PES (Fnfit_PES.dat) and residuals (residuals_Fnfit_PES.dat) to: \n {}".format(FnFit_data))
            f.write("\n\nSaving fitted PES (Fnfit_PES.dat) and residuals (residuals_Fnfit_PES.dat) to: \n {} \n\n".format(FnFit_data))
            #print("\nSaving fitted PES to : {}".format(FnFit_data))
            np.savetxt(FnFit_data+"Fnfit_PES.dat", final_data, delimiter=",",fmt='%.2f,%.2f,%.2f,%.2f,%.16f')
            if HELR_Fit == True:
                np.savetxt(FnFit_data+"HELRfit_PES.dat", HELR_Fit_PES, delimiter=",",fmt='%.2f,%.2f,%.2f,%.2f,%.16f')
                print("\nSaving Only High Energy and Long Range region fitted PES (HELR_Fit_PES.dat) to : \n {}".format(FnFit_data))
                f.write("\n\nSaving Only High Energy and Long Range region fitted PES (HELR_Fit_PES.dat) to : \n {} \n\n".format(FnFit_data))
            else:
                f_fnout.close()

            np.savetxt(FnFit_data+"residuals_Fnfit_PES.dat", residuals_data, delimiter=",",fmt='%.16f,%.16f')

            print("\nPlotting residuals for E fit (R) at location: \n {} ".format(FnFit_plots))
            f.write("\nPlotting residuals for E fit (R) at location: \n {} \n\n".format(FnFit_plots))
            driver.residual_plot_E(Origi_E,residuals,FnFit_plots,inp,'custom')

            f.write("\n\nSaving a copy of fitted PES (Fnfit_PES.dat) to: \n {} \n\n".format(out_data))
            np.savetxt(out_data+"Fnfit_PES.dat", final_data, delimiter=",",fmt='%.2f,%.2f,%.2f,%.2f,%.16f')

            print("#-------------------------------------------------------------------#")
            print("#-------#    4D PES Fitted into analytical expression!    #---------#")
            print("#-------------------------------------------------------------------#")
    
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n#-------#    4D PES Fitted into analytical expression!    #---------#")
            f.write("\n#-------------------------------------------------------------------#")
            f.write("\n\n")

        else:
            print("\nIncorrect PES_typ. Must be either '1D', '2D' or '4D'.")

    else:
        print("\nIncorrect Fnfit_type. Must be either 'PES' or 'Vlam'.")

else:
    print(" \n FnFit = False : Skipping Analytical Fitting of Radial Coefficients \n")
    f.write('\n FnFit = False : Skipping Analytical Fitting of Radial Coefficients! \n ')
#################################################################################

    # Calculate the runtime.
run_time = time.time() - start_time
# Convert runtime to hours, minutes, and seconds.
hours, rem = divmod(run_time, 3600)
minutes, seconds = divmod(rem, 60)

print("#####################################################################")
print("!!!!!!!!!!!!!!!!         PES2MP Finished        !!!!!!!!!!!!!!!!!!!!!")
print("#####################################################################")
print("Run time: {} hours, {} minutes, {:.2f} seconds".format(int(hours), int(minutes), seconds))
print("#####################################################################")

print("\n\n\n")

f.write("\n#####################################################################")
f.write("\n#####################    PES2MP Finished     ########################")
f.write("\n#####################################################################")
f.write("\nRun time: {} hours, {} minutes, {:.2f} seconds".format(int(hours), int(minutes), seconds))
f.write("\n#####################################################################")

f.write("\n\n\n")

f.close()


