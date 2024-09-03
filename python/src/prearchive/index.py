#!/bin/python3
"""
index.py
---
--------------------------------------------------------------------------------
This application interacts creates an index of projects in an XNAT prearchive

Example usage of the CLI:
```bash
$ python3
```
"""

__version__ = (1, 0, 0)

import argparse
import csv

class SessionFolder:
    def __init__(self):
        self.full_path        = ""
        self.relative_path    = ""
        self.project          = ""
        self.most_recent_time = ""
        self.scan_folders     = 0
        self.total_files      = 0
        self.dcm_files        = 0
        self.symbolic_links   = 0
        self.patient_name     = ""
        self.patient_id       = ""
        self.modalities       = []
        self.sop_classes      = []

# Scan the prearchive folders and build an array of SessionFolder objects
# This function looks through the folders and creates a baseline object for each session folder.
# The function relies on the XNAT directory structure and does not open/read any files.
# Not reading DICOM files is an intentional decision.
def initial_prearchive_scan(args: argparse.Namespace, session_folders):
    f1 = SessionFolder()
    f1.full_path = "/opt/Customer-Support/CNDA/xnat-ville/helper_scripts/python/src/prearchive/x"
    f1.relative_path = "x"
    session_folders.append(f1)

    f2 = SessionFolder()
    f2.full_path = "/opt/Customer-Support/CNDA/xnat-ville/helper_scripts/python/src/prearchive/y"
    f2.relative_path = "y"
    session_folders.append(f2)


# This function performs a secondary scan of the prearchive if either of the
# args.demographics or args.modality flags are set. In that case, the function
# walks through the list of session_folders, reads select DICOM files from each
# session folder, and updates the entry.
# If neither of those flags are set, the function returns immediately without
# modifying the session_folders data
def secondary_prearchive_scan(args: argparse.Namespace, session_folders):
    if (args.demographics or args.modality):
        # Add auxiliary data
        print(f"Perform auxiliary scan for demographics {args.demographics} and/or modality {args.modality}")


# Generate output of the index information that was gathered previously.
# The variables args.csv and args.json give the path(s) to output files.
# If neither of those variables is set, output is sent in CSV format to the stdout.
# Output includes base values for all session folders. Extra information is included
# if either the args.demographics or the args.modality flags are set.
def index_output(args: argparse.Namespace, session_folders):
    for session in session_folders:
        print(f"{session.relative_path} {session.full_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List projects from an XNAT system")
    parser.add_argument('-c', '--csv',             dest='csv',             help="Path to CSV output")
    parser.add_argument('-j', '--json',            dest='json',            help="Path to CSV output")
    parser.add_argument('-p', '--projects',        dest='projects',        help="Path to input list of projects to index")
    parser.add_argument('-f', '--folders',         dest='folders',         help="Path to input list of folders to index")
    parser.add_argument('-D', '--demographics',    dest='demographics',    help="Add demographic data to base output",  action='store_true')
    parser.add_argument('-M', '--modality',        dest='modality',        help="Add demographic data to base output",  action='store_true')
    parser.add_argument('prearchive_path',                                 help="Path to prearchive folder")

    args = parser.parse_args()
    session_folders = []
    initial_prearchive_scan(args, session_folders)
    secondary_prearchive_scan(args, session_folders)
    index_output(args, session_folders)


