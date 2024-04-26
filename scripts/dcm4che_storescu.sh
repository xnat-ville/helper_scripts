#!/bin/bash

# Script determines the location of the DCM4CHE storescu command
# First version just looked for it on the users PATH, but that
# did not work when users also had installed DCMTK which has
# it's own version with the same name.


# This function of the meat of the script
# I commented out the original code that looked on the user's PATH
# As mentioned above, that fails when DCMTK is installed
# and the DCMTK storescu is on the PATH before the DCM4CHE version

find_storescu() {
# storescu_path=`which storescu`
# if [[ $? -ne 0 ]] ; then
#  if [ -z ${DCM4CHE_BASE+x} ] ; then
#   # Variable is not set
#   storescu_path=`which storescu`
#  else
#   # Variable is set
#   storescu_path="$DCM4CHE_BASE/bin/storescu"
#  fi
# fi

 storescu_path="$DCM4CHE_BASE/bin/storescu"
 echo "$storescu_path"
}

export DCM4CHE_STORESCU=$(find_storescu)
