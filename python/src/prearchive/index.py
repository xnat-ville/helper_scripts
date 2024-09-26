#!/bin/python3
"""
index.py
---
--------------------------------------------------------------------------------
This application interacts with and creates an index of projects in the CNDA prearchive.
It performs an initial scan to gather basic metadata about project folders or timestamp
folders (e.g., file counts, modification times), without opening DICOM files.

If the user specifies the `-D` (demographics) or `-M` (modality) flags, a secondary scan
is performed, which opens DICOM files to extract specific patient information or modality
details. The collected data can be written to a CSV file or logged.

Example usage of the CLI:
```bash
$ python3
```
"""
__version__ = (1, 0, 0)

import argparse
import csv
import pydicom
from datetime import datetime
from pathlib import Path

#This class holds relevant details about each session folder found during the prearchive scanning process
class SessionFolder:

  #Initializes a new SessionFolder object with default values for all attributes.
  def __init__(self):
        self.project_path     = ""
        self.project_label    = ""
        self.timestamp_folder = ""
        self.timestamp =        ""
        self.session_path     = ""
        self.session_label    = ""
        self.last_modified_time = ""
        self.scan_folders     = 0 #number of scan series folders in a session
        self.total_files      = 0 # total number of file
        self.dcm_files        = 0 #total amount of dcm files
        self.patient_name     = ""
        self.patient_id       = ""
        self.modalities       = set()
        self.sop_classes      = set()
      # self.symbolic_links   = 0

"""
Scans the prearchive folder structure and builds an array of SessionFolder objects.
This function scans for projects, timestamps, and sessions, and gathers basic metadata
(e.g., file counts, modification times). DICOM files are not opened or processed here.
Detailed metadata extraction (ex. demographics or modality) occurs in secondary prearchive scan based on flags set.
"""

#This function reads the project list from the given .txt file.
def read_project_list(file_path: str, log_f=None):
    try:
        with open(file_path, 'r') as file:
            projects_or_timestamps = [line.strip() for line in file if line.strip()]
        return projects_or_timestamps, True  # Return True to indicate success
    except FileNotFoundError:
        error_message = f"Error: The file {file_path} was not found."
        print(error_message)
        if log_f:
            log_f.write(error_message + "\n")  # Log the error to the log file
        return [], False  # Return False to indicate failure
    except Exception as e:
        error_message = f"Error reading file {file_path}: {e}"
        print(error_message)
        if log_f:
            log_f.write(error_message + "\n")  # Log the error to the log file
        return [], False

# Helper function to check if a directory is a timestamp folder in the format YYYYMMDD_HHMMSSsss
def is_timestamp_folder(folder: Path):
    try:
        # Attempt to parse the folder name in the given format (YYYYMMDD_HHMMSSsss)
        datetime.strptime(folder.name, "%Y%m%d_%H%M%S%f")
        return True
    except ValueError:
        return False

def initial_prearchive_scan(args: argparse.Namespace, session_folders):
    folder_path = Path(args.prearchive_path)

    # Open the log file if specified
    log_f = None
    if args.log:
        log_f = open(args.log, 'w')

    try:
        # Use the helper function to read the list from the file if provided
        if args.top_level_folders:
            top_level_folders, success = read_project_list(args.top_level_folders, log_f)
            if not success:
                return  # Stop the function if reading the project list failed
        else:
            top_level_folders = [folder.name for folder in folder_path.iterdir() if folder.is_dir()]

        # Process each project or timestamp if the list was successfully read
        for folder_name in top_level_folders:
            folder_name = folder_name.strip()

            # Process as usual
            folder_path_to_process = folder_path / folder_name
            if folder_path_to_process.is_dir():
                if is_timestamp_folder(folder_path_to_process):
                    process_timestamp_folder(args, "Unassigned", folder_path_to_process, session_folders, log_f)
                else:
                    process_project_folder(args, folder_path_to_process, session_folders, log_f)
            else:
                print(f"Warning: {folder_path_to_process} is not a valid directory.")
    finally:
        if log_f:
            log_f.close()  # Ensure the log file is closed properly

"""
Helper function to process project-named folders.
This function iterates through the timestamp folders inside a project folder,
passing each timestamp folder to the process_timestamp_folder function.
It is used when scanning specific project-named folders or the entire prearchive.
"""
def process_project_folder(args: argparse.Namespace, project_folder: Path, session_folders, log_f):
    project_name = project_folder.name
    for timestamp_folder in project_folder.iterdir():
        if timestamp_folder.is_dir():
            process_timestamp_folder(args, project_name, timestamp_folder, session_folders, log_f)

# Function to process the timestamp folder and gather session data
def process_timestamp_folder(args: argparse.Namespace, project_name: str, timestamp_folder: Path, session_folders, log_f):
    # Iterate over the session folders inside each timestamp
    for session_folder in timestamp_folder.iterdir():
        if session_folder.is_dir():
            session_label = session_folder.name

            # Initialize counters and variables
            total_files = 0
            dcm_files = 0
            last_modified_unix_timestamp = 0
            last_modified_formatted_timestamp = ""
            scan_folders = 0

            # Iterate over all items in the session folder
            for item in session_folder.rglob('*'):
                scans_folder = session_folder / 'SCANS'
                if scans_folder.is_dir():
                    scan_folders = sum(1 for folder in scans_folder.iterdir() if folder.is_dir())
                if item.is_file():
                    total_files += 1
                    if item.suffix == '.dcm':
                        dcm_files += 1
                    file_time = item.stat().st_mtime
                    if file_time > last_modified_unix_timestamp:
                        last_modified_unix_timestamp = file_time
                        last_modified_formatted_timestamp = datetime.fromtimestamp(last_modified_unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            f1 = SessionFolder()
            f1.project_path = str(timestamp_folder.parent) if project_name != "Unassigned" else str(timestamp_folder)
            f1.project_label = project_name
            f1.timestamp_folder = timestamp_folder
            f1.timestamp = timestamp_folder.name
            f1.session_path = session_folder
            f1.session_label = session_label
            f1.last_modified_time = last_modified_formatted_timestamp
            f1.scan_folders = scan_folders
            f1.total_files = total_files
            f1.dcm_files = dcm_files

            session_folders.append(f1)

            # Log the session if a log file is specified
            if args.log:
                log_f.write(f"{f1.timestamp},{f1.session_path}\n")
                log_f.flush()

    #f2 = SessionFolder()
    #f2.session_path = "/opt/Customer-Support/CNDA/xnat-ville/helper_scripts/python/src/prearchive/y"
    #f2.relative_path = "y"
    #session_folders.append(f2)

# Uses the pydicom library to open and read DICOM files.
# For demographics (-D), it extracts and stores the patient name and ID.
# For modality (-M), it extracts the DICOM modality and SOP Class UID.

def fill_session_data(session_folder: SessionFolder, args: argparse.Namespace):
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
                if not file_list:
                    continue
                first_file = file_list[0]

                # Pick the first DICOM file in the folder
                try:
                    dicom_data = pydicom.dcmread(first_file)

                    # Extract demographics data if the -D flag is set
                    if args.demographics:
                        session_folder.patient_name = dicom_data.PatientName if 'PatientName' in dicom_data else "Unknown"
                        session_folder.patient_id = dicom_data.PatientID if 'PatientID' in dicom_data else "Unknown"

                    # Extract modality data if the -M flag is set
                    if args.modality:
                        modality = dicom_data.Modality if 'Modality' in dicom_data else "Unknown"
                        session_folder.modalities.add(modality)

                        sop_class_uid = dicom_data.SOPClassUID if 'SOPClassUID' in dicom_data else "Unknown"
                        session_folder.sop_classes.add(sop_class_uid)

                except Exception as e:
                    print(f"Error reading DICOM file {first_file}: {e}")
                    return  # Exit after the first failure
    else:
        print(f"Scans folder not found in {session_folder.session_path}")


# This function performs a secondary scan of the prearchive. If the -D (demographics) or
# -M (modality) flags are set, it processes the session folders, reads the first DICOM file found,
# and updates the session information accordingly.
# If neither flag is set, the function exits without modifying the session data.

def secondary_prearchive_scan(args: argparse.Namespace, session_folders):
    for session_folder in session_folders:
        #print(session_folder.session_path)

        # Call the combined function to fill both demographics and modality data
        fill_session_data(session_folder, args)

# Generates output for the session data collected. If the --csv flag is provided, the output
# is written to a CSV file. If no CSV file is provided, output is sent to stdout.
# The output includes base session data, and if any flags are set, additional information is included in accordance with those flags.

def index_output(args: argparse.Namespace, session_folders):
    if args.csv:
        with open(args.csv, mode='w', newline='') as csv_file:
            # Start with the base fields
            fieldnames = ['Project Path', 'Project Label', 'Session Timestamp Folder', 'Timestamp',
                          'Session Path', 'Session Label', 'Last Modified Time', 'Scan Folders', 'Total Files',
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
                    'Last Modified Time': session.last_modified_time,
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

    parser.add_argument('-t', '--top-level-folders',
                        help="Path to text file containing a list of project folders or timestamps",
                        dest='top_level_folders')

    # Mandatory path to the prearchive folder
    parser.add_argument('prearchive_path', help="Path to prearchive folder")

    args = parser.parse_args()

    # Initialize an empty list to hold session folder objects
    session_folders = []
    log_entries = []

    # Perform the initial scan of the prearchive directory
    initial_prearchive_scan(args, session_folders)

    # Perform a secondary scan for demographics or modality if flags are set
    secondary_prearchive_scan(args, session_folders)

    # Output the collected data to CSV, JSON, or stdout
    index_output(args, session_folders)

    # Now that logging is complete, print the log written message
    if args.log:
        print(f"Log has been written to txt file: {args.log}")

    # tail -f will let you see progress of the logging in the terminal


    #tail -f will let you see progress of the logging in terminal

    # The text document will be made by someone going into the prearchive directory and running ls -d CCIR* 2020* > /tmp/project_list.txt
    # or they might run ls -d CCIR* > /tmp/project_list.txt
    # or they might run ls -d 2023* > /tmp/project_list.txt

    # to follows status is tail -f /tmp/log_of_prearchive.txt


