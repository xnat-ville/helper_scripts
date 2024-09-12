#!/bin/sh

export PYTHONPATH=/data/CNDA/home/helper_scripts/python/src

python3 -m prearchive.index -M -D -c /tmp/prearchive.csv /data/CNDA/prearchive

