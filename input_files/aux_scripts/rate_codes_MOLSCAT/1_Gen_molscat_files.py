
# Importing Libraries
import os
import math;

j = int(1) # counter for file name (Do not change)

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
        if (step < 1):
            energy = i * step
        else:
            energy = i

        f1.write('  &input ured = 1.94051, nnrg=1, energy=%.4f\n' %(energy))

        if (energy < 10):
            f1.write('   intflg=8, steps=100, rmin=1.5, rmax=50.0, BCYOMN=10000, \n')
        elif ( (energy > 10) and (energy < 30) ):
            f1.write('   intflg=8, steps=50, rmin=1.5, rmax=50.0, BCYOMN=10000, \n')
        else:
            f1.write('   intflg=8, steps=20, rmin=1.5, rmax=50.0, BCYOMN=10000, \n')

        f1.write("   label='H2-cncn system', jtotu = -1, \n")
        f1.write('   prntlv=1, isigpr=1, LASTIN = 1,\n')
        f1.write('/ \n')

        f1.write(' &basis itype=3,  j1max=37, j2min=0, j2max=2, j2step=2 \n')
        f1.write('    be= 0.1726,60.853,\n')
        f1.write('/ \n')
        f1.write(' &potl rm=1.0, epsil=1.0, mxlam=174, \n')
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

# Use fractional values only when step size < 1
j1 = loop (0.05, 30.0,  0.05, j)     # initial / final value / step size / counter
j2 = loop (30.1, 100.0, 0.1,  j1)    # initial / final value / step size / counter

# When step size > 1, do not use fractional values
j3 = loop (101,  200,   1,    j2)    # initial / final value / step size / counter
j4 = loop (210,  500,   25,   j3)    # initial / final value / step size / counter
j5 = loop (600,  900,   100,  j4)    # initial / final value / step size / counter
jF = loop (1000, 2500,  500,  j5)    # initial / final value / step size / counter

#################################################################################
# keep last counter name jF
print("total number of files are %d" %(jF-1))
print("In bat.sh file use 'for k in 1..%d'" %(jF-1))
print("to run loop form 1 to %d" %(jF-1))
#############################################################
