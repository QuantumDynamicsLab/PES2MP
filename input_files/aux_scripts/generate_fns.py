#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
# Python script to generate series of Slater exponential functions
################################################################################
import numpy as np
import sys

#------------------------------------------------------------------------------#
# Input Required (alpha * exp(-beta*x))
#------------------------------------------------------------------------------#
N_exp = 50

# automatic beta generation
beta_c = np.linspace(0.001, 5.0, N_exp)

# manual example:
# beta_c = [0.25, 1, 2, 3]

#------------------------------------------------------------------------------#
# Checks
#------------------------------------------------------------------------------#
print("Input has :", N_exp, "Slater functions")
print("          {} beta coefficients\n".format(len(beta_c)))

if len(beta_c) < N_exp:
    print("Error! Increase beta coefficients to :", N_exp)
    sys.exit()

elif len(beta_c) > N_exp:
    print("Warning! Number of beta coefficients =", len(beta_c))
    print("Using first", N_exp, "terms.")
    beta_c = beta_c[:N_exp]

#------------------------------------------------------------------------------#
# Generate fnfit_custom
#------------------------------------------------------------------------------#
print("def fnfit_custom(x", end='')
for i in range(1, N_exp + 1):
    print(f", a{i}", end='')
    if i % 17 == 0:
        print(" \\\n                ", end='')
print("):")

print("    import numpy as np")
print("    return ", end='')

for i in range(1, N_exp + 1):
    term = f"a{i}*np.exp(-{beta_c[i-1]:.6f}*x)"
    if i != N_exp:
        print(term + " + ", end='')
    else:
        print(term)

    if i % 4 == 0 and i != N_exp:
        print("\\")
        print("           ", end='')

print("\n")

#------------------------------------------------------------------------------#
# Initial guess
#------------------------------------------------------------------------------#
print(f"initial_val = [1e4]*{N_exp}")

#------------------------------------------------------------------------------#
# Matching N_Vals for PES2MP
#------------------------------------------------------------------------------#
n_vals = [-float(f"{b:.6f}") for b in beta_c]

print("N_Vals =", n_vals)