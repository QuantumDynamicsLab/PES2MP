''' Same as 3_molrates but more automated and generates rate coefficients data
 in BASECOL format. '''

import os
import sys
import math
import numpy as np
import scipy
from scipy import integrate
import pandas as pd
from tqdm import tqdm

# ------------------------ User Parameters ------------------------
tmax        = 100       # maximum temperature in kelvin
redm        = 3.8267    # reduced mass in amu

sigma_file  = "sigma.dat"
pair_e_file = "pair_E.dat"

################################################################################
# Which channels to include
dex_tr = True    # de-excitation transitions
exc_tr = False   # excitation transitions
el_tr  = False   # elastic transitions

max_J = 11      # maximum J_i (0 = all available transitions)

# Manual override of transitions (MOLSCAT labels) See 3_molrates.py to use them
manual_ji = []  # e.g. [2,3,4]
manual_jf = []  # e.g. [1,1,2]

################################################################################
# Label conversion flags (pick exactly one)
subtract_1 = True   # Most common case (subtract -1 from Molscat's N): x -> N-1
even_j1    = False  # Symmetric, I=0 and 1Sigma (C2) x -> 2*(N-1)
odd_j      = False  # Symmetric, I=0 and 3Sigma (C4) x -> 2*(N-1)+1

################################################################################
two_j2     = True  # x -> (x-1)/2 For Two states of H2/collider p(0,2) or o(1,3)
################################################################################

# Subtract internal energy only for de-excitation
sub_E = True

# Integration option (False = summation, True = Simpson)
use_integration = False

# ------------------------ Helpers ------------------------
def map_label(idx):
    """Convert Molscat index (1-based) to physical J."""
    if two_j2:
        idx = int(idx / 2)
    if odd_j:
        return 2*idx + 1
    if even_j1:
        return 2*idx
    if subtract_1:
        return idx
    return idx + 1

def rate_fname(ch):
    return f"k_{ch}.dat"

def sig_fname(ch):
    return f"sig_{ch}.csv"

def basecol_fname(ch):
    return os.path.join("basecol", f"basecol_{ch}.dat")

# ------------------------ Constants ------------------------
akb    = scipy.constants.Boltzmann             # J/K
uamu   = scipy.constants.physical_constants['unified atomic mass unit'][0]
invcmJ = scipy.constants.physical_constants['inverse meter-joule relationship'][0] * 100
avag   = scipy.constants.physical_constants['Avogadro constant'][0]
amu    = redm * uamu

# ------------------------ Read Data ------------------------
molout = np.loadtxt(sigma_file, skiprows=1)
pair_E  = np.loadtxt(pair_e_file)

# Build transition list
if manual_ji and manual_jf:
    if len(manual_ji) != len(manual_jf):
        sys.exit("manual_ji/jf lengths differ")
    transitions = list(zip(manual_ji, manual_jf))
else:
    all_j_raw = set(zip(molout[:,5].astype(int), molout[:,4].astype(int)))
    transitions = []
    for ji, jf in sorted(all_j_raw):
        # Skip even-numbered Ji or Jf in two_j2 case (i.e., skip alternate MOLSCAT Ji)
        if two_j2 and (ji % 2 == 0 or jf % 2 == 0):
            continue
        if   ji>jf and dex_tr and (max_J==0 or ji<=max_J):
            transitions.append((ji,jf))
        elif ji<jf and exc_tr and (max_J==0 or ji<=max_J):
            transitions.append((ji,jf))
        elif ji==jf and el_tr and (max_J==0 or ji<=max_J):
            transitions.append((ji,jf))

print(f"Total transitions selected: {len(transitions)}")

# Precompute temperature‐dependent constants
temps  = np.arange(1, tmax+1)
vel    = np.sqrt(8*akb*temps/(np.pi*amu)) * 1e2
prefac = vel * (akb*temps)**-2

# Ensure output dirs
os.makedirs("basecol", exist_ok=True)

# Prepare storage
rates   = {'dex':[], 'exc':[], 'elastic':[]}
basecol = {'dex':[], 'exc':[], 'elastic':[]}

# Main loop
for ji, jf in tqdm(transitions, desc="Transitions"):
    Ni = map_label(ji-1)
    Nf = map_label(jf-1)
    print(f"  Molscat levels {ji}->{jf}  →  N = {Ni}->{Nf}")

    if   ji>jf:  ch = 'dex'
    elif ji<jf:  ch = 'exc'
    else:        ch = 'elastic'

    mask = (molout[:,5].astype(int)==ji) & (molout[:,4].astype(int)==jf)
    sub  = molout[mask]
    Ecm = sub[:,0]
    sigma_cm2 = sub[:,6] * 1e-16

    if ch=='dex' and sub_E:
        Eint = pair_E[ji-1,1]
        Erel = (Ecm - Eint) * invcmJ
        good = Erel>0
        Erel = Erel[good]
        sigma_cm2 = sigma_cm2[good]
    else:
        Erel = Ecm * invcmJ

    karr = np.zeros_like(temps, dtype=float)
    if not use_integration:
        for i,T in enumerate(temps):
            karr[i] = prefac[i] * np.sum(sigma_cm2 * Erel * np.exp(-Erel/(akb*T))) / avag
    else:
        for i,T in enumerate(temps):
            integrand = sigma_cm2 * Erel * np.exp(-Erel/(akb*T))
            I = integrate.simpson(integrand)
            karr[i] = prefac[i] * I / avag

    rates[ch].append((ji,jf,karr))
    basecol[ch].append([ji, jf, 1, 1] + karr.tolist())

    # TO save labels in J format uncomment below line 
    #basecol[ch].append([map_label(ji-1), map_label(jf-1), 1, 1] + karr.tolist())

# Write per‐channel outputs
for ch, flag in [('dex',dex_tr), ('exc',exc_tr), ('elastic',el_tr)]:
    if not flag or not rates[ch]:
        continue

    arr = np.column_stack([temps] + [k for _,_,k in rates[ch]])
    hdr = 'T\t' + ''.join(f"{map_label(ji-1)}->{map_label(jf-1)}\t"
                          for ji,jf,_ in rates[ch])
    np.savetxt(rate_fname(ch), arr, header=hdr, comments='')

    sigd = {}
    for ji,jf,_ in rates[ch]:
        mask = (molout[:,5].astype(int)==ji) & (molout[:,4].astype(int)==jf)
        sub  = molout[mask]
        sigd[f"E_{ji}->{jf}"]   = pd.Series(sub[:,0])
        sigd[f"σ_{ji}->{jf}"]   = pd.Series(sub[:,6])
    pd.DataFrame(sigd).to_csv(sig_fname(ch), index=False)

    rows = basecol[ch]
    ncol = len(rows[0])
    fmt  = ['%d','%d','%d','%d'] + ['%.5e']*(ncol-4)
    header = 'I1 F1 I2 F2 ' + ' '.join(f"{T}" for T in temps)
    np.savetxt(basecol_fname(ch), rows, fmt=fmt, header=header, comments='')

# Write pair_E_levels.dat
with open('pair_E_levels.dat','w') as f:
    f.write("Level(I)\tEnergy (cm^-1)\tJ\n")
    for idx, (L, E) in enumerate(pair_E, start=1):
        # Skip even labels if two_j2 is True
        if two_j2 and (idx % 2 == 0):
            continue
        J = map_label(idx-1)
        f.write(f"{idx}\t{E:.8f}\t{J}\n")

print("All done.")


