import csv

# Define the input and output file paths
input_file = '/tmp/prearchive.csv'
output_file = '/tmp/carrots.csv'

# Open the input CSV file for reading
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Open the output CSV file for writing
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()  # Write the headers

        # Filter rows where Patient Name or Patient ID contain '^'
        for row in reader:
            if '^' in row.get('Patient Name', '') or '^' in row.get('Patient ID', ''):
                writer.writerow(row)  # Write the matching row

print(f"Filtered data with '^' in Patient Name or Patient ID written to {output_file}")
