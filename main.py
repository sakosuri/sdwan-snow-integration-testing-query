import requests
import json
from datetime import datetime, timedelta




# vManage connection details
VMANAGE_HOST = "<ip address of vManage>"  # Replace with your vManage IP or FQDN
USERNAME = "<username>"                  # Replace with your username
PASSWORD = "<password>"                  # Replace with your password

# Disable warnings for self-signed certificates (optional)
requests.packages.urllib3.disable_warnings()

def get_jwt_token(session, host, username, password):
    """Authenticate and retrieve JWT token."""
    url = f"{host}/j_security_check"
    payload = {'j_username': username, 'j_password': password}
    response = session.post(url, data=payload, verify=False)
    if response.status_code != 200 or 'JSESSIONID' not in session.cookies:
        raise Exception("Login failed. Check credentials.")
    # For newer vManage versions, you may need to get a token as well
    token_url = f"{host}/dataservice/client/token"
    token_response = session.get(token_url, verify=False)
    if token_response.status_code == 200:
        return token_response.text
    return None

def get_control_connection_alarms(session, host, token=None):
    """Retrieve only control-connection-state-change alarms."""
    url = f"{host}/dataservice/alarms"
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['X-XSRF-TOKEN'] = token
    
    # Get current time in UTC
    current_time = datetime.utcnow()
    # # Subtract 10 minutes
    ten_mins_ago = current_time - timedelta(minutes=10)
    # Format to match your requirement: YYYY-MM-DDTHH:MM:SS UTC
    current_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S UTC")
    ten_mins_ago_str = ten_mins_ago.strftime("%Y-%m-%dT%H:%M:%S UTC")

    query = {
        "query": {
            "condition": "AND",
            "rules": [
                {
                    "value": ["OMP sessions with all vsmarts in the network is down"],
                    "field": "message",
                    "type": "string",
                    "operator": "equal"
                },
                {
                    "value": [
                        ten_mins_ago_str,
                        current_time_str
                    ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "between"
                },
                {
                    "value": ["Critical"],
                    "field": "sever",
                    "type": "string",
                    "operator": "equal"
                }
                
            ]
        }
    }

    response = session.post(url, headers=headers, data=json.dumps(query), verify=False)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Failed to retrieve alarms: {response.status_code} {response.text}")
        return []

def main():
    with requests.Session() as session:
        token = get_jwt_token(session, VMANAGE_HOST, USERNAME, PASSWORD)
        alarms = get_control_connection_alarms(session, VMANAGE_HOST, token)
        print(json.dumps(alarms, indent=2))

if __name__ == "__main__":
    main()
