#!/bin/sh


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

