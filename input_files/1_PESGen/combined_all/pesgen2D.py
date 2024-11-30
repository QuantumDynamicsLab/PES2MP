#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:28:43 2023
@author: Apoorv Kushwaha, Pooja Chahal, Habit Tatin & Dr. T. J. Dhilip Kumar

This is main input for Creating PES input files using Gaussian, Molpro or PySCF
It automatically creates PES input files for 2D i.e. rigid rotor-atom collision.

RR_atoms can have any number of atoms: E.g.

RR_atoms      Mg------C---C-----C---C-----C--H    ['Mg','C','O','N','P','S','H']
RR_bond_len      1.8   1.0  1.2  1.0  1.5  0.8    [1.8, 1.0, 1.2, 1.1, 1.5, 0.8]

Enter colliding atom   =>  ['He']
Enter charge and multiplicity as mentioned in comments => [0,0,0] and [1,1,1]
"""

############################  Global Options        ############################
Create_PES_input = True       # Set JOB Type(s) (True/False)
#------------------------------------------------------------------------------#
Proj_name        = 'pesgen2D' # Set a folder (Project) name
#------------------------------------------------------------------------------#
# Enter parameter for RR1 : Enter experimental/theoretical bond length(s)
RR1_atoms        = ['H','H']  # Enter rigid rotor (RR1) atoms from one end
RR1_bond_len     = [0.7414]   # Enter bond lengths from the same end (see above)
# Enter parameter for second (collider) atom
RR2_atoms        = ['He']     # Enter collider atom
#------------------------------------------------------------------------------#
# Enter charge & multiplicity (Do NOT change order)
Charge           = [0, 0, 0]  # charge of [atom 1, atom 2, whole system]
Multiplicity     = [1, 1, 1]  # multiplicity of [atom 1, atom 2, whole system]
#------------------------------------------------------------------------------#
# create rough (hf/cc-pvdz) PES internally (Set parameters below)
Run_psi4                         = False      # run internal rough calculation?
# create input files for external calculation of PES
Create_GAUSSIAN_input_files      = True      # option 1  = Gaussian(CP)
Create_MOLPRO_CP_input_files     = True      # option 2  = MOLPRO(CP)
Create_MOLPRO_CBS_input_files    = True      # option 3  = MOLPRO(CBS)
Create_MOLPRO_custom_input_files = True      # option 4  = Custom MOLPRO input
Create_Psi4_custom_input_files   = True      # option 5  = Custom Psi4 input
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
#---------------           If Run_psi4 == True               ------------------#
#------------------------------------------------------------------------------#
# Use for rough estimation : default parameters (scf (hf) and cc-pvdz basis)
# The program will run calculations and plot PES(s) in cm-1.
psi4_mem           = '4 GB'             # total memory
psi4_proc          = 1                  # number of processors(doesn't scale)
psi4_reference     = 'rhf'              # Reference WF: rhf/uhf/rohf
psi4_method_basis  = 'scf/cc-pvdz'      # Method/Basis Set
psi4_Frozen_Core   = True               # frozen core : True/False
psi4_bsse          = None               # counterpoise : 'cp'
# Enter coordinate(s) to calculate energy at infinity (convert energies to cm-1)
R_inf              = 200                # R @ infinity = 200 Angstrom
theta_2D_inf       = 90                 # Angular Coordinate for E_infinity
PES_filename       = "psi4_PES.dat"     # PES output file (in Hartree)
PES_filename_cm    = "psi4_PES_cm.dat"  # PES output file (in cm-1)
thetax             = [0,30,60,90]       # Angles to be plotted (R vs E plot)
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
#--------------    If Create_MOLPRO_*_input_files == True)   ------------------#
#------------------------------------------------------------------------------#
# for molpro real memory = memory*8*num_proc
#           Example: 1 g = 8 GB per processor
# processors are defined externally (molpro -n 4 $filename) 4*8 = 32GB

#------------------------------------------------------------------------------#
# GENERAL OPTIONS
#------------------------------------------------------------------------------#
mem_m      = '1 g'                    # memory per thread/processor (in words)
run_method = '''{{rhf;rccsd(t)}}'''   # molpro function to declare method

#------------------------------------------------------------------------------#
# MOLPRO_CP (counterpoise correced)
#------------------------------------------------------------------------------#
basis_cp   = 'AVQZ'                   # basis set for cp calculation

#------------------------------------------------------------------------------#
# MOLPRO_CBS (complete basis set limit)
#------------------------------------------------------------------------------#
basis_ref = 'avdz'    # reference basis - NOT included in CBS extrapolation
                      # 'avdz' : better convergence | change to 'avtz' if needed
basis_cbs  = ['avtz','avqz','av5z']  # basis set for cbs calculation (only 3)
                                     # USES EX1 and L3 (npc=2) extrapolation

#------------------------------------------------------------------------------#
# MOLPRO_custom (custom input file)
#------------------------------------------------------------------------------#
# IMPORTANT : Since python string input treats {} as internal command, make sure
# to use double brackets {{commands}} in place of single {commands}.

# Python converts double curly brackets into single bracket

molpro_ext = """

! Edit below lines for MRCI/SAPT/other coordinate dependent calculations
! Replace with advanced commands like         {{hf;wf,xx,xx,xx;}}
!                                             {{ci;occ,xx,xx,xx;wf,xx,xx,xx;}}
! if needed. Provided below is a simple example!

basis = AVQZ

{{RHF}}
{{Multi; STATE,3}}
{{MRCI; STATE,3}}

E1 = energy(1)
E2 = energy(2)
E3 = energy(3)

table,$R, $Theta $E1,$E1,$E3
digits,2,2,10,10,10

"""

#------------------------------------------------------------------------------#
#------------    If Create_Psi4_custom_input_files == True)   -----------------#
#------------------------------------------------------------------------------#
# See templates for more examples

psi4_bsse          = 'cp'      # counterpoise : 'cp' or None (update same below)

psi4_ext = """

memory 2 GB
set_num_threads(16)

set basis cc-pvdz
set reference rhf
# For psi4_bsse = None use | En = energy('scf')
En = energy('scf', bsse_type='cp',return_total_data=True)

# Clean Table
print('%.4f\t%.4f\t%.12f'%(R, Theta, En))

"""
#------------------------------------------------------------------------------#
################################################################################
