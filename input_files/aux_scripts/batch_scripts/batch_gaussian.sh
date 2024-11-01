#!/bin/bash 

# Load Gaussian with scratch dir information
. /home/dummy_path/g16_lin/gaussian_vars_16.sh

cd Gaussian_CP

for k in {0..7237}
do 
g16 $k.gjf
done 


