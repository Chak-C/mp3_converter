import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import yt_dlp
from youtubesearchpython import VideosSearch
from mutagen.easyid3 import EasyID3

import config as c

# Initialize global variables
file_name, title, thumbnail_url, duration = '', '', '', ''


# Function to fetch video information
def fetch_video_info(video_url):
    global title, duration, thumbnail_url

    # Get video ID
    try:
        video_id = video_url.split("v=")[1]
    except IndexError:
        messagebox.showerror("Error", "Invalid URL")
        return

    params = {
        'part': 'snippet,contentDetails',
        'id': video_id,
        'key': c.API_KEY
    }

    response = requests.get(c.API_ENDPOINT, params=params)

    if response.status_code == 200:
        video_data = response.json()
        if 'items' in video_data and len(video_data['items']) > 0:
            title = video_data['items'][0]['snippet']['title']
            thumbnail_url = video_data['items'][0]['snippet']['thumbnails']['default']['url']
            unparsed_duration = video_data['items'][0]['contentDetails']['duration']
            duration = parse_duration(unparsed_duration, 'start')
            channel = video_data['items'][0]['snippet']['channelTitle']
            year = video_data['items'][0]['snippet']['publishedAt'][:4]

            c.CURRENT_TRACK_TITLE = title
            c.CURRENT_TRACK_CHANNEL = channel
            c.CURRENT_TRACK_YEAR = year
            
            return {'title': title, 'duration': duration, "thumbnail": thumbnail_url, 'channel': channel, 'year': year}
        else:
            messagebox.showerror("Error", "Video not found")
            return None
    else:
        messagebox.showerror("Error", f"Error fetching video. Status code: {response.status_code}")
        return None
    
    
# Function to download video
def download_video(video_url, properties_enabled, properties):
    """
    Downloads the video in mp3 format at 256 kbps (adjustable if enabled)
    Param: url, properties_enabled (boolean), properties dictionary
    """
    global file_name, s_bitrate, title

    title = properties["Title"].get() if properties_enabled else title

    # Set file name
    if c.DEFAULT_DOWNLOAD_FOLDER:
        file_name = c.DEFAULT_DOWNLOAD_FOLDER + '/' + title
    else:
        file_name = filedialog.asksaveasfilename(defaultextension=".mp3", initialfile=title, title="Save As")
    
    s_bitrate = properties["Bit Rate"].get() if properties_enabled else ''
    s_bitrate == '256' if s_bitrate == '' else s_bitrate

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_name,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': s_bitrate
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        return ydl.prepare_filename(info_dict)

def modify_advanced_properties(properties_enabled, properties):
    """
    If properties are enabled, change the metadata of the downloaded file.
    Params: properties_enabled (boolean), properties (dictionary)
    """
    if properties_enabled:
        try:
            audio = EasyID3(file_name+'.mp3')
            audio["title"]  = properties["Title"].get()
            audio["artist"] = properties["Contributing Artists"].get()
            audio["date"] = properties["Year"].get()
            audio["albumartist"] = properties["Album Artist"].get()
            audio["album"] = properties["Album"].get()
            audio["genre"] = properties["Genre"].get()
            audio.save()
            pass
        except Exception:
            pass
    else:
        pass

def full_download_process(video_url, properties_enabled, properties):
    download_video(video_url, properties_enabled, properties)
    modify_advanced_properties(properties_enabled, properties)
    pass

def search_youtube(title, artist):
    """
    Given title and artist, provides a url from youtube
    """
    query = f"{title} {artist}"
    search = VideosSearch(query,limit=1)
    result = search.result()
    if result['result']:
        video_url = result['result'][0]['link']
        return video_url
    else:
        return 'No video found'
    
def parse_duration(duration_str, default_type):
    """
    From this format, PT5M28S, to this format, 5 min 28 sec.
    (e.g. PT6M -> 6 min 0 sec, for more examples check test block)
    """
    if default_type == 'start':
        duration_str = duration_str[2:]
        default_type = 'sec'

    if 'H' in duration_str:
        hours, minutes = duration_str.split('H')
        return f"{hours} hr " + parse_duration(minutes, 'min')
    if 'M' in duration_str:
        minutes, seconds = duration_str.split('M')
        return f"{minutes} min " + parse_duration(seconds, 'sec')
    if 'S' in duration_str and default_type == 'min':
        return f"0 min {duration_str[:-1]} sec"
    if 'S' in duration_str and default_type == 'sec':
        return f"{duration_str[:-1]} sec"

    return f"0 {default_type}"