#!/bin/python3

import argparse
import csv
import os
from datetime import datetime
from pathlib import Path
import pydicom

# Define function to parse the command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Scan MRF Relay storage folders and extract DICOM info.")
    parser.add_argument('-s', '--start-date', type=str, help="Start date in YYYYMMDD format")
    parser.add_argument('-e', '--end-date', type=str, help="End date in YYYYMMDD format")
    parser.add_argument('-c', '--csv', type=str, required=True, help="Path to CSV output")
    return parser.parse_args()

# Define function to check if folder date is in the given range
def date_in_range(date_str, start_date=None, end_date=None):
    date = datetime.strptime(date_str, '%Y%m%d')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y%m%d')
        if date < start_date:
            return False
    if end_date:
        end_date = datetime.strptime(end_date, '%Y%m%d')
        if date > end_date:
            return False
    return True

# Define function to format Study Time into HH:MM:SS
def format_study_time(study_time):
    if len(study_time.split('.')[0]) >= 6:
        hours = study_time[:2]
        minutes = study_time[2:4]
        seconds = study_time[4:6]
        return f"{hours}:{minutes}:{seconds}"
    return "Unknown"

# Define function to process each DICOM file and extract required information
def process_dicom_file(dicom_path):
    dicom_data = pydicom.dcmread(dicom_path)
    patient_name = dicom_data.get('PatientName', 'Unknown')
    patient_id = dicom_data.get('PatientID', 'Unknown')
    study_date = dicom_data.get('StudyDate', 'Unknown')
    study_time_raw = dicom_data.get('StudyTime', 'Unknown')
    study_time = format_study_time(study_time_raw)
    return patient_name, patient_id, study_date, study_time

# Define main function to scan the storage folders and collect data
def main():
    args = parse_args()

    # Define Bay locations
    bay_paths = [
        '/ceph/mrf_ctp/mrf_ctp1/bay1/storage',
        '/ceph/mrf_ctp/mrf_ctp1/bay2/storage',
        '/ceph/mrf_ctp/mrf_ctp1/bay3/storage'
    ]

    # Prepare CSV output
    with open(args.csv, 'w', newline='') as csvfile:
        fieldnames = ['Relay Folder Name', 'Patient Name', 'Patient ID', 'Study Date', 'Study Time', 'Bay Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for bay_path in bay_paths:
            bay_location = Path(bay_path).parent.name  # Extracts "bay1", "bay2", or "bay3"
            for date_folder in Path(bay_path).iterdir():
                if date_folder.is_dir() and date_folder.name.isdigit() and date_in_range(date_folder.name, args.start_date, args.end_date):
                    for scan_folder in date_folder.iterdir():
                        if scan_folder.is_dir() and '_xfered' in scan_folder.name:
                            dicom_files = list(scan_folder.glob('*.dcm'))
                            if dicom_files:
                                dicom_path = dicom_files[0]  # Take the first DICOM file found
                                patient_name, patient_id, study_date, study_time = process_dicom_file(dicom_path)
                                writer.writerow({
                                    'Relay Folder Name': scan_folder.name,
                                    'Patient Name': patient_name,
                                    'Patient ID': patient_id,
                                    'Study Date': study_date,
                                    'Study Time': study_time,
                                    'Bay Location': bay_location
                                })
                            else:
                                print(f"No DICOM files found in {scan_folder}")
    
    print(f"Output has been printed to {args.csv}")

if __name__ == "__main__":
    main()

