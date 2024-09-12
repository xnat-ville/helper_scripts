#!/bin/bash

# Script acts as a C-STORE delegate for scanners in the MR Facility:
#  Bay 1
#  Bay 2
#  Bay 3
#
# The script will send one folder (including subfolders) of files
# that corresponds to one imaging session. The user specifies
#  * Folder to send
#  * Scanner label
#  * Project
#  * Subject Label
#  * Session Label
# Optional parameters allow you to specify a different DICOM receiver
# for testing purposes

check_args() {
 if [ $# -lt 5 ] ; then
  echo "
Arguments:
  Folder to send
  Scanner Label: BAY1 BAY2 BAY3 NRB1
  Project Label
  Subject Label
  Session Label
  [Alternate Target AE title]
  [Alternate Target Host]
  [Alternate Target Port]
"
  exit 1
fi
}

check_storescu_bin() {
 storescu_binx=$(find_storescu)
 if [[ -z "$storescu_binx" ]] ; then
  echo "Could not find storescu on our PATH nor using the variable DCM4CHE_BASE"
  echo "Script exits"
  exit 1
 fi
}

find_storescu() {
 storescu_path=`which storescux`
 if [[ $? -ne 0 ]] ; then
  if [ -z ${DCM4CHE_BASE+x} ] ; then
   # Variable is not set
   storescu_path=`which storescux`
  else
   # Variable is set
   storescu_path="$DCM4CHE_BASE/bin/storescu"
  fi
 fi

 echo "$storescu_path"
}

determine_calling_title() {
 scanner_label=$2
 if [[ $scanner_label == "BAY1" || $scanner_label == "BAY2" || $scanner_label == "BAY3" ]] ; then
  rtn_label=MRF-CTP1_$scanner_label
 else
  rtn_label=MRF-CTP1_BAY1
 fi

 echo "$rtn_label"
}

determine_called_title() {
 scanner_label=$2
 if [[ $scanner_label == "BAY1" || $scanner_label == "BAY2" || $scanner_label == "BAY3" ]] ; then
  rtn_label=CNDA_$scanner_label
 else
  rtn_label=CNDA_BAY1
 fi

 if [[ $# -ge 6 ]] ; then
  rtn_label="$6"
 fi

 echo "$rtn_label"
}

determine_host() {
 rtn_host="cnda-shadow03.nrg.wustl.edu"
 if [[ $# -ge 7 ]] ; then
  rtn_host="$7"
 fi

 echo "$rtn_host"
}

determine_port() {
 rtn_port="8104"
 if [[ $# -ge 8 ]] ; then
  rtn_port="$8"
 fi

 echo "$rtn_port"
}

check_args $*
check_storescu_bin

folder=$1
scanner=$2
project=$3
subject=$4
session=$5

calling_title=$(determine_calling_title $*)
called_title=$(determine_called_title   $*)
host=$(determine_host                   $*)
port=$(determine_port                   $*)
storescu_bin=$(find_storescu)

echo "Calling:   $calling_title"
echo "Called:    $called_title"
echo "Host:      $host"
echo "Port:      $port"
echo "Store SCU: $storescu_bin"

x="$storescu_bin				\
  -s \"00100010=$subject\"		\
  -s \"00100020=$session\"		\
  -s \"00104000=Project:$project\"	\
  -b $calling_title			\
  -c $called_title@$host:$port $folder"

echo $x
`$x &> /tmp/$session.log`
