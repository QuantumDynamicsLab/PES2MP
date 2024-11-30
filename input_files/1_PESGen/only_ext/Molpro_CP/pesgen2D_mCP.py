#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################  Global Options        ############################
Create_PES_input = True       # Set JOB Type(s) (True/False)
#------------------------------------------------------------------------------#
Proj_name        = 'H2_He' # Set a folder (Project) name
#------------------------------------------------------------------------------#
# Enter parameter for RR1 : Enter experimental/theoretical bond length(s)
RR1_atoms        = ['H','H'] # Enter rigid rotor (RR1) atoms from one end
RR1_bond_len     = [0.7414]  # Enter bond lengths from the same end (see manual)
# Enter parameter for second (collider) atom
RR2_atoms        = ['He']    # Enter collider atom
#------------------------------------------------------------------------------#
# Enter charge & multiplicity (Do NOT change order)
Charge           = [0, 0, 0] # charge of [atom 1, atom 2, whole system]
Multiplicity     = [1, 1, 1] # multiplicity of [atom 1, atom 2, whole system]
#------------------------------------------------------------------------------#
# create input files for external calculation of PES
Create_MOLPRO_CP_input_files      = True       # MOLPRO(CP)
#------------------------------------------------------------------------------#
# Psi4 internal calculation
R_lim = [2,8]      # Enter R limit [start,end] in Angstroms(Rough PES!)
fmt   = 'pdf'      # Enter plot(s) format: pdf, eps, png, jpeg etc.
#--------------------  Use Isotope (Optional)  --------------------------------#
#Use_isotope = True # only for calculating isotopic dependent COM (PES is same)!
#RR1_isotope_mass = [0, 13.00335483507]     # Enter isotope mass  (0 = default)
#RR2_isotope_mass = [0]                     # Enter isotope mass  (0 = default)
#------------------------------------------------------------------------------#

################################################################################
################### Advanced PES/Plot Options  #################################
################################################################################

# Radial coordinates (enter as many range and step sizes as desired)
R_i   = [1.0,  6.0,  9.0, 15.0,  50.0] # initial R in Ang. (eg. 0.1 Ang.)
R_f   = [6.0,  9.0, 15.0, 25.1, 100.1] # final R - R_stp (eg 1.95 Ang.)
R_stp = [0.1,  0.2,  0.5,  1.0,  50.0] # step size for R_i-R_f
# Loops run from initial to penultimate value (eg. loop 2-6 goes till 5.9 Ang.)

# 2D Angular template [theta] (to includes the final value i.e. 90, use 91)
theta  = [0, 91, 30]    # python loop will run from 0 to 90 with step size of 30

#------------------------------------------------------------------------------#
#--------------    If Create_MOLPRO_CP_input_files == True)    ----------------#
#------------------------------------------------------------------------------#
# for molpro real memory = memory*8*num_proc
#           Example: 1 g = 8 GB per processor
# processors are defined externally (molpro -n 4 $filename) 4*8 = 32GB
#------------------------------------------------------------------------------#
mem_m      = '1 g'                    # memory per thread/processor (in words)
run_method = '''{{rhf;rccsd(t)}}'''   # molpro function to declare method
basis_cp   = 'AVQZ'                   # basis set for cp calculation

#------------------------------------------------------------------------------#
################################################################################