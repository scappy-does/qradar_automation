import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import argparse
import os

# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_offense_details(offense_id):
    api_key = os.getenv('QRADAR_API_KEY')
    url = f'<QRADAR URL>/api/siem/offenses/{offense_id}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'SEC': api_key
    }

    response = requests.get(url, headers=headers, verify=False, timeout=10)  # Timeout in seconds

    if response.status_code == 200:
        offense_details = response.json()
        print("Offense Details:")
        for key, value in offense_details.items():
            print(f"{key}: {value}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get details of a specific QRadar offense by ID.')
    parser.add_argument('offense_id', type=int, help='The ID of the offense to retrieve.')
    args = parser.parse_args()

    get_offense_details(args.offense_id)
