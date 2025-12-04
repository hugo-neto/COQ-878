#!/usr/bin/env bash

for rcut in 12.0 13.0 14.0
do
  echo "RCUT1" $rcut
  # make INCAR file on-the-fly
  cat << EOF > INCAR
ML_LMLFF  = TRUE
ML_MODE   = refit
ML_RCUT1  = ${rcut}
KSPACING  = 300
EOF
  mpirun -np 4 vasp_gam
  cp ML_LOGFILE ML_LOGFILE_${rcut}
  cp ML_FFN ML_FF_${rcut}
done
