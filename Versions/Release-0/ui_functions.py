import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from PIL import Image, ImageTk
import io

import api_functions as af
import config as c

# Function to toggle default download folder option
def toggle_default_folder(default_folder_var):
    
    if default_folder_var.get() == 1:
        c.DEFAULT_DOWNLOAD_FOLDER = filedialog.askdirectory()
    else:
        c.DEFAULT_DOWNLOAD_FOLDER = ''

def handle_scan(url_entry, widget, properties):
    """
    Function to handle scan button click.
    Params: url, widget [title widget, duration widget, image widget, button widget, checkbox], properties (dictionary)
    """
    video_url = url_entry.get()

    if af.is_youtube_link(video_url):
        info = af.fetch_video_info(video_url)
        if info:
            handle_text_change(widget['title_label'], f"{info['title']}")
            widget['duration_label'].config(text=f"Duration: {info['duration']}")
            display_thumbnail(info['thumbnail'], widget['image_label'])
            
             # Adjust command of download button
            widget['download_button'].config(command=lambda: af.full_download_process(video_url, widget['advanced_properties_var'].get(), properties))
    elif af.is_bili_link(video_url):
        handle_text_change(widget['title_label'], "No information for bilibili links")
        widget['download_button'].config(command=lambda: af.full_download_process(video_url, widget['advanced_properties_var'].get(), properties))
    else:
        messagebox.showwarning("Warning", "Please enter a URL")

def display_thumbnail(url, image_label):
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

def toggle_advanced_properties(widget, properties):
    """
    Function for setting up advanced properties.
    Param: widgets (advanced_properties_var, additional_properties_frame), 
            properties (dictionary) 
    """
    if widget['advanced_properties_var'].get():
        properties_refresh(properties)

        widget['additional_properties_frame'].pack(side="top", fill="both", expand=True)
        widget['recommend_frame'].pack()
    else:
        widget['additional_properties_frame'].pack_forget()
        widget['recommend_frame'].pack_forget()

def properties_refresh(properties):
    for prop_name, prop_var in properties.items():
        if prop_name == 'Title':
            prop_var.set(c.CURRENT_TRACK_TITLE[:42])
        elif prop_name == 'Contributing Artists' or prop_name == 'Album Artist':
            prop_var.set(c.CURRENT_TRACK_CHANNEL[:42])
        elif prop_name == 'Year':
            prop_var.set(c.CURRENT_TRACK_YEAR)
        elif prop_name == 'Genre' or prop_name == 'Bit Rate':
            pass
        else:
            prop_var.set("")
        

def handle_text_change(widget, text):
    """
    Handles change of text for text widgets
    Param: widget (one), text (string)
    """
    widget.config(state=tk.NORMAL)
    widget.config(width=len(text)+1)
    widget.delete('1.0', tk.END)
    widget.insert(tk.END, text)
    widget.config(state=tk.DISABLED)