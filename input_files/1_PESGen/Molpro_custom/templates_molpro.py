#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
# Various Molpro custom calculation templates for MRCI/special calculations
# Make sure to --->
# 1. create table using R/theta(s)/phi coordinates
# 2. Use double curly brackets "{{RHF}}" for "{RHF}" in Input file
#                           --> python treats {} as special input
################################################################################

#------------------------------------------------------------------------------#
# Template for simple CCSD-F12a calculation with AVQZ
#------------------------------------------------------------------------------#
molpro_ext = """
basis = AVQZ

{{RHF}}
E_HF = energy

{{CCSD-F12a}}
E_CC = energy

table,R,$E_HF,$E_CC     ! 2D: R,Theta    ! 4D: R,Phi,Theta2,Theta1
digits,2,10,10

"""

#------------------------------------------------------------------------------#
# Template for simple excited states using MRCI
#------------------------------------------------------------------------------#
molpro_ext = """
basis = AVQZ

{{RHF}}                 ! Use wf card if needed! e.g. {{hf;wf,xx,xx,xx;}}
{{Multi; STATE,3}}
{{MRCI; STATE,3}}       ! {{ci;occ,xx,xx,xx;wf,xx,xx,xx;}}

E1 = energy(1)
E2 = energy(2)
E3 = energy(3)

table,R,$E1,$E2,$E3     ! 2D: R,Theta    ! 4D: R,Phi,Theta2,Theta1
digits,2,10,10,10

"""


#------------------------------------------------------------------------------#
# Template for SAPT calculations
#------------------------------------------------------------------------------#
molpro_ext = """
basis = AVQZ

!wf records
ca=2101.2
cb=2102.2
                  ! Consider e.g. C2H2 (H-C-C-H) - HCl collision
!monomer RR1      ! Numbering(as provided in RR1/RR2): H1, C2, C3, H4 - H5, Cl6
dummy,H5,Cl6      ! replace with your RR2 atom list
{hf; save,$ca}
sapt;monomerRR1

!monomer RR2
dummy,H1, C2, C3, H4                  ! replace with your RR1 atom list
{hf; start,atdens; save,$cb}
sapt;monomerRR2

!interaction contributions
sapt;intermol,ca=$ca,cb=$cb

elst(i)=E1pol;  exch(i)=E1ex
ind(i)=E2ind;   exind(i)=E2exind
disp(i)=E2disp; exdisp(i)=E2exdisp
etot(i)=E12tot

! Replace table, :: 2D: R,Theta  |  4D: R,Phi,Theta2,Theta1
table,R,elst,exch,ind,exind,disp,exdisp,etot
digits,2,10,10,10,10,10,10,10

"""



#------------------------------------------------------------------------------#
# Template for energy calculations at various level of theories
#------------------------------------------------------------------------------#
molpro_ext = """

basis = AVQZ

rhf
Eref = energy

rci                                    !CISD using MRCI code
E1 = energy

rcepa(1)                               !cepa-1 using MRCI code
E2 = energy

rcisd                                  !CISD using special closed-shell code
E3 = energy

rccsd(t)                               !coupled-cluster CCSD(T)
E4 = energy

!fci                                   !full CI -- Way too expensive

table,R,$Eref,$E1,$E2,$E3,$E4     ! 2D: R,Theta    ! 4D: R,Phi,Theta2,Theta1
digits,2,10,10,10,10,10

"""

#------------------------------------------------------------------------------#
# Template for chemical shielding tensors σ and a summary of the chemical shifts
#------------------------------------------------------------------------------#
molpro_ext = """

! basis = VDZ
basis={
default,cc-pVDZ
set,mp2fit
default,vdz/mp2fit
set,jkfit
default,vdz/jkfit
}

df-hf,df_basis=jkfit
df-lmp2,df_basis=mp2fit
nmrshld;comp


table,R,$Eref,$E1,$E2,$E3,$E4     ! 2D: R,Theta    ! 4D: R,Phi,Theta2,Theta1
digits,2,10,10,10,10,10

"""

#------------------------------------------------------------------------------#
################################################################################
