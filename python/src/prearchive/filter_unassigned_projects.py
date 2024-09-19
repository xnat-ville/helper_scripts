import csv

# Define the input and output file paths
input_file = '/tmp/prearchive.csv'
output_file = '/tmp/unassigned_projects.csv'

# Open the input CSV file for reading
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Open the output CSV file for writing
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()  # Write the headers

        # Filter rows where the 'Project Label' is "Unassigned"
        for row in reader:
            if row.get('Project Label', '').lower() == 'unassigned':
                writer.writerow(row)  # Write the matching row

print(f"Filtered unassigned projects written to {output_file}")
