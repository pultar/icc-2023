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
from autode.wrappers.keywords.ri import rijcosx
from autode.wrappers.keywords import MaxOptCycles
from autode.reactions.reaction import Reaction
from enum import Enum
import os

class Method(Enum):
    """
    An enum that defines which hmethod will be used
    """
    XTB = 1
    R2SCAN3C = 2
    BP86 = 3
    B3LYP = 4
    PBE0 = 5

def calculate_reaction_profile(rxn_obj, rxn_solvent, rxn_temperature, rxn_name, n_cores = 4, max_core = 1024, method = Method.BP86):
    """Calculates a reaction profile and returns the reaction object

    Args:
        rxn_obj: reaction identifier, can be a rxn_smiles (str) or autodE Reaction object
        rxn_solvent: solvent of the reaction
        rxn_temperature: temperature of the reaction in Kelvin
        rxn_name: reaction name (str)
        n_cores: number of cores
        max_core: memory per core in MB
        method (optional): computational method (e.g. functional). Defaults to Method.BP86.

    Returns:
        Returns the reaction after the profile has been calculated
    """
    # Check type is valid
    assert(isinstance(rxn_obj, str) or isinstance(rxn_obj, Reaction), f"rxn_object must be a reaction SMILES or an autodE reaction object but was {type(rxn_obj)}")

    # Check if modules have been loaded and debug resources from environment
    if not ade.methods.ORCA().is_available and ade.methods.XTB().is_available:
        exit("This script requires that ORCA and xtb are available")

    # Configure autode
    _setup_template_folder()

    # Set autode methods and get environment variables from calling shell script
    ade.Config.lcode = "xtb"
    ade.Config.hcode = "orca"
    ade.Config.n_cores = n_cores
    ade.Config.max_core = max_core

    # Set hmethod
    if (method == Method.XTB):
        _setup_xtb(rxn_solvent)
        rxn_solvent = None
    elif (method == Method.R2SCAN3C):
        _setup_r2scan3c()
    elif (method == Method.BP86):
        _setup_bp86()
    elif (method == Method.B3LYP):
        _setup_b3lyp()
    elif (method == Method.PBE0):
        _setup_pbe0()

    # Define reaction and calculate profile
    print(f"Using {ade.Config.n_cores} cores and {ade.Config.max_core} MB of memory per core for {rxn_name}.")
    if isinstance(rxn_obj, str): # assume reaction SMILES
        print("Starting from rxn_smiles")
        rxn = ade.Reaction(rxn_obj, name=rxn_name, solvent_name=rxn_solvent, temp=rxn_temperature) 
    else: # assume autodE reaction
        print("Starting from autodE reaction object")
        rxn = rxn_obj
    rxn.calculate_reaction_profile(free_energy=True)
    return rxn

def print_results(rxn):
    """Outputs electronic energy, enthalpy, Gibbs free energy, and imaginary frequency information

    Args:
        rxn: A completed autodE reaction
    """
    print('-'*40)
    print("Energies")
    print('-'*40)
    print("∆E_r (kcal mol-1) = %-8.2f" % (rxn.delta("E").to("kcal mol-1")))
    print("∆E‡ (kcal mol-1)  = %-8.2f" % (rxn.delta("E‡").to("kcal mol-1")))
    print("∆H_r (kcal mol-1) = %-8.2f" % (rxn.delta("H").to("kcal mol-1")))
    print("∆H‡ (kcal mol-1)  = %-8.2f" % (rxn.delta("H‡").to("kcal mol-1")))
    print("∆G_r (kcal mol-1) = %-8.2f" % (rxn.delta("G").to("kcal mol-1")))
    print("∆G‡ (kcal mol-1)  = %-8.2f" % (rxn.delta("G‡").to("kcal mol-1")))
    print('-'*40)
    print("TS info")
    print('-'*40)
    print("Number of imaginary freqs   = %-2i" % (len(rxn.ts.imaginary_frequencies)))
    print("First imaginary freq (cm-1) = %-8.1f" % (rxn.ts.imaginary_frequencies[0]))


def _setup_template_folder():
    """
    Save templates in home folder, create folder if it does not exist. Should not be called directly.
    """
    home_folder = os.path.expanduser("~")
    lib_folder = os.path.join(home_folder, ".icc-2023", "autode-lib")
    if not os.path.exists(lib_folder):
        os.makedirs(lib_folder)
        print(f"Created folder {lib_folder}")
    ade.Config.ts_template_folder_path = lib_folder
    print(f"Saving transition state templates in {ade.Config.ts_template_folder_path}")

# keywords for optts
optts_block = (
      "\n%geom\n"
      "Calc_Hess true\n"
      "Recalc_Hess 20\n"
      "Trust -0.1\n"
      "MaxIter 100\n"
      "end"
    )

def _setup_xtb(rxn_solvent):
    """Sets up keywords required to use xtb as hmethod. Should not be called directly.

    Args:
        rxn_solvent: The reaction solvent string
    """
    solvent_model = 'ALPB(' + rxn_solvent + ')'
    ade.Config.ORCA.keywords.sp = ['SP', 'XTB2', solvent_model]
    ade.Config.ORCA.keywords.low_sp = ['SP', 'XTB2', solvent_model]
    ade.Config.ORCA.keywords.opt = ['TightOpt', 'XTB2', solvent_model]
    ade.Config.ORCA.keywords.low_opt = ['LooseOpt', 'XTB2', solvent_model, MaxOptCycles(10)]
    ade.Config.ORCA.keywords.opt_ts = ['OptTS', 'XTB2', 'NumFreq', solvent_model, optts_block]
    ade.Config.ORCA.keywords.grad = ['EnGrad', 'XTB2', solvent_model]
    ade.Config.ORCA.keywords.hess = ['NumFreq', 'XTB2', solvent_model]

    # symbolic link to ORCA binaries and otool_xtb
    home_folder = os.path.expanduser("~")
    orcaxtb_path = os.path.join(home_folder, "bin/orca_with_xtb", "orca")
    ade.Config.ORCA.path = orcaxtb_path 
    print("Using xTB-GFN2 as hmethod")
    print(f"Path to ORCA with xTB support: {orcaxtb_path}")

def _setup_r2scan3c():
    """
    Sets up keywords required to use r2SCAN-3c as hmethod. Should not be called directly.
    """
    ade.Config.ORCA.keywords.sp = ['SP', 'r2SCAN-3c']
    ade.Config.ORCA.keywords.low_sp = ['SP', 'r2SCAN-3c']
    ade.Config.ORCA.keywords.opt = ['TightOpt', 'r2SCAN-3c']
    ade.Config.ORCA.keywords.low_opt = ['LooseOpt', 'r2SCAN-3c', MaxOptCycles(10)]
    ade.Config.ORCA.keywords.opt_ts = ['OptTS', 'Freq', 'r2SCAN-3c', optts_block]
    ade.Config.ORCA.keywords.grad = ['EnGrad', 'r2SCAN-3c']
    ade.Config.ORCA.keywords.hess = ['Freq', 'r2SCAN-3c']
    ade.Config.ORCA.keywords.ecp = def2ecp
    print("Using r2SCAN-3c functional as hmethod")

def _setup_bp86():
    """
    Sets up keywords required to use BP86 as hmethod. Should not be called directly.
    """
    ade.Config.ORCA.keywords.sp = ['SP', 'BP86', 'RI', def2tzvp, d3bj]
    ade.Config.ORCA.keywords.low_sp = ['SP', 'BP86', 'RI', def2svp, d3bj]
    ade.Config.ORCA.keywords.opt = ['TightOpt', 'BP86', 'RI', def2svp, d3bj]
    ade.Config.ORCA.keywords.low_opt = ['LooseOpt', 'BP86', 'RI', def2svp, d3bj, 'def2/J', MaxOptCycles(10)]
    ade.Config.ORCA.keywords.opt_ts = ['OptTS', 'Freq', 'BP86', 'RI', def2svp, d3bj, optts_block]
    ade.Config.ORCA.keywords.grad = ['EnGrad', 'BP86', 'RI', def2svp, d3bj]
    ade.Config.ORCA.keywords.hess = ['Freq', 'BP86', 'RI', def2svp, d3bj]
    ade.Config.ORCA.keywords.ecp = def2ecp
    print("Using BP86 functional as hmethod")

def _setup_b3lyp():
    """
    Sets up keywords required to use B3LYP as hmethod. Should not be called directly.
    """
    ade.Config.ORCA.keywords.sp = ['SP', 'B3LYP', rijcosx, def2tzvp, d3bj]
    ade.Config.ORCA.keywords.low_sp = ['SP', 'B3LYP', rijcosx, def2svp, d3bj]
    ade.Config.ORCA.keywords.opt = ['TightOpt', 'B3LYP', rijcosx, def2svp, d3bj]
    ade.Config.ORCA.keywords.low_opt = ['LooseOpt', 'B3LYP', rijcosx, def2svp, d3bj, 'def2/J', MaxOptCycles(10)]
    ade.Config.ORCA.keywords.opt_ts = ['OptTS', 'Freq', 'B3LYP', rijcosx, def2svp, d3bj, optts_block]
    ade.Config.ORCA.keywords.grad = ['EnGrad', 'B3LYP', rijcosx, def2svp, d3bj]
    ade.Config.ORCA.keywords.hess = ['Freq', 'B3LYP', rijcosx, def2svp, d3bj]
    ade.Config.ORCA.keywords.ecp = def2ecp
    print("Using B3LYP functional as hmethod")

def _setup_pbe0():
    """
    Sets up keywords required to use PBE0 as hmethod. Should not be called directly.
    """
    ade.Config.ORCA.keywords.sp = ['SP', 'PBE0', rijcosx, def2tzvp, d3bj]
    ade.Config.ORCA.keywords.low_sp = ['SP', 'PBE0', rijcosx, def2svp, d3bj]
    ade.Config.ORCA.keywords.opt = ['TightOpt', 'PBE0', rijcosx, def2svp, d3bj]
    ade.Config.ORCA.keywords.low_opt = ['LooseOpt', 'PBE0', rijcosx, def2svp, d3bj, 'def2/J', MaxOptCycles(10)]
    ade.Config.ORCA.keywords.opt_ts = ['OptTS', 'Freq', 'PBE0', rijcosx, def2svp, d3bj, optts_block]
    ade.Config.ORCA.keywords.grad = ['EnGrad', 'PBE0', rijcosx, def2svp, d3bj]
    ade.Config.ORCA.keywords.hess = ['Freq', 'PBE0', rijcosx, def2svp, d3bj]
    ade.Config.ORCA.keywords.ecp = def2ecp
    print("Using PBE0 functional as hmethod")
