#python file to get rates for single transition
import re
import os
import scipy
import math
import numpy as np

path = os.getcwd()

tmax = 500    # in kelvin
redm = 1.9354 # in amu
si_n = 10      # skips sigma for every nth element

molout = np.loadtxt("2-0.dat")    # input file (molscat output) without header
molout = molout[::si_n]              

#print(molout)
#molout = np.loadtxt("2-0.dat",skiprows=1) # use this for input file with header

fr = f"k20py_{si_n}.dat"                  # output file using summation 
fr_int = f"k20pyint_{si_n}.dat"           # output file using scipy integration

akboltz = scipy.constants.Boltzmann    # boltzmann const in J K-1
uamu = scipy.constants.physical_constants['unified atomic mass unit'][0]
inv_cm_j = scipy.constants.physical_constants['inverse meter-joule relationship'][0]*100
avaga = scipy.constants.physical_constants['Avogadro constant'][0]

amu = redm*uamu

energ = molout[:,0]  
sigma = molout[:,6]

en_j = energ*inv_cm_j       # energy convtd to joule units
cr_cm2 = sigma * 1e-16      # sigma convtd to cm2 units from ang2

j_i = molout[:,5].astype(int)  # initial rotational level 
j_f = molout[:,4].astype(int)  # final rotational level 

arelvel = np.zeros(tmax)
const = np.zeros(tmax)
rate = np.zeros(tmax)
rate_int = np.zeros(tmax)
for tp in range (1,tmax+1,1):    # For decimal temp increase tmax to 10 times and uncomment below line
    #tp = tp/10.0
    arelvel[tp-1] = (math.sqrt((8*akboltz*tp)/(np.pi*amu)))*1e2 # relative velocity  in cm/s
    const[tp-1] = arelvel[tp-1]*math.pow((akboltz*tp),-2)                  # pre integration constant

# rate by summation
for tp in range (1,tmax+1,1):
    summ = 0.0
    for i in range (len(molout)):
        expont = math.exp(-en_j[i]/(akboltz*tp))
        summ += (cr_cm2[i]*en_j[i]*expont)
    rate[tp-1] = const[tp-1]*summ/avaga              # rate = (const*summ)/(mol-1)     
temp = np.arange(1,tmax+1)
arr = np.stack((temp, rate), axis=1)            
np.savetxt(fr,arr)

# rate by integration

def integrand(e_j, sigma, t):
    akboltz = scipy.constants.Boltzmann    # boltzmann const in J K-1
    return sigma*en_j*np.exp(-e_j/(akboltz*t))

#res = integrand(en_j,cr_cm2,1)

#I1 = scipy.integrate.romb(res)
#I11 = scipy.integrate.cumulative_simpson(res)
#I = scipy.integrate.cumulative_trapezoid(res)
#I2 = scipy.integrate.trapezoid(res)
#I3 = scipy.integrate.simpson(res)

#print('romb\t',I1,I1*const[0]/avaga)
#print('cutrap\t',I,I*const[0]/avaga)
#print('cusimps\t',I11,I11*const[0]/avaga)
#print('trapez\t',I2,I2*const[0]/avaga)
#print('simpson\t',I3,I3*const[0]/avaga)

#summ = 0.0
#for i in range (len(molout)):
#    expont = math.exp(-en_j[i]/(akboltz*1)) # tp=1
#    summ += (cr_cm2[i]*en_j[i]*expont)   
#print('exact\t',summ,summ*const[0]/avaga)

# integration using composite Simpson's rule
for tp in range (1,tmax+1,1):
    res = integrand(en_j,cr_cm2,tp)
    I = scipy.integrate.simpson(res)
    rate_int[tp-1] = const[tp-1]*I/avaga
temp = np.arange(1,tmax+1)
arr_int = np.stack((temp, rate_int), axis=1)            
np.savetxt(fr_int,arr_int)



