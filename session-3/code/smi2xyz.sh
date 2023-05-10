#!/bin/bash

# Script to generate a XTB optimized .xyz file from a SMILES code

# Colors for fancy reasons
RED='\033[0;31m'
NC='\033[0m' # No color

# Read arguments
readonly ARGS="$@"

# Define argument parsing function
function get_args () {

    # Default paramters:
    mu=1 # multiplicity
    chg=0 # charge
    out_name=dummy # name of the output files
    thrsh=tight # Optimization threshold for xTB
    verbose=1 # Print the log on the screen
    files=0 # Keep the log files

    # Parse the arguments
    local OPTIND OPTARG flag u c o t v f
    while getopts ':u:c:o:t:v:f:' flag; do
        case $flag in
            u)   mu=${OPTARG};;
            c)   chg=${OPTARG};;
            o)   out_name=${OPTARG};;
            t)   thrs=${OPTARG};;
            v)   verbose=${OPTARG};;
            f)   files=${OPTARG};;
            *)
              usage
              exit
              ;;
        esac
    done
    smile=${@:OPTIND:1}
}

# Function to print the usage
function usage () {
    echo "  $(basename $0) [-u multiplicity] [-c charge] [-t opt_threshold] [-o out_filename] [-v (verbose) 1/0] [-f (keep log files) 1/0] \"SMILES\""
    echo -e "  ${RED}The flags must come first and the SMILES code must be between quotation marks.${NC}"
    echo "  The flags are optional - all of them have default values. They must be called without the brackets."
    echo "  The default parameters are u=1, c=0, o=dummy, t=tight, v=1, f=0. See xtb documentation for t options."
}

# Function to generate the initial xyz guess
function gen_xyz () {

  # Generate the .xyz file from SMILES with openbabel
  obabel -:"${smile}" -oxyz -O ${out_name}_obabel.xyz --gen3d

}

# Function to optimize the initial xyz with xtb
function xtb_opt () {

   # Optimize with xtb
   # print on the screen if verbose
   if [ "$verbose" = 1 ]; then
      xtb ${out_name}_obabel.xyz --chrg $chg --uhf $(( mu - 1 )) --opt ${thrsh} | tee ${out_name}_xtbopt.log
   # only write to the file if not verbose
   else 
      xtb ${out_name}_obabel.xyz --chrg $chg --uhf $(( mu - 1 )) --opt ${thrsh} > ${out_name}_xtbopt.log
   fi
   # Add the SMILES code to the xyz comment line
   sed -i "2s|$|; SMILES: ${smile}|" xtbopt.xyz 
   # Rename the optimized xyz file
   mv xtbopt.xyz ${out_name}.xyz

}

# Main function
function main () {

   # Print usage and exit if no arguments given
   if [[ -z $ARGS ]]; then
      usage
      exit
   fi

   # Parse arguments
   get_args $ARGS

   # unlimit system stack to avoid overflow with xtb
   ulimit -s unlimited

   # Generate the xyz with obabel and optimize with xtb
   gen_xyz
   xtb_opt
   
   # Remove the unnecessary files unless specified otherwise
   if [ "$files" = 0 ]; then
      rm ${out_name}_obabel.xyz xtbrestart xtbopt.log wbo charges .xtboptok ${out_name}_xtbopt.log xtbtopo.mol
   fi
}

# Call the main function
main

