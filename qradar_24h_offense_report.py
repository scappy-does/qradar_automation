from datetime import datetime, timedelta
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from collections import defaultdict
import csv
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api_key = os.getenv('QRADAR_API_KEY')
url = '<QRADAR URL>/api/siem/offenses'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'SEC': api_key
}
# Calculate the timestamp for 24 hours ago
twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
timestamp_24_hours_ago = int(twenty_four_hours_ago.timestamp() * 1000)  # Convert to milliseconds

params = {
    'filter': f'start_time>{timestamp_24_hours_ago}',  # Filter offenses from the last 24 hours
    'sort': '-start_time',  # Sort by start_time in descending order
    'fields': 'id,start_time,description,status,closing_user,assigned_to'  # Include the assigned_to field
}

response = requests.get(url, headers=headers, params=params, verify=False, timeout=10)  # Timeout in seconds

if response.status_code == 200:
    offenses = response.json()
    if offenses:
        description_counts = defaultdict(lambda: {'open_unassigned': 0, 'open_assigned': 0, 'closed': 0, 'total': 0})
        
        for offense in offenses:
            #print(f"ID: {offense['id']}")
            #print(f"Start Time: {offense['start_time']}")
            #print(f"Description: {offense['description']}")
            #print(f"Status: {offense['status']}")
            if offense['status'] == 'CLOSED':
                #print(f"Closed By: {offense.get('closing_user', 'Unknown')}")
                description_counts[offense['description']]['closed'] += 1
            else:
                if offense.get('assigned_to'):
                    description_counts[offense['description']]['open_assigned'] += 1
                else:
                    description_counts[offense['description']]['open_unassigned'] += 1
                    
            description_counts[offense['description']]['total'] += 1
            #print("-----")
        
        # Save the final table as a CSV file
        with open('offense_counts.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Description', 'Open Unassigned Count', 'Open Assigned Count', 'Closed Count', 'Total Count'])
            for description, counts in description_counts.items():
                writer.writerow([description.strip(), counts['open_unassigned'], counts['open_assigned'], counts['closed'], counts['total']])
        
        print("\nThe final table has been saved as offense_counts.csv.")
    else:
        print("No offenses found in the last 24 hours.")
else:
    print(f"Error: {response.status_code} - {response.text}")
