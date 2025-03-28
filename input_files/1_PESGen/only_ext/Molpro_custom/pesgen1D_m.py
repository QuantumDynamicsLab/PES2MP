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
Create_MOLPRO_custom_input_files   = True      # Custom MOLPRO input
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
#------------    If Create_MOLPRO_custom_input_files == True)   ---------------#
#------------------------------------------------------------------------------#
# For molpro, total memory is needed to be calculated manually
#       Simple approximation = memory * 8 * number of processor

#    Where 1 g = 1 GigaWords = approx. 8 GB per processor
#    Therefore, total memory = 1g * 8 (words to GB) * 4 (procs) = ~ 32GB
# Processors can be defined while executing Molpro e.g. "molpro -n 4 $filename"
#------------------------------------------------------------------------------#
mem_m      = '1 g'                    # memory per thread/processor (in words)
#------------------------------------------------------------------------------#
# IMPORTANT : Since python string input treats {} as internal command, make sure
# to use double brackets {{commands}} in place of single {commands}.

# Python converts double curly brackets into single bracket
#------------------------------------------------------------------------------#
molpro_ext = """

! Edit below lines for MRCI/SAPT/other coordinate dependent calculations
! Custom files will print memory, xyz coordinates
! R, theta variables will also be printed for table

basis = AVQZ

{{RHF}}                 ! Use wf card if needed! e.g. {{hf;wf,xx,xx,xx;}}
{{Multi; STATE,3}}
{{MRCI; STATE,3}}       ! {{ci;occ,xx,xx,xx;wf,xx,xx,xx;}}

E1 = energy(1)
E2 = energy(2)
E3 = energy(3)

table,R,$E1,$E2,$E3
digits,2,10,10,10

"""

#------------------------------------------------------------------------------#
################################################################################
