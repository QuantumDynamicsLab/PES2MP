#python file to get rates for all transitions
import re
import os
import sys
import scipy
import math
import numpy as np
# loop for each angle subdirectory

path = os.getcwd()
####################################################################################
tmax = 200    # in kelvin
redm = 1.9354 # in amu

#molout = np.loadtxt("2-0.dat",skiprows=1) # use for labeled output
molout = np.loadtxt("sigma.dat") 
fr = f"k20py.dat"                  # output file using summation (f90 method)
fr_int = f"k20pyint.dat"           # output file using scipy integration

# transitions required! Set all_tr to false and select initial and final j
all_tr = False    # calculate all transitions in the input file 

ji = np.arange(1,4,1)     # 1 to 3      [1,2,3]
jf = np.arange(2,5,1)     # 2 to 4      [2,3,4]

# Remember :: molscat starts j from 1.
# change lebel by using below template (there are two options)
subtract_1 = True       # 1-->0, 2-->1 , 3-->2, etc...
even_j     = False      # 1-->0, 2-->2 , 3-->4, etc...

# subtract energy: take relative energy for de-excitation
pair_E = np.loadtxt("pair_energy.dat") 
sub_E = False

####################################################################################
# template for de-excitation delta j=1 (first 20 transitions)
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
#ji = [1,1,1,1,1]
#jf = [1,2,3,4,5]
####################################################################################

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
for i in range (len(ji)):
    if subtract_1 == True and even_j == False:
        header_x += "%d->%d\t"%(ji[i]-1,jf[i]-1)
    elif subtract_1 == True and even_j == True:
        header_x += "%d->%d\t"%((ji[i]-1)*2,(jf[i]-1)*2)
    else:
        pass
ct1=0
ct2=0 
for i in range (len(ji)):         # loop over j_i
    ctt=0 
    for k in range (len(molout)):   # loop over input file rows
        if (int(molout[k,5]) == ji[i] and int(molout[k,4]) == jf[i]):
            if ctt==0:
                molout_i = molout[k]
                ctt=1
            else:
                molout_i = np.vstack([molout_i, molout[k]])
    print("Transition No: ", i)
    #print(molout_i)
    # specific transition data is stored in molout_i
    n_mol = len(molout_i) # total number of energy units
    energ = molout_i[:,0]  
    sigma = molout_i[:,6]
    if sub_E == True:
        en_j = (energ-pair_E[ji[i],5])*inv_cm_j
    else:
        en_j = energ*inv_cm_j       # energy convtd to joule units
    cr_cm2 = sigma * 1e-16          # sigma convtd to cm2 units from ang2
    
    j_i = molout_i[:,5].astype(int)  # initial rotational level 
    j_f = molout_i[:,4].astype(int)  # final rotational level 
    
    # rate by summation
    for tp in range (1,tmax+1,1):
        summ = 0.0
        for i in range (n_mol):
            expont = math.exp(-en_j[i]/(akboltz*tp))
            summ += (cr_cm2[i]*en_j[i]*expont)
        rate[tp-1] = const[tp-1]*summ/avaga              # rate = (const*summ)/(mol-1)     
    if ct1==0:
        arr = np.stack((temp, rate), axis=1)   
        ct1=1
    else:
        arr = np.c_[arr, rate]      


    # rate by integration
    def integrand(e_j, sigma, t):
        akboltz = scipy.constants.Boltzmann    # boltzmann const in J K-1
        return sigma*en_j*np.exp(-e_j/(akboltz*t))

    for tp in range (1,tmax+1,1):
        res = integrand(en_j,cr_cm2,tp)
        I = scipy.integrate.simpson(res)
        rate_int[tp-1] = const[tp-1]*I/avaga
    if ct2==0:
        arr_int = np.stack((temp, rate_int), axis=1)   
        ct2=1
    else:
        arr_int = np.c_[arr_int, rate_int]  

            
np.savetxt(fr,arr,header=header_x)
np.savetxt(fr_int,arr_int,header=header_x)
        
        
