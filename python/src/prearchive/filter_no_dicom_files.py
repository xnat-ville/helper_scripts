import csv

# Define the input and output file paths
input_file = '/tmp/prearchive.csv'
output_file = '/tmp/no_dicom_files.csv'

# Open the input CSV file for reading
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    
    # Write the headers to the output file
    writer.writeheader()
    
    # Process each row line by line
    for row in reader:
        # Check if 'DCM Files' is 0 and write to the output file if true
        if row['DCM Files'] == '0':
            writer.writerow(row)

print(f"Filtered data written to {output_file}")
