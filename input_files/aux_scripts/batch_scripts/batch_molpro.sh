#!/bin/bash 
mkdir ${PWD}/molpro_tmp

export TMPDIR="/${PWD}/molpro_tmp" 
export TMPDIR4="/${PWD}/molpro_tmp"

cd Molpro_CP 

for k in {0..7237}
do 
/usr/local/molpro/dummy_location/bin/molpro -n 16 $k.inp 
done 

# export TMPDIR : choose temp directory
# go into input file directory : cd Molpro_CP or cd Molpro_CBS
# replace /usr/local/molpro/dummy_location/bin/molpro with molpro executable path
#  -n 16 defines number of processor
# loop runs from 7237 to 0 with step of -1 

