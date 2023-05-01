"""
Provides helper functions to easily set up autode calculations
Author: Felix Pultar, Eno Paenurk, Patrick Finkelstein
Date: April 17, 2023
"""

import autode as ade
from autode.wrappers.keywords.basis_sets import (
    def2svp,
    def2tzvp,
    def2ecp
)
from autode.wrappers.keywords.dispersion import d3bj
from autode.wrappers.keywords import KeywordsSet, MaxOptCycles
from enum import Enum
import os

class ComputationalMethod(Enum):
    """
    An enum that defines, which hmethod will be used
    """
    PBE0 = 1
    XTB = 2
    BP86 = 3
    B3LYP = 4

def calculate_reaction_profile(rxn_smiles, rxn_solvent, rxn_temperature, method = ComputationalMethod.BP86):
    """
    Calculates a reaction profile and returns the reaction object
    """
    # Check if modules have been loaded and debug resources from environment
    if not ade.methods.ORCA().is_available and ade.methods.XTB().is_available:
        exit("This example requires an ORCA and XTB install")

    # Configure autode
    setup_template_folder()

    # Set autode methods and get environment variables from calling shell script
    ade.Config.lcode = "xtb"
    ade.Config.hcode = "orca"
    ade.Config.n_cores = int(os.environ["NCORES"])
    ade.Config.max_core = int(0.9 * int(os.environ["MEMORY"])) # only use 90% of the memory
    rxn_name = os.environ["RXN"]

    # Set hmethod
    if (method == ComputationalMethod.PBE0):
        setup_pbe0()
    elif (method == ComputationalMethod.XTB):
        setup_xtb()
    elif (method == ComputationalMethod.BP86):
        setup_bp86()
    elif (method == ComputationalMethod.B3LYP):
        setup_b3lyp()

    # Define reaction and calculate profile
    print(f"Using environment variables: {ade.Config.n_cores} cores and {ade.Config.max_core} memory per core for {rxn_name}.")
    rxn = ade.Reaction(rxn_smiles, name=rxn_name, solvent_name=rxn_solvent, temp=rxn_temperature) 
    rxn.calculate_reaction_profile(free_energy=True)
    return rxn

def print_results(rxn):
    """
    Outputs electronic energy, enthalpy, Gibbs free energy, and imaginary frequency information
    """
    print("∆E_r (kcal mol-1) = ", rxn.delta("E").to("kcal mol-1"))
    print("∆E‡ (kcal mol-1)  = ", rxn.delta("E‡").to("kcal mol-1"))
    print("∆H_r (kcal mol-1) = ", rxn.delta("H").to("kcal mol-1"))
    print("∆H‡ (kcal mol-1)  = ", rxn.delta("H‡").to("kcal mol-1"))
    print("∆G_r (kcal mol-1) = ", rxn.delta("G").to("kcal mol-1"))
    print("∆G‡ (kcal mol-1)  = ", rxn.delta("G‡").to("kcal mol-1"))
    print("Number of imaginary freq's = ", len(rxn.ts.imaginary_frequencies))
    print("First TS imaginary freq = ", rxn.ts.imaginary_frequencies[0])

def setup_template_folder():
    """
    Save templates in home folder, create folder if it does not exist
    """
    home_folder = os.path.expanduser("~")
    lib_folder = os.path.join(home_folder, ".icc-2023", "autode-lib")
    if not os.path.exists(lib_folder):
        os.makedirs(lib_folder)
        print(f"Created folder {lib_folder}")
    ade.Config.ts_template_folder_path = lib_folder
    print(f"Saving transition state templates in {ade.Config.ts_template_folder_path}")

def setup_pbe0():
    """
    Sets up keywords required to use PBE0 as hmethod
    """
    print("Using PBE0 functional as hmethod")
    pass

def setup_xtb():
    """
    Sets up keywords required to use xtb as hmethod
    """
    print("Using xtb as hmethod")
    pass

def setup_bp86():
    """
    Sets up keywords required to use BP86 as hmethod
    """
    optts_block = (
      "\n%geom\n"
      "Calc_Hess true\n"
      "Recalc_Hess 20\n"
      "Trust -0.1\n"
      "MaxIter 100\n"
      "end"
    )
    ade.Config.ORCA.keywords.low_opt = ['LooseOpt', 'BP86', 'RI', def2svp, d3bj, 'def2/J', MaxOptCycles(10)]
    ade.Config.ORCA.keywords.grad = ['EnGrad', 'BP86', 'RI', def2svp, d3bj]
    ade.Config.ORCA.keywords.low_sp = ['SP', 'BP86', 'RI', def2svp, d3bj]
    ade.Config.ORCA.keywords.opt = ['TightOpt', 'BP86', 'RI', def2svp, d3bj]
    ade.Config.ORCA.keywords.opt_ts = ['OptTS', 'Freq', 'BP86', 'RI', def2svp, d3bj, optts_block]
    ade.Config.ORCA.keywords.hess = ['Freq', 'BP86', 'RI', def2svp, d3bj]
    ade.Config.ORCA.keywords.sp = ['SP', 'BP86', 'RI', def2tzvp, d3bj]
    ade.Config.ORCA.keywords.ecp = def2ecp
    print("Using BP86 functional as hmethod")

def setup_b3lyp():
    """
    Sets up keywords required to use B3LYP as hmethod
    """
    print("Using B3LYP functional as hmethod")
    pass