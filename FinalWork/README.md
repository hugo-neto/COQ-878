# 1 - Folders
List of all folders

## MLFF_VASP
Contains the inputs and outputs files from the full VASP workflow

#### Running LOCAL
mpirun -np 1 vasp_std_gpu_mlff

#### Running CLUSTER
mpirun -np 1 vasp_std

#### Hardware
22 GB RAM <br>
3 GB GPU <br>

### MLFF1
AIMD and MLFF trainning <br>
Ensemble (NVT) <br>
Nosé-Hoover chain thermostat <br>
10.000 steps <br>
Temperature constant <br>

### MLFF2
AIMD only <br>
Ensemble (NVT) <br>
Nosé-Hoover chain thermostat <br>
25.000 steps <br>
Temperature ramp <br>
<b>NOTES: </b> Stopped in 10k because there wasn't a ramp

### MLFF3
AIMD + MLFF (Adaptative Sampling) <br>
Ensemble (NVT) <br>
Nosé-Hoover chain thermostat <br>
12.000 steps <br>
Temperature ramp 300-400 <br>

### MLFF4
AIMD only (AIMD Sampling) <br>
Ensemble (NVT) <br>
Nosé-Hoover chain thermostat <br>
12.000 steps <br>
Temperature ramp 300-400 <br>

## AIMD_Cellulose_300K_Test
Contains input file and outputs from a test simulation of cellulse in 300 K

## CluserATOMS
Contains input to carry out simulations in ATOMS cluster

## COQ-875-ISIF3
Contains the position file of IB-Cellulose obtained in COQ-875

## MD_VASP_Example
Lists all VASP examples

# 2 - Training MLFF from scratch
## 2.1 - Necessary files (from VASP example)
ICONST - NOT USED <br>
Constrains for each bonds.
KPOINTS - OK <br>
Parameters to specifie the Bloch vectors (k points) used to sample the Brillouin zone <br>
POSCAR - OK <br>
Initial position of your system (from your geometry optimization) <br>
POTCAR - OK <br>
File containing psceutopotentials for "C", "O" and "H" <br>
INCAR - OK <br>
Input parameters for the simulation <br>