"""
Sample script to submit an autodE calculation as taught in the ICC course 2023 at ETH Zurich.
Customize the first section accordingly.

Author: Felix Pultar, Eno Paenurk, Patrick Finkelstein
Date: April 17, 2023
"""

from icctools import librxn

# EDIT THE SECTIONS BELOW
# -----------------------------------------------------------------------------------------------
# DEFINE YOUR REACTION
# -----------------------------------------------------------------------------------------------
rxn_name = "REACTION_NAME" # no spaces
rxn_smiles = "REACTION_SMILES_GOES_HERE"
rxn_solvent = "SOLVENT_NAME_GOES_HERE"
rxn_temperature = 298.15
# -----------------------------------------------------------------------------------------------
# DEFINE THE RESOURCES AND THE METHOD
# -----------------------------------------------------------------------------------------------
n_cores = 4
memory_per_core = 1024 # in MB
method = librxn.Method.XTB
# Available methods:
# librxn.Method.XTB   - semiempirical (very fast)
# librxn.Method.BP86  - cheap DFT (reasonably fast)
# librxn.Method.B3LYP - DFT of choice for organic chemists (slow)
# librxn.Method.PBE0  - DFT of choice for inorganic chemists (slow)
# -----------------------------------------------------------------------------------------------

# DO NOT EDIT THE CODE BELOW (UNLESS YOU REALLY WANT TO)

# Calculate the reaction profile
rxn = librxn.calculate_reaction_profile(rxn_smiles, rxn_solvent, rxn_temperature, rxn_name,
                                        n_cores, memory_per_core, method)

# Print the results
librxn.print_results(rxn)
