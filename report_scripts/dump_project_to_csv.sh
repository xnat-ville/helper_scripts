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

# Args:
#        Input file with text
#        Unique string for grep
extract_value() {
 v=`grep "$2" $1 | cut -d ' ' -f 3 | sed -e 's/^.//' -e 's/.$//'`
 echo $v
}

# Dump Study and Series information to separate files
# Args:
#       List of DICOM files to dump
#       Output study information file
#       Output series information file
#       Output tmp file
dump_study_series() {
 rm -f $2 $3 $4
 TAB="   "

 cat $1
 while read -r line; do
#  dcmdump $line > $4
#  study_txt=$line
#  for field in 0008,0016 '^.0010,0010' '   .0010,0010' '^.0010,0020' '   .0010,0020'  StudyDate StudyTime 0008,1010 StudyInstanceUID ; do
#   value=$(extract_value $4 $field)
#   study_txt="${study_txt}${TAB}${value}"
#  done
#  series_txt=$study_txt
#  for field in SeriesNumber SeriesInstanceUID ; do
#   value=$(extract_value $4 $field)
#   series_txt="${series_txt}${TAB}${value}"
#  done
#
#  echo "$study_txt"
#  echo "$study_txt"  >> $2
#  echo "$series_txt" >> $3

  P=/data/CNDA/home/helper_scripts
  export PYTHONPATH=$P
  csv_line=`python3 -m xnat_cli_scripts.dicom_metadata --extract --filename $line`
  echo "$csv_line"  >> $2

 done < $1
 echo "Done"
}

BASE=`dirname $0`
. $BASE/common_report_functions.sh

PROJECT=$1
pushd /data/CNDA/archive

#set -e
check_args $PROJECT
X=/tmp/uids
rm -rf $X; mkdir -p $X

list_scan_folders   $1                     $X/scan_folders.txt
list_one_dicom_file $X/scan_folders.txt    $X/dicom_file_list.txt
dump_study_series   $X/dicom_file_list.txt $X/study_info.txt $X/series_info.txt $X/tmp.txt

echo Found `wc -l $X/scan_folders.txt` folders
echo Found `wc -l $X/dicom_file_list.txt` DICOM files
