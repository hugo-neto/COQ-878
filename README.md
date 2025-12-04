# COQ-878
Quantum Computational Activity Repository

## PBL-01
Calculate the $\Delta E$ and $\Delta H$ of adsorption for the reactants and products involved in one of the pathway reactions of the water gas shift reaction catalyzed by Pt111.

## FinalWork
The final work will employ <b>Born–Oppenheimer Ab Initio Molecular Dynamics (AIMD)</b> to parametrize a <b>Machine Learning Force Field (MLFF)</b> for the Iβ-cellulose system. Two workflow options are considered. In the first workflow, raw AIMD data are generated using Density Functional Theory (DFT) within the <b>(N,V,T) ensemble</b> in VASP, providing ground-state energies and forces for each configuration. These data are then used to train an MLFF using MACE-MP-0. The second workflow relies exclusively on VASP for both the DFT calculations and the MLFF parametrization, also in the (N,V,T) ensemble. The selection of the final workflow will depend on the available computational time, with either method serving as a viable fallback in case issues arise. Ultimately, this study aims to obtain an MLFF capable of accurately predicting the mechanical response of cellulose under a range of external loads.