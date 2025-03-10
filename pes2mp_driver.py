#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:28:43 2023

@author: Apoorv Kushwaha, Pooja Chahal, Habit Tatin & Prof. T. J. Dhilip Kumar

This is the driver file for PES2MP containing most of the functions.
The changes to PES tamplate can be done directly here.

"""
###############################################################################
#--------------------------- Input Sanity Check! -----------------------------#
###############################################################################
#-----------------------------------------------------------------------------#
def exit_program():
    import sys
    print("\n Error in input file. Exiting the program...")
    sys.exit(0)

def lenerr(var, lenx):
    print("\n List Size Error! length of {} must be {}".format(var, lenx))
    exit_program()

def varerr(inp, var):
    try:
        var
    except NameError:
        print("\n variable not found! ")
        print("\n Provide {} in {}.py".format(var, inp))
        exit_program()
    else:
        pass
#-----------------------------------------------------------------------------#
def PES_handler(inp,coll_typ):
    print('\n Checking input file parameters! \n ')

    if len (inp.Charge) !=3:
        print("\n Invalid Charge list")
        lenerr('Charge', 3)
    if len (inp.Multiplicity) !=3:
        print("\n Multiplicity Charge list")
        lenerr('Multiplicity', 3)

    print("Checking Radial coordinates (R_i, R_f & R_stp) ")
    varerr(inp, inp.R_i)
    varerr(inp, inp.R_f)
    varerr(inp, inp.R_stp)
    if (inp.R_i != inp.R_i != inp.R_i):
        print("Inconsistent length of R_i, R_f, R_stp. \n Lists must be of equal length. ")
    else:
        print("Passed! Radial coordinates")

    try:
        inp.Use_isotope
    except:
        print('Not using Isotopes for COM')
    else:
        #if len(inp.RR1_isotope_G) != len(inp.RR1_atoms):
        #    lenerr('RR1_isotope_G', 'equal to RR1_atoms')
        #if len(inp.RR2_isotope_G) != len(inp.RR2_atoms):
        #    lenerr('RR2_isotope_G', 'equal to RR2_atoms')
        if len(inp.RR1_isotope_mass) != len(inp.RR1_atoms):
            lenerr('RR1_isotope_mass', 'equal to RR1_atoms')
        if len(inp.RR2_isotope_mass) != len(inp.RR2_atoms):
            lenerr('RR2_isotope_mass', 'equal to RR2_atoms')
        else:
            print("\n List length of isotopes passed!: ")


    if coll_typ == 1:
        print("\n Requred parameters for 1D collision --> Passed! ")

    elif (coll_typ == 2):
        varerr(inp, inp.theta)
        varerr(inp, inp.RR1_bond_len)

        if len(inp.theta) != 3:
            print("Invalid angular coordinates for collision type")
            lenerr('theta', 3)

        if len(inp.RR1_bond_len) != (len(inp.RR1_atoms)-1):
            print("Invalid RR1_bond_length")
            lenerr('RR1_bond_length', 'equal to RR1_atoms - 1 ')

            print("\n Requred parameters for 2D collision --> Passed! ")
    elif(coll_typ == 4):
        varerr(inp, inp.phi)
        varerr(inp, inp.theta2)
        varerr(inp, inp.theta1)
        varerr(inp, inp.RR1_bond_len)
        varerr(inp, inp.RR2_bond_len)

        if len(inp.phi) != 3:
            print("Invalid angular coordinates for collision type")
            lenerr('phi', 3)

        if len(inp.theta2) != 3:
            print("Invalid angular coordinates for collision type")
            lenerr('theta2', 3)

        if len(inp.theta1) != 3:
            print("Invalid angular coordinates for collision type")
            lenerr('theta1', 3)

        if len(inp.RR1_bond_len) != (len(inp.RR1_atoms)-1):
            print("Invalid RR1_bond_length")
            lenerr('RR1_bond_length', 'equal to RR1_atoms - 1 ')


        if len(inp.RR2_bond_len) != (len(inp.RR2_atoms)-1):
            print("Invalid RR2_bond_length")
            lenerr('RR2_bond_length', 'equal to RR2_atoms - 1 ')
        print("\n Requred parameters for 4D collision --> Passed! ")
    else :
        print("Unrecognised collision type                    ↓     ")
        print("Check PES2MP.py --> driver.file_handler(args*, x) !! ")
###############################################################################

def delete_files_in_directory(directory_path):
   import os
   import glob
   try:
     files = glob.glob(os.path.join(directory_path, '*'))
     for file in files:
       if os.path.isfile(file):
         os.remove(file)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

###############################################################################
#------------------------- Get COM for Rigid Rotor! --------------------------#
###############################################################################
def RR_com(f,RR_atoms, RR_bond_len,Charge, Multiplicity,RR_isotope_mass):
    import psi4

    # Creating rigid rotor (RR) coordinates below
    RR_geom_x = RR_goem_iso(RR_atoms, RR_bond_len, RR_isotope_mass)

    print("\n\nOriginal Geometry without charge and multiplicity!\n")
    print('-x'*30)
    print(RR_geom_x)

    f.write("\n\n Original Geometry without charge and multiplicity!\n")
    f.write('-x'*30)
    f.write(str(RR_geom_x))
    f.write('-x'*30)
    f.write('\n')
    RR_psi4 = psi4.geometry(RR_geom_x.format(Charge,Multiplicity))  # passing geometry in Psi4
    psi4.core.Molecule.move_to_com(RR_psi4)                 # moving RR to COM
    print('-x'*30)
    print("\n\n Geometry after moving molecule to COM \n")
    molvec = psi4.core.Molecule.save_string_xyz(RR_psi4)    # printing new coorddinates
    print(molvec)  # printing molecule after moving to com
    print('-x'*30)
    print("\n The estimated rotational constant [x y z]  by Psi4 in cm-1 : \n")
    rtvec = psi4.core.Molecule.rotational_constants(RR_psi4)
    print(str(rtvec.to_array()))  # printing rotational constant (estimate)


    f.write("\n\n Geometry after moving molecule to COM \n")
    f.write('-x'*30)
    f.write(str(psi4.core.Molecule.save_string_xyz(RR_psi4)))   # saving new coorddinates
    f.write('-x'*30)
    f.write("\n The estimated rotational constant  [x y z]  by Psi4 in cm-1 : \n")
    f.write(str(rtvec.to_array()))  # printing rotational constant (estimate)


    RR_COM_len = RR_com_extract(RR_psi4)

    print('\nExtracted COM coordinates : \n ')
    print(RR_atoms)
    print(RR_COM_len)
    f.write('\nExtracted COM coordinates for RR : \n ')
    f.write(str(RR_atoms)+'\n')
    f.write(str(RR_COM_len)+'\n')

    return RR_psi4, RR_COM_len

#-----------------------------------------------------------------------------#
def RR_goem_iso(RR_atoms, RR_bond_len, RR_isotope_mass):
    if RR_isotope_mass[0] == 0 :
        RR_geom_x = """
        {{}} {{}}
        {}         0.000000        0.000000        0.000000
        """.format(RR_atoms[0])
    else:
        RR_geom_x = """
        {{}} {{}}
        {}@{}         0.000000        0.000000        0.000000
        """.format(RR_atoms[0], RR_isotope_mass[0])

    R_tot = 0.000000
    for i in range (len(RR_bond_len)):
        R_tot    += RR_bond_len[i]
        if RR_isotope_mass[i+1] == 0 :
            RR_geom_x += '''{}         0.000000        0.000000         {}\n'''.format(RR_atoms[i+1],R_tot)
        else:
            RR_geom_x += '''{}@{}         0.000000        0.000000         {}\n'''.format(RR_atoms[i+1],
                                                                                      RR_isotope_mass[i+1],
                                                                                      R_tot)
    return RR_geom_x

#-----------------------------------------------------------------------------#
# extract coordinates after moving molecule to COM
def RR_com_extract(RR_psi4):
    import psi4
    RR_COM_str = psi4.core.Molecule.save_string_xyz(RR_psi4)                    # convert psi4 input to string
    pattern = ''.join((x if x in '0123456789.-' else ' ') for x in RR_COM_str)  # pattern to extract all numbers in string
    rr_all_num = [float(i) for i in pattern.split()]                            # split numbers into list
    RR_COM_len = rr_all_num[4::3]                                               # [start: end : step] drops unnecessary terms
    return RR_COM_len
###############################################################################

###############################################################################
#-------------------- Get 2D and 4D projected Coordinates! -------------------#
###############################################################################
#-----------------------------------------------------------------------------#
def proj2D (R, gamma):
    from math import sin, cos, radians

    # Rigid rotor (RR) lies on Z axis (no rotation of RR : no projection)
    R_x = sin(radians(gamma))*R                   # projection of He on X axis
    R_z = cos(radians(gamma))*R                   # projection of He on Z axis
    return R_x, R_z
###############################################################################


#-----------------------------------------------------------------------------#
def proj4D (R, phi, theta2, theta1, RR1_COM_len, RR2_COM_len):
    from math import sin, cos, radians

    # Rigid rotor (RR) lies on Z axis (no rotation of RR : no projection)
    # 3D projection for RR1
    a1=sin(radians(theta1))*sin(radians(phi))           # projection on X axis
    a2=sin(radians(theta1))*cos(radians(phi))           # projection on Y axis
    a3=cos(radians(theta1))                             # projection on Z axis

    # 2D projection for RR2 (No Dihedral: No X axis projection)
    b1=sin(radians(theta2))                             # projection on Y axis
    b2=cos(radians(theta2))                             # projection on Z axis

    RR_mat = [0] * (len(RR1_COM_len)*3 + len(RR2_COM_len)*2)
    ct1=0
    for i in range (0,len(RR1_COM_len)):
        RR_mat[ct1]   = RR1_COM_len[i] * a1
        RR_mat[ct1+1] = RR1_COM_len[i] * a2
        RR_mat[ct1+2] = RR1_COM_len[i] * a3
        ct1+=3
    for i in range (0,len(RR2_COM_len)):
        RR_mat[ct1]   = RR2_COM_len[i]     *b1
        RR_mat[ct1+1] = R + RR2_COM_len[i] *b2
        ct1+=2
    return RR_mat
###############################################################################

###############################################################################
#---------------- Create Gaussian Input Files (CP corrected) -----------------#
###############################################################################
#-----------------------------------------------------------------------------#
def gaussian_auxcm(Charge,Multiplicity):
    FxD_geom_G = '{},{} {},{} {},{}\n'.format(Charge[2], Multiplicity[2], Charge[0],
                                             Multiplicity[0], Charge[1], Multiplicity[1])
    return FxD_geom_G

def gaussian_files_1D(f,Gaussian_input_template,RR1_atoms,RR2_atoms, Charge,Multiplicity,R,gaussian_data):
    from tqdm import tqdm
    # create 1D gaussian input Files (CP corrected)

    F1D_geom_G = Gaussian_input_template + '\n\nR = {:.4f}\n\n'
    F1D_geom_G += gaussian_auxcm(Charge, Multiplicity)
    F1D_geom_G += '''{}(Fragment=1)         0.000000        0.000000         0.000000\n'''.format(RR1_atoms[0])
    F1D_geom_G += '''{}(Fragment=2)         0.000000        0.000000         {{:.6f}}\n\n\n'''.format(RR2_atoms[0])
    for j in tqdm(range (len(R))):             # python loop to generate PES (using try and except to suppress error)
        R_ii     = R[j]                         # radial  coordinate
        inp_file = open(gaussian_data + '{:d}.gjf'.format(int(j)), "w")      # open input file
        inp_file.write(F1D_geom_G.format(R_ii, R_ii))                        # write string to file
        inp_file.close()                                                     # close file
    return F1D_geom_G
###############################################################################

#-----------------------------------------------------------------------------#
def gaussian_files_2D(f,Gaussian_input_template,RR1_atoms,RR2_atoms,
                      Charge,Multiplicity,R,gaussian_data,RR1_COM_len,A):

    from tqdm import tqdm
    # create 2D gaussian input Files
    F2D_geom_G = Gaussian_input_template + '\n\nR = {:.4f}, Theta={:.2f}\n\n'
    F2D_geom_G += gaussian_auxcm(Charge,Multiplicity)
    # appending gaussian template with RR atoms
    for i in range (len(RR1_COM_len)):
        F2D_geom_G += '''{}(Fragment=1)         0.000000        0.000000         {:.6f}\n'''.format(RR1_atoms[i],RR1_COM_len[i])
    # appending gaussian template with collider atom and two blank lines
    F2D_geom_G += '''{}(Fragment=2)        {{:.6f}}        0.000000         {{:.6f}}\n\n\n'''.format(RR2_atoms[0])

    for j in tqdm(range (len(A))):             # python loop to generate PES (using try and except to suppress error)
        R     = A[j,0]                         # radial  coordinate
        gamma = A[j,1]                         # angular coordinate
        R_x, R_z = proj2D (R, gamma)           # calling 2D projection function
        inp_file = open(gaussian_data + '{:d}.gjf'.format(int(j)), "w")      # open input file
        inp_file.write(F2D_geom_G.format(R, gamma, R_x, R_z))                # write string to file
        inp_file.close()                                                     # close file
    return F2D_geom_G
###############################################################################


#-----------------------------------------------------------------------------#
def gaussian_files_4D(f,Gaussian_input_template,RR1_atoms,RR2_atoms,
                      Charge,Multiplicity,R,gaussian_data,RR1_COM_len,RR2_COM_len,A):
    from tqdm import tqdm
    F4D_geom_G = Gaussian_input_template + '\n\nR = {:.4f}, Phi={:.2f}, Theta2={:.2f}, Theta1={:.2f}\n\n'
    F4D_geom_G += gaussian_auxcm(Charge,Multiplicity)

    # appending gaussian template with RR atoms
    for i in range (len(RR1_COM_len)):
        F4D_geom_G += '''{}(Fragment=1)         {{:.6f}}        {{:.6f}}         {{:.6f}}\n'''.format(RR1_atoms[i])
    # appending gaussian template with collider atom
    for i in range (len(RR2_COM_len)):
        F4D_geom_G += '''{}(Fragment=1)         0.000000        {{:.6f}}         {{:.6f}}\n'''.format(RR2_atoms[i])
    F4D_geom_G += '\n\n'
    for j in tqdm(range (len(A))):             # python loop to generate PES (using try and except to suppress error)
        R      = A[j,0]                        # radial  coordinate
        phi    = A[j,1]                        # angular coordinate phi
        theta2 = A[j,2]                        # angular coordinate theta2
        theta1 = A[j,3]                        # angular coordinate theta1
        RR_mat = proj4D (R, phi, theta2, theta1, RR1_COM_len, RR2_COM_len)   # calling 4D projection function
        inp_file = open(gaussian_data + '{:d}.gjf'.format(int(j)), "w")      # open input file
        inp_file.write(F4D_geom_G.format(R, phi, theta2, theta1, *RR_mat))   # write string to file
        inp_file.close()                                                     # close file

    return F4D_geom_G
###############################################################################

###############################################################################
#------------------ Create Molpro Input Files (CP corrected) -----------------#
###############################################################################
#-----------------------------------------------------------------------------#
def molpro_files_f1(Molpro_input_template):
    FxD_geom_M = Molpro_input_template + """
Angstrom
!****************************************************************
!                      Energy of Complex                        !
!****************************************************************

text, complex
geometry={{{{
""".format()
    return FxD_geom_M

#-----------------------------------------------------------------------------#
def molpro_files_CP_f2_1(Charge, Multiplicity):
    FxD_geom_M = """}}}}
set, charge={}, spin={}
run_method
E_complex = energy

!****************************************************************
!                Energy by ghosting other fragment              !
!****************************************************************
""".format(Charge[2],Multiplicity[2]-1)

    return FxD_geom_M

def molpro_files_CP_f2_2():
    FxD_geom_M = """
text, cp for RR{}
dummy, {}
set, charge={}, spin={}
run_method
E_RR{} = energy

!**************************************************************** """
    return FxD_geom_M


def molpro_files_CP_f2_3():
    FxD_geom_M = """
!                  Energy of fragments at Infinity              !
!****************************************************************

text, inf E for RR1
Angstrom
geometry={{{{
""".format()

    return FxD_geom_M
#-----------------------------------------------------------------------------#
def molpro_files_CP_f3(Charge, Multiplicity):
    FxD_geom_M = """}}}}
set, charge={}, spin={}
run_method
E_RR1_inf = energy

!****************************************************************

text, inf E for RR2
Angstrom
geometry={{{{
""".format(Charge[0],Multiplicity[0]-1)
    return FxD_geom_M
#-----------------------------------------------------------------------------#
def molpro_files_CP_f4(Charge, Multiplicity):
    FxD_geom_M = """}}}}
set, charge={}, spin={}
run_method
E_RR2_inf = energy

!****************************************************************
!****************************************************************

BSSE_RR1 = (E_RR1 - E_RR1_inf)         !BSSE for RR
BSSE_RR2 = (E_RR2 - E_RR2_inf)         !BSSE for Atom
bsse_tot = BSSE_RR1 + BSSE_RR2         !total BSSE
E_CP = E_complex - bsse_tot            !CP correced E
    """.format(Charge[1],Multiplicity[1]-1)         # Molpro multiplicity = 2*S not 2S+1

    return FxD_geom_M
#-----------------------------------------------------------------------------#

def molpro_files_CP_1D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_data):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    F1D_geom_M  = molpro_files_f1(Molpro_input_template)
    F1D_geom_M += '''{}         0.000000        0.000000         0.000000\n'''.format(RR1_atoms[0])
    F1D_geom_M += '''{}         0.000000        0.000000         {{:.6f}}\n'''.format(RR2_atoms[0])
    # appending molpro template for bsse for each (using dummy)
    F1D_geom_M += molpro_files_CP_f2_1(Charge, Multiplicity)

    dumm1 = molpro_files_CP_f2_2()
    F1D_geom_M += dumm1.format(1, RR2_atoms[0], Charge[0], Multiplicity[0]-1, 1)
    dumm2 = molpro_files_CP_f2_2()
    F1D_geom_M += dumm2.format(2, RR1_atoms[0], Charge[1], Multiplicity[1]-1, 2)
    F1D_geom_M += molpro_files_CP_f2_3()

    # appending molpro template for E_inf
    F1D_geom_M += '''{}         0.000000        0.000000         0.000000\n'''.format(RR1_atoms[0])
    F1D_geom_M += molpro_files_CP_f3(Charge, Multiplicity)
    F1D_geom_M += '''{}         0.000000        0.000000         {{:.6f}}\n'''.format(RR2_atoms[0])
    F1D_geom_M += molpro_files_CP_f4(Charge, Multiplicity)

    # table
    F1D_geom_M += """

R = {{:.4f}}

table,R,E_CP
digits, 4, 12
""".format()

    for j in tqdm(range (len(R))):             # python loop to generate PES (using try and except to suppress error)
        R_ii     = R[j]                         # radial  coordinate
        inp_file = open(molpro_data + '{:d}.inp'.format(int(j)), "w")             # open input file
        inp_file.write(F1D_geom_M.format(R_ii, R_ii, R_ii))                       # write string to file
        inp_file.close()                                                            # close file
    #print("\n Molpro files created! \n")
    return F1D_geom_M
#--------------------------------------------------------------------------------------#

def molpro_files_CP_2D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_data, RR1_COM_len, A):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    F2D_geom_M  = molpro_files_f1(Molpro_input_template)
    for i in range (len(RR1_COM_len)):
        F2D_geom_M += '''{}         0.000000        0.000000         {}\n'''.format(RR1_atoms[i], RR1_COM_len[i])
    F2D_geom_M += '''{}         {{:.6f}}       0.000000         {{:.6f}}\n'''.format(RR2_atoms[0])
    F2D_geom_M += molpro_files_CP_f2_1(Charge, Multiplicity)
    # appending molpro template for bsse for each (using dummy)
    dumm1 = molpro_files_CP_f2_2()
    F2D_geom_M += dumm1.format(1, RR2_atoms[0], Charge[0], Multiplicity[0]-1, 1)
    dumm2 = molpro_files_CP_f2_2()
    F2D_geom_M += dumm2.format(2, ', '.join(map(str, RR1_atoms)), Charge[1], Multiplicity[1]-1, 2)
    F2D_geom_M += molpro_files_CP_f2_3()

    # appending molpro template for E_inf
    for i in range (len(RR1_COM_len)):
        F2D_geom_M += '''{}         0.000000        0.000000         {:.6f}\n'''.format(RR1_atoms[i],RR1_COM_len[i])
    F2D_geom_M += molpro_files_CP_f3(Charge, Multiplicity)
    F2D_geom_M += '''{}         {{:.6f}}        0.000000         {{:.6f}}\n'''.format(RR2_atoms[0])
    F2D_geom_M += molpro_files_CP_f4(Charge, Multiplicity)

    # table
    F2D_geom_M += """

R = {{:.4f}}
Theta={{:.4f}}

table,R,Theta,E_CP
digits, 4, 4, 12
""".format()

    for j in tqdm(range (len(A))):             # python loop to generate PES (using try and except to suppress error)
        R     = A[j,0]                         # radial  coordinate
        gamma = A[j,1]                         # angular coordinate
        R_x, R_z = proj2D (R, gamma)           # calling 2D projection function
        inp_file = open(molpro_data + '{:d}.inp'.format(int(j)), "w")               # open input file
        inp_file.write(F2D_geom_M.format(R_x, R_z, R_x, R_z, R, gamma))             # write string to file
        inp_file.close()                                                            # close file
    #print("\n Molpro files created! \n")
    return F2D_geom_M

def molpro_files_CP_4D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_data, RR1_COM_len, RR2_COM_len, A):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    F4D_geom_M  = molpro_files_f1(Molpro_input_template)
    for i in range (len(RR1_COM_len)):
        F4D_geom_M += '''{}         {{:.6f}}        {{:.6f}}         {{:.6f}} \n'''.format(RR1_atoms[i])
    for i in range (len(RR2_COM_len)):
        F4D_geom_M += '''{}         0.000000        {{:.6f}}         {{:.6f}} \n'''.format(RR2_atoms[i])
    F4D_geom_M += molpro_files_CP_f2_1(Charge, Multiplicity)
    # appending molpro template for bsse for each (using dummy)
    dumm1 = molpro_files_CP_f2_2()
    F4D_geom_M += dumm1.format(1, ', '.join(map(str, RR2_atoms)), Charge[0], Multiplicity[0]-1, 1)
    dumm2 = molpro_files_CP_f2_2()
    F4D_geom_M += dumm2.format(2, ', '.join(map(str, RR1_atoms)), Charge[1], Multiplicity[1]-1, 2)
    F4D_geom_M += molpro_files_CP_f2_3()

    # appending molpro template for E_inf
    for i in range (len(RR1_COM_len)):
        F4D_geom_M += '''{}         {{:.6f}}        {{:.6f}}         {{:.6f}} \n'''.format(RR1_atoms[i])
    F4D_geom_M += molpro_files_CP_f3(Charge, Multiplicity)
    for i in range (len(RR2_COM_len)):
        F4D_geom_M += '''{}         0.000000         {{:.6f}}        {{:.6f}} \n'''.format(RR2_atoms[i])
    F4D_geom_M += molpro_files_CP_f4(Charge, Multiplicity)

    # table
    F4D_geom_M += """

R = {{:.4f}}
Phi={{:.4f}}
Theta2={{:.4f}}
Theta1={{:.4f}}

table,R,Phi,Theta2,Theta1,E_CP
digits, 4, 4, 4, 4, 12
""".format()

    for j in tqdm(range (len(A))):             # python loop to generate PES (using try and except to suppress error)
        R      = A[j,0]                        # radial  coordinate
        phi    = A[j,1]                        # angular coordinate phi
        theta2 = A[j,2]                        # angular coordinate theta2
        theta1 = A[j,3]                        # angular coordinate theta1
        RR_mat = proj4D (R, phi, theta2, theta1, RR1_COM_len, RR2_COM_len)   # calling 4D projection function
        inp_file = open(molpro_data + '{:d}.inp'.format(int(j)), "w")               # open input file
        inp_file.write(F4D_geom_M.format(*RR_mat, *RR_mat, R, phi, theta2, theta1 )) # write string to file
        inp_file.close()                                                            # close file
    #print("\n Molpro files created! \n")
    return F4D_geom_M
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

###############################################################################
#---------------- Create Molpro Input Files (CBS extrapolated) ---------------#
###############################################################################
#-----------------------------------------------------------------------------#
def molpro_files_CBS_f2(basis_ref, basis):
    F1D_geom_M_cbs = """
basis= {}
run_method
E_ref=energy
text,compute energies, extrapolate reference energy using EX1 and correlation energy using L3
extrapolate,basis={}:{}:{},method_c=l3,method_r=ex1,npc=2
{}=energy(1)
{}=energy(2)
{}=energy(3)
e_cbs=energy(4)
""".format(basis_ref,*basis,*basis)
    return F1D_geom_M_cbs
#-----------------------------------------------------------------------------#

def molpro_files_CBS_1D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_cbs_data,
                        basis_ref,basis):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    F1D_geom_M_cbs  = molpro_files_f1(Molpro_input_template)
    F1D_geom_M_cbs += '''{}         0.000000        0.000000         0.000000\n'''.format(RR1_atoms[0])
    F1D_geom_M_cbs += '''{}         0.000000        0.000000         {{:.6f}}\n'''.format(RR2_atoms[0])
    F1D_geom_M_cbs += """}}}}
set, charge={}, spin={}
""".format(Charge[2],Multiplicity[2]-1)
    F1D_geom_M_cbs += molpro_files_CBS_f2(basis_ref, basis)
    F1D_geom_M_cbs += """
!****************************************************************
R = {{:.4f}}

!****************************************************************
table,$R,${},${},${},$e_cbs
digits,2,10,10,10,10

""".format(*basis)

    for j in tqdm(range (len(R))):             # python loop to generate PES (using try and except to suppress error)
        R_ii     = R[j]                         # radial  coordinate
        inp_file = open(molpro_cbs_data + '{:d}.inp'.format(int(j)), "w")             # open input file
        inp_file.write(F1D_geom_M_cbs.format(R_ii, R_ii, R_ii))                       # write string to file
        inp_file.close()                                                            # close file
    #print("\n Molpro files created! \n")
    return F1D_geom_M_cbs

###############################################################################

#-----------------------------------------------------------------------------#
def molpro_files_CBS_2D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_cbs_data, RR1_COM_len,
                        A,basis_ref,basis):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    F2D_geom_M_cbs  = molpro_files_f1(Molpro_input_template)
    for i in range (len(RR1_COM_len)):
        F2D_geom_M_cbs += '''{}         0.000000        0.000000         {}\n'''.format(RR1_atoms[i],RR1_COM_len[i])
    F2D_geom_M_cbs += '''{}        {{:.6f}}        0.000000         {{:.6f}}\n'''.format(RR2_atoms[0])
    F2D_geom_M_cbs += """}}}}
set, charge={}, spin={}
""".format(Charge[2],Multiplicity[2]-1)
    F2D_geom_M_cbs += molpro_files_CBS_f2(basis_ref,basis)
    F2D_geom_M_cbs += """
!****************************************************************
R = {{:.4f}}
Theta={{:.4f}}

!****************************************************************
table,$R,$Theta,${},${},${},$e_cbs
digits,2,2,10,10,10,10

""".format(*basis)

    for j in tqdm(range (len(A))):             # python loop to generate PES (using try and except to suppress error)
        R     = A[j,0]                         # radial  coordinate
        gamma = A[j,1]                         # angular coordinate
        R_x, R_z = proj2D (R, gamma)           # calling 2D projection function
        inp_file = open(molpro_cbs_data + '{:d}.inp'.format(int(j)), "w")               # open input file
        inp_file.write(F2D_geom_M_cbs.format(R_x, R_z, R, gamma))             # write string to file
        inp_file.close()                                                            # close file
    #print("\n Molpro files created! \n")
    return F2D_geom_M_cbs
###############################################################################


#-----------------------------------------------------------------------------#
def molpro_files_CBS_4D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_cbs_data, RR1_COM_len,
                        RR2_COM_len, A, basis_ref, basis):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    F4D_geom_M_cbs  = molpro_files_f1(Molpro_input_template)
    for i in range (len(RR1_COM_len)):
        F4D_geom_M_cbs += '''{}         {{:.6f}}        {{:.6f}}         {{:.6f}}\n'''.format(RR1_atoms[i])
    for i in range (len(RR2_COM_len)):
        F4D_geom_M_cbs += '''{}         0.000000        {{:.6f}}         {{:.6f}}\n'''.format(RR2_atoms[i])
    F4D_geom_M_cbs += """}}}}
set, charge={}, spin={}
""".format(Charge[2],Multiplicity[2]-1)
    F4D_geom_M_cbs += molpro_files_CBS_f2(basis_ref,basis)
    F4D_geom_M_cbs += """
!****************************************************************
R = {{:.4f}}
Phi = {{:.4f}}
Theta2 = {{:.4f}}
Theta1 = {{:.4f}}

!****************************************************************
table,R,Phi,Theta2,Theta1,${},${},${},$e_cbs
digits,2,2,2,2,10,10,10,10

""".format(*basis)

    for j in tqdm(range (len(A))):             # python loop to generate PES (using try and except to suppress error)
        R      = A[j,0]                        # radial  coordinate
        phi    = A[j,1]                        # angular coordinate phi
        theta2 = A[j,2]                        # angular coordinate theta2
        theta1 = A[j,3]                        # angular coordinate theta1
        RR_mat = proj4D (R, phi, theta2, theta1, RR1_COM_len, RR2_COM_len)   # calling 4D projection function
        inp_file = open(molpro_cbs_data + '{:d}.inp'.format(int(j)), "w")           # open input file
        inp_file.write(F4D_geom_M_cbs.format(*RR_mat, R, phi, theta2, theta1 ))     # write string to file
        inp_file.close()                                                            # close file
    #print("\n Molpro files created! \n")
    return F4D_geom_M_cbs
#-----------------------------------------------------------------------------#
###############################################################################
#----------- Create Molpro Input Files (Custom for SAPT/MRCI etc.) -----------#
###############################################################################

def molpro_files_custom_1D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_ext_data,molpro_ext):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    F1D_geom_M_ext  = Molpro_input_template + '''
!****************************************************************
!                 Molpro custom calculations                    !
!****************************************************************
'''
    F1D_geom_M_ext += "R = {:.6f}"
    F1D_geom_M_ext += '''
Angstrom
geometry={{{{
'''.format()
    F1D_geom_M_ext += '''{}         0.000000        0.000000         0.000000\n'''.format(RR1_atoms[0])
    F1D_geom_M_ext += '''{}         0.000000        0.000000         R\n'''.format(RR2_atoms[0])
    F1D_geom_M_ext += """}}}}
set, charge={}, spin={}
""".format(Charge[2],Multiplicity[2]-1)
    F1D_geom_M_ext += molpro_ext
    for j in tqdm(range (len(R))):             # python loop to generate PES (using try and except to suppress error)
        R_ii     = R[j]                         # radial  coordinate
        inp_file = open(molpro_ext_data + '{:d}.inp'.format(int(j)), "w")  # open input file
        inp_file.write(F1D_geom_M_ext.format(R_ii,R_ii))                # write string to file
        inp_file.close()                                                 # close file
    #print("\n Molpro files created! \n")
    return F1D_geom_M_ext

###############################################################################

#-----------------------------------------------------------------------------#
def molpro_files_custom_2D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_ext_data,
                           RR1_COM_len, A, molpro_ext):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    print(Molpro_input_template)
    F2D_geom_M_ext  = Molpro_input_template + '''
!****************************************************************
!                 Molpro custom calculations                    !
!****************************************************************
'''
    print(F2D_geom_M_ext)
    for ii in range (len(RR1_COM_len)):                             # variables are declaired separately
        F2D_geom_M_ext += "R{} = {} \n".format(ii+1, RR1_COM_len[ii])
    F2D_geom_M_ext += "R{} = {{:.6f}} \nR{} = {{:.6f}} \n".format(ii+2, ii+3)
    F2D_geom_M_ext += '''
Angstrom
geometry={{{{
'''.format()

    for i in range (len(RR1_COM_len)):
        F2D_geom_M_ext += '''{}         0.000000        0.000000         R{}\n'''.format(RR1_atoms[i],i+1)

    F2D_geom_M_ext += '''{}        R{}              0.000000         R{}\n'''.format(RR2_atoms[0], i+2, i+3)
    F2D_geom_M_ext += """}}}}
set, charge={}, spin={}
""".format(Charge[2],Multiplicity[2]-1)
    F2D_geom_M_ext += '''
R = {:.4f}
Theta = {:.4f}
    '''
    F2D_geom_M_ext += molpro_ext

    for j in tqdm(range (len(A))):             # python loop to generate PES (using try and except to suppress error)
        R     = A[j,0]                         # radial  coordinate
        gamma = A[j,1]                         # angular coordinate
        R_x, R_z = proj2D (R, gamma)           # calling 2D projection function
        inp_file = open(molpro_ext_data + '{:d}.inp'.format(int(j)), "w")               # open input file
        inp_file.write(F2D_geom_M_ext.format(R_x, R_z, R, gamma))             # write string to file
        inp_file.close()                                                            # close file
    #print("\n Molpro files created! \n")
    return F2D_geom_M_ext
###############################################################################


#-----------------------------------------------------------------------------#
def molpro_files_custom_4D(f,Molpro_input_template,RR1_atoms,RR2_atoms,Charge,Multiplicity,R,molpro_ext_data,
                           RR1_COM_len, RR2_COM_len, A, molpro_ext):
    from tqdm import tqdm
    # appending molpro template for E_complex energy
    F4D_geom_M_ext  = Molpro_input_template + '''
!****************************************************************
!                 Molpro custom calculations                    !
!****************************************************************
'''
    for ii in range (len(RR1_COM_len)):                             # variables are declaired separately
        F4D_geom_M_ext += "R{} = {{:.6f}} \nR{} = {{:.6f}} \nR{} = {{:.6f}} \n".format(ii*3+1,ii*3+2,ii*3+3)
    for jj in range (len(RR2_COM_len)):                             # variables are declaired separately
        F4D_geom_M_ext += "R{} = {{:.6f}} \nR{} = {{:.6f}} \n".format((ii+1)*3+(jj*2)+1,(ii+1)*3+(jj*2)+2)

    F4D_geom_M_ext += '''
Angstrom
geometry={{{{
'''.format()

    for i in range (len(RR1_COM_len)):
        F4D_geom_M_ext += '''{}         R{}              R{}         R{}\n'''.format(RR1_atoms[i], i*3+1,i*3+2,i*3+3)
    for j in range (len(RR2_COM_len)):
        F4D_geom_M_ext += '''{}         0.000000        R{}         R{}\n'''.format(RR2_atoms[j],(i+1)*3+(j*2)+1,(i+1)*3+(j*2)+2)
    F4D_geom_M_ext += """}}}}
set, charge={}, spin={}
""".format(Charge[2],Multiplicity[2]-1)
    F4D_geom_M_ext += '''
R = {:.4f}
Phi = {:.4f}
Theta2 = {:.4f}
Theta1 = {:.4f}
    '''
    F4D_geom_M_ext += molpro_ext

    for j in tqdm(range (len(A))):             # python loop to generate PES (using try and except to suppress error)
        R      = A[j,0]                        # radial  coordinate
        phi    = A[j,1]                        # angular coordinate phi
        theta2 = A[j,2]                        # angular coordinate theta2
        theta1 = A[j,3]                        # angular coordinate theta1
        RR_mat = proj4D (R, phi, theta2, theta1, RR1_COM_len, RR2_COM_len)   # calling 4D projection function
        inp_file = open(molpro_ext_data + '{:d}.inp'.format(int(j)), "w")           # open input file
        inp_file.write(F4D_geom_M_ext.format(*RR_mat, R, phi, theta2, theta1 ))     # write string to file
        inp_file.close()                                                            # close file
    #print("\n Molpro files created! \n")
    return F4D_geom_M_ext

###############################################################################
#-------------------- Create Psi4 Input Files with coordinates ---------------#
###############################################################################

def psi4_input_1D(inp):
    F1D_geom = ''
    if inp.psi4_bsse == None:
        F1D_geom += " {} {} \n".format(inp.Charge[2],inp.Multiplicity[2])
        F1D_geom += '''{}         0.000000           0.000000        0.000000 \n'''.format(inp.RR1_atoms[0])
        F1D_geom += '''{}         0.000000           0.000000        {{:.6f}}\n'''.format(inp.RR2_atoms[0])
    else:
        F1D_geom += "{} {} \n-- \n".format(inp.Charge[2],inp.Multiplicity[2])
        F1D_geom += ' {} {} \n'.format(inp.Charge[0],inp.Multiplicity[0])
        F1D_geom += '''{}         0.000000           0.000000        0.000000 \n'''.format(inp.RR1_atoms[0])
        F1D_geom += "-- \n {} {} \n".format(inp.Charge[1],inp.Multiplicity[1])
        F1D_geom += '''{}         0.000000           0.000000        {{:.6f}}\n'''.format(inp.RR2_atoms[0])
    F1D_geom += "\n no_com \n no_reorient \n "

    return F1D_geom
#-----------------------------------------------------------------------------#

def psi4_input_2D(inp,RR1_psi4):
    import psi4
    F2D_geom = ''
    if inp.psi4_bsse == None:
        #F2D_geom += " {} {} \n".format(inp.Charge[2],inp.Multiplicity[2])
        RR1_psi4_xyz = psi4.core.Molecule.save_string_xyz(RR1_psi4)
        F2D_geom += RR1_psi4_xyz
        F2D_geom += '''{}         {{:.6f}}           0.000000        {{:.6f}}'''.format(inp.RR2_atoms[0])
    else:
        F2D_geom += "{} {} \n-- \n".format(inp.Charge[2],inp.Multiplicity[2])
        #F2D_geom += " {} {} \n".format(inp.Charge[0],inp.Multiplicity[0])
        RR1_psi4_xyz = psi4.core.Molecule.save_string_xyz(RR1_psi4)
        F2D_geom += RR1_psi4_xyz
        F2D_geom += "-- \n {} {} \n".format(inp.Charge[1],inp.Multiplicity[1])
        F2D_geom += '''{}         {{:.6f}}           0.000000        {{:.6f}}'''.format(inp.RR2_atoms[0])
    F2D_geom += "\n no_com \n no_reorient \n"
    return F2D_geom
#-----------------------------------------------------------------------------#

def psi4_input_4D(inp,RR1_COM_len,RR2_COM_len):
    F4D_geom = ''
    if inp.psi4_bsse == None:
        F4D_geom += " {} {} \n".format(inp.Charge[2],inp.Multiplicity[2])
        for i in range (len(RR1_COM_len)):
            F4D_geom += '''{}         {{:.6f}}        {{:.4f}}         {{:.6f}}\n'''.format(inp.RR1_atoms[i])
        for i in range (len(RR2_COM_len)):
            F4D_geom += '''{}         0.000000        {{:.6f}}         {{:.6f}}\n'''.format(inp.RR2_atoms[i])
    else:
        F4D_geom += "{} {} \n-- \n".format(inp.Charge[2],inp.Multiplicity[2])
        F4D_geom += " {} {} \n".format(inp.Charge[0],inp.Multiplicity[0])
        for i in range (len(RR1_COM_len)):
            F4D_geom += '''{}         {{:.6f}}        {{:.4f}}         {{:.6f}}\n'''.format(inp.RR1_atoms[i])
        F4D_geom += "-- \n {} {} \n".format(inp.Charge[1],inp.Multiplicity[1])
        for i in range (len(RR2_COM_len)):
            F4D_geom += '''{}         0.000000        {{:.6f}}         {{:.6f}}\n'''.format(inp.RR2_atoms[i])
    F4D_geom += "\n no_com \n no_reorient \n symmetry c1 \n"
    return F4D_geom
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

###############################################################################
#-------------------------------- Various Plots ------------------------------#
###############################################################################

def mirror(df_out1,header_keep,z1_3d):
    import pandas as pd
    max_theta = max(df_out1[header_keep].unique())
    if (max_theta == 90):
        print('Max angle is 90 mirroring to 180')
        z1_3d_mir90 = z1_3d.iloc[:,::-1]                                         # new df mirror
        z1_3d_mir90 = z1_3d_mir90.drop(90,axis=1)                                # dropping 90
        z1_3d_mir90.columns = list(map(lambda x: 180-x , z1_3d_mir90.columns))   # renaming columns (angles)
        lst = [z1_3d, z1_3d_mir90]                                               # List of two dataframes
        z1_3d = pd.concat(lst, axis =1)                                          # combining dataframes
        max_theta = 180

    if (max_theta == 180):
        print('Max angle is 180 mirroring to 360')
        z1_3d_mir180 = z1_3d.iloc[:,::-1]                                         # new df mirror
        z1_3d_mir180 = z1_3d_mir180.drop(180,axis=1)                              # dropping 180
        z1_3d_mir180.columns = list(map(lambda x: 360-x , z1_3d_mir180.columns))  # renaming columns (angles)
        #z1_3d_mir180 = z1_3d_mir180.drop(360,axis=1)                             # dropping 360
        lst = [z1_3d, z1_3d_mir180]                                               # List of two dataframes
        z1_3d = pd.concat(lst, axis =1)                                           # combining dataframes

    print("New dataframe till 360 degrees!")
    return z1_3d
###############################################################################


#-----------------------------------------------------------------------------#
def plot_4D_proj(df_out1, header_keep, header_drop1, header_drop1_val, header_drop2,
                 header_drop2_val, out_data_plots, out_plots, inp):
    import numpy as np
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 16})

    df_res = df_out1.loc[(df_out1[header_drop1]==header_drop1_val) &
                         (df_out1[header_drop2]==header_drop2_val)]
    df_res = df_res.drop([header_drop1, header_drop2], axis=1)
    df_res.reset_index(drop=True, inplace=True)
    df_res.to_csv(out_data_plots + "data_df_%s_%s_%d_%d.dat"
                  %(header_drop1,header_drop2, header_drop1_val,header_drop2_val),
                  index=None,columns =['R',header_keep,'E'],sep=',')

    z1_3d = df_res.pivot(index=df_res.columns[0], columns=df_res.columns[1],
                         values=df_res.columns[2])
    z1_3d.to_csv(out_data_plots + "data_mat_%s_%s_%d_%d.dat"
                 %(header_drop1,header_drop2, header_drop1_val,header_drop2_val),
                 header=True,sep='\t')

    z1_3d = mirror(df_res,header_keep,z1_3d)                         # mirroring to 360 degrees
    plt.figure(figsize=(20,8))                                       # plot size
    theta = np.radians(z1_3d.columns)                                # theta converted to radians
    r = df_res[df_out1.columns[0]].unique()                          # extracting R values
    try:
        inp.E_lim
        inp.E_stp
    except:
        min_E = int(min(z1_3d.min()))-1
        levels_min = np.arange(min_E,0,0.1)        # levels for energies minima
        levels_max = np.arange(0,-min_E+1,0.1)     # levels for energies maxima
    else:
        levels_min = np.arange(inp.E_lim[0],0,inp.E_stp)             # levels for energies minima
        levels_max = np.arange(0,inp.E_lim[1] + inp.E_stp,inp.E_stp) # levels for energies maxima

    levels = np.append(levels_min, levels_max)                       # combined levels
    ax = plt.axes(projection="polar")                                # polar plot initialization
    [X, Y] = np.meshgrid(theta, r)                                   # 2D mesh creation
    cp = plt.contourf(X, Y, z1_3d,levels,cmap='seismic', extend="both")  # contour plot
    cp.set_rasterized(True)

    plt.colorbar(cp, pad = 0.12)                                     # colorbar position
    ax.set_facecolor("maroon")                                       # set background color

    plt.grid(True,linestyle=':')                                     # grid on
    plt.minorticks_on()                                              # minor ticks are on
    
    #plt.title(r"Polar Plot of {} vs R at ({} = {} and {} = {})".format (header_keep,header_drop1,
    #                                                                   header_drop1_val, header_drop2,
    #                                                                   header_drop2_val)) # title of plot
    plt.title(f"Polar Plot ($\{header_keep}$, R) at ($\{header_drop1}$ = {header_drop1_val}\u00B0 and $\{header_drop2}$ = {header_drop2_val}\u00B0)", pad=30)

    try:
        inp.plt_x_axis
    except:
        print('No x lebel provided. Using Default!')
        plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
    else:
        plt.xlabel(inp.plt_x_axis)

    ax.xaxis.set_label_coords(1.07, 0.745)                           # position of label R

    plt.ylim(0,inp.R_lim[1])                                         # y limit
    #plt.xlim(0, 2*np.pi)                                            # x limit (not needed)

    plt.tight_layout()
    # Use polar_plot_%s_%s_%d_%d.eps and format='eps to save polar contour in eps format
    plt.savefig(out_plots+'polar_plot_%s_%s_%d_%d.'
                %(header_drop1,header_drop2,int(header_drop1_val),int(header_drop2_val)) + inp.fmt,
                format=inp.fmt,bbox_inches='tight')                  # save polar contour in pdf (tight layout)
    #plt.show()                                                      # preview for jupyter notebook only
    plt.close()
###############################################################################


#-----------------------------------------------------------------------------#
def plot_2D_proj(df_out1, z1_3d, out_data, out_plots, inp):
    import numpy as np
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(20,8))                            # figure size

    theta = np.radians(z1_3d.columns)                     # theta converted to radians
    r = df_out1[df_out1.columns[0]].unique()              # extracting R values

    try:
        inp.E_lim
        inp.E_stp
    except:
        min_E = int(min(z1_3d.min()))-1
        levels_min = np.arange(min_E,0,0.1)        # levels for energies minima
        levels_max = np.arange(0,-min_E+1,0.1)     # levels for energies maxima
    else:
        levels_min = np.arange(inp.E_lim[0],0,inp.E_stp)             # levels for energies minima
        levels_max = np.arange(0,inp.E_lim[1] + inp.E_stp,inp.E_stp) # levels for energies maxima

    levels = np.append(levels_min, levels_max)                       # combined levels
    #print('Energy levels are : ', levels)

    ax = plt.axes(projection="polar")                     # polar plot initialization
    [X, Y] = np.meshgrid(theta, r)                        # 2D mesh creation
    cp = plt.contourf(X, Y, z1_3d,levels,cmap='seismic', extend="both")     # contour plot
    cp.set_rasterized(True)

    plt.colorbar(cp, pad = 0.12)                           # colorbar position
    ax.set_facecolor("maroon")                             # set background color

    plt.grid(True,linestyle=':')                           # grid on
    plt.minorticks_on()                                    # minor ticks are on

    try:
        inp.plt_title
    except:
        print('No plot title provided!')
        plt.title(r"Polar Plot ($\theta$, R)", pad=30)                                       # title of plot
    else:
        plt.title(inp.plt_title)

    try:
        inp.plt_x_axis
    except:
        print('No x lebel provided. Using Default!')
        plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
    else:
        plt.xlabel(inp.plt_x_axis)

    ax.xaxis.set_label_coords(1.07, 0.745)                 # position of label R

    plt.ylim(0,inp.R_lim[1])                                                 # y limit
    #plt.xlim(0, 2*np.pi)                                  # x limit (not needed)
    plt.tight_layout()

    # plt.savefig(out_plots+'Polar_plot.eps', format='eps')  # save polar contour in eps
    plt.savefig(out_plots+'Polar_plot_2D.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save ploar plot in pdf

    #plt.show()                                            # preview off (use only for jupyter)
    plt.close()
###############################################################################


#-----------------------------------------------------------------------------#
def plot_1D (df_out1,z1_3d,out_plots, inp, x):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 15})
    plt.figure(figsize=(20,8))                             # figure size
    if x == 1:
        df_out1.plot(x=df_out1.columns[0],y=df_out1.columns[1])
    else:
        z1_3d.plot()                                       # plotting from dataframe
    plt.grid(True,linestyle=':')                           # grid on
    plt.minorticks_on()                                    # minor ticks are on

    try:
        inp.plt_title
    except:
        print('No plot title provided. Using Default!')
        plt.title("PES")                                       # title of plot
    else:
        plt.title(inp.plt_title)

    try:
        inp.plt_x_axis
    except:
        print('No x lebel provided. Using Default!')
        plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
    else:
        plt.xlabel(inp.plt_x_axis)

    try:
        inp.plt_y_axis
    except:
        print('No y lebel provided. Using Default!')
        plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
    else:
        plt.ylabel(inp.plt_y_axis)

    try:
        inp.legend_loc
    except:
        print('No legend location provided. Using Default!')
        legend_loc="lower right"             # legend location
    else:
        legend_loc=inp.legend_loc

    try:
        inp.ncol
    except:
        plt.legend(loc=legend_loc, prop={'size': 14})  # name and position of legend
    else:
        plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=inp.ncol,prop={'size': 12})  # name and position of legend

    try:
        inp.E_lim
    except:
        elim = df_out1[df_out1.columns[x]].min()
        e_lim = elim + (elim/10)
        plt.ylim(e_lim,-e_lim)                             # Fix upper/lower energy limit for plots (keep symmetric)
    else:
        plt.ylim(inp.E_lim[0],inp.E_lim[1])
    #l_lim = z1_3d[z1_3d.columns[0]].min()
    plt.xlim(inp.R_lim[0], inp.R_lim[1])                   # x limit
    # plt.savefig(out_plots+'Combined_ang_plots.eps', format='eps')  # save combined figure
    plt.savefig(out_plots+'R_plots_1D.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save combined figure
    plt.close()
###############################################################################

###############################################################################

###############################################################################
#----------------------------- TensorFlow Scaling ----------------------------#
###############################################################################

# function to scale Energy
def E_Scale(df, i):
    Scale_name = ['Ha.','mHa.','eV','kJ/mol','kcal/mol','cm⁻¹']
    Scales = [1,1000.0,27.211399,2625.5002,627.5096080,219474.63]
    print (" Energy Scaling Avaliable: 0: 'Ha.' 1: 'mHa.' 2: 'eV' 3: 'kJ/mol' 4: 'kcal/mol' 5: 'cm⁻¹' \n Values wrt Ha. ", Scales)

    Scaling_Inp = int(input("\n Enter Input Unit (0-5): Default = 0 (Ha.) : "))
    Scaling_Out = int(input("\n Enter Output Scale required (0-5): Default = 5 (cm⁻¹) : "))

    if (Scaling_Out < 7):
        E_scal_param = Scales[Scaling_Out]/Scales[Scaling_Inp]
        y_scale = Scale_name[Scaling_Out] # not needed but can be returned for plotting purpose

        Ref_va = int(input("\n Do you want to use reference energy from dataframe or enter manually? (0: from dataframe 1: Enter Manually) : "))

        if (Ref_va==0):
            dfr = int(input ("Enter the column number for radial coordinates (Default: 0) : "))
            print (" The max value of R is: ", df[dfr].max(), "\n Corrosponding vlues: ")
            print (df[df[dfr] == df[dfr].max()])
            Ref_val_df =  int(input(" \n Enter Row number to be used as reference: "))
            Ref_val = df[i][Ref_val_df]
        else:
            Ref_val = float(input("\n Enter Reference Energy (at R = Infinity) (With negative sign)) : "))

        df[i] = (df[i]-Ref_val)*E_scal_param
        print("The new dataframe with updated E scale is : \n", df)

    else:
      E_scal_param = 1
      y_scale = 'Unknown Energy unit'
      print(" Incorrect scaling input. no scaling will be done.\n Rerun the program to correctly register the input.")

    return df, y_scale

# function to scale radial coordinates
def R_Scale(df, i):
    # coverting R to bohr and degree to radians (Use if required)
    conver_au = 1.8897259886  # angstrom to bohr
    R_scl = int(input("\n Enter Scaling Factor for Distance: (0. No change (default) 1. Angstrom to Bohr 2. Bohr to Angstrom) : "))

    if (R_scl == 1):
        print("Changing Angstrom to Bohr")
        df[i] = df[i]*conver_au
    elif (R_scl == 2):
        print("Changing Bohr to Angstrom")
        df[i] = df[i]/conver_au
    else :
        print("No R Scaling")

    print("The new dataframe with updated R scale is : \n", df)

    return df

# function to scale angular coordinates
def theta_Scale(df, i):
    import numpy as np
    # degree to radian and vice-versa
    Th_scale = int(input("\n Enter Scaling Factor for Angle: (0. No change (default) 1. Degree to Radians 2. Radians to Degrees) : "))
    if (Th_scale == 1):
        print("Changing Degree to Radians")
        df[i] = np.deg2rad(df[i])
    elif (Th_scale == 2):
        print("Changing Radians to Degrees")
        df[i] = np.rad2deg(df[i])
    else :
        print("No Angular Scaling")
    print("The new dataframe with updated angular scale is : \n", df)
    return df


###############################################################################
#--------------------------- TensorFlow Partition ----------------------------#
###############################################################################

# functions for visualizing the partitions: minima and high energy data points
def pl_trim_part(df_pl, num_XY, num_X, x_shape , trim, out_plots, inp):
    df_pl_minima = df_pl.iloc[:trim]#.reset_index(drop = True)
    df_pl_HE = df_pl.iloc[trim:]#.reset_index(drop = True)
    pl_trim_vis_part(df_pl_minima, df_pl_HE, num_XY, num_X, x_shape, trim, out_plots, inp)
    return df_pl_minima, df_pl_HE

def pl_trim_vis_full(df_pl, num_XY, num_X, x_shape, out_plots, inp):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 16})
    import numpy as np
    try:
        inp.plt_srt_yscale
    except:
        plt_srt_yscale = 'symlog'
    else:
        plt_srt_yscale = inp.plt_srt_yscale

    try:
        inp.plt_srt_xscale
    except:
        plt_srt_xscale = 'linear'
    else:
        plt_srt_xscale = inp.plt_srt_xscale

    for i in range (num_X,num_XY):
        #plt.figure(figsize=(9, 2.5))
        #plt.ion()
        z1 = df_pl.to_numpy()[:,i]
        x1 = np.arange(x_shape)
        plt.title("Full Dataset: Unpartitioned data \n Column Number {}".format(i))
        plt.plot(x1,z1)
        plt.yscale(plt_srt_yscale)
        plt.xscale(plt_srt_xscale)
        plt.grid(True,linestyle=':')
        plt.minorticks_on()
        plt.xlabel("Number of data points")
        plt.ylabel("Energy / Output")
        plt.savefig(out_plots+'Non_partitioned_Full_Dataset_E_sorted_{}.'.format(i)+inp.fmt, format=inp.fmt,bbox_inches='tight')
        plt.close()
        #plt.show()
        #plt.pause(0.01)
        #print(" \n ")
    print("\n Full dataset sorted by energy and plotted!!")

def pl_trim_vis_part(df_pl_min, df_pl_HE, num_XY, num_X, x_shape, trim, out_plots, inp):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 10})
    import numpy as np
    try:
        inp.plt_srt_yscale
    except:
        plt_srt_yscale = 'symlog'
    else:
        plt_srt_yscale = inp.plt_srt_yscale

    try:
        inp.plt_srt_xscale
    except:
        plt_srt_xscale = 'linear'
    else:
        plt_srt_xscale = inp.plt_srt_xscale
    for i in range (num_X,num_XY):
        #plt.figure(figsize=(9, 3))
        #plt.ion()
        z1 = df_pl_min.to_numpy()[:,i]
        x1 = np.arange(trim)
        sub1 = plt.subplot(2, 1, 1)  # Create the first subplot
        sub1.set_title("Partition A: (Minima + Asymptotic region) \n Column Number {}".format(i))
        sub1.plot(x1,z1)
        sub1.set_yscale(plt_srt_yscale)
        sub1.set_xscale(plt_srt_xscale)
        sub1.grid(True,linestyle=':')
        sub1.minorticks_on()
        sub1.set_xlabel("Number of data points")
        sub1.set_ylabel("Energy / Output")

        z2 = df_pl_HE.to_numpy()[:,i]
        x2 = np.arange(trim, x_shape)
        sub2 = plt.subplot(2, 1, 2)  # Create the second subplot
        sub2.set_title("Partition B: (High energy region) \n Column Number {}".format(i))
        sub2.plot(x2,z2)
        sub2.set_yscale(plt_srt_yscale)
        sub2.set_xscale(plt_srt_xscale)
        sub2.grid(True,linestyle=':')
        sub2.minorticks_on()
        sub2.set_xlabel("Number of data points")
        sub2.set_ylabel("Energy / Output")

        plt.tight_layout()
        plt.savefig(out_plots+'Partitioned_Dataset_E_sorted_{}.'.format(i)+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save combined figure
        plt.close()
        #plt.show()
        #plt.pause(0.01)
        #print(" \n ")
    print("\n Dataset partitioned and plotted!! \n")


###############################################################################
#------------------ TensorFlow Extract Boundary Elements ---------------------#
###############################################################################

# required functions for partition and plotting
def extract_boundary_elements(df, num_X):
    import pandas as pd
    # Extract the boundary elements from the dataframe
    df_bd1 = pd.DataFrame()
    df_bd2 = pd.DataFrame()
    boundary_df = pd.DataFrame()

    # extracting boundary terms part 1 (Radial boundary)
    for i in range (1, num_X):
      unique_values = df[0].unique()
      for j in (unique_values):
        max_value = df.loc[df[0] == j, i].max()
        min_value = df.loc[df[0] == j, i].min()
        df_bd1 = df[(df[0] == j) & (df[i] == max_value)] # Extracting row elements with maximum value of column
        df_bd2 = df[(df[0] == j) & (df[i] == min_value)] # Extracting row elements with minimum value of column
        if (num_X>2):
          df_bd1 = df_bd1.sort_values(by=num_X).iloc[[-1]]
          df_bd2 = df_bd2.sort_values(by=num_X).iloc[[0]]
        df_bd1 = pd.concat([df_bd1, df_bd2], axis = 0)  # appending df_bd1 to include both boundaries of the column i
        boundary_df = pd.concat([boundary_df, df_bd1], axis = 0)  # appending boundary_df to include both boundaries of all columns

    # extracting boundary term part 2 (for each angular boundary)
    for i in range (1, num_X):
      unique_values = df[i].unique()
      for j in (unique_values):
        max_value = df.loc[df[i] == j, 0].max()
        min_value = df.loc[df[i] == j, 0].min()
        df_bd1 = df[(df[0] == max_value) & (df[i] == j)] # Extracting row elements with maximum value of column
        df_bd2 = df[(df[0] == min_value) & (df[i] == j)] # Extracting row elements with minimum value of column
        if (num_X>2):
          df_bd1 = df_bd1.sort_values(by=num_X).iloc[[-1]]
          df_bd2 = df_bd2.sort_values(by=num_X).iloc[[0]]
        df_bd1 = pd.concat([df_bd1, df_bd2], axis = 0)  # appending df_bd1 to include both boundaries of the column i
        boundary_df = pd.concat([boundary_df, df_bd1], axis = 0)  # appending boundary_df to include both boundaries of all columns

    boundary_df.drop_duplicates(inplace=True)  # remove duplicate columns

    return boundary_df

# Function to plot boundary elements for non-partitioned data (2D plots only).
def plot_boundary(df_pl, i, j, out_plots, inp):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 16})
    try:
        inp.plt_bnd_yscale
    except:
        plt_bnd_yscale = 'linear'
    else:
        plt_bnd_yscale = inp.plt_bnd_yscale

    try:
        inp.plt_bnd_xscale
    except:
        plt_bnd_xscale = 'linear'
    else:
        plt_bnd_xscale = inp.plt_bnd_xscale

    #print("boundary elements of dataframe at Original Dataframe \n", df_pl)
    #plt.figure(figsize=(14.5, 3))  # Adjust the figsize as needed
    plt.scatter(df_pl[i], df_pl[j])
    plt.title("Full Dataset Boundary elements for \n Column {} (R) vs Column {} (r/Phi/Theta)".format(i,j))
    plt.xlabel("Column {} \nR (Angstrom) ".format(i))
    plt.ylabel("Column {} \ntheta/phi (Degrees)".format(j))
    plt.grid(True,linestyle=':')
    plt.minorticks_on()
    plt.yscale(plt_bnd_yscale)
    plt.xscale(plt_bnd_xscale)
    plt.savefig(out_plots+'Boundary_Full_Dataset{}.'.format(j)+inp.fmt, format=inp.fmt,bbox_inches='tight')
    print("\n Boundary elements separated and plotted!!")
    plt.close()
  #plt.show()

# function to plot boundary elements of 2 partitioned data (minima and high energy)
def plot_boundary_partition(boundary_df_pl_minima,boundary_df_pl_HE, i, j, out_plots, inp):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 12})
    try:
        inp.plt_bnd_yscale
    except:
        plt_bnd_yscale = 'linear'
    else:
        plt_bnd_yscale = inp.plt_bnd_yscale

    try:
        inp.plt_bnd_xscale
    except:
        plt_bnd_xscale = 'linear'
    else:
        plt_bnd_xscale = inp.plt_bnd_xscale

    #print("boundary elements of dataframe at Minima region \n", boundary_df_pl_minima)
    #plt.figure(figsize=(12, 3))  # Adjust the figsize as needed
    sub1 = plt.subplot(2, 1, 1)  # Create the first subplot
    sub1.scatter(boundary_df_pl_minima[i], boundary_df_pl_minima[j])
    sub1.set_title("Partition A: Minima boundary")
    sub1.grid(True,linestyle=':')
    sub1.minorticks_on()
    sub1.set_yscale(plt_bnd_yscale)
    sub1.set_xscale(plt_bnd_xscale)
    #plt.xlabel("R (Angstrom)")
    #plt.ylabel("theta/phi (Degrees)")
    sub1.set_xlabel("Column {} \nR (Angstrom) ".format(i))
    sub1.set_ylabel("Column {} \ntheta/phi (Degrees)".format(j))

    #print("boundary elements of dataframe at High Energy region \n", boundary_df_pl_HE)
    sub2 = plt.subplot(2, 1, 2)  # Create the second subplot
    sub2.scatter(boundary_df_pl_HE[i], boundary_df_pl_HE[j])
    sub2.set_title("Partition B: High energy boundary")
    sub2.grid(True,linestyle=':')
    sub2.minorticks_on()
    sub2.set_yscale(plt_bnd_yscale)
    sub2.set_xscale(plt_bnd_xscale)
    sub2.set_xlabel("Column {} \nR (Angstrom) ".format(i))
    sub2.set_ylabel("Column {} \ntheta/phi (Degrees)".format(j))

    plt.tight_layout()
    plt.savefig(out_plots+'Boundary_Partitioned_Dataset_{}.'.format(j)+inp.fmt, format=inp.fmt,bbox_inches='tight')
    plt.close()
    print("\n Boundary elements for minima and high energy regions separated and plotted!!")
  #plt.show()


###############################################################################
#--------------- Split dataset using Random Seed/stratification --------------#
###############################################################################


### Function to Split dataset using Random Seed/stratification
def split_dataframe(df, df2, num_X, num_Y, train_ratio, val_test_ratio, stratify_val, num_bins, seed_inp, model_num, out_plots, inp):
    import pandas as pd
    from sklearn.model_selection import train_test_split

    input_features = range(num_X)
    output_features = range(-num_Y, 0)
    #stratify_columns = pd.DataFrame()
    X = df.iloc[:, input_features]
    Y = df.iloc[:, output_features]

    X_b = df2.iloc[:, input_features]
    Y_b = df2.iloc[:, output_features]

    test_ratio_tr  = (100-train_ratio)/100
    test_ratio_val = (100-val_test_ratio)/100

    # Input columns stratified
    if (stratify_val == 2):
        pd.set_option('mode.chained_assignment', None)
        X['sum_bins'] = 0
        for i in range(num_X):
            X[f'X{i+1}_bins'] = pd.cut(X.iloc[:, i], bins=num_bins, labels=False)
            X['sum_bins'] += X[f'X{i+1}_bins']
        stratify_columns = ['sum_bins']
        bins_val = X['sum_bins'].to_numpy()
        # Splitting Datasets based on bins
        X_train, X_rem, Y_train, Y_rem = train_test_split(X, Y, test_size=test_ratio_tr, stratify=X[stratify_columns], random_state=None)
        X_val, X_test, Y_val, Y_test = train_test_split(X_rem, Y_rem, test_size=test_ratio_val, stratify=X_rem[stratify_columns], random_state=None)
        # Removing extra columns used for binning
        X_train, X_val, X_test = X_train.iloc[:, :-(num_X+1)], X_val.iloc[:, :-(num_X+1)], X_test.iloc[:, :-(num_X+1)]
        # Histogram plot for bins
        if (model_num == 0 or model_num == 99):
            Plot_Histogram(bins_val, num_X, num_bins, model_num, out_plots, inp)
        else:
            pass

    # Output columns stratified
    elif (stratify_val == 3):
        pd.set_option('mode.chained_assignment', None)
        Y['sum_bins'] = 0
        for i in range(num_Y):
            Y[f'Y{i+1}_bins'] = pd.cut(Y.iloc[:, i], bins=num_bins, labels=False)
            Y['sum_bins'] += Y[f'Y{i+1}_bins']
        stratify_columns = ['sum_bins']
        bins_val = Y['sum_bins'].to_numpy()
        # Splitting Datasets based on bins
        X_train, X_rem, Y_train, Y_rem = train_test_split(X, Y, test_size=test_ratio_tr,  stratify=Y[stratify_columns], random_state=None)
        X_val, X_test, Y_val, Y_test = train_test_split(X_rem, Y_rem, test_size=test_ratio_val, stratify=Y_rem[stratify_columns], random_state=None)
        # Removing extra columns used for binning
        Y_train, Y_val, Y_test = Y_train.iloc[:, :-(num_Y+1)], Y_val.iloc[:, :-(num_Y+1)], Y_test.iloc[:, :-(num_Y+1)]
        # Histogram plot for bins
        if (model_num == 0 or model_num == 99):
            Plot_Histogram(bins_val, num_Y, num_bins, model_num, out_plots, inp)
        else:
            pass

    # random seed splitting
    else:
        print("Using random seed for train/test/validation split!!! ")
        # Split the original DataFrame into train dataset
        X_train, X_rem, Y_train, Y_rem = train_test_split(X, Y, test_size=test_ratio_tr, random_state=seed_inp)
        # Split the reamining dataset into test and validation datasete
        X_val, X_test, Y_val, Y_test = train_test_split(X_rem, Y_rem, test_size=test_ratio_val, random_state=seed_inp)

    print ("\n    Training, Test, Validation Shape \n")
    print (f"Split without boundary elements for Model {model_num}")
    print ("X: ", X_train.shape, X_test.shape, X_val.shape)
    print ("Y: ", Y_train.shape, Y_test.shape, Y_val.shape)

    # Concatenate DataFrame 2 (boundary coordinates) with the training dataset
    X_train = pd.concat([X_train, X_b])
    Y_train = pd.concat([Y_train, Y_b])

    print (f"Split with boundary elements added to training dataset for Model {model_num}")
    print ("X: ", X_train.shape, X_test.shape, X_val.shape)
    print ("Y: ", Y_train.shape, Y_test.shape, Y_val.shape)

    return X_train, X_val, X_test, Y_train, Y_val, Y_test

### Function to Split dataset using that does not contain validation dataset (not used: provided if needed for modification)
def split_dataframenoval(df, df2, num_X, num_Y, train_ratio, stratify_val, num_bins, seed_inp, model_num, out_plots, inp):
    import pandas as pd
    from sklearn.model_selection import train_test_split

    input_features = range(num_X)
    output_features = range(-num_Y, 0)
    #stratify_columns = pd.DataFrame()
    X = df.iloc[:, input_features]
    Y = df.iloc[:, output_features]

    X_b = df2.iloc[:, input_features]
    Y_b = df2.iloc[:, output_features]

    test_ratio_tr  = (100-train_ratio)/100

    # Input columns stratified
    if (stratify_val == 2):
        pd.set_option('mode.chained_assignment', None)
        X['sum_bins'] = 0
        for i in range(num_X):
            X[f'X{i+1}_bins'] = pd.cut(X.iloc[:, i], bins=num_bins, labels=False)
            X['sum_bins'] += X[f'X{i+1}_bins']
        stratify_columns = ['sum_bins']
        bins_val = X['sum_bins'].to_numpy()
        # Splitting Datasets based on bins
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_ratio_tr, stratify=X[stratify_columns], random_state=None)
        # Removing extra columns used for binning
        X_train, X_test = X_train.iloc[:, :-(num_X+1)], X_test.iloc[:, :-(num_X+1)]
        # Histogram plot for bins
        if (model_num == 0 or model_num == 99):
            Plot_Histogram(bins_val, num_X, num_bins, model_num, out_plots, inp)
        else:
            pass

    # Output columns stratified
    elif (stratify_val == 3):
        pd.set_option('mode.chained_assignment', None)
        Y['sum_bins'] = 0
        for i in range(num_Y):
            Y[f'Y{i+1}_bins'] = pd.cut(Y.iloc[:, i], bins=num_bins, labels=False)
            Y['sum_bins'] += Y[f'Y{i+1}_bins']
        stratify_columns = ['sum_bins']
        bins_val = Y['sum_bins'].to_numpy()
        # Splitting Datasets based on bins
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_ratio_tr,  stratify=Y[stratify_columns], random_state=None)
        # Removing extra columns used for binning
        Y_train, Y_test = Y_train.iloc[:, :-(num_Y+1)], Y_test.iloc[:, :-(num_Y+1)]
        # Histogram plot for bins
        if (model_num == 0 or model_num == 99):
            Plot_Histogram(bins_val, num_Y, num_bins, model_num, out_plots, inp)
        else:
            pass

    # random seed splitting
    else:
        print("Using random seed for train/test/validation split!!! ")
        # Split the original DataFrame into train dataset
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_ratio_tr, random_state=seed_inp)
        # Split the reamining dataset into test and validation datasete

    print ("\n    Training, Test, Validation Shape \n")
    print (f"Split without boundary elements for Model {model_num}")
    print ("X: ", X_train.shape, X_test.shape)
    print ("Y: ", Y_train.shape, Y_test.shape)

    # Concatenate DataFrame 2 (boundary coordinates) with the training dataset
    X_train = pd.concat([X_train, X_b])
    Y_train = pd.concat([Y_train, Y_b])

    print (f"Split with boundary elements added to training dataset for Model {model_num}")
    print ("X: ", X_train.shape, X_test.shape)
    print ("Y: ", Y_train.shape, Y_test.shape)

    return X_train, X_test, Y_train, Y_test

def Plot_Histogram(bins_val,num_col,num_bins,model_num, out_plots, inp):
    import numpy as np
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 16})
    #column_name = f'_bins'
    plt.hist(bins_val, bins=np.arange(-0.5,((num_bins-1)*num_col)+0.51,1),
              edgecolor='black')
    plt.xlabel('Bins')
    plt.ylabel('Frequency')
    if (model_num <= num_col):
      plt.title(f'Histogram for Model {model_num} (Minima+Asymptotic) region')
    else:
      plt.title(f'Histogram for Model {model_num} High Energy region')

    plt.tight_layout()
    plt.savefig(out_plots+'Histogram_stratification_{}.'.format(model_num)+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save combined figure
    plt.close()
    #plt.show()
    #plt.pause(0.01)




def plot_residuals(y_original, predictions, output_path, output_label, fmt):
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.size': 16})
    fig = plt.figure(figsize=(10, 8))
    plt.scatter(y_original, y_original - predictions)
    plt.axhline(color='black', linestyle=':')
    plt.minorticks_on()  # Minor ticks are on
    plt.title(r"Residual plot NN model")  # Title of the plot
    plt.ylabel(r'Residuals $(\mathrm{cm}^{-1})$')  # Y label
    plt.xlabel(r'Energy $(\mathrm{cm}^{-1})$')  # X label
    if (output_label == 'Residuals_all') :
        plt.yscale('symlog')
    else:
        pass
    plt.xscale('symlog')  # Symmetric log scale for X axis
    plt.tight_layout()  # Tight layout
    plt.savefig(output_path + output_label + '.' + fmt, format=fmt ,bbox_inches='tight')
    plt.close(fig)  # Close the figure to release memory

    residuals = np.c_[y_original,predictions]
    np.savetxt(output_path + f'/{output_label}.txt' , residuals, delimiter='\t', fmt='%.4f,%.4f')


def plot_loss_and_mae(history, output_path, output_label, fmt):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 16})
    fig = plt.figure(figsize =(10, 8))
    # Plot training & validation loss values
    plt.plot(history[output_label])
    plt.plot(history['val_{}'.format(output_label)])
    plt.title('Model Training Metrics')
    plt.ylabel('{} (scaled)'.format(output_label))
    plt.xlabel('Epoch')
    plt.yscale('log')
    plt.legend(['Train', 'Validation'], loc='upper right')
    plt.savefig(output_path+'NN_{}_History.'.format(output_label)+fmt, format=fmt ,bbox_inches='tight')
    plt.close(fig)



#-----------------------------------------------------------------------------#

def create_silent_bayesian_optimization():
    import keras_tuner as kt
    class SilentBayesianOptimization(kt.tuners.BayesianOptimization):
        def run_trial(self, trial, x, y, **kwargs):
            from tqdm.keras import TqdmCallback
            tqdm_prog = TqdmCallback(verbose=1)
            kwargs['verbose'] = 0
            # Build the model using the current trial's hyperparameters
            model = self.hypermodel.build(trial.hyperparameters)
            # Fit the model with verbose=0 to suppress epoch printing
            history = model.fit(x, y, callbacks=[tqdm_prog], **kwargs)
            final_metrics = {k: min(v) for k, v in history.history.items()}
            # Update the trial and save the model
            self.oracle.update_trial(trial.trial_id, final_metrics)
            # Save the model
            self.save_model(trial.trial_id, model)

        def save_model(self, trial_id, model):
            # Define a directory to save the models
            import os
            model_dir = os.path.join(self.project_dir, "trial_" + str(trial_id))
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, "model.keras")
            model.save(model_path)  # Save the model as a keras file
    return SilentBayesianOptimization

#-----------------------------------------------------------------------------#

def create_TrainableActivation():
    import tensorflow as tf
    from tensorflow.keras.layers import Layer
    class TrainableActivation(Layer):
        def __init__(self, activation_type='gaussian', **kwargs):
            super(TrainableActivation, self).__init__(**kwargs)
            # Trainable parameters for Gaussian activation
            self.alpha = self.add_weight(shape=(1,), initializer='ones', trainable=True, name='alpha')
            self.beta = self.add_weight(shape=(1,), initializer='ones', trainable=True, name='beta')
            self.gamma = self.add_weight(shape=(1,), initializer='zeros', trainable=True, name='gamma')
            self.activation_type = activation_type

        def call(self, inputs):
            import tensorflow as tf
            if self.activation_type == 'Gaussian':
                return self.beta * tf.exp(-self.alpha * tf.square((inputs + self.gamma)))
            elif self.activation_type == 'NGelu':
                #return (-1) * self.beta * tf.exp(tf.pow(inputs,-self.alpha)) * tf.math.log(inputs + self.gamma)    #
                return self.beta * 0.5 * (-1 * (inputs + self.gamma)) * (1 + tf.math.erf( (-1 * (inputs + self.gamma)) / (self.alpha * tf.sqrt(2.0) )))
            else:
                raise ValueError("Invalid activation type. Choose 'Gaussian' or 'NGelu'.")

        def get_config(self):
            config = super(TrainableActivation, self).get_config()
            config.update({
            "activation_type": self.activation_type,
            "alpha": self.alpha.numpy().tolist(),
            "beta": self.beta.numpy().tolist(),
            "gamma": self.gamma.numpy().tolist()
            })
            return config
        @classmethod
        def from_config(cls, config):
            activation_type = config.pop('activation_type')
            instance = cls(activation_type=activation_type)
            instance.alpha.assign(config['alpha'])
            instance.beta.assign(config['beta'])
            instance.gamma.assign(config['gamma'])
            return instance
    return TrainableActivation

#-----------------------------------------------------------------------------#
##############################################################################################
# A more constrained trainable function with minima (Warning: may cause HE region to invert!)
##############################################################################################
# def create_CustomDecayLayer():
#     import tensorflow as tf
#     from tensorflow.keras.layers import Layer
#     class CustomDecayLayer(Layer):
#         def __init__(self, **kwargs):
#             #import tensorflow as tf
#             from tensorflow.keras.constraints import NonNeg
#             super(CustomDecayLayer, self).__init__(**kwargs)
#             # Define trainable parameters u and v
#             self.u = tf.Variable(initial_value=10.0, trainable=True, dtype=tf.float32, name="u",constraint=NonNeg())
#             self.v = tf.Variable(initial_value=100.0, trainable=True, dtype=tf.float32, name="v",constraint=NonNeg())
#             self.a = tf.Variable(initial_value=1.0, trainable=True, dtype=tf.float32, name="a",constraint=NonNeg())
#             self.b = tf.Variable(initial_value=1.0, trainable=True, dtype=tf.float32, name="b",constraint=NonNeg())
#             self.c = tf.Variable(initial_value=1.0, trainable=True, dtype=tf.float32, name="c",constraint=NonNeg())
#             #self.u = self.add_weight(shape=(1,), initializer='ones', trainable=True, name="u",constraint=NonNeg())
#             #self.v = self.add_weight(shape=(1,), initializer='ones', trainable=True, name="v",constraint=NonNeg())
#         def call(self, inputs):
#             #import tensorflow as tf
#             x = inputs
#             modx = tf.abs(self.u * x)
#             return self.v * tf.exp(-self.a * modx) * ((1 / (self.b * modx)) - self.c * modx) # EDM function
#             #return self.v * tf.exp(-modx) / (modx)  # EDM function
#     return CustomDecayLayer
###################################################################################
# trainable slater-reciprocal and slater-reciprocal-log function (change if needed)
###################################################################################
def create_CustomDecayLayer():
    import tensorflow as tf
    from tensorflow.keras.layers import Layer
    class CustomDecayLayer(Layer):
        def __init__(self, **kwargs):
            from tensorflow.keras.constraints import NonNeg
            super(CustomDecayLayer, self).__init__(**kwargs)
            # Define trainable parameters a, b and c
            self.a = tf.Variable(initial_value=1.0, trainable=True, dtype=tf.float32, name="a",constraint=NonNeg())
            self.b = tf.Variable(initial_value=1.0, trainable=True, dtype=tf.float32, name="b",constraint=NonNeg())
            self.c = tf.Variable(initial_value=1.0, trainable=True, dtype=tf.float32, name="c",constraint=NonNeg())
        def call(self, inputs):
            x = inputs
            #return ( self.a * tf.exp( -self.b * x + self.c) ) ) / (x) # slater-reciprocal (Amplified Decay function) (no minima)
            #return ( - self.a * tf.exp(-self.b * x))*tf.math.log(self.c*x)/(x) # coupled slater-reciprocal-log (has a minima)
            return ( self.a * tf.exp( -self.b * (x - self.c) ) ) / (x) # Amplified Decay function with shift
    return CustomDecayLayer
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#

def create_ND_model(hp, input_dim, num_outputs, NN_hyperpara):
    import tensorflow as tf
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense, Concatenate, Multiply
    from tensorflow.keras.utils import get_custom_objects

    CustomDecayLayer =  create_CustomDecayLayer()
    TrainableActivation = create_TrainableActivation()
    # Broken after 3.11.7 update
    #get_custom_objects().update({'gaussian': TrainableActivation(name='Gaussian', activation_type='Gaussian'),
    #                             'ngelu': TrainableActivation(name='NGelu', activation_type='NGelu')})

    deep_l = NN_hyperpara['NN_nodes']     # number of units per layer
    hidd_l = NN_hyperpara['NN_layers']    # number of hidden layer (between input and output) per branch
    bran_l = NN_hyperpara['NN_branches']  # number of branches (each with hidden layers coupled with other branches)

    # Define the input (R and theta)
    inputs = Input(shape=(input_dim,), name='input_layer')  # input_dim = 2 for R and theta
    R = inputs[:, 0:1]  # Radial component R
    x = CustomDecayLayer()(R)      # custom trainable decay function
    # direct functions
    #x = (1/R)                     # reciprocal function
    #x = (tf.exp(-R) / (R))        # moderately flexible decay function
    #x = (tf.exp((1/R) - R)) / (R) # very rigid decay function
    #x = (tf.exp(-R))*(1/(R) - R)  # custom decay function with minima

    units_pl = hp.Choice(f'units', deep_l)
    branches = hp.Choice(f'branches', bran_l)

    for i in range(branches):
        globals()[f'x_th{i}'] = Dense(units_pl, activation='linear', use_bias=False)(inputs)  # Linear activation
    combined = Concatenate()([globals()[f'x_th{i}'] for i in range(branches)])

    hidden_layers = hp.Choice(f'hidden_layers', hidd_l)  # Number of hidden layers for R
    for h in range(hidden_layers):
        for i in range(0,branches,2):
            # Broken after 3.11.7 update
            #globals()[f'x_th{i}'] = Dense(units_pl, activation='gaussian', use_bias=False)(combined)  # Gaussian activation
            #globals()[f'x_th{i+1}'] = Dense(units_pl, activation='ngelu', use_bias=False)(combined)  # Modified Gaussian Error activation
            # Applying newer fix (Tested up to 3.11.11)
            temp = Dense(units_pl, activation=None, use_bias=False)(combined)
            globals()[f'x_th{i}'] = TrainableActivation(name=f'Gaussian_{h}_{i}', activation_type='Gaussian')(temp)
            
            temp2 = Dense(units_pl, activation=None, use_bias=False)(combined)
            globals()[f'x_th{i+1}'] = TrainableActivation(name=f'NGelu_{h}_{i+1}', activation_type='NGelu')(temp2)
        combined = Concatenate()([globals()[f'x_th{i}'] for i in range(branches)])

    for i in range(branches):
        globals()[f'x_th{i}'] = Dense(num_outputs, activation='linear', use_bias=False)(globals()[f'x_th{i}'])  # Linear activation
    #combined = Concatenate()([globals()[f'x_th{i}'] for i in range(branches)])

    combined = Concatenate()([globals()[f'x_th{i}'] for i in range(branches)])
    combined =  Multiply()([x, combined])
    output = Dense(num_outputs, activation='linear', name='output_layer', use_bias=False)(combined)
    # Build the model
    model = Model(inputs=inputs, outputs=output)

    optimizer_instance = tf.keras.optimizers.Adam(amsgrad=True)
    model.compile(optimizer=optimizer_instance, loss='huber', metrics=['mae'])
    return model
#-----------------------------------------------------------------------------#
def create_generic_model(hp, input_dim, num_outputs, NN_hyperpara):
    import tensorflow as tf
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense, Concatenate

    deep_l = NN_hyperpara['NN_nodes']     # number of units per layer
    hidd_l = NN_hyperpara['NN_layers']    # number of hidden layer (between input and output) per branch
    bran_l = NN_hyperpara['NN_branches']  # number of branches (each with hidden layers coupled with other branches)

    # Define the input (R and theta)
    inputs = Input(shape=(input_dim,), name='input_layer')  # input_dim

    units_pl = hp.Choice(f'units', deep_l)
    branches = hp.Choice(f'branches', bran_l)

    for i in range(branches):
        globals()[f'x_th{i}'] = Dense(units_pl, activation='linear')(inputs)  # Linear activation
    combined = Concatenate()([globals()[f'x_th{i}'] for i in range(branches)])

    hidden_layers = hp.Choice(f'hidden_layers', hidd_l)  # Number of hidden layers for R
    for h in range(hidden_layers):
        for i in range(0,branches,1):
            globals()[f'x_th{i}'] = Dense(units_pl, activation='gelu')(combined)  # Gaussian Error activation
        combined = Concatenate()([globals()[f'x_th{i}'] for i in range(branches)])

    for i in range(branches):
        globals()[f'x_th{i}'] = Dense(num_outputs, activation='linear')(globals()[f'x_th{i}'])  # Linear activation
    #combined = Concatenate()([globals()[f'x_th{i}'] for i in range(branches)])

    combined = Concatenate()([globals()[f'x_th{i}'] for i in range(branches)])
    output = Dense(num_outputs, activation='linear', name='output_layer')(combined)
    # Build the model
    model = Model(inputs=inputs, outputs=output)

    optimizer_instance = tf.keras.optimizers.Adam(amsgrad=True)
    model.compile(optimizer=optimizer_instance, loss='huber', metrics=['mae'])
    return model

###############################################################################
#------------------------------ Plot MP Expansion ----------------------------#
###############################################################################

# Plot raw data separately
def plot_MP(lm, sym, R_arr, df_Vnf, MP_plots, inp):
    df_Vnf.columns = df_Vnf.columns.astype(str)
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 12})
    for i in range(0,lm):               # loop over V_lambda terms
        y_dummy = df_Vnf['{}'.format(i*sym)]         # stores individual V_lambda for each loop
        plt.figure(figsize=(11,3))      # size of figure

        # Plot each V_lambda_separately to view features
        plt.subplot(1,3,1)                      # first subplot at visually appropriate x, y limit
        plt.plot(R_arr, y_dummy)                    # first plot
        plt.grid(True,linestyle=':')                # grid on
        plt.minorticks_on()                         # minor ticks are on
        plt.title("V_lambda = %d" %(i*sym))         # title of plot
        plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
        plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
        min_E = int(y_dummy.min())-1
        max_E = int(y_dummy.max())+1
        plt_lim = min(abs(min_E),abs(max_E))
        plt.ylim(-plt_lim, plt_lim)   # y limit
        plt.xlim(inp.R_lim[0], inp.R_lim[1])

        plt.subplot(1,3,2)                      # second subplot at maximum x, y limit
        plt.plot(R_arr, y_dummy)
        plt.grid(True,linestyle=':')
        plt.minorticks_on()
        plt.title("V_lambda = %d" %(i*sym))
        plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
        plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
        plt.ylim(y_dummy.min(), y_dummy.max())
        plt.xlim(0.0, R_arr.max())

        plt.subplot(1,3,3)                      # third subplot at zoomed in y limit [-1, +1]
        plt.plot(R_arr, y_dummy)
        plt.grid(True,linestyle=':')
        plt.minorticks_on()
        plt.title("V_lambda = %d" %(i*sym))
        plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
        plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
        plt.ylim(-1.0, 1.0)
        plt.xlim(inp.R_lim[0], inp.R_lim[1])

        plt.tight_layout()                      # tight layout
        # plt.savefig(out_plots+'Polar_plot.eps', format='eps')  # save polar contour in eps
        plt.savefig(MP_plots+'V_lam_{}.'.format(i*sym)+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save ploar plot in pdf

        #plt.show()                                            # preview off (use only for jupyter)
        plt.close()

#-----------------------------------------------------------------------------#

def plot_MP_combined(lm, sym, R_arr, df_Vnf, MP_plots, inp):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 14})
    df_Vnf.columns = df_Vnf.columns.astype(str)
    for i in range(0,lm):                                      # loop over V_lambda terms
        y_dummy = df_Vnf['{}'.format(i*sym)]                   # stores individual V_lambda for each loop
        # Plot the data
        plt.plot(R_arr, y_dummy,label='{}'.format(i*sym))      # plot each V_lambda
        plt.grid(True,linestyle=':')                           # grid on
        plt.minorticks_on()                                    # minor ticks on
        try:
            inp.ncol
        except:
            ncol = 1
        else:
            ncol = inp.ncol
        if inp.Expansion_typ == '2D':
            plt.legend(title = r'$\lambda $', bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=ncol,prop={'size': 12})  # name and position of legend
        else:
            plt.legend(title = r'$\Lambda $', bbox_to_anchor=(0.5, -0.15), loc='upper center' , ncol=ncol,prop={'size': 12})  # name and position of legend

        plt.title("Radial Coefficients")                       # title of plot
        plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
        if inp.Expansion_typ == '2D':
            plt.ylabel(r'$V_\lambda$ $(\mathrm{cm}^{-1})$')        # Y label (written in latex $...$ format)
        else:
            plt.ylabel(r'$V_\Lambda$ $(\mathrm{cm}^{-1})$')        # Y label (written in latex $...$ format)
        plt.ylim(inp.E_lim[0], inp.E_lim[1])                                      # y limit (y_min, y_max)
        plt.xlim(inp.R_lim[0], inp.R_lim[1])                   # x limit (x_min, x_max)
    #plt.show()                                                 # to combine individual plots, plt.show() is used outside loop.
    plt.savefig(MP_plots+'Combined_V_lam.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save combined figure
    plt.close()

#-----------------------------------------------------------------------------#

def Bispher_SF(L1,L2,L,ph,th2,th1):
    from sympy.physics.wigner import clebsch_gordan
    import pyshtools as pysh
    import numpy as np
    from math import sin, cos, radians

    Total=0
    M_max= min(L1,L2)
    theta1 = radians(th1)
    theta2 = radians(th2)
    phi = radians(ph)

    U00 = np.sqrt((2*L+1)/(4*np.pi))
    T01 = clebsch_gordan(L1, L2, L, 0, 0, 0).evalf()
    P0L1 = pysh.legendre.legendre_lm (L1, 0, cos(theta1), 'unnorm', -1, 0)
    P0L2 = pysh.legendre.legendre_lm (L2, 0, cos(theta2), 'unnorm', -1, 0)
    T1 = T01*P0L1*P0L2
    Total += T1
    M=1
    while (M<=M_max):
        T02 = clebsch_gordan(L1, L2, L, M, -M, 0).evalf()
        PmL1 = pysh.legendre.legendre_lm (L1, M, cos(theta1), 'unnorm', -1, 0)
        PmL2 = pysh.legendre.legendre_lm (L2, M, cos(theta2), 'unnorm', -1, 0)
        T2 = T02*PmL1*PmL2
        Total += 2.0*pow((-1),M)*T2*(cos(M*phi))
        M+=1
    Total=Total*U00
    return Total

#-----------------------------------------------------------------------------#

def residual_plot(Origi_E,residuals,MP_plots,inp):
    # Plot error distribution
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 16})
    fig = plt.figure(figsize =(10, 8))
    plt.scatter(Origi_E, residuals)
    plt.axhline(color='black',linestyle=':')
    plt.yscale(inp.scale_y)
    plt.xscale(inp.scale_x)
    plt.minorticks_on()                                              # minor ticks are on
    plt.title(r"Residual plot for regenerated potentials from $V_\lambda$")         # title of plot
    plt.ylabel(r'Residuals $(\mathrm{cm}^{-1})$')                      # X label (written in latex $...$ format)
    #plt.yticks(rotation = 50)
    plt.xlabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
    plt.tight_layout()                      # tight layout
    plt.savefig(MP_plots+'Residuals_Vlam2E.'+inp.fmt, format=inp.fmt,bbox_inches='tight')
    plt.ylim(inp.Y_lim[0], inp.Y_lim[1])
    try:
        inp.cutoff
    except:
        cutoff = 1000
    else:
        cutoff = inp.cutoff
    plt.yscale('linear')
    plt.xlim(Origi_E.min(), cutoff)
    plt.savefig(MP_plots+'Residuals_Vlam2E_zoom.'+inp.fmt, format=inp.fmt,bbox_inches='tight')
    plt.close()

#-----------------------------------------------------------------------------#
def find_nearest(array, value):
    import numpy as np
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]
#-----------------------------------------------------------------------------#

###############################################################################
#----------------------- Analytical Function Fitting -------------------------#
###############################################################################

def plot_Vlam(x_dummy, y_dummy,parsx,strt,i,inp,FnFit_plots,x,scale_R,scale_Energy):
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.size': 12})

    plt.figure(figsize=(12,4))      # size of figure
    plt.subplot(1,3,1)                      # first subplot at visually appropriate x, y limit
    plt.scatter(x_dummy, y_dummy,s=20, color='#00b3b3',label = r'$ab-initio$ potential')
    plt.plot(x_dummy, inp.fnfit_custom(x_dummy*scale_R, *parsx)/scale_Energy, linestyle='-.', linewidth=2, color='black', label = 'custom fit (S0)')
    plt.grid(True,linestyle=':')                # grid on
    plt.minorticks_on()                         # minor ticks are on
    plt.legend(loc="upper right")
    plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
    plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
    plt.axhline(y=0, color='grey', linestyle=':')
    plt.title("V_lambda = %d" %(i))         # title of plot
    min_E = int(y_dummy.min())-1
    max_E = int(y_dummy.max())+1
    plt_lim = min(abs(min_E),abs(max_E))
    plt.ylim(-plt_lim, plt_lim)   # y limit
    plt.xlim(inp.R_lim[0], inp.R_lim[1])

    plt.subplot(1,3,2)                      # second subplot at maximum x, y limit
    plt.scatter(x_dummy, y_dummy,s=20, color='#00b3b3',label = r'$ab-initio$ potential')
    plt.plot(x_dummy, inp.fnfit_custom(x_dummy*scale_R, *parsx)/scale_Energy, linestyle='-.', linewidth=2, color='black', label = 'custom fit (S0)')
    plt.grid(True,linestyle=':')                # grid on
    plt.minorticks_on()                         # minor ticks are on
    plt.legend(loc="upper right")
    plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
    plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
    plt.axhline(y=0, color='grey', linestyle=':')
    plt.title("V_lambda = %d" %(i))         # title of plot
    plt.ylim(y_dummy.min(), y_dummy.max())
    plt.xlim(0.0, x_dummy.max())

    plt.subplot(1,3,3)                      # third subplot at zoomed in y limit [-1, +1]
    plt.scatter(x_dummy, y_dummy,s=20, color='#00b3b3',label = r'$ab-initio$ potential')
    plt.plot(x_dummy, inp.fnfit_custom(x_dummy*scale_R, *parsx)/scale_Energy, linestyle='-.', linewidth=2, color='black', label = 'custom fit (S0)')
    plt.grid(True,linestyle=':')                # grid on
    plt.minorticks_on()                         # minor ticks are on
    plt.legend(loc="upper right")
    plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
    plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
    plt.axhline(y=0, color='grey', linestyle=':')
    plt.title("V_lambda = %d" %(i))         # title of plot
    plt.ylim(-1.0, 1.0)
    plt.xlim(inp.R_lim[0], inp.R_lim[1])

    plt.tight_layout()                      # tight layout
    plt.savefig(FnFit_plots+'V_lam_{}.'.format(i)+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save ploar plot in pdf
    RMSE = np.sqrt(np.average(np.power((inp.fnfit_custom(x_dummy[strt:], *parsx) - y_dummy[strt:]),2)))
    print('RMSE Custom Fn = {} \n'.format(RMSE))
    plt.close()
    #plt.show()                            # preview off (use only for jupyter)
    return RMSE

def residual_plot_E(Origi_E,residuals,MP_plots,inp,x):
    # Plot error distribution
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 16})

    fig = plt.figure(figsize =(10, 8))
    plt.scatter(Origi_E, residuals)
    plt.axhline(color='black',linestyle=':')
    plt.yscale(inp.scale_y)
    plt.xscale(inp.scale_x)
    plt.minorticks_on()                                              # minor ticks are on
    plt.title(r"Residual plot for potentials from FnFit")         # title of plot
    plt.ylabel(r'Residuals $(\mathrm{cm}^{-1})$')                      # X label (written in latex $...$ format)
    #plt.yticks(rotation = 50)
    plt.xlabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
    plt.tight_layout()                      # tight layout
    plt.savefig(MP_plots+'Residuals_EFnFit_{}.'.format(x)+inp.fmt, format=inp.fmt,bbox_inches='tight')
    plt.ylim(inp.Y_lim[0], inp.Y_lim[1])
    try:
        inp.cutoff
    except:
        cutoff = 1000
    else:
        cutoff = inp.cutoff
    plt.yscale('linear')
    plt.xlim(Origi_E.min(), cutoff)
    plt.savefig(MP_plots+'Residuals_EFnFit_zoom_{}.'.format(x)+inp.fmt, format=inp.fmt,bbox_inches='tight')
    plt.close()

def C_fit1D_Plot(Origi_E,predicted_energies,predicted_energiesHELR,R_arr,x_dummy,FnFit_plots,inp):
    # Plot error distribution
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.size': 16})

    plt.figure(figsize=(12,8))      # size of figure
    y_dummy = Origi_E
    plt.scatter(x_dummy, y_dummy, s=20, color='#00b3b3',label = r'$ab-initio$ potential')
    plt.plot(R_arr, predicted_energies, linestyle='-', linewidth=2, color='black', label = 'custom full range fit')
    plt.plot(x_dummy, predicted_energiesHELR, linestyle='dotted', linewidth=4, color='red', label = 'HE and LR fit')
    plt.grid(True,linestyle=':')                # grid on
    plt.minorticks_on()                         # minor ticks are on
    plt.legend(loc="upper right")
    plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
    plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
    plt.axhline(y=0, color='grey', linestyle=':')
    plt.title("Fitted 1D PES")         # title of plot
    min_E = int(y_dummy.min())+0.1*int(y_dummy.min())
    plt.ylim(min_E, -min_E)   # y limit
    plt.xlim(inp.R_lim[0], inp.R_lim[1])
    plt.tight_layout()                      # tight layout
    plt.savefig(FnFit_plots+'C_1D_PES_Fit.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save polar plot in pdf
    min_E = int(y_dummy.min())-1
    max_E = int(y_dummy.max())+1
    plt.ylim(min_E, max_E)   # y limit
    plt.xlim(inp.R_lim[0], inp.R_lim[1])
    plt.tight_layout()                      # tight layout
    plt.savefig(FnFit_plots+'C_1D_PES_Fit_full.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save polar plot in pdf
    min_E = -5
    max_E = +5
    plt.ylim(min_E, max_E)   # y limit
    plt.xlim(inp.R_lim[0], inp.R_lim[1])
    plt.tight_layout()                      # tight layout
    plt.savefig(FnFit_plots+'C_1D_PES_Fit_zoom.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save polar plot in pdf
    plt.close()

def fit1D_Plot(Origi_E,predicted_energies,fit_name,R_arr,x_dummy,FnFit_plots,inp):
    # Plot error distribution
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.size': 16})

    plt.figure(figsize=(12,8))      # size of figure
    y_dummy = Origi_E
    plt.scatter(x_dummy, y_dummy, s=20, color='#00b3b3',label = r'$ab-initio$ potential')
    plt.plot(R_arr, predicted_energies, linestyle='-', linewidth=2, color='black', label = fit_name)
    plt.grid(True,linestyle=':')                # grid on
    plt.minorticks_on()                         # minor ticks are on
    plt.legend(loc="upper right")
    plt.ylabel(r'Energy $(\mathrm{cm}^{-1})$')             # Y label (written in latex $...$ format)
    plt.xlabel(r'R $\mathrm{(\AA)}$')                      # X label (written in latex $...$ format)
    plt.axhline(y=0, color='grey', linestyle=':')
    plt.title("Fitted 1D PES")         # title of plot
    min_E = int(y_dummy.min())+0.1*int(y_dummy.min())
    plt.ylim(min_E, -min_E)   # y limit
    plt.xlim(inp.R_lim[0], inp.R_lim[1])
    plt.tight_layout()                      # tight layout
    plt.savefig(FnFit_plots+f'{fit_name}_1D_PES_Fit.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save polar plot in pdf
    min_E = int(y_dummy.min())-1
    max_E = int(y_dummy.max())+1
    plt.ylim(min_E, max_E)   # y limit
    plt.xlim(inp.R_lim[0], inp.R_lim[1])
    plt.tight_layout()                      # tight layout
    plt.savefig(FnFit_plots+f'{fit_name}_1D_PES_Fit_full.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save polar plot in pdf
    min_E = -5
    max_E = +5
    plt.ylim(min_E, max_E)   # y limit
    plt.xlim(inp.R_lim[0], inp.R_lim[1])
    plt.tight_layout()                      # tight layout
    plt.savefig(FnFit_plots+f'{fit_name}_1D_PES_Fit_zoom.'+inp.fmt, format=inp.fmt,bbox_inches='tight')  # save polar plot in pdf
    plt.close()
