#!/bin/bash

# Define the script path and other variables
SCRIPT_PATH="/home.zfs/wustl/nrg-svc-research/helper_scripts/python/src/mrf_relay/index.py"
START_DATE="20240920"
END_DATE="20241003"
OUTPUT_CSV="/tmp/relay.csv"

# Run the Python script with the specified parameters
python3 "$SCRIPT_PATH" -s "$START_DATE" -e "$END_DATE" -c "$OUTPUT_CSV"

