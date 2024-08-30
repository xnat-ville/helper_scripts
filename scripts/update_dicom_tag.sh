#!/bin/bash

#This script allows you to manually edit a DICOM tag by using DCMTK.

# Prompt the user to enter the filename of the DICOM file
echo "Enter the filename of the DICOM file:"
read file_name

# Check if the file exists
if [ ! -f "$file_name" ]; then
    echo "File does not exist."
    exit 1
fi

# Prompt the user to enter the DICOM tag
echo "Enter the DICOM tag to update (e.g., 0010,0010):"
read dicom_tag

# Prompt the user to enter the new value for the DICOM tag
echo "Enter the new value for the DICOM tag:"
read new_value

# Update the DICOM tag using dcmodify
dcmodify -m "$dicom_tag=$new_value" "$file_name"

# Check if dcmodify was successful
if [ $? -eq 0 ]; then
    echo "DICOM tag updated successfully."
else
    echo "Failed to update DICOM tag."
fi
