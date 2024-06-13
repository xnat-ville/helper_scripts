#!/bin/bash

# This script finds the location of the DCM4CHE version of the storescu command

find_storescu() {
storescu_path="$DCM4CHE_BASE/bin/storescu"
echo "$storescu_path"
}

export DCM4CHE_STORESCU=$(find_storescu)
