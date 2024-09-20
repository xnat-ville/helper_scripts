import csv
import pydicom
from pathlib import Path

# Define the input and output file paths
input_file = '/tmp/unassigned_projects.csv'
output_file = '/tmp/reassign_info.csv'

# Open the input CSV file for reading
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    # Add new fields to the existing headers
    fieldnames = reader.fieldnames + ['Study Description', 'Study Comments', 'Institution Name', 'Institution Address', 'Station Name']

    # Open the output CSV file for writing
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the headers

        # Iterate over each row in the input CSV
        for row in reader:
            session_path = Path(row['Session Path'])
            dicom_folder = session_path / 'DICOM'

            # If "DICOM" folder doesn't exist, check for "secondary"
            if not dicom_folder.is_dir():
                dicom_folder = session_path / 'secondary'

            # Check if the DICOM or secondary folder exists
            if dicom_folder.is_dir():
                file_list = list(dicom_folder.glob('*.dcm'))
                if file_list:
                    first_file = file_list[0]

                    # Attempt to read the DICOM file and extract metadata
                    try:
                        dicom_data = pydicom.dcmread(first_file)

                        # Extract relevant DICOM tags
                        row['Study Description'] = dicom_data.get('StudyDescription', 'N/A')
                        row['Study Comments'] = dicom_data.get('StudyComments', 'N/A')
                        row['Institution Name'] = dicom_data.get('InstitutionName', 'N/A')
                        row['Institution Address'] = dicom_data.get('InstitutionAddress', 'N/A')
                        row['Station Name'] = dicom_data.get('StationName', 'N/A')
                    except Exception as e:
                        print(f"Error reading DICOM file {first_file}: {e}")

            # Write the updated row to the output file
            writer.writerow(row)

print(f"Filtered data with additional DICOM information written to {output_file}")
