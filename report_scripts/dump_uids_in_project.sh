#!/bin/sh

# Check the program arguments
# Args:
#        Project Folder
check_args() {
 if [ ! -e "$1" ] ; then
  echo Did not find project folder $1 in current directory `pwd`
  exit 1
 fi

 if [ ! -e "$1/arc001" ] ; then
  echo Did not find archive folder $1/arc001 in current directory `pwd`
  exit 1
 fi

}

# Make a list of all scan folders in the project
# Args:
#        Project Folder
#        Output file
list_scan_folders() {
 echo Scanning $1 for folders. Output goes in $2
 rm -f $2
 find $1/arc001 -mindepth 3 -maxdepth 3 -type d | tee -a $2 | cat
 echo ""
}

# Find a representative DICOM file for each folder in the input list
# Args:
#        File with list of folders to search
#        Output file
list_one_dicom_file() {
 echo Find one DICOM file in each folder listed in $1
 rm -f $2

 while read -r line; do
  echo    $line
  find $line -type f -name '*dcm' | tail -1 | tee -a $2 | cat
 done < $1
 echo ""
}

# Dump Study and Series information to separate files
# Args:
#       List of DICOM files to dump
#       Output study information file
#       Output series information file
dump_study_series() {
 echo "Dump Study and Series info: $1 $2 $3"

 rm -f $2 $3

 while read -r line; do
  echo    $line
  dcmdump $line | grep --label $line -H -e 0010,0010 -e 0010,0020 -e 0008,1030 -e StudyDate -e StudyTime -e StudyInstanceUID                                      >> $2
  dcmdump $line | grep --label $line -H -e 0010,0010 -e 0010,0020 -e 0008,1030 -e StudyDate -e StudyTime -e StudyInstanceUID -e SeriesNumber -e SeriesInstanceUID >> $3
 done < $1
 echo ""

}

PROJECT=$1

set -e
check_args $PROJECT
X=/tmp/uids
rm -rf $X; mkdir -p $X

list_scan_folders   $1                     $X/scan_folders.txt
list_one_dicom_file $X/scan_folders.txt    $X/dicom_file_list.txt
dump_study_series   $X/dicom_file_list.txt $X/study_info.txt $X/series_info.txt

echo Found `wc -l $X/scan_folders.txt` folders
echo Found `wc -l $X/dicom_file_list.txt` DICOM files
