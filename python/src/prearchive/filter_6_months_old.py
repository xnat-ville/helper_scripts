import csv
from datetime import datetime, timedelta

# Define the input and output file paths
input_file = '/tmp/prearchive.csv'
output_file = '/tmp/old_sessions.csv'

# Calculate the date 6 months ago from today
six_months_ago = datetime.now() - timedelta(days=6*30)  # Approximate 6 months

# Open the input CSV file for reading
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Open the output CSV file for writing
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()  # Write the headers

        # Filter rows where Last Modified Time is older than 6 months
        for row in reader:
            last_modified = datetime.strptime(row['Last Modified Time'], '%Y-%m-%d %H:%M:%S')
            if last_modified < six_months_ago:
                writer.writerow(row)  # Write the matching row

print(f"Filtered data of sessions older than 6 months written to {output_file}")
