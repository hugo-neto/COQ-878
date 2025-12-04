#!/usr/bin/env bash

mkdir MLFF_data

for i in {1..50}; do
   echo "test configuration " $i
   cp ../test_set/structures/POSCAR.${i} POSCAR
   mpirun -np 4 vasp_gam
   cp ./vaspout.h5 ./MLFF_data/vaspout_${i}.h5
done
