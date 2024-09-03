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

 ## prune.py
This script prunes prearchive folders that do not contain any DICOM files.
This will happen if some error occurs during the archive process.
The program uses the CSV or JSON file produced by index_prearchive as input.
It does not rescan the prearchive folder to look for candidate files.

### Invocation
```
export PYTHONPATH=.../helper_scripts/python
python3 -m prearchive.prune [flags] index-file
```
Flag values are:

| Flag               | Description                                            |
|--------------------|--------------------------------------------------------|
| -l, --log          | Path to output log information                         |
| -a, --age          | Minimum age in days for a folder to be deleted         |
| -d, --dryrun       | Perform a dry run, but do not delete any files/folders |
| -s, --silent       | Produce no log output                                  |
| -v, --verbose      | Enable verbose output                                  |

The program will assume the format of the index file (csv, json) by the file extension.
Both file types include the same information needed to prune the prearchive.
The index file is not updated during this operation.

If the --output flag is not specified, output will be sent to the stdout.
In the event the user specifies both --silent and --verbose, the --silent flag
will be observed.