#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################  Global Options        ############################
Create_PES_input = True       # Set JOB Type(s) (True/False)
#------------------------------------------------------------------------------#
Proj_name        = 'H2_H2' # Set a folder (Project) name
#------------------------------------------------------------------------------#
# Enter parameter for RR1 : Enter experimental/theoretical bond length(s)
RR1_atoms        = ['H','H'] # Enter rigid rotor (RR1) atoms from one end
RR1_bond_len     = [0.7414]  # Enter bond lengths from the same end (see manual)
# Enter parameter for second (collider) atom
RR2_atoms        = ['H','H']  # Enter atom(s) for RR2
RR2_bond_len     = [0.7414]   # Enter bond lengths from the same end for RR2
#------------------------------------------------------------------------------#
# Enter charge & multiplicity (Do NOT change order)
Charge           = [0, 0, 0]  # charge of [atom 1, atom 2, whole system]
Multiplicity     = [1, 1, 1]  # multiplicity of [atom 1, atom 2, whole system]
#------------------------------------------------------------------------------#
# create input files for external calculation of PES
Create_MOLPRO_CBS_input_files      = True      # MOLPRO(CBS)
#------------------------------------------------------------------------------#
# Psi4 internal calculation
R_lim = [2,8]      # Enter R limit [start,end] in Angstroms(Rough PES!)
fmt   = 'pdf'      # Enter plot(s) format: pdf, eps, png, jpeg etc.
#--------------------  Use Isotope (Optional)  --------------------------------#
#Use_isotope = True # only for calculating isotopic dependent COM (PES is same)!
#RR1_isotope_mass = [0, 13.00335483507]     # Enter isotope mass  (0 = default)
#RR2_isotope_mass = [0,  3.0160492779 ]     # Enter isotope mass  (0 = default)
#------------------------------------------------------------------------------#


################################################################################
################### Advanced PES/Plot Options  #################################
################################################################################

# Radial coordinates (enter as many range and step sizes as desired)
R_i   = [1.0,  6.0,  9.0, 15.0,  50.0] # initial R in Ang. (eg. 0.1 Ang.)
R_f   = [6.0,  9.0, 15.0, 25.1, 100.1] # final R - R_stp (eg 1.95 Ang.)
R_stp = [0.1,  0.2,  0.5,  1.0,  50.0] # step size for R_i-R_f
# Loops run from initial to penultimate value (eg. loop 2-6 goes till 5.9 Ang.)

# 4D angular [phi, theta2, theta1]  coordinates
phi    = [0,  91, 30]    # phi    0 to 90 with step size of 30
theta2 = [0,  91, 30]    # theta2 0 to 90 with step size of 30
theta1 = [0, 181, 60]    # theta1 0 to 90 with step size of 30

#------------------------------------------------------------------------------#
#--------------    If Create_MOLPRO_CBS_input_files == True)   ----------------#
#------------------------------------------------------------------------------#
# for molpro real memory = memory*8*num_proc
#           Example: 1 g = 8 GB per processor
# processors are defined externally (molpro -n 4 $filename) 4*8 = 32GB
#------------------------------------------------------------------------------#
mem_m      = '1 g'                    # memory per thread/processor (in words)
run_method = '''{{rhf;rccsd(t)}}'''   # molpro function to declare method
basis_ref = 'avdz'                    # reference basis - NOT included in CBS
                                      # sometimes needed for better convergence
basis_cbs  = ['avtz','avqz','av5z']  # basis set for cbs calculation (only 3)
                                     # USES EX1 and L3 (npc=2) extrapolation
#------------------------------------------------------------------------------#
################################################################################
