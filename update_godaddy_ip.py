import os
import requests

# Retrieve environment variables
godaddy_api_key = os.getenv('GODADDY_API_KEY')
godaddy_api_secret = os.getenv('GODADDY_API_SECRET')
domain = os.getenv('DOMAIN')
record_name = os.getenv('RECORD_NAME')
pushover_user_key = os.getenv('PUSHOVER_USER_KEY')
pushover_api_token = os.getenv('PUSHOVER_API_TOKEN')
ip_state_file = '/app/current_ip.txt'  # Path to store the last known IP address

# Check for required environment variables
required_vars = [godaddy_api_key, godaddy_api_secret, domain, record_name, pushover_user_key, pushover_api_token]
if None in required_vars:
    raise ValueError("Ensure all required environment variables are set.")

# Retrieve the current public IP address
def get_public_ip():
    return requests.get('https://api.ipify.org?format=json').json()['ip']

# Send a notification via Pushover
def send_pushover_notification(message):
    requests.post(
        'https://api.pushover.net/1/messages.json',
        data={'token': pushover_api_token, 'user': pushover_user_key, 'message': message}
    )

# Update the GoDaddy DNS record
def update_godaddy_dns(ip_address):
    headers = {
        'Authorization': f'sso-key {godaddy_api_key}:{godaddy_api_secret}',
        'Content-Type': 'application/json'
    }
    payload = [{'data': ip_address, 'ttl': 600}]
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/A/{record_name}'
    requests.put(url, headers=headers, json=payload).raise_for_status()

    print(f'Successfully updated {record_name}.{domain} to {ip_address}')
    send_pushover_notification(f'{record_name}.{domain} updated to {ip_address}')

# Read the last known IP address from a file
def read_last_ip():
    try:
        with open(ip_state_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Write the current IP address to a file
def write_current_ip(ip_address):
    with open(ip_state_file, 'w') as f:
        f.write(ip_address)

if __name__ == '__main__':
    public_ip = get_public_ip()
    last_ip = read_last_ip()

    if public_ip != last_ip:
        update_godaddy_dns(public_ip)
        write_current_ip(public_ip)
    else:
        print(f'IP address has not changed: {public_ip}')

