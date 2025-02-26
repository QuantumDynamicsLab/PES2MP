#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#-------------------------    Important Options     ---------------------------#
################################################################################
#------------------------------------------------------------------------------#
# Enter parameter for first atom ----------------------------------------------#
RR1_atoms        = ['F']      # Enter atom 1
# Enter parameter for second (collider) atom ----------------------------------#
RR2_atoms        = ['He']      # Enter atom 2
#------------------------------------------------------------------------------#
# Enter charge & multiplicity (Do NOT change order) ---------------------------#
Charge           = [-1,  0, -1]  # charge of [atom 1, atom 2, whole system]
Multiplicity     = [ 1,  1,  1]  # multiplicity of [atom 1, atom 2, whole system]
#------------------------------------------------------------------------------#
# Psi4 parameters (memory, processor, method, basis etc.) ---------------------#
psi4_mem           = '4 GB'             # total memory
psi4_proc          = 1                  # number of processors(doesn't scale)
psi4_reference     = 'rhf'              # Reference WF: rhf/uhf/rohf
#psi4_method_basis  = 'hf-d4/cc-pvdz'      # Method/Basis Set
psi4_method_basis  = 'sherrill_gold_standard'      # Method/Basis Set
psi4_Frozen_Core   = True               # frozen core : True/False
psi4_bsse          = None               # counterpoise : 'cp'/None
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
#---------------------- Advanced PES/Plot Options  ----------------------------#
#------------------------------------------------------------------------------#
# Radial coordinates (enter as many range and step sizes as desired) ----------#
R_i   = [1,    2.0,  6.0,  9.0, 15.0,  50.0] # initial R in Ang. (eg. 0.1 Ang.)
R_f   = [2.0,  6.0,  9.0, 15.0, 25.1, 100.1] # final R - R_stp (eg 1.95 Ang.)
R_stp = [0.1,  0.05,  0.2,  0.5,  1.0,  50.0] # step size for R_i-R_f
# Loops run from initial to penultimate value (eg. loop 2-6 goes till 5.9 Ang.)#
#------------------------------------------------------------------------------#
#--------------------  Use Isotope (Optional)  --------------------------------#
#Use_isotope = True # only for calculating isotopic dependent COM (PES is same)!
#RR1_isotope_mass = [1.0078]     # Enter isotope mass  (0 = default)
#RR2_isotope_mass = [0]          # Enter isotope mass  (0 = default)
#------------------------------------------------------------------------------#
# Psi4 internal calculation (Plot Options R range and format) -----------------#
R_lim = [0,10]     # Enter R limit [start,end] in Angstroms(Rough PES!)
fmt   = 'pdf'      # Enter plot(s) format: pdf, eps, png, jpeg etc.
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#---------------           If Run_psi4 == True               ------------------#
#------------------------------------------------------------------------------#
# create rough (hf/cc-pvdz) PES internally (Set parameters below) -------------#
Run_psi4                         = True      # run internal rough calculation?
#------------------------------------------------------------------------------#
# Use for rough estimation : default parameters (scf (hf) and cc-pvdz basis) --#
# The program will run calculations and plot PES(s) in cm-1. ------------------#
# Enter coordinate(s) to calculate energy at infinity (convert energies to cm-1)
R_inf              = 200                # R = 200 Angstrom
PES_filename       = "psi4_PES.dat"     # PES output file (in Hartree)
PES_filename_cm    = "psi4_PES_cm.dat"  # PES output file (in cm-1)
#------------------------------------------------------------------------------#
################################################################################
################################################################################
