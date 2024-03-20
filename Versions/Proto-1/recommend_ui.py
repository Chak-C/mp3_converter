import tkinter as tk
from tkinter import ttk
import pandas as pd

import spotify_analysis as sa
import feature_graph_ui as fgu
import api_functions as af
from converter_ui import load_recommended_url
import config as c

recommendation_window = ''
canvas = ''
scrollable_frame = ''

def start_recommendation_ui(track_title, artist):
    global recommendation_window
  
    # Create a new window
    recommendation_window = tk.Toplevel()
    recommendation_window.title("Recommendations")
    recommendation_window.protocol("WM_DELETE_WINDOW", destroy)

    if track_title:
        # Connect to spotify API 
        sa.activate_spotify()
        # Get track_id and get artist
        track_id = sa.get_trackID(track_title, artist)

        if not track_id: 
            no_track_provided_screen()
        else:
            artist_name = c.CURRENT_TRACK_ARTIST if c.CURRENT_TRACK_ARTIST else 'No Artist Found'
            intro_label = tk.Label(recommendation_window, text=f"Recommendations for:")
            title_label = tk.Label(recommendation_window, text=f"Title: {track_title}", justify=tk.LEFT)
            artist_label = tk.Label(recommendation_window, text=f"Artist: {artist_name}", justify=tk.LEFT)

            button = tk.Button(recommendation_window, text="Refresh")

            intro_label.pack()
            title_label.pack()
            artist_label.pack()
            button.pack()
            # Create recommendation list
            create_recommendation(track_id, 'pearson', 0.8, 10)
    else:
        no_track_provided_screen()

    return None

def create_recommendation(track_id, method, threshold, show_limit):
    rec_list, rec_feats = sa.recommend_from_track(track_id, 20, method, threshold, show_limit)
    create_rec_frame(rec_list, rec_feats)
    return None

def create_rec_frame(rec_list, rec_feats):
    global recommendation_window, canvas, scrollable_frame

    canvas = tk.Canvas(recommendation_window)
    scrollbar = ttk.Scrollbar(recommendation_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    rec_list = rec_list.sort_values(by='similarity', ascending=False)
    for index in range(1,len(rec_list)-1):
        df = rec_list.iloc[index]
        feat_df = pd.DataFrame(rec_feats.iloc[index]).transpose()
        create_track_frame(df['name'],df['artists'][0]['name'],df['duration_ms'],df['similarity'],feat_df)
        
    return None

def create_track_frame(title, artist, miliseconds, similarity, features):
    global scrollable_frame

    miliseconds = sa.parse_miliseconds(miliseconds)

    frame = ttk.Frame(scrollable_frame, relief="groove", borderwidth=2, padding=(10, 5))
    frame.pack(fill="x", padx=10, pady=5)

    # Song name
    song_name_label = ttk.Label(frame, text=title, width=40)
    song_name_label.grid(row=0, column=0, padx=(10, 0))

    # Analytics button
    analytics_button = ttk.Button(frame, 
                                  text="Analytics", 
                                  command=lambda f = features, s = similarity: fgu.create_graph(f, s))
    analytics_button.grid(row=0, column=3, sticky="e")

    # Artist
    artist_label = ttk.Label(frame, text=f"Artist: {artist}", width=40)
    artist_label.grid(row=1, column=0, padx=(10, 0))

    # Duration
    duration_label = ttk.Label(frame, text=f"Duration: {miliseconds}", width=40)
    duration_label.grid(row=2, column=0, padx=(10, 0))

    # Load button
    load_button = ttk.Button(frame, text="Load", command=load_recommendation(title, artist))
    load_button.grid(row=2, column=3, sticky="e")

    return None


def load_recommendation(title, artist):
    url = af.search_youtube(title, artist)
    load_recommended_url(url)
    return None

def no_track_provided_screen():
    sim_label = tk.Label(recommendation_window, text="No track found. Please try again.")
    close_button = tk.Button(recommendation_window, text='Close', command=destroy)
    sim_label.pack()
    close_button.pack()
    return None


def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def destroy():
    """
    Destroy recommendation window and graph_window if exists
    """
    global recommendation_window, canvas, scrollable_frame

    fgu.destroy()
    if recommendation_window: 
        recommendation_window.destroy()
        canvas = ''
        scrollable_frame = ''
        print('Recommendation destroyed')
    pass