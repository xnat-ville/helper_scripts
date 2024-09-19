import csv

# Define the input and output file paths
input_file = '/tmp/prearchive.csv'
output_file = '/tmp/no_dicom_files.csv'

# Open the input CSV file for reading
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    
    # Filter rows where 'DCM Files' is 0
    filtered_rows = [row for row in reader if row['DCM Files'] == '0']
    
    # Write the filtered rows to the output CSV file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        
        # Write the headers and the filtered rows
        writer.writeheader()
        writer.writerows(filtered_rows)

print(f"Filtered data written to {output_file}")
