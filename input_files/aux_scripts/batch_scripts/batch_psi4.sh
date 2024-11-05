#!/bin/bash 

# scratch dir information (change if needed! and delete after done!)
mkdir ${PWD}/psi4_tmp
export PSI_SCRATCH=/${PWD}/psi4_tmp

cd psi4_custom

for k in {0..118}
do 
psi4 $k.inp >> ../PES.dat
done 


