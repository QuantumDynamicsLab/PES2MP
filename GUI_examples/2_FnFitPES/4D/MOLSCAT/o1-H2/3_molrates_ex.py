''' python file to get rates for all/selected transitions '''

# importing libraries
import re
import os
import sys
import scipy
import math
import numpy as np
import pandas as pd
from tqdm import tqdm

path = os.getcwd()
##################################################################################
#################### Input parameters (make changes here) ########################
##################################################################################
#--------------------------------------------------------------------------------#
tmax = 50    # maximum temperature in kelvin
redm = 1.8596 # reduced mass in amu
#--------------------------------------------------------------------------------#
# File name for input (extract using result_extract_molscat.py)
sigma_file = "sigma.dat"   # name of the (extracted) file containing cross-sections
#--------------------------------------------------------------------------------#
# File names for output (will contain rate coefficients till tmax)
fr = f"k_ex.dat"           # output rate file using summation method
fr_int = f"kint_ex.dat"    # output rate file using scipy integration
sig_out = "sig_ex.csv"     # output cross-section file for selected transitions
#--------------------------------------------------------------------------------#
# transitions required! Set all_tr to false and select initial and final j
all_tr = False    # calculate all transitions (not recommended: keep false)

# molscat labels start from 1 (dont give ji/jf values with 0) [see templates below]
ji = [1 ,1, 2, 3]     # use labels same as for molscat
jf = [2, 3, 3, 4]     # 1->2, 1->3, 2->3 and 3->4 

#--------------------------------------------------------------------------------#
# Remember molscat starts j from 1. Change labels to rotational states as shown:
# To keep labels as it is, set both of them False.

# For He and H2 (P0: J=0 and O1: J=1) set    subtract_1 = True and even_j = False
# Only for case: H2 (P2) i.e. (J=0,2) set    subtract_1 = False and even_j = True

#--------------------------------------------------------------------------------#
# change label (x-1) to convert 1 to 0 and so on. (He and 1 rotational state of H2)
subtract_1 = False       # 1-->0, 2-->1 , 3-->2, etc...
#--------------------------------------------------------------------------------#
# Special Cases

# For cases when only even states are present for cases with I=0 like C2, C3 etc. 
# Subtracting -1 from States and doubling to give J (Keep subtract_1 = False)
even_j1    = True        # 1-->0, 2-->2 , 3-->4, etc...

# change label (x-1)/2) (case where 2 rotational state of H2 are included in basis)
# Subtracting -1 from States and halving to give J (Keep subtract_1 = False)
two_j2     = False       # 1-->0, 2-->2 , 3-->4, etc...
#--------------------------------------------------------------------------------#

# subtract energy: take relative energy for (de-excitation transitions/ortho_H2)
sub_E = True   # If true, rotational energy (from pair_E file) is subtracted
pair_E = np.loadtxt("pair_E_o.dat")  # name for the file containing rotational energy
####################################################################################
# Example template for de-excitation delta j=1 (first 20 transitions)
#ji = np.arange(2,21,1)    # 2 to 20       [2,3,4,.....,19,20]
#jf = np.arange(1,20,1)    # 1 to 19       [1,2,3,.....,18,19]

# template for excitation delta j=1
#ji = np.arange(1,20,1)    # 1 to 19      [1,2,3,.....,18,19]
#jf = np.arange(2,21,1)    # 2 to 20      [2,3,4,.....,19,20]

# template for de-excitation delta j=2
#ji = np.arange(3,21,1)    # 3 to 20      [3,4,5,.....,19,20]
#jf = np.arange(1,19,1)    # 1 to 19      [1,2,3,.....,17,18]

# template for excitation delta j=2
#ji = np.arange(1,19,1)    # 1 to 19      [1,2,3,.....,17,18]
#jf = np.arange(3,21,1)    # 3 to 20      [3,4,5,.....,19,20]

# template for specific transitions
#ji = [1,1,1,2,3]         # example transitions like 1-1, 1-2, 1-3, 2-1 and 3-1
#jf = [1,2,3,1,1]         #
####################################################################################
########################### Input parameters end ###################################
####################################################################################


molout = np.loadtxt(sigma_file, skiprows=1)   # file containing cross-sections

akboltz = scipy.constants.Boltzmann    # boltzmann const in J K-1
uamu = scipy.constants.physical_constants['unified atomic mass unit'][0]
inv_cm_j = scipy.constants.physical_constants['inverse meter-joule relationship'][0]*100
avaga = scipy.constants.physical_constants['Avogadro constant'][0]

amu = redm*uamu
# extract cross-sections for specific transition (j_i --> j_f)
arelvel = np.zeros(tmax)
const = np.zeros(tmax)

j_i = molout[:,5].astype(int)  # initial rotational level
j_f = molout[:,4].astype(int)  # final rotational level

rate = np.zeros(tmax)
rate_int = np.zeros(tmax)
temp = np.arange(1,tmax+1)

for tp in range (1,tmax+1,1):    # For decimal temp increase tmax to 10 times and uncomment below line
    #tp = tp/10.0
    arelvel[tp-1] = (math.sqrt((8*akboltz*tp)/(np.pi*amu)))*1e2 # relative velocity  in cm/s
    const[tp-1] = arelvel[tp-1]*math.pow((akboltz*tp),-2)                  # pre integration constant

if all_tr:
    ji = []
    jf = []
    for i in range (1, max(j_i)+1):         # loop over j_i
        for j in range (1, max(j_f)+1):     # loop over j_i
            ji = np.append(ji,i)
            jf = np.append(ji,j)
    print("Total Transitions:", len(ji))

else:
    if (len(ji) != len(jf)):
        print ("Error! length of ji must be equal to jf")
        print("ji = ", len(ji), "and jf = ", len(jf))
        print("Exiting the program...")
        sys.exit(0)
    else:
        print("Total Transitions:", len(ji))

header_x = 'T\t'
header_y = []
for i in range (len(ji)):
    header_y += ['E (cm-1)']
    if ( subtract_1 == True or (even_j1 == True and two_j2 == True) ):
        i == 0 and print("\n Subtracting -1 from States to give J \n ")
        header_x += "%d->%d\t"%(ji[i]-1,jf[i]-1)
        header_y += ["%d->%d\t"%(ji[i]-1,jf[i]-1)] 
    elif even_j1 == True:
        i == 0 and print("\n Subtracting -1 from States and doubling to give J \n ")
        header_x += "%d->%d\t"%((ji[i]-1)*2,(jf[i]-1)*2)
        header_y += ["%d->%d\t"%((ji[i]-1)*2,(jf[i]-1)*2)]
    elif two_j2 == True:
        i == 0 and print("\n Subtracting -1 from States and halving to give J \n ")
        header_x += "%d->%d\t"%((ji[i]-1)/2,(jf[i]-1)/2)
        header_y += ["%d->%d\t"%((ji[i]-1)/2,(jf[i]-1)/2)]
    else:
        i == 0 and print("\n Keeping States as it is: \n The resulting Quantum States (N) may or may not represent J \n ")
        header_x += "%d->%d\t"%(ji[i],jf[i])
        header_y += ["%d->%d\t"%(ji[i],jf[i])]
ct1=0
ct2=0
for i in tqdm(range (len(ji))):         # loop over j_i
    ctt=0
    # Check for existing transitions in molout
    transition_found = False
    for k in range (len(molout)):   # loop over input file rows
        if (int(molout[k,5]) == ji[i] and int(molout[k,4]) == jf[i]):
            transition_found = True
            if ctt==0:
                molout_i = molout[k]
                ctt=1
            else:
                molout_i = np.vstack([molout_i, molout[k]])
    if not transition_found:
        raise ValueError(f"Transition {ji[i]}->{jf[i]} does not exist in {sigma_file}! ")

    #print("Transition No: ", i)
    #print(len(molout_i))
    #sys.exit(0)
    # specific transition data is stored in molout_i
    sigma = molout_i[:,6]
    cr_cm2 = sigma * 1e-16          # sigma convtd to cm2 units from ang2
    energ = molout_i[:,0]

    if sub_E == True:
        mask = (pair_E[:, 0] == ji[i])
        if not np.any(mask):
            raise ValueError(f"Energy entry for ji={ji[i]} not found in pair_E.dat")
        E_ji = pair_E[mask, 1][0]  # Extract energy value
        print(f"Subtracting {E_ji} corresponding to ji={ji[i]}: Total Energies --> Kinetic Energies!")
        en_j = (energ-E_ji)*inv_cm_j
        neg_val_index = np.where(en_j <= 0)
        en_j = np.delete(en_j, neg_val_index)
        cr_cm2 = np.delete(cr_cm2, neg_val_index)
    else:
        en_j = energ*inv_cm_j       # energy convtd to joule units
    n_mol = len(en_j) # total number of energy units
    j_i = molout_i[:,5].astype(int)  # initial rotational level
    j_f = molout_i[:,4].astype(int)  # final rotational level

    # rate by summation
    for tp in range (1,tmax+1,1):
        summ = 0.0
        for ik in range (n_mol):
            expont = math.exp(-en_j[ik]/(akboltz*tp))
            summ += (cr_cm2[ik]*en_j[ik]*expont)
        rate[tp-1] = const[tp-1]*summ/avaga              # rate = (const*summ)/(mol-1)
    if ct1==0:
        arr = np.stack((temp, rate), axis=1)
        if sub_E == True:
            arr_sigma = [(energ-E_ji), sigma]
        else:
            arr_sigma = [energ, sigma]
        ct1=1
    else:
        arr = np.c_[arr, rate]
        if sub_E == True:
            arr_sigma += [(energ-E_ji), sigma]
        else:
            arr_sigma += [energ, sigma]


    # rate by integration
    def integrand(e_j, sigma, t):
        akboltz = scipy.constants.Boltzmann    # boltzmann const in J K-1
        return sigma*e_j*np.exp(-e_j/(akboltz*t))

    for tp in range (1,tmax+1,1):
        res = integrand(en_j,cr_cm2,tp)
        I = scipy.integrate.simpson(res, x=en_j)
        rate_int[tp-1] = const[tp-1]*I/avaga
    if ct2==0:
        arr_int = np.stack((temp, rate_int), axis=1)
        ct2=1
    else:
        arr_int = np.c_[arr_int, rate_int]


np.savetxt(fr,arr,header=header_x,comments='')
np.savetxt(fr_int,arr_int,header=header_x,comments='')

df_list = pd.DataFrame({ i:pd.Series(value) for i, value in enumerate(arr_sigma) })
df_list.to_csv(sig_out,header=header_y,index=False)
