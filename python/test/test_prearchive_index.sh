#!/bin/sh

export PYTHONPATH=/data/CNDA/home/helper_scripts/python/src

# Run the Python script, using the provided top-level folders if given
python3 -m prearchive.index -M -D -c /tmp/prearchive.csv -l /tmp/log_of_prearchive.txt -t /tmp/project_list.txt /data/CNDA/prearchive
