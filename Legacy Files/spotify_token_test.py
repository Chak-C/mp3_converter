import base64
import requests

# Define client credentials
client_id = '49b8247f173447b3a2bf1bda588153c4'
client_secret = '43fd0edf8b0e495c81dc1b38cc237b77'

# Code for token
# Concatenate client ID and client secret separated by a colon
client_credentials = f"{client_id}:{client_secret}"

# Encode the client credentials using base64
encoded_credentials = base64.b64encode(client_credentials.encode()).decode()
print(encoded_credentials)
# Define headers and payload for the request
headers = {
    'Authorization': f'Basic {encoded_credentials}',
}
payload = {
    'grant_type': 'client_credentials',
}

# Make the POST request to obtain the access token
response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=payload)

# Parse the JSON response
if response.status_code == 200:
    access_token = response.json()['access_token']
    print(f"Access token: {access_token}")
else:
    print(f"Failed to obtain access token. Status code: {response.status_code}")
"""
# Authentication endpoint
auth_url = 'https://accounts.spotify.com/api/token'

# Authentication request parameters
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}

# Send authentication request
response = requests.post(auth_url, data=data)

# Parse response JSON
auth_response = response.json()

# Extract access token
access_token = 'BQAETGeuT4vFtkzhEu1Zp_mfYqCOcU6wkJ6qCs97x4VvmPx0zwizmhtj6zXKT--y7DEGxeKAXA1WvVmkMzFD5j1sH3ids0BWVSdzU4YEs8XIDM6llKM'

song_name = 'Something Just Like This'

# Make a request to search for the song
headers = {'Authorization': f'Bearer {access_token}'}
params = {'q': song_name, 'type': 'track'}
api_url = 'https://api.spotify.com/v1/search'
response = requests.get(api_url, headers=headers, params=params)

# Handle the response data
data = response.json()

# Extract relevant information from the response
# For example, print the name of the first track in the search results
first_track_name = data['tracks']['items'][0]['name']
print(data)
"""