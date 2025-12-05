# %% [markdown]
# # Geometry Optimization using VASP and ASE
# 
# Author: PhD. Hugo de Lacerda Coutinho Neto
# 
# Contact: [hneto@peq.coppe.ufrj.br](mailto:hneto@peq.coppe.ufrj.br) - [Programa de Engenharia Química, PEQ/COPPE, UFRJ, Brasil](https://www.peq.coppe.ufrj.br/)
# 
# Cod. Ref.: [Prof. Elvis do A. Soares](https://github.com/elvissoares) 
# 
# ---

# %% [markdown]
# Importando variáveis do VASP

# %% [markdown]
# # Importing libraries

# %%
import os
# Definindo o path para os arquivos de potencial de pseudopotenciais do VASP
# Certifique-se de que o caminho esteja correto para o seu sistema
os.environ['VASP_PP_PATH'] = '/home/public/Programs/vasp.6.5.1/pp'
os.environ['ASE_VASP_COMMAND'] = 'mpirun -np 1 vasp_std'
os.environ['NO_STOP_MESSAGE'] = '1' # to avoid warning from mpirun

# %%
import numpy as np
import matplotlib.pyplot as plt

from ase import Atoms, Atom
from ase.build import molecule
from ase.io import write, read
from ase.calculators.vasp import Vasp      # Importando o VASP calculator do ASE

from ase.visualize.plot import plot_atoms
from ase.visualize import view

from ase.constraints import FixAtoms, FixCartesian
from ase.geometry import cellpar_to_cell   # Convert cell parameters to cell vectors

from ase.vibrations import Vibrations

# %% [markdown]
# # Importing Relaxed Geometry

# %% [markdown]
# # Cellulose Crystal

# %%
ActualDir   = os.getcwd()

# %% [markdown]
# ## Optmize Geometry (Only Hydrogen is Free)

# %% [markdown]
# ### I/O Definitions

# %%
# *************** INPUT DIR ***************
Input   = "hydrogen_bonds/MonobDGlu_MonobDGlu_H_variable"
Input   = os.path.join(ActualDir, Input)

# %%
# *************** OUT DIR ***************
OutputDir0   = "hydrogen_bonds/MonobDGlu_MonobDGlu_H_vari_freq_ISIF_2"
OutputDir0   = os.path.join(ActualDir, OutputDir0)

# %% [markdown]
# ### Calculating Vibrational Frequencys

# %%
calc            = Vasp(restart=True,directory=Input)
Cellulose_Beta  = calc.get_atoms()
Cellulose_Beta.set_constraint(None)

# %%
calc = Vasp(
    directory=OutputDir0,
    xc='PBE',
    encut=800,              # Energy cutoff for plane waves (from paper)
    kpts=[2,2,2],           # Reciprocal space sampling (from paper)
    gamma=True,
    ismear=0, sigma=0.05,   # Gaussian smearing          
    ediff=1e-6,             # SCF convergence criterion (from paper)
    nelm=150,               # sets the maximum number of electronic SC (self-consistency) steps
    nfree=2,                # Just ensure to use centered differences
    lepsilon=True,          # enables to calculate and to print the BEC
    # tensors         
    ibrion=7,               # switches on the DFPT vibrational analysis (with no symmetry constraints)
    nsw=1,                  # Maximum number of ionic steps ("1" for IBRION=5,6,7)
    lreal='Auto',           # Projection operators are evaluated in real space if the unit cell is large enough
    #ivdw=11,                # DFT-D2
    nwrite=3,               # affects OUTCAR verbosity: explicitly forces
    # How VASP will calculate the dipol moment
    ldipol=False,           # Removes artificial electrostatic interactions between periodic images (important in non-periodic systems simulated with periodic boundary conditions) 
    idipol = 4,             # full 3D dipole (molecules) (it's a VASP correction for dipole calculation)
    dipol=Cellulose_Beta.get_center_of_mass(), # dipole position is CM
    atoms=Cellulose_Beta
)

# %%
calc.calculate(Cellulose_Beta) # doing all the calculations

# %%
cellulose_dipole = calc.read_dipole()

print("Momento de dipolo elétrico da celulose cristalina é:", cellulose_dipole, "e.A")
print("Magnitude (Debye):", (sum(x**2 for x in cellulose_dipole)**0.5) * 4.80321)

# %% [markdown]
# Determinando as frequências de vibração

# %%
vib_freq = calc.read_vib_freq()

for i, f in enumerate(vib_freq[0]):
    print("{0:02d}: {1} meV".format(i, f))

# %%
vib_cellulose = calc.get_vibrations()

# %%
freq = vib_cellulose.get_frequencies()

for i, f in enumerate(freq):
    print("{0:01d}: {1} cm-1".format(i, f))

# %%
for i, f in enumerate(freq):
    write(f"cellulose_vib_mode{i:01d}.gif", vib_cellulose.iter_animated_mode(i), rotation="0x,90y,0z", interval=100) 


