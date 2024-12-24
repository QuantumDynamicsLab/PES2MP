#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
# Various Psi4 custom calculation templates
# Make sure to --->
# 1. create table using R/theta(s)/phi coordinates
# 2. Use double curly brackets "{{RHF}}" for "{RHF}" in Input file
#                            --> python treats {} as special input
# 3. Use single quotes ('') inside double quotes ("") to avoid confusion
# 4. Get table templates from 1D/2D/4D psi4_custom files
#                --> R/Theta(s) variables are written in each input file
################################################################################

#------------------------------------------------------------------------------#
# Template for simple CCSD(T) caluclation with counterpoise correction
#------------------------------------------------------------------------------#
psi4_bsse = 'cp'      # counterpoise : 'cp' or None (update same below)
psi4_ext = """

memory 2 GB
set_num_threads(16)

set basis cc-pvtz
set reference rhf

# Comment Line | For psi4_bsse = None use | En = energy('ccsd(t)')
En = energy('ccsd(t)', bsse_type='cp',return_total_data=True)

# Comment Line | Print clean Table in bash (4D)
print('%.4f\t%.4f\t%.4f\t%.4f\t%.12f'%(R, Phi, Theta2, Theta1, En))
"""

#------------------------------------------------------------------------------#
# Template for simple CCSD(T) caluclation with CBS Expansion
#------------------------------------------------------------------------------#
psi4_bsse = None     # counterpoise : 'cp' or None (update same below)
psi4_ext = """

memory 2 GB
set_num_threads(16)

set reference rhf

En = energy('ccsd(t)/aug-cc-pv[tq5]z')

# Comment Line | Print clean Table in bash (4D)
print('%.4f\t%.4f\t%.4f\t%.4f\t%.12f'%(R, Phi, Theta2, Theta1, En))
"""

#------------------------------------------------------------------------------#
# Template for simple excited states using TDSCF
#------------------------------------------------------------------------------#
psi4_bsse = None      # counterpoise : 'cp' or None (update same below)
psi4_ext = """

memory 2 GB
set_num_threads(16)

set {{
tdscf_states 4
}}

En = energy('td-scf/cc-pvdz')

# Print clean Table in bash (1D)
print('%.4f\t%.12f\t%.12f\t%.12f\t%.12f'%(R, *En))
"""

#------------------------------------------------------------------------------#
# Template for internal MRCC (Multireference coupled cluster) calculation
#------------------------------------------------------------------------------#
psi4_bsse = None      # counterpoise : 'cp' or None (update same below)
psi4_ext  = """

memory 2 GB
set_num_threads(16)

set {{
     basis aug-cc-pVQZ
     reference rhf
}}
En = energy('psimrcc')

# Comment Line | Print clean Table in bash (2D)
print('%.4f\t%.4f\t%.12f'%(R, Theta, En))

"""

#------------------------------------------------------------------------------#
# Template for external MRCC (M. Kállay and J. Gauss) calculation with AVQZ
#------------------------------------------------------------------------------#
psi4_bsse = None      # counterpoise : 'cp' or None (update same below)
psi4_ext  = """

memory 2 GB
set_num_threads(16)

set {{
     basis aug-cc-pVQZ
     reference rhf
     qc_module mrcc
}}
En = energy('ccsdt(q)')

# Print clean Table in bash (4D)
print('%.4f\t%.4f\t%.4f\t%.4f\t%.12f'%(R, Phi, Theta2, Theta1, En))

"""

#------------------------------------------------------------------------------#
# Template for SAPT calculations (Use psi4_bsse = 'cp' to define fragments)
#------------------------------------------------------------------------------#
psi4_bsse = 'cp'      # counterpoise : 'cp' or None (update same below)
psi4_ext = """

memory 2 GB
set_num_threads(16)

set reference rhf
set basis cc-pvtz

En = energy('sapt0-ct')

# Print clean Table in bash (1D)
print('%.4f\t%.12f'%(R, En))
"""

#------------------------------------------------------------------------------#
# Template for energy calculations at various level of theories
#------------------------------------------------------------------------------#
molpro_ext = """

set reference rhf
set basis cc-pvtz

# CISD calculation with wavefn
cisd_e, cisd_wfn = energy('cisd', return_wfn=True)

# FCI calculation with CISD wavefn
fci_e = energy('fci', ref_wfn=cisd_wfn)

# Print clean Table in bash (1D)
print('%.4f\t%.12f\t%.12f'%(R, cisd_e, fci_e))
"""
#------------------------------------------------------------------------------#
