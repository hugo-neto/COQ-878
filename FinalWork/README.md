# Downloading repository

```bash
# Clone the repository
git clone https://github.com/hugo-neto/COQ-878.git
cd COQ-878
```

If you have a SSH key

```bash
# Clone the repository with SSH key
git clone git@github.com:hugo-neto/COQ-878.git
cd COQ-878
```

# Folders
List of all folders

## MLFF Folders

<b>NOTE:</b> The MLFF5 and MLFF6 were used to write the final work!

### MLFF5 - MACE
AIMD only (foundation models) <br>
Ensemble (NVT) <br>
Langevin thermostat <br>
80.000 steps <br>
0,5 ps / step
Fixed Temperature in 300 K <br>

### MLFF6 - VASP
AIMD + MLFF (Adaptative Sampling) <br>
Ensemble (NVT) <br>
Langevin thermostat <br>
80.000 steps <br>
0,5 ps / step
Fixed Temperature in 300 K <br>
Flexibilized creteria <br>

--- 

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

### NOTE1
After meeting with Elvis, the best option to avoid high time consuming it is to carry out simulations using the foundation models of MACE

--- 

## AIMD_Cellulose_300K_Test
Contains input file and outputs from a test simulation of cellulse in 300 K

## CluserATOMS
Contains input to carry out simulations in ATOMS cluster

## COQ-875-ISIF3
Contains the position file of IB-Cellulose obtained in COQ-875

## MD_VASP_Example
Lists all VASP examples

# Running VASP in Therminal
Contains the inputs and outputs files from the full VASP workflow

#### Running LOCAL
```bash
# Running VASP in therminal with GPU - Local Machine
mpirun -np 1 vasp_std_gpu_mlff
```

#### Running CLUSTER
```bash
# Running VASP in therminal with GPU - Cluster
mpirun -np 1 vasp_std
```

#### Hardware for VASP (Adaptative Sampling)
- 22 GB RAM <br>
- 3 GB GPU <br>

---