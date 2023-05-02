#!/bin/bash

# Script that sets up a directory with symbolic links to the orca executables
# and the xtb executable.
# Defines orcaxtb variable in .bash_profile

# Directories
currentdir=$(pwd)
linkdir=orca_with_xtb

# Make directory if does not exist
if [ ! -d "${linkdir}" ]; then
  mkdir ${linkdir}
fi

# Link the executables
cd ${linkdir}
# orca
orcadir=$(dirname $(which orca))
for exe in $(ls ${orcadir} | sed -e '/.pdf/d' -e '/contrib/d'); do
  ln -s ${orcadir}/${exe} ${exe}
done
# xtb
ln -s $(which xtb) otool_xtb

cd ..

# Set up executable in bin
echo "${currentdir}/${linkdir}/orca \$1" > ~/bin/orcaxtb
chmod 755 ~/bin/orcaxtb

