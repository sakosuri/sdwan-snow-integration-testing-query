# sdwan-snow-integration-testing-query

vManage Alarm Retrieval Script
This Python script retrieves control-connection-state-change alarms from a Cisco vManage instance using the vManage REST API. It filters alarms based on message content, severity, and a time window (last 40 minutes by default).

Features
1. Authenticates to Cisco vManage using username and password
2. Retrieves alarms with:
Message: "OMP sessions with all vsmarts in the network is down"
Severity: "Critical"
Entry time: between the last 10 minutes and now
3. Prints the filtered alarms in JSON format
-----------------------------------------------------------------------------------------------------------------------------------------------

Prerequisites
Python 3.x, requests library
Edit the script:Replace the following placeholders at the top of the script with your vManage details

-----------------------------------------------------------------------------------------------------------------------------------------------

Output:
The script will print the retrieved alarms in formatted JSON.

-----------------------------------------------------------------------------------------------------------------------------------------------
Notes:
Adjust the time window or filter rules in the get_control_connection_alarms function as needed.
The script uses the vManage /dataservice/alarms POST endpoint with a custom query.

-----------------------------------------------------------------------------------------------------------------------------------------------
Troubleshooting:
If you receive authentication errors, verify your credentials and vManage URL.
If you receive no alarms, check your filter criteria and time window.
