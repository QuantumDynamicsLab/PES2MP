#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################  Global Options        ############################
Create_PES_input = True       # Set JOB Type(s) (True/False)
#------------------------------------------------------------------------------#
Proj_name        = 'H_H' # Set a folder (Project) name
#------------------------------------------------------------------------------#
# Enter parameter for first atom
RR1_atoms        = ['H']      # Enter atom 1
# Enter parameter for second (collider) atom
RR2_atoms        = ['H']      # Enter atom 2
#------------------------------------------------------------------------------#
# Enter charge & multiplicity (Do NOT change order)
Charge           = [0, 0, 0]  # charge of [atom 1, atom 2, whole system]
Multiplicity     = [2, 2, 1]  # multiplicity of [atom 1, atom 2, whole system]
#------------------------------------------------------------------------------#
# create input files for external calculation of PES
Create_GAUSSIAN_input_files      = True      # option 1  = Gaussian(CP)
#------------------------------------------------------------------------------#
# Psi4 internal calculation
R_lim = [0,10]     # Enter R limit [start,end] in Angstroms(Rough PES!)
fmt   = 'pdf'      # Enter plot(s) format: pdf, eps, png, jpeg etc.
#--------------------  Use Isotope (Optional)  --------------------------------#
#Use_isotope = True # only for calculating isotopic dependent COM (PES is same)!
#RR1_isotope_mass = [1.0078]     # Enter isotope mass  (0 = default)
#RR2_isotope_mass = [0]          # Enter isotope mass  (0 = default)
#------------------------------------------------------------------------------#

################################################################################
################### Advanced PES/Plot Options  #################################
################################################################################

# Radial coordinates (enter as many range and step sizes as desired)
R_i   = [0.1,  2.0,  6.0,  9.0, 15.0,  50.0] # initial R in Ang. (eg. 0.1 Ang.)
R_f   = [2.0,  6.0,  9.0, 15.0, 25.1, 100.1] # final R - R_stp (eg 1.95 Ang.)
R_stp = [0.05, 0.1,  0.2,  0.5,  1.0,  50.0] # step size for R_i-R_f
# Loops run from initial to penultimate value (eg. loop 2-6 goes till 5.9 Ang.)

#------------------------------------------------------------------------------#
#---------------   If Create_GAUSSIAN_input_files == True)   ------------------#
#------------------------------------------------------------------------------#
proc_g = 4            # number of processors (% nprocshared)
mem_g  = '32GB'       # total memory (%mem)
chk_g  = Proj_name    # Checkpoint file (% chk)
                      # Using project name. Replace with string '' if needed!
# COMMAND LINE: Default Options : CCSD(T) / AVQZ with counterpoise correction
cmd_g  = '# CCSD=(T,SaveAmplitudes,ReadAmplitudes)/aug-cc-pVQZ Counterpoise=2'

#------------------------------------------------------------------------------#
################################################################################
