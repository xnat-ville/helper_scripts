#!/bin/sh

export PYTHONPATH=/data/CNDA/home/helper_scripts/python/src

# Check if the first argument (-t) for Top Level Folders is provided
if [ -z "$1" ]; then
    # Prompt user with a yes/no question
    echo "Warning: No top-level folder names provided. If you continue, the script will scan the entire prearchive."
    read -p "Do you want to continue? (yes/no): " answer

    case "$answer" in 
        [Yy]* ) 
            echo "Continuing to scan the entire prearchive..."
            ;;
        [Nn]* ) 
            echo "Exiting script."
            exit 1
            ;;
        * ) 
            echo "Invalid input. Exiting script."
            exit 1
            ;;
    esac
fi

# Run the Python script, using the provided top-level folders if given
python3 -m prearchive.index -M -D -c /tmp/prearchive.csv -l /tmp/log_of_prearchive.txt -t "$1" /data/CNDA/prearchive

