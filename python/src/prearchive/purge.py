#!/bin/python3
"""
purge.py
---
--------------------------------------------------------------------------------
This application purges the file system of an XNAT prearchive.

Example usage of the CLI:
```bash
$ python3
```
"""

__version__ = (1, 0, 0)

import argparse
import csv



def purge_prearchive_folder(args: argparse.Namespace):
    f1 = ""



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List projects from an XNAT system")
    parser.add_argument('-l', '--log',      dest='log',      help="Path to log output")
    parser.add_argument('-a', '--age',      dest='age',      help="Minimum age in days for a folder to be deleted")
    parser.add_argument('-d', '--dryrun',   dest='dryrun',   help="Perform a dry run, but do not delete any files/folders",  action='store_true')
    parser.add_argument('-s', '--silent',   dest='silent',   help="Add demographic data to base output",  action='store_true')
    parser.add_argument('-v', '--verbose',  dest='verbose',  help="Enable verbose output",                action='store_true')
    parser.add_argument('index_file',                        help="Path to index")


    args = parser.parse_args()

# Read the index file into an array
# Invoke purge_prearchive_folder with both the args structure and index file array


