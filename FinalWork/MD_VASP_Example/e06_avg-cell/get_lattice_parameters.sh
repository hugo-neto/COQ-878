#!/bin/bash

if test -f lv.dat
then
  rm lv.dat
  rm lr1.dat lr2.dat lr3.dat lr.dat
fi

step=1

while [ $step -le 3 ]
do
  if test -f run$step/REPORT
  then
    grep LV run$step/REPORT |awk '{print $3}' >> lv.dat
    grep LR run$step/REPORT |awk '{if (NR%3==1) {print $3}}' >> lr1.dat
    grep LR run$step/REPORT |awk '{if (NR%3==2) {print $3}}' >> lr2.dat
    grep LR run$step/REPORT |awk '{if (NR%3==0) {print $3}}' >> lr3.dat
    grep LR run$step/REPORT |awk '{print $3}' >> lr.dat
  fi
  let step=step+1
done

avR1=$(awk 'BEGIN {a=0.} {a+=$1} END {printf("%12.16f\n",a/NR)}' lr1.dat )
avR2=$(awk 'BEGIN {a=0.} {a+=$1} END {printf("%12.16f\n",a/NR)}' lr2.dat )
avR3=$(awk 'BEGIN {a=0.} {a+=$1} END {printf("%12.16f\n",a/NR)}' lr3.dat )
avR=$(awk 'BEGIN {a=0.} {a+=$1} END {printf("%12.16f\n",a/NR)}' lr.dat )

av=$(awk 'BEGIN {a=0.} {a+=$1} END {printf("%12.16f\n",a/NR)}' lv.dat )

echo "            volume:" $av "A^3"
echo "      lat. vect. 1:" $avR1 "A"
echo "      lat. vect. 2:" $avR2 "A"
echo "      lat. vect. 3:" $avR3 "A"
echo "average lat. vect.:" $avR "A"
