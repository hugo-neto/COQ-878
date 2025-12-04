#!/usr/bin/env bash

rm training_error.dat
# write header to file
echo "# rcut  energy        force         stress " > training_error.dat
for rcut in 12.0 13.0 14.0
do
   # extract energy, force, stress training-set 
   # errors from ML_LOGFILE and 
   # write to output file
   grep ERR ML_LOGFILE_${rcut} | tail -n 1 | awk -v r=${rcut} '{print r, $3, $4, $5}' 
done >> training_error.dat
