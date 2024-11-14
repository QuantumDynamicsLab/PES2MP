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

N_exp  = 4                            # number of pair exponential functions
beta_c = np.linspace(5, 0.2, N_exp) # beta coeff range (automatic generation)
                                      # initial value, fin value, no. of points

diff_c = [0.05,0.1]*2                # Difference between pair coefficients
                                      # alternate difference of 0.05 and 0.1
#------------------------------------------------------------------------------#
# Program/script/code/wizardry
#------------------------------------------------------------------------------#

print("Input has :", N_exp, "pairs of Slater functions and ")
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
    ci = beta_c[i-1]
    di = diff_c[i-1]
    print("a{}*(np.exp(-{:.4f}*x) - np.exp(-{:.4f}*x)) + ".format(i, ci, ci-di), end=' ')
    if (i%2 == 0):
        print("\\\n    ", end=' ')
print("a{}*(np.exp(-{:.4f}*x) - np.exp(-{:.4f}*x)) ".format(N_exp, beta_c[N_exp-1],beta_c[N_exp-1] - diff_c[N_exp-1]), end=' ')
print("\n")

print("initial_val  = [1e4]*{}".format(N_exp))

#------------------------------------------------------------------------------#
