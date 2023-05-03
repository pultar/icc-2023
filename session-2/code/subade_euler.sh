#!/bin/bash

# Bash script for submitting autodE scripts (ICC 2023 format) to Slurm (euler version)
# run subade for help message

readonly ARGS="$@"

function get_args () {
    # Set up default parameter
    walltime=4 # wall time in h
    scr=10000 # scratch space in MB

    # Parse the arguments
    local OPTIND OPTARG flag t r
    while getopts ':t:r:' flag; do
        case $flag in
            t) walltime=${OPTARG};;
            r) scr=${OPTARG};;
            *)
              usage
              exit
              ;;
        esac
    done
    file=${@:OPTIND:1}
}

# print usage
function usage () {
    echo "  subade.sh [-t time_in_h] [-r scratch_space_in_MB] rxn_script.py"
    echo "  (default parameters are 4 h run time and 10000 MB scratch space)"
}

# main function
function main () {

    # if no arguments, print usage and exit
    if [[ -z $ARGS ]]; then
        usage
        exit
    fi

    # get the arguments and define file variables
    get_args $ARGS
    fpath=$(readlink -f $file)
    filename=$(basename $fpath)
	name=${filename/.py}

    # get number of processor from the script
	ncore=$(grep "n_cores = " $fpath | awk '{print $3}')
    # get memory per processor from the script
	mem=$(grep "memory_per_core =" $fpath | awk '{print $3}')

    # in case processors or memory not given in the input, exit
    if [[ -z $ncore || -z $mem ]]; then
        echo " n_cores or memory_per_core not specified in the script"
        echo " Exiting."
        exit
    fi

    # multiply memory by some overhead as orca may use more memory than you request
	mem=$((mem * 110 / 100))

    # set autodE-specific environment variables
    export AUTODE_LOG_LEVEL=INFO # comprehensive logging
    export AUTODE_LOG_FILE=autode.log # name of the log file

# submit the job
sbatch <<-script
#!/bin/bash

#SBATCH --job-name=$name
#SBATCH -n $ncore
#SBATCH --mem-per-cpu=$mem
#SBATCH --time=$walltime:00:00
#SBATCH --tmp=$scr
#SBATCH --out=${fpath/.py/.out}
#SBATCH --error=${fpath/.py/.err}

python "$fpath"

script

}

# call the main function and check for success
if main; then
    echo "autodE script submitted"
    echo "Cores:" $ncore
    echo "Time (hours):" $walltime:00
    echo "Memory (MB per core):" $mem "(scaled 1.1x)"
    echo "Scratch space (MB):" $scr
    echo "Script file:" $fpath
else
    echo "Submission failed"
fi