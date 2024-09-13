#!/bin/python3
"""
index.py
---
--------------------------------------------------------------------------------
This application interacts with and creates an index of projects in an XNAT prearchive

Example usage of the CLI:
```bash
$ python3
```
"""

# TODO: Implement handling for "Unassigned" projects in the prearchive. These might
#  not exist in a separate folder and may require additional logic to detect and handle.
#  You can ssh into a machine and check on server--HOW IS UNASSIGNED laid out

__version__ = (1, 0, 0)

import argparse
import csv
import pydicom
from datetime import datetime
from pathlib import Path

class SessionFolder:
    def __init__(self):
        self.project_path     = ""
        self.project_label    = ""
        self.timestamp_folder = ""
        self.timestamp =        ""
        self.session_path     = ""
        self.session_label    = ""
        self.most_recent_time = "" #time of the newest file under the session folder
        self.scan_folders     = 0 #number of scan series folders in a session
        self.total_files      = 0 # total number of file
        self.dcm_files        = 0 #total amount of dcm files

        #self.symbolic_links   = 0
        self.patient_name     = ""
        self.patient_id       = ""
        self.modalities       = set()
        self.sop_classes      = set()


# Scans the prearchive folder structure and builds an array of SessionFolder objects.
# This function scans for projects, timestamps, and sessions, and gathers basic metadata
# (e.g., file counts, modification times). DICOM files are not opened or processed here.
# Detailed metadata extraction (demographics or modality) occurs in later stages based on flags (-D, -M).

def initial_prearchive_scan(args: argparse.Namespace, session_folders):
    # Define the path to the prearchive folder
    folder_path = Path(args.prearchive_path)

    # List all directories (could be projects or directly timestamp folders if Unassigned)
    projects_or_timestamps = folder_path.iterdir()

    for project_or_timestamp in projects_or_timestamps:
        if project_or_timestamp.is_dir():
            # Case 1: Check if this is a timestamp folder directly (i.e., Unassigned project)
            timestamp_folder = project_or_timestamp
            if is_timestamp_folder(timestamp_folder):
                # Treat as Unassigned project
                process_timestamp_folder(args, "Unassigned", timestamp_folder, session_folders)
            else:
                # Case 2: Process as a regular project folder
                project_name = project_or_timestamp.name
                for timestamp_folder in project_or_timestamp.iterdir():
                    if timestamp_folder.is_dir():  # Ensure it's a directory
                        process_timestamp_folder(args, project_name, timestamp_folder, session_folders)

# Helper function to check if a directory is a timestamp folder in the format YYYYMMDD_HHMMSSsss
def is_timestamp_folder(folder: Path):
    try:
        # Attempt to parse the folder name in the given format (YYYYMMDD_HHMMSSsss)
        datetime.strptime(folder.name, "%Y%m%d_%H%M%S%f")
        return True
    except ValueError:
        return False


# Function to log details to a log file (text format)
def log_session(log_file, session_folder_path, timestamp_folder_name):
    with open(log_file, mode='a') as log_f:
        log_f.write(f"Timestamp Folder: {timestamp_folder_name}, Session Path: {session_folder_path}\n")

# Helper function to process the timestamp folder and gather session data
def process_timestamp_folder(args: argparse.Namespace, project_name: str, timestamp_folder: Path, session_folders):
    # Iterate over the session folders inside each timestamp
    for session_folder in timestamp_folder.iterdir():
        if session_folder.is_dir():  # Ensure it's a directory
            session_label = session_folder.name

            # Initialize counters and variables
            total_files = 0
            dcm_files = 0
            most_recent_unix_timestamp = 0
            most_recent_formatted_timestamp = 0
            scan_folders = 0

            # Iterate over all items in the session folder
            for item in session_folder.rglob('*'):  # Recursively scan the folder
                scans_folder = session_folder / 'SCANS'
                if scans_folder.is_dir():
                    # Only count the top-level directories in the SCANS folder (scan series)
                    scan_folders = sum(1 for folder in scans_folder.iterdir() if folder.is_dir())
                if item.is_file():
                    total_files += 1  # Count all files
                    if item.suffix == '.dcm':
                        dcm_files += 1  # Count only .dcm files
                    # Track the most recent modification time
                    file_time = item.stat().st_mtime
                    if file_time > most_recent_unix_timestamp:
                        most_recent_unix_timestamp = file_time
                        most_recent_formatted_timestamp = datetime.fromtimestamp(most_recent_unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            # Create a new session object and append it to the session_folders list
            f1 = SessionFolder()

            # Set the project path differently for assigned vs unassigned projects
            if project_name == "Unassigned":
                f1.project_path = str(timestamp_folder)  # Use the full path to the timestamp folder
            else:
                f1.project_path = str(timestamp_folder.parent)  # Use the parent folder (project folder)

            f1.project_label = project_name
            f1.timestamp_folder = timestamp_folder
            f1.timestamp = timestamp_folder.name
            f1.session_path = session_folder
            f1.session_label = session_label
            f1.most_recent_time = most_recent_formatted_timestamp
            f1.scan_folders = scan_folders
            f1.total_files = total_files
            f1.dcm_files = dcm_files

            session_folders.append(f1)

            # Log session folder and timestamp folder name if the log argument is provided
            if args.log:
                log_session(args.log, session_folder, f1.timestamp)



    #f2 = SessionFolder()
    #f2.session_path = "/opt/Customer-Support/CNDA/xnat-ville/helper_scripts/python/src/prearchive/y"
    #f2.relative_path = "y"
    #session_folders.append(f2)

# Uses the pydicom library to open and read DICOM files.
# For demographics (-D), it extracts and stores the patient name and ID.
# For modality (-M), it extracts the DICOM modality and SOP Class UID.

def fill_demographics(session_folder: SessionFolder):
    folder_path = Path(session_folder.session_path)
    scans_folder = folder_path / 'SCANS'

    # Check if the scans folder exists
    if scans_folder.is_dir():
        # Iterate over the numbered scan series folders
        for scan_series_folder in scans_folder.iterdir():
            if scan_series_folder.is_dir():
                dicom_folder = scan_series_folder / 'DICOM'

            # If "DICOM" folder doesn't exist, check for "secondary"
            if not dicom_folder.is_dir():
                dicom_folder = scan_series_folder / 'secondary'

            # Check if the DICOM or secondary folder exists
            if dicom_folder.is_dir():
                file_list = list(dicom_folder.glob('*.dcm'))
                first_file = file_list[0]

                # Pick the first DICOM file in the folder
                try:
                    dicom_data = pydicom.dcmread(first_file)

                    # Extracts patient name and patient ID
                    session_folder.patient_name = dicom_data.PatientName if 'PatientName' in dicom_data else "Unknown"
                    session_folder.patient_id = dicom_data.PatientID if 'PatientID' in dicom_data else "Unknown"

                    print(f"Extracted demographics from {first_file}:")
                    print(f"Patient Name: {session_folder.patient_name}, Patient ID: {session_folder.patient_id}")

                except Exception as e:
                    print(f"Error reading DICOM file {first_file}: {e}")
                    return  # Exit after the first failure
    else:
        print(f"Scans folder not found in {session_folder.session_path}")


def fill_modality(session_folder: SessionFolder):
    folder_path = Path(session_folder.session_path)
    scans_folder = folder_path / 'SCANS'

    # Check if the scans folder exists
    if scans_folder.is_dir():
        # Iterate over the numbered scan series folders
        for scan_series_folder in scans_folder.iterdir():
            if scan_series_folder.is_dir():
                dicom_folder = scan_series_folder / 'DICOM'

            # If "DICOM" folder doesn't exist, check for "secondary"
            if not dicom_folder.is_dir():
                dicom_folder = scan_series_folder / 'secondary'

            # Check if the DICOM or secondary folder exists
            if dicom_folder.is_dir():
                file_list = list(dicom_folder.glob('*.dcm'))
                first_file = file_list[0]

                # Pick the first DICOM file in the folder
                try:
                    dicom_data = pydicom.dcmread(first_file)

                    # Extracts Modality and adds it to the to modalities set
                    modality = dicom_data.Modality if 'Modality' in dicom_data else "Unknown"
                    session_folder.modalities.add(modality)

                    # Extracts SOP Class UID and adds it to the sop_classes set
                    sop_class_uid = dicom_data.SOPClassUID if 'SOPClassUID' in dicom_data else "Unknown"
                    session_folder.sop_classes.add(sop_class_uid)

                    print(f"Extracted modality from {first_file}:")
                    print(f"Modality: {modality}, SOP Class UID: {sop_class_uid}")

                except Exception as e:
                    print(f"Error reading DICOM file {first_file}: {e}")
                    return  # Exit after the first failure
    else:
        print(f"Scans folder not found in {session_folder.session_path}")


# This function performs a secondary scan of the prearchive if any flags are set. It processes the session folders, reads the first DICOM file
# found, and updates the session information accordingly.
# If neither flag is set, the function exits without modifying the session data.

def secondary_prearchive_scan(args: argparse.Namespace, session_folders):
    for session_folder in session_folders:
        print(session_folder.session_path)

        # If demographics flag is set, call demographics function
        if args.demographics:
            fill_demographics(session_folder)

        # If modality flag is set, call modality function
        if args.modality:
            fill_modality(session_folder)


# Generates output for the session data collected. If the --csv flag is provided, the output
# is written to a CSV file. If no CSV file is provided, output is sent to stdout.
# The output includes base session data, and if any flags are set, additional information is included in accordance with those flags.

def index_output(args: argparse.Namespace, session_folders):
    if args.csv:
        with open(args.csv, mode='w', newline='') as csv_file:
            # Start with the base fields
            fieldnames = ['Project Path', 'Project Label', 'Session Timestamp Folder', 'Timestamp',
                          'Session Path', 'Session Label', 'Most Recent Time', 'Scan Folders', 'Total Files',
                          'DCM Files']

            # Add demographic fields if the -D flag is set
            if args.demographics:
                fieldnames += ['Patient Name', 'Patient ID']  # Add these fields only if -D is passed

            # Add modality fields if the -M flag is set
            if args.modality:
                fieldnames += ['Modalities', 'SOP Classes']  # Add these fields only if -M is passed

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            # Write the data for each session
            for session in session_folders:
                # Base row data (present in all outputs)
                row = {
                    'Project Path': session.project_path,
                    'Project Label': session.project_label,
                    'Session Timestamp Folder': session.timestamp_folder,
                    'Timestamp': session.timestamp,
                    'Session Path': session.session_path,
                    'Session Label': session.session_label,
                    'Most Recent Time': session.most_recent_time,
                    'Scan Folders': session.scan_folders,
                    'Total Files': session.total_files,
                    'DCM Files': session.dcm_files
                }

                # Add demographics data if the -D flag is set
                if args.demographics:
                    row['Patient Name'] = session.patient_name
                    row['Patient ID'] = session.patient_id

                # Add modality data if the -M flag is set
                if args.modality:
                    row['Modalities'] = ', '.join(session.modalities)
                    row['SOP Classes'] = ', '.join(session.sop_classes)

                # Write the row to the CSV file
                writer.writerow(row)

        print(f"Data has been written to CSV file: {args.csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List projects from an XNAT system")

    # CSV and JSON output options
    parser.add_argument('-c', '--csv', dest='csv', help="Path to CSV output")
    parser.add_argument('-j', '--json', dest='json', help="Path to JSON output")

    # Optional project and folder input paths
    parser.add_argument('-p', '--projects', dest='projects', help="Path to input list of projects to index")
    parser.add_argument('-f', '--folders', dest='folders', help="Path to input list of folders to index")

    # Flags for demographics and modality data
    parser.add_argument('-D', '--demographics', dest='demographics', help="Add demographic data to base output",
                        action='store_true')
    parser.add_argument('-M', '--modality', dest='modality', help="Add modality data to base output",
                        action='store_true')

    # Log file path (optional, logs session details only if log file exists)
    parser.add_argument('-l', '--log', dest='log', help="Path to log file for session details")

    # Mandatory path to the prearchive folder
    parser.add_argument('prearchive_path', help="Path to prearchive folder")

    args = parser.parse_args()

    # Initialize an empty list to hold session folder objects
    session_folders = []

    # Perform the initial scan of the prearchive directory
    initial_prearchive_scan(args, session_folders)

    # Perform a secondary scan for demographics or modality if flags are set
    secondary_prearchive_scan(args, session_folders)

    # Output the collected data to CSV, JSON, or stdout
    index_output(args, session_folders)



