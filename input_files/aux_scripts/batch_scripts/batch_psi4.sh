#!/bin/bash 

# scratch dir information
mkdir ${PWD}/psi4_tmp
export PSI_SCRATCH=/${PWD}/psi4_tmp

cd Psi4_custom

for k in {0..118}
do 
psi4 $k.inp
done 


