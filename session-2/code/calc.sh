#!/bin/bash

#################################################################################################
## Script name : calc.sh                                                                       ##
## Description : Submit an autodE calculation as taught in the ICC 2023 course at ETH Zurich   ##
## Execute     : ./calc.sh                                                                     ##
## Author      : Felix Pultar, Eno Paenurk, Patrick Finkelstein                                ##
## Datum       : April 17, 2023                                                                ##
#################################################################################################

# -----------------------------------------------------------------------------------------------
# Declare some variables, change resources and RXN name here
# -----------------------------------------------------------------------------------------------
export RXN=reaction_name # enter reaction name here
export NCORES=8 # how many cores
export TIME=24:00:00 # how much time for the job
export MEMORY=2500 # per core !!
export SCRATCH=50000 # per node!!
# -----------------------------------------------------------------------------------------------

export AUTODE_LOG_LEVEL=INFO # comprehensive logging
export AUTODE_LOG_FILE=autode.log # name of the log file

# Run the actual job
echo "Submitting Slurm job: ${NCORES} cores, ${MEMORY} MB per CPU memory, ${SCRATCH} MB per node scratch space for reaction ${RXN} (max runtime: ${TIME} h)"
sbatch -n ${NCORES} --time=${TIME} --job-name="${RXN}" --mem-per-cpu=${MEMORY} --tmp=${SCRATCH} --output="${RXN}-slurm.out" --error="${RXN}-slurm.err" --open-mode=truncate --wrap="python ${RXN}.py > ${RXN}.out"
