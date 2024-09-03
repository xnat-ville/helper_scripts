#!/bin/sh

export PYTHONPATH=/opt/Customer-Support/CNDA/xnat-ville/helper_scripts/python/src

python3 -m prearchive.index /opt/runtimes/XNAT-runtimes/test-contrast/data/xnat/prearchive
