#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
# Python script to generate series of Slater functions
################################################################################
import numpy as np
import sys
#------------------------------------------------------------------------------#
# Input Required (alpha*e^{-beta*x} # x is R)
#------------------------------------------------------------------------------#

N_exp  = 4                          # number of exponential functions
beta_c = np.linspace(0.1, 5, N_exp) # beta coeff range (automatic generation)
                                    # initial value, final value, no. of points

# beta_c = [-0.25,-1,-2,-3]         # beta coeff range (manual input)

#------------------------------------------------------------------------------#
# Program/script/code/wizardry
#------------------------------------------------------------------------------#

print("Input has :", N_exp, "Slater functions and ")
print("          {} beta coefficients \n".format(len(beta_c)))

if (len(beta_c) < N_exp):
    print("Error! Increase number of :", len(beta_c))
    sys.exit()
elif (len(beta_c) > N_exp):
    print("Warning! Number of beta coefficients: ", len(beta_c))
    print(" are larger than N_exp Using first ", N_exp, " terms.")
else:
    pass

print("def fnfit_custom(x ", end='')
for i in range (1, N_exp+1):
    print(",a{}".format(i), end='')
    if (i%17==0):
        print(" \\\n                ", end='')
print("):", end=' ')

print("\n    import numpy as np ", end=' ')
print("\n    return", end=' ')
for i in range (1, N_exp):
    print("a{}*np.exp(-{:.4f}*x) + ".format(i, beta_c[i-1]), end=' ')
    if (i%4 == 0):
        print("\\\n    ", end=' ')
print("a{}*np.exp(-{:.4f}*x) ".format(N_exp, beta_c[N_exp-1]), end=' ')
print("\n")

print("initial_val  = [1e4]*{}".format(N_exp))

#------------------------------------------------------------------------------#

