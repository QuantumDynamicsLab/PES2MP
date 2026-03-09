''' Same as 1_Gen_molscat_files but generates MOLSCAT input files for ultracold collisions. '''


# Importing Libraries
import os
import math;

j = int(1) # counter for file name starts from 1 (Do not change)

#########################################################################################################
#                                   Find input parameters at the end                                    #
#-------------------------------------------------------------------------------------------------------#
# Either enter &POTL values directly or read from 'MOLSCAT_POT.txt' file (recommended and implemented)  #
# mxlam is the maximum number of radial terms which will be printed when MP_Exp code is executed        #
# set steps parameter carefully (always test for convergence) [add if-else block as needed]             #
# if jtotu automatic convergence (-1) fails(usually at high energies), manually set to high values      #
# set maxmimum rotational basis for rigid rotor of interest using j1max (always test for convergence)   #
#                                                                                                       #
# P0 para H2                    (J2 = 0)    i.e j2min=0, j2max=0, j2step=2                              #
# P2 para H2 with extra basis   (J2 = 0,2)  i.e j2min=0, j2max=2, j2step=2                              #
# O1 ortho H2                   (J2 = 1)    i.e j2min=1, j2max=1, j2step=2                              #
# O1 ortho H2 with extra basis  (J2 = 1,3)  i.e j2min=1, j2max=3, j2step=2                              #
#                                                                                                       #
# other parameters can be found in MOLSCAT's manual                                                     #ß
#########################################################################################################

# function for creating Molscat input files
def loop(start,fin,step,j):
    # loop for creating
    if (step < 1):
        start = int(start/step)
        fin = int(fin/step)
        stp = 1
    else:
        stp = step
    for i in range (start,fin+1,stp):   # initial/final value /step size
        # creating jobscript file in each folder
        f1= open("%d" %(j),"w+")
        potf = open("MOLSCAT_POT.txt", "r+") # POT: reads potential from 'MOLSCAT_POT.txt' file
        
        # he examples uses rotational energy of J=8 state of C2 (131.047200000000 cm-1). 
        f1.write('  &input ured = 3.4309, nnrg=1, energy=%.8f\n' %(131.047200000000+i* step))

        if (i*stp < 10):
            f1.write('   intflg=8, steps=100, rmin=2.5, rmax=20.0, BCYOMN=10000, \n')
        elif ( (i*stp > 10) and (i*stp < 30) ):
            f1.write('   intflg=8, steps=50, rmin=2.5, rmax=20.0, BCYOMN=10000, \n')
        else:
            f1.write('   intflg=8, steps=20, rmin=2.5, rmax=20.0, BCYOMN=10000, \n')

        f1.write("   label='C2-He system', jtotu = -1, \n")
        f1.write('   prntlv=1, isigpr=1, LASTIN = 1,\n')
        f1.write('/ \n')
        # j1step=2 (C2 does not have odd states 1Sigma_g with I=0)
        f1.write(' &basis itype=21,  j1max=21, j1step=2 \n')
        f1.write('    be= 1.8201,\n')
        f1.write('/ \n')
        f1.write(' &potl rm=1.0, epsil=1.0, mxlam=4, IHOMO=2 \n')
        f1.write(potf.read())  # print potential file
        f1.write('  \n')
        f1.write('/ \n')
        f1.write('  \n')
        f1.write('  \n')

        f1.close()
        j+=1
    return int(j)

#################################################################################
############################### Input Parameters ################################
#################################################################################
# Use as many descrete steps as needed
# Just remember to constantly increase j1, j2 ... and keep last j as jF

# Use fractional values (e.g. 100.0) only when step size < 1
j1 = loop(0.000001, 0.00001, 0.000001, j)    # very fine increment
j2 = loop(0.00001, 0.0001, 0.00001, j1)      # small increment
j3 = loop(0.0001, 0.01, 0.0001, j2)          # small increment
j4 = loop(0.05, 30.0, 0.05, j3)              # intermediate region (lots of resonances)
j5 = loop(30.1, 100.0, 0.1, j4)              # cold region (fractional increment)

# When step size > 1, do not use fractional values (e.g. 500)
j6 = loop(101, 500, 1, j5)                   # integer steps (high T/KE)
# keep last counter name jF
jF = loop(550, 1500, 50, j6)                 # large integer steps (very high T/KE)

#################################################################################
print("total number of files are %d" %(jF-1))
print("In bat.sh file use 'for k in 1..%d'" %(jF-1))
print("to run loop form 1 to %d" %(jF-1))
#############################################################
