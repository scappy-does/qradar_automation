# qradar_automation
This Project contains useful scripts for automating Offense reporting in QRadar.  The QRadar web interface can be fairly unintuitive, so I have attempted to simplify the process using the API and Python.

# Setup
1. Log into the QRadar console as an administrator.
2. Navigate to Admin > Authorized Services.
3. Click on +Add and create an API key.
4. Save it in a password vault as you will not be able to view it in the console after closing the browser window.

# qradar_24h_offense_report.py
This script connects to the Qradar API using the previously generated API key, and outputs all Offenses in the last 24 hours.
These offenses are broken down by Open or Closed.  For Open Offenses, these are further broken down by assigned_user.  If the Offense is unassigned, that means that the Offense still needs to be worked on, if the open Offense has been assigned, that means that the offense is in progress. 

