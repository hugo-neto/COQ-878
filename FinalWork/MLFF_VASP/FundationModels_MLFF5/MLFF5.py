# %% [markdown]
# # Machine Learning Force Field usando VASP, MACE e ASE
# 
# Authors: <br>
# [Prof. Elvis do A. Soares](https://github.com/elvissoares) <br>
# [PhD. Hugo de L. C. Neto](https://github.com/hugo-neto) <br>
# 
# Contacts: <br>
# [elvis@peq.coppe.ufrj.br](mailto:elvis@peq.coppe.ufrj.br) - [Programa de Engenharia Química, PEQ/COPPE, UFRJ, Brasil](https://www.peq.coppe.ufrj.br/) <br>
# [hneto@peq.coppe.ufrj.br](mailto:hneto@peq.coppe.ufrj.br) - [Programa de Engenharia Química, PEQ/COPPE, UFRJ, Brasil](https://www.peq.coppe.ufrj.br/)
# 
# ---

# %%
import os
# Definindo o path para os arquivos de potencial de pseudopotenciais do VASP
# Certifique-se de que o caminho esteja correto para o seu sistema
os.environ['VASP_PP_PATH'] = '/home/elvis/Programs/vasp-6.5.1/pp'
os.environ['ASE_VASP_COMMAND'] = 'mpirun -np 1 vasp_std'
os.environ['NO_STOP_MESSAGE'] = '1' # to avoid warning from mpirun

# Importando o VASP calculator do ASE
from ase.calculators.vasp import Vasp

from ase.io import write, read
from ase import units
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary, ZeroRotation

import time
import numpy as np
import matplotlib.pyplot as plt
from IPython import display
#%matplotlib inline

# %% [markdown]
# [Foundation models](https://mace-docs.readthedocs.io/en/latest/guide/foundation_models.html) <br>
# [MACE](https://mace-docs.readthedocs.io/en/latest/index.html) <br>
# [MACE documentation](https://mace-docs.readthedocs.io/en/latest/guide/foundation_models.html) <br>
# [Fine tunning](https://mace-docs.readthedocs.io/en/latest/guide/finetuning.html)

# %% [markdown]
# ## Step 0: Auxiliar function to carry out Molecular Dynamics in ASE

# %%
np.random.seed(701) #fazendo com que os resultados sejam reprodutíveis

# ================================================
# MD ensemble (N,V,T)
# Thermostat: Langevin
# ================================================
# init_conf : obj
#       initial system configuration
# temp : float
#       temperature of the (N,V,T) simulations
# calc : obj 
#       MACE object
# fname : str
#       output name
# s : int
#       print at each frame
# T : int
#       number of frames
# TimeStep : float
#       Time step of the MD
# initTemp : float
#       Initial Temperature
# ================================================
def simpleMD(init_conf, temp, calc, fname, s, T, TimeStep=0.5, initTemp=300, langevin_friction=0.1):
    init_conf.calc = calc

    #initialize the temperature

    MaxwellBoltzmannDistribution(init_conf, temperature_K=initTemp) #initialize temperature at 300
    Stationary(init_conf)
    ZeroRotation(init_conf)

    dyn         = Langevin(init_conf, TimeStep*units.fs, temperature_K=temp, friction=langevin_friction) #drive system to desired temperature

    time_fs     = []
    temperature = []
    energies    = []

    #remove previously stored trajectory with the same name
    os.system('rm -rfv '+fname)

    fig, ax = plt.subplots(2, 1, figsize=(6,6), sharex='all', gridspec_kw={'hspace': 0, 'wspace': 0})

    def write_frame():
            dyn.atoms.info['energy_mace']   = dyn.atoms.get_potential_energy()
            dyn.atoms.arrays['forces_mace'] = dyn.atoms.calc.get_forces()
            dyn.atoms.write(fname, append=True)
            time_fs.append(dyn.get_time()/units.fs)
            temperature.append(dyn.atoms.get_temperature())
            energies.append(dyn.atoms.get_potential_energy()/len(dyn.atoms))

            ax[0].plot(np.array(time_fs), np.array(energies), color="b")
            ax[0].set_ylabel('E (eV/atom)')

            # plot the temperature of the system as subplots
            ax[1].plot(np.array(time_fs), temperature, color="r")
            ax[1].set_ylabel('T (K)')
            ax[1].set_xlabel('Time (fs)')

            display.clear_output(wait=True)
            display.display(plt.gcf())
            time.sleep(0.01)

    dyn.attach(write_frame, interval=s)
    t0 = time.time()
    dyn.run(T)
    plt.savefig("Cellulose_Beta_NPT_300K.png", dpi=300, bbox_inches='tight')
    t1 = time.time()
    print("MD finished in {0:.2f} minutes!".format((t1-t0)/60))

# %% [markdown]
# ## Step 1: Molecular Dynamics using _foundation models_ from MACE

# %% [markdown]
# Remember to use kernel in VSCode of 'mlff' (if your conda environment for MACE is mlff)

# %%
from mace.calculators import mace_mp

macemp = mace_mp(model="small", dispersion=True, default_dtype = "float32", device="cuda")

# %% [markdown]
# Initial configuration loading and carrying out the MD simulations

# %%
simu_dir  = "Cellulose_Beta"

init_conf = "Cellulose_Beta.cif"
init_conf = read(os.path.join(os.getcwd(), simu_dir, init_conf)) # It works in Linux and Windows
out_MD    = "Cellulose_Beta_NVT_300K.xyz"
out_MD    = read(os.path.join(os.getcwd(), simu_dir, out_MD))    # It works in Linux and Windows

simpleMD(init_conf, temp=300, calc=macemp, fname=out_MD, s=10, T=80000)

# %% [markdown]
# > It took ~X min, compared to XX min of VASP Ab Initio

# %% [markdown]
# ## Step 2: Comparing the results of energy with Ab Initio calculations of VASP

# %% [markdown]
# Creating the Vasp calculator to carry out the single point calculation (SCF): `ibrion=-1`

# %%
simu_dir  = "Cellulose_Beta"
out_vasp  = "Cellulose_Beta_VASP_SCF"
out_vasp  = read(os.path.join(os.getcwd(), simu_dir, out_vasp)) # It works in Linux and Windows

vasp_calc = Vasp(
    directory=out_vasp,
    xc='pbe',
    encut=450,
    kpts=[2, 2, 2], gamma=True,                     # k-points
    ivdw=12, vdw_radius = 50, vdw_cnradius = 20,    # D3(BJ) van der Waals correction
    ismear=0, sigma=0.1,
    ediff=1e-5,       
    isym=0,
    ibrion=-1, nelm=100,                            # single point SCF calculation
    lreal = 'Auto', lwave=False, lcharg=False, lvtot=False
)

# %% [markdown]
# Ab Inition calculations to some frames of  `.xyz` file

# %%
from tqdm import tqdm

print("Evaluating MACE configurations with VASP")

traj        = read(out_MD, ':')

periodicity = 10

for at in tqdm(traj[::periodicity]): # Reading every "periodicity" frames to save time
    at.calc                  = vasp_calc
    at.info['energy_vasp']   = at.get_potential_energy()
    at.arrays['forces_vasp'] = at.get_forces()
    at.calc                  = None  #remove calculator to save memory

# %% [markdown]
# > Demorou ~55 minutos para efetuar cálculos de SCF no VASP (aqui não tem AIMD, só SCF)

# %% [markdown]
# Storeging the information in a new file but with the recalculated frames
# 
# In this new file, we have `energy_mace`, `energy_vasp`, `forces_mace` and `forces_vasp`

# %%
simu_dir  = "Cellulose_Beta"

new_frams = "Cellulose_Beta_NVT_300K_each10.xyz"
new_frams = read(os.path.join(os.getcwd(), simu_dir, new_frams)) # It works in Linux and Windows

write(new_frams, traj[::periodicity]) #save full result

# %% [markdown]
# Loading the file to compare the energies. 

# %%
from aseMolec import extAtoms as ea

traj = read(new_frams, '50:')

frames = np.arange(len(traj))
vasp_energies = ea.get_prop(traj, 'info', 'energy_vasp', peratom=True)
mace_energies = ea.get_prop(traj, 'info', 'energy_mace', peratom=True)

fig, axs = plt.subplots(1, 2,figsize=(7,3), sharey=True, gridspec_kw={'width_ratios': [3, 1], 'wspace': 0.05} )

axs[0].plot(frames, vasp_energies, label='VASP')
axs[0].plot(frames, mace_energies, label='MACE')
axs[0].legend()
axs[0].set_xlabel('Frame')
axs[0].set_ylabel('Total Energy per Atom (eV)')

axs[1].hist(vasp_energies,bins=30,density=True, color='C0', alpha=0.5, label='VASP', orientation="horizontal")
axs[1].hist(mace_energies,bins=30,density=True, color='C1', alpha=0.5, label='MACE', orientation="horizontal")

Umean = np.mean(vasp_energies)
sigmaU = np.std(vasp_energies)
uarray = Umean+np.arange(-3*sigmaU,3*sigmaU,0.01*sigmaU)
axs[1].plot(np.sqrt(1/(2*np.pi*sigmaU**2))*np.exp(-0.5*(uarray-Umean)**2/sigmaU**2),uarray, color='C0')
Umean = np.mean(mace_energies)
sigmaU = np.std(mace_energies)
uarray = Umean+np.arange(-3*sigmaU,3*sigmaU,0.01*sigmaU)
axs[1].plot(np.sqrt(1/(2*np.pi*sigmaU**2))*np.exp(-0.5*(uarray-Umean)**2/sigmaU**2),uarray, color='C1')
axs[1].legend()
axs[1].set_xlabel('Density Prob.')

# %%
RMSE = np.sqrt(np.mean((mace_energies-vasp_energies)**2))

print("RMSE between energies of MACE and VASP: {:.3f} eV/átomo".format(RMSE))

# %%
vasp_forces = ea.get_prop(traj, 'arrays', 'forces_vasp', peratom=True)
mace_forces = ea.get_prop(traj, 'arrays', 'forces_mace', peratom=True)

RMSE_forces = np.sqrt(np.mean((mace_forces-vasp_forces)**2))

print("RMSE between forces of MACE and VASP: {:.4f} eV/Å".format(RMSE_forces))

# %% [markdown]
# ## Passo 3: Realizando _fine tunning_ da rede MACE

# %% [markdown]
# Definindo arquivos para treino e para teste
