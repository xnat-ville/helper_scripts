import csv
from datetime import datetime

# Define the input and output file paths
input_file = '/tmp/prearchive.csv'
output_file = '/tmp/reminders.csv'

# Initialize a dictionary to store project details
projects = {}

# Open the input CSV file for reading
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Process each row to extract project details
    for row in reader:
        project_name = row['Project Label']
        session_date = row['Last Modified Time']  # Adjust if needed to reflect the correct date column

        # Convert session date to Unix timestamp for comparison
        try:
            session_timestamp = datetime.strptime(session_date, '%Y-%m-%d %H:%M:%S').timestamp()
        except ValueError:
            continue  # Skip rows with invalid date format

        # Update project details in the dictionary
        if project_name not in projects:
            projects[project_name] = {
                'session_count': 0,
                'newest_session': session_timestamp,
                'oldest_session': session_timestamp
            }
        
        # Increment session count
        projects[project_name]['session_count'] += 1
        
        # Update newest and oldest session dates
        projects[project_name]['newest_session'] = max(
            projects[project_name]['newest_session'], session_timestamp)
        projects[project_name]['oldest_session'] = min(
            projects[project_name]['oldest_session'], session_timestamp)

# Prepare data for output
output_data = []
for project_name, details in projects.items():
    output_data.append({
        'Project Name': project_name,
        'Session Count': details['session_count'],
        'Newest Session Date': datetime.fromtimestamp(details['newest_session']).strftime('%Y-%m-%d %H:%M:%S'),
        'Oldest Session Date': datetime.fromtimestamp(details['oldest_session']).strftime('%Y-%m-%d %H:%M:%S')
    })

# Write the output CSV file
with open(output_file, 'w', newline='') as outfile:
    fieldnames = ['Project Name', 'Session Count', 'Newest Session Date', 'Oldest Session Date']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write headers and data rows
    writer.writeheader()
    writer.writerows(output_data)

print(f"Reminder data written to {output_file}")
