# config.py

# Initialize general global variables
DEFAULT_DOWNLOAD_FOLDER = '' # default download folder path
CURRENT_TRACK_TITLE = ''
CURRENT_TRACK_CHANNEL = ''
CURRENT_TRACK_ARTIST = '' # configurated in get_trackID (spotify_analysis.py)
CURRENT_TRACK_YEAR = ''

# Youtube
API_ENDPOINT = 'https://www.googleapis.com/youtube/v3/videos' # Use URL to get video information (length, size, thumbnail, title)
API_KEY = '' # Enter key

# Spotify
CLIENT_ID = '' # enter id
CLIENT_SECRET = '' # enter secret

SPOTIFY_API_ENDPOINT = 'https://accounts.spotify.com/api/token'
SPOTIFY_TOKEN = '' # Valids for 30-60 mins every run
CURRENT_TRACK_FEATURES = ''

# Functions
def refresh_spotify_token():
    global SPOTIFY_TOKEN
    import base64
    import requests
    """
    Using client id and secret in config file, generates and sets access token string in config.py
    Access token is valid for 1 hour every generation.
    """
    client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    
    # Encode with base64
    encoded_credentials = base64.b64encode(client_credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }
    payload = {
        'grant_type': 'client_credentials',
    }

    # Post request for access token
    response = requests.post(SPOTIFY_API_ENDPOINT, headers=headers, data=payload)

    if response.status_code == 200:
        SPOTIFY_TOKEN = response.json()['access_token']
        print(f"Spotify Access Token created.")
    else:
        print(f"Failed to obtain access token. Status code: {response.status_code}")
