#!/bin/bash

# Bash script for submitting ORCA calculations to Slurm
# run suborca for help message

readonly ARGS="$@"

function get_args () {
    # Set up default paramters;
    scr=4000 # scratch space in MB
    walltime=4 # wall time in h

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
    echo "  suborca.sh [-r scratchspace_in_MB] [-t walltime_in_h] filename.inp"
    echo "  (default parameters are 4000 MB of scratch space and 4 h"
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
    name=${filename/.inp}

    # get orca path
    orca_path=$(which orca)

    # converting file to unix from dos, just in case
    dos2unix $fpath 

    # get number of processor from orca input
    nproc=$(grep -i "%pal" $fpath | awk '{print $3}')
    # get memory per processor from orca input
    mem=$(grep -i "%maxcore" $fpath | awk '{print $2}')
    
    # in case processors or memory not given in the input, exit
    if [[ -z $nproc || -z $mem ]]; then
        echo " %pal or %maxcore not specified in the input file."
        echo " Exiting."
        exit
    fi

    # multiply by some overhead as orca may use more memory than you request
    mem=$((mem * 110 / 100))

    export RSH_COMMAND="ssh" # Required to run multi-process numerical calculations on multiple nodes
    export OMPI_MCA_btl=self,tcp,vader # Removes messages about OpenMPI network interface in the output files

    # submit the job
    sbatch <<-script
#!/bin/bash

#SBATCH --job-name=$name
#SBATCH --ntasks=$nproc
#SBATCH --mem-per-cpu=$mem
#SBATCH --tmp=$scr
#SBATCH --time=$walltime:00:00
#SBATCH --out=${fpath/.inp/.out}
#SBATCH --error=${fpath/.inp/.err}

"$orca_path" "$fpath"

script
}

# call the main function and check for success
if main; then
    echo "ORCA calculation submitted"
    echo "Cores:" $nproc
    echo "Time (hours):" $walltime:00
    echo "Memory (MB per core):" $mem "(scaled 1.1x)"
    echo "Scratch space (MB per core):" $scr
    echo "ORCA path:" $orca_path
    echo "Input file:" $fpath
else
    echo "Submission failed"
fi