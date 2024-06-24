#!/bin/bash

# Function to display usage instructions
usage() {
  echo "Usage: $0 [-s subject] [-h host] directory"
  exit 1
}

# Determine the script directory and source the dcm4che_storescu.sh script
SCRIPTS=`dirname $0`
source $SCRIPTS/dcm4che_storescu.sh

# Initialize variables
subject=""
host="cnda-shadow01.nrg.wustl.edu" # Default value for the host

# Parse command-line options
while getopts "s:h:" opt; do
  case $opt in
    s)
      subject=$OPTARG
      ;;
    h)
      host=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

# Shift off the options and arguments processed by getopts
shift $((OPTIND - 1))

# Check for the mandatory directory argument
if [ $# -ne 1 ]; then
  usage
fi

directory=$1

# Build the storescu command using the DCM4CHE_STORESCU variable
storescu_cmd="$DCM4CHE_STORESCU -b CCIR-CTP -c CNDA_CCIR@$host:8104"

# If subject is provided, add the -s option for StudyDescription
if [ -n "$subject" ]; then
  storescu_cmd="$storescu_cmd -s 00081030=$subject"
fi

# Add the directory to the storescu command
storescu_cmd="$storescu_cmd $directory"

# Print the constructed command for debugging
echo "Executing command: $storescu_cmd"

# Execute the storescu command
eval $storescu_cmd
