"""
Sample script to submit an autodE calculation as taught in the ICC course 2023 at ETH Zurich.
Customize the first section accordingly.

Author: Felix Pultar, Eno Paenurk, Patrick Finkelstein
Date: April 17, 2023
"""

import autode as ade
import os

# -----------------------------------------------------------------------------------------------
# EDIT THIS SECTION: DEFINE YOUR REACTION
# -----------------------------------------------------------------------------------------------
rxn_smiles = "REACTION_SMILES_GOES_HERE"
rxn_solvent = "SOLVENT_NAME_GOES_HERE"
rxn_temperature = 298.15
# -----------------------------------------------------------------------------------------------


# Set autode methods and get environment variables from calling shell script
ade.Config.lcode = "xtb"
ade.Config.hcode = "orca"
ade.Config.n_cores = int(os.environ["NCORES"])
ade.Config.max_core = int(0.9 * int(os.environ["MEMORY"])) # only use 90% of the memory
rxn_name = os.environ["RXN"]

# Check if modules have been loaded and debug resources from environment
if not ade.methods.ORCA().is_available and ade.methods.XTB().is_available:
    exit("This example requires an ORCA and XTB install")

# Define reaction and calculate profile
print(f"Using environment variables: {ade.Config.n_cores} cores and {ade.Config.max_core} memory per core for {rxn_name}.")
rxn = ade.Reaction(rxn_smiles, name=rxn_name, solvent_name=rxn_solvent, temp=rxn_temperature)
rxn.calculate_reaction_profile(free_energy=True)

# Output electronic energy, enthalpy, Gibbs free energy, and imaginary frequency information
print("∆E_r (kcal mol-1) = ", rxn.delta("E").to("kcal mol-1"))
print("∆E‡ (kcal mol-1)  = ", rxn.delta("E‡").to("kcal mol-1"))
print("∆H_r (kcal mol-1) = ", rxn.delta("H").to("kcal mol-1"))
print("∆H‡ (kcal mol-1)  = ", rxn.delta("H‡").to("kcal mol-1"))
print("∆G_r (kcal mol-1) = ", rxn.delta("G").to("kcal mol-1"))
print("∆G‡ (kcal mol-1)  = ", rxn.delta("G‡").to("kcal mol-1"))
print("Number of imaginary freq's = ", len(rxn.ts.imaginary_frequencies))
print("First TS imaginary freq = ", rxn.ts.imaginary_frequencies[0])
