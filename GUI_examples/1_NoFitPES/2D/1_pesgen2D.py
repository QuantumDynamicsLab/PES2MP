#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#-------------------------    Important Options     ---------------------------#
################################################################################
#------------------------------------------------------------------------------#
# Enter parameter for RR1 : Enter experimental/theoretical bond length(s) -----#
RR1_atoms        = ['C','C'] # Enter rigid rotor (RR1) atoms from one end
RR1_bond_len     = [1.2425]  # Enter bond lengths from the same end (see manual)
# Enter parameter for second (collider) atom ----------------------------------#
RR2_atoms        = ['He']    # Enter collider atom
#------------------------------------------------------------------------------#
# Enter charge & multiplicity (Do NOT change order) ---------------------------#
Charge           = [0, 0, 0] # charge of [atom 1, atom 2, whole system]
Multiplicity     = [1, 1, 1] # multiplicity of [atom 1, atom 2, whole system]
#------------------------------------------------------------------------------#
# Psi4 parameters (memory, processor, method, basis etc.) ---------------------#
psi4_mem           = '4 GB'             # total memory
psi4_proc          = 1                  # number of processors(doesn't scale)
psi4_reference     = 'rhf'              # Reference WF: rhf/uhf/rohf

# C2_He_D4CBS
psi4_method_basis  = 'hf-d4/cc-pvdz'      # Method/Basis Set
# C2_He_SGS
#psi4_method_basis  = 'sherrill_gold_standard'      # Method/Basis Set

psi4_Frozen_Core   = True               # frozen core : True/False
psi4_bsse          = None               # counterpoise : 'cp' | None for cbs/sgs
#------------------------------------------------------------------------------#

################################################################################
#-----------------------    2D/4D Plot Options     ----------------------------#
################################################################################
# 2D Angular template [theta] (ab initio calculation) -------------------------#
# A loop from 0-91 means 0-90 in python ---------------------------------------#
theta  = [0, 91, 15]    # python loop will run from 0 to 90 with step size of 30
thetax = [0,15,30,45,60,75,90]   # Angles to be plotted (R vs E plot) 
#------------------------------------------------------------------------------#



################################################################################
################################################################################
#----------      Codes that probably don't need changes         ---------------#
################################################################################
################################################################################
#------------------------------------------------------------------------------#
# some necessary pieces of code for running job and grabbing project name -----#
Create_PES_input = True       # Set JOB Type(s) (True/False)
#------------------------------------------------------------------------------#
import os        # Gettig project name from GUI interface ---------------------#
Proj_name        =  os.getenv("Proj_name", "default_project_name") # Auto-set
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#---------------------- Advanced PES/Plot Options  ----------------------------#
#------------------------------------------------------------------------------#
# Radial coordinates (enter as many range and step sizes as desired) ----------#
R_i   = [2.5,  6.0,  9.0, 15.0,  50.0] # initial R in Ang. (eg. 0.1 Ang.)
R_f   = [6.0,  9.0, 15.0, 25.1, 100.1] # final R - R_stp (eg 1.95 Ang.)
R_stp = [0.1,  0.2,  0.5,  1.0,  50.0] # step size for R_i-R_f
# Loops run from initial to penultimate value (eg. loop 2-6 goes till 5.9 Ang.)#
#------------------------------------------------------------------------------#
#--------------------  Use Isotope (Optional)  --------------------------------#
#Use_isotope = True # only for calculating isotopic dependent COM (PES is same)!
#RR1_isotope_mass = [0, 13.00335483507]     # Enter isotope mass  (0 = default)
#RR2_isotope_mass = [0]                     # Enter isotope mass  (0 = default)
#------------------------------------------------------------------------------#
# Psi4 internal calculation (Plot Options R range and format) -----------------#
R_lim = [3,8]      # Enter R limit [start,end] in Angstroms(Rough PES!)
fmt   = 'pdf'      # Enter plot(s) format: pdf, eps, png, jpeg etc.
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#---------------           If Run_psi4 == True               ------------------#
#------------------------------------------------------------------------------#
# create rough PES internally (Set parameters below) --------------------------#
Run_psi4                         = True      # run internal rough calculation?
#------------------------------------------------------------------------------#
# Use for rough estimation : default parameters (scf (hf) and cc-pvdz basis) --#
# The program will run calculations and plot PES(s) in cm-1. ------------------#
# Enter coordinate(s) to calculate energy at infinity (convert energies to cm-1)
R_inf              = 200                # R @ infinity = 200 Angstrom
theta_2D_inf       = 90                 # Angular Coordinate for E_infinity
PES_filename       = "psi4_PES.dat"     # PES output file (in Hartree)
PES_filename_cm    = "psi4_PES_cm.dat"  # PES output file (in cm-1)
#------------------------------------------------------------------------------#
################################################################################
################################################################################
