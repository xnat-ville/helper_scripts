# Scripts for Managing XNAT Prearchive

## index_prearchive.py
This script searches the prearchive file system and creates an index of the entries.
The output can be a CSV file, a JSON file or both.
The output contains a set of basic values for each session found in the archive.
The basic output would not contain PHI unless the folder names themselves contain PHI.
Auxiliary output such as the DICOM values for Patient Name and Patient ID might contain PHI.

### Invocation
```
export PYTHONPATH=.../helper_scripts/python
python3 -m prearchive.index [flags] prearchive-path
```
Flag values are:

| Flag               | Description                                         |
|--------------------|-----------------------------------------------------|
| -c, --csv          | Path to output CSV file                             |
| -j, --json         | Path to output JSON file                            |
| -p, --projects     | File with list of projects to index. Ignore others. |
| -f, --folders      | File with list of folders to index. Ignore others.  |
| -D, --demographics | Add additional demographics to output. See below.   |
| -M, --modality     | Add modality/SOP class information.                 |

If neither the CVS nor the JSON flag is included, the software will print the output in CSV format to the stdout.


### Output
The standard output contains these data items:
1. Project (can be "Unassigned")
1. Folder name
1. Date/Time of most recent file
1. Number of scan folders
1. Total files
1. Number of files with .dcm extension
1. Number of symbolic links

These flags will augment the output with more items.
 * -D Adds demographic fields (Patient Name and Patient ID)
 * -M Adds Modality and SOP Class information