"""
Sample script to submit an autodE calculation as taught in the ICC course 2023 at ETH Zurich.
Customize the first section accordingly.

Author: Felix Pultar, Eno Paenurk, Patrick Finkelstein
Date: April 17, 2023
"""

import icctools

# -----------------------------------------------------------------------------------------------
# EDIT THIS SECTION: DEFINE YOUR REACTION
# -----------------------------------------------------------------------------------------------
rxn_smiles = "REACTION_SMILES_GOES_HERE"
rxn_solvent = "SOLVENT_NAME_GOES_HERE"
rxn_temperature = 298.15
# -----------------------------------------------------------------------------------------------

# Calculate the reaction profile
rxn = icctools.calculate_reaction_profile(rxn_smiles, rxn_solvent, rxn_temperature, method = icctools.ComputationalMethod.XTB)

# Print the results
icctools.print_results(rxn)
