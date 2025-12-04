#!/usr/bin/env bash
file=PCDAT
awk <$file >PCDAT.xy '
NR==8 { pcskal=$1}
NR==9 { pcfein=$1}
NR==7 { npaco=$1}
NR>=13 {  
  line=line+1
  if (line==1) s=s+1
  if (line==(npaco+1))  {
     print " "
     line=0
  }
  else  {
     a1[line]=  a1[line] + $1
     a2[line]=  a2[line] + $2
     a3[line]=  a3[line] + $3
     a4[line]=  a4[line] + $4
     print (line-0.5)*pcfein/pcskal,$1,$2, $3, $4, $5
  }
}
'
