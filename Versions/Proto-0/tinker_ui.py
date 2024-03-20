import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
import yt_dlp

from PIL import Image, ImageTk
import io

from mutagen.easyid3 import EasyID3

# Initialize global variables
api_key = 'AIzaSyAQcQcyi2CHRo2ly8wWfoZmuecTvp3fLzw'
file_name, title, thumbnail_url, duration = '', '', '', ''
default_download_folder = ''  # Default download folder path

# Function to fetch video information
def fetch_video_info(video_url):
    global title, duration, thumbnail_url

    # Use URL to get video information (length, size, thumbnail, title)
    api_endpoint = 'https://www.googleapis.com/youtube/v3/videos'

    # Get video ID
    try:
        video_id = video_url.split("v=")[1]
    except IndexError:
        messagebox.showerror("Error", "Invalid URL")
        return

    params = {
        'part': 'snippet,contentDetails',
        'id': video_id,
        'key': api_key
    }

    response = requests.get(api_endpoint, params=params)

    if response.status_code == 200:
        video_data = response.json()

        if 'items' in video_data and len(video_data['items']) > 0:
            title = video_data['items'][0]['snippet']['title']
            thumbnail_url = video_data['items'][0]['snippet']['thumbnails']['default']['url'] # not used yet
            unparsed_duration = video_data['items'][0]['contentDetails']['duration']
            duration = parse_duration(unparsed_duration, 'start')

            return {'title': title, 'duration': duration, "thumbnail": thumbnail_url}
        else:
            messagebox.showerror("Error", "Video not found")
            return None
    else:
        messagebox.showerror("Error", f"Error fetching video. Status code: {response.status_code}")
        return None

# Function to download video
def download_video(video_url):
    global file_name, s_bitrate, title

    title = properties["Title"].get() if advanced_properties_var.get() else title

    # Set file name
    if default_download_folder:
        print(default_download_folder)
        file_name = default_download_folder + '/' + title
        print(file_name)
    else:
        file_name = filedialog.asksaveasfilename(defaultextension=".mp3", initialfile=title, title="Save As")
    
    s_bitrate = properties["Bit Rate"].get() if advanced_properties_var.get() else ''
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

# Function to parse duration
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

# Function to handle button click event
def handle_download():
    video_url = url_entry.get()

    if video_url:
        info = fetch_video_info(video_url)
        if info:
            title_label.config(text=f"Title: {info['title']}")
            duration_label.config(text=f"Duration: {info['duration']}")
            display_thumbnail(thumbnail_url)
            
             # Adjust command of download button
            download_button.config(command=lambda: full_download_process(video_url))
    else:
        messagebox.showwarning("Warning", "Please enter a URL")

def display_thumbnail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            picture = ImageTk.PhotoImage(image)
            image_label.image = picture
            image_label.config(image = picture)
            
            print('Thumbnail found')
        else:
            print("Failed to fetch image:", response.status_code)
    except Exception as e:
        print("Error fetching image:", e)

# Function to toggle default download folder option
def toggle_default_folder():
    global default_download_folder
    if default_folder_var.get() == 1:
        default_download_folder = filedialog.askdirectory()
    else:
        default_download_folder = ''

def toggle_advanced_properties():
    if advanced_properties_var.get():
        additional_properties_frame.pack(side="top", fill="both", expand=True)
    else:
        additional_properties_frame.pack_forget()

def modify_advanced_properties():
    if advanced_properties_var.get():
        audio = EasyID3(file_name+'.mp3')
        audio["title"]  = properties["Title"].get()
        audio["artist"] = properties["Contributing Artists"].get()
        audio["date"] = properties["Year"].get()
        audio["albumartist"] = properties["Album Artist"].get()
        audio["album"] = properties["Album"].get()
        audio["genre"] = properties["Genre"].get()
        audio.save()
        pass
    else:
        pass

def full_download_process(video_url):
    download_video(video_url)
    modify_advanced_properties()
    pass
# Create GUI
root = tk.Tk()
root.title("YouTube Converter")

# URL Entry
url_label = tk.Label(root, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Default folder option
default_folder_var = tk.IntVar(value=0)
default_folder_checkbox = tk.Checkbutton(root, text="Use default download folder", variable=default_folder_var, command=toggle_default_folder)
default_folder_checkbox.pack()

# Download Button
download_button = tk.Button(root, text="URL Search", command=handle_download)
download_button.pack()

# Information Labels
title_label = tk.Label(root, text="")
title_label.pack()
duration_label = tk.Label(root, text="")
duration_label.pack()
image_label = tk.Label(root)
image_label.pack()

# Advanced Properties Checkbutton
advanced_properties_var = tk.BooleanVar(value=False)
advanced_properties_checkbox = tk.Checkbutton(root, text="Show Advanced Properties", variable=advanced_properties_var, command=toggle_advanced_properties)
advanced_properties_checkbox.pack()

download_button = tk.Button(root, text="Download", command=lambda: '')
download_button.pack()

# Dropdown menu for additional properties
additional_properties_frame = tk.Frame(root)
properties = {
    "Title": tk.StringVar(),
    "Subtitle": tk.StringVar(),
    "Contributing Artists": tk.StringVar(),
    "Album Artist": tk.StringVar(),
    "Album": tk.StringVar(),
    "Year": tk.StringVar(),
    "Genre": tk.StringVar(),
    "Bit Rate": tk.StringVar()
}

for prop_name, prop_var in properties.items():
    property_frame = tk.Frame(additional_properties_frame)
    property_frame.pack(side="top", fill="x", padx=5, pady=5)
    
    label = tk.Label(property_frame, text=prop_name)
    label.pack(side="left", padx=5, pady=5)
    
    dropdown = ttk.Entry(property_frame, textvariable=prop_var, width = 40)
    dropdown.pack(side="right", padx=5, pady=5, anchor="center")

root.mainloop()