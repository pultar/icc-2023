"""
Sample script to submit an autodE calculation as taught in the ICC course 2023 at ETH Zurich.
Customize the first section accordingly.

Author: Felix Pultar, Eno Paenurk, Patrick Finkelstein
Date: April 17, 2023
"""

from icctools import librxn

# -----------------------------------------------------------------------------------------------
# EDIT THIS SECTION: DEFINE YOUR REACTION
# -----------------------------------------------------------------------------------------------
rxn_smiles = "REACTION_SMILES_GOES_HERE"
rxn_solvent = "SOLVENT_NAME_GOES_HERE"
rxn_temperature = 298.15
# -----------------------------------------------------------------------------------------------

# Calculate the reaction profile
rxn = librxn.calculate_reaction_profile(rxn_smiles, rxn_solvent, rxn_temperature, method = librxn.Method.XTB)

# Print the results
librxn.print_results(rxn)
