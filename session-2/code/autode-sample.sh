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
export SCRATCH=10000 # per node!!
# -----------------------------------------------------------------------------------------------

export AUTODE_LOG_LEVEL=INFO # comprehensive logging
export AUTODE_LOG_FILE=autode.log # name of the log file

# Display resources and run the actual job
echo "Submitting Slurm job for reaction ${RXN}:"
echo "${NCORES} cores"
echo "${MEMORY} MB per CPU memory"
echo "${SCRATCH} MB per node scratch space"
echo "Max runtime: ${TIME} h"

sbatch <<-script
#!/bin/bash

#SBATCH --job-name=${RXN}
#SBATCH -n ${NCORES}
#SBATCH --mem-per-cpu=${MEMORY}
#SBATCH --time=${TIME}
#SBATCH --tmp=${SCRATCH}
#SBATCH --out=${RXN}-slurm.out
#SBATCH --error=${RXN}-slurm.err
#SBATCH --open-mode=truncate 

python ${RXN}.py > ${RXN}.out

script