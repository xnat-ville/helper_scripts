import csv
import pydicom
from pathlib import Path

# Define the input and output file paths
input_file = '/tmp/unassigned_projects.csv'
output_file = '/tmp/reassign_info.csv'

# Open the input CSV file for reading
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Add new DICOM-related headers to the existing ones
    fieldnames = reader.fieldnames + [
        'Study Description', 'Study Comments', 'Institution Name',
        'Institution Address', 'Station Name'
    ]

    # Open the output CSV file for writing
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the headers

        # Iterate over each row in the input CSV
        for row in reader:
            session_path = Path(row['Session Path'])

            # Navigate into SCANS folder
            scans_folder = session_path / 'SCANS'
            if scans_folder.is_dir():
                # Iterate through each Scan Series folder inside SCANS
                for scan_series_folder in scans_folder.iterdir():
                    if scan_series_folder.is_dir():
                        # Look for the DICOM or secondary folder
                        dicom_folder = scan_series_folder / 'DICOM'
                        if not dicom_folder.is_dir():
                            dicom_folder = scan_series_folder / 'secondary'

                        # If we found a valid DICOM or secondary folder, look for DICOM files
                        if dicom_folder.is_dir():
                            dicom_files = list(dicom_folder.glob('*.dcm'))
                            if dicom_files:
                                # Read the first DICOM file
                                try:
                                    dicom_data = pydicom.dcmread(dicom_files[0])

                                    # Extract required DICOM tags and update row with values
                                    row['Study Description'] = dicom_data.get('StudyDescription', '')
                                    row['Study Comments'] = dicom_data.get('StudyComments', '')
                                    row['Institution Name'] = dicom_data.get('InstitutionName', '')
                                    row['Institution Address'] = dicom_data.get('InstitutionAddress', '')
                                    row['Station Name'] = dicom_data.get('StationName', '')

                                except Exception as e:
                                    print(f"Error reading DICOM file {dicom_files[0]}: {e}")

                            break  # Stop after finding and reading the first DICOM file

            # Write the updated row to the new CSV
            writer.writerow(row)

print(f"Data with additional DICOM information written to {output_file}")

