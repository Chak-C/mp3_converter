import tkinter as tk
from tkinter import ttk
import pandas as pd

import spotify_analysis as sa
import api_functions as af
import config as c
from feature_graph_ui import FeatureGraphUI
from ui_mediator import Mediator
from typing import Type

class RecommendUI:
    def __init__(self, mediator: Type[Mediator]):
        self.url_mediator = mediator
        mediator.subscribe(self)

        self.recommendation_window = tk.Toplevel()
        self.recommendation_window.title("Recommendations")
        self.recommendation_window.protocol("WM_DELETE_WINDOW", self.destroy)

    def start_recommendation_ui(self, track_title, artist):
        if track_title:
            sa.activate_spotify()
            track_id = sa.get_trackID(track_title, artist)

            if not track_id:
                self.no_track_provided_screen()
            else:
                artist_name = c.CURRENT_TRACK_ARTIST if c.CURRENT_TRACK_ARTIST else 'No Artist Found'
                self.intro_label = tk.Label(self.recommendation_window, text=f"Recommendations for:")
                self.title_label = tk.Label(self.recommendation_window, text=f"Title: {track_title}", justify=tk.LEFT)
                self.artist_label = tk.Label(self.recommendation_window, text=f"Artist: {artist_name}", justify=tk.LEFT)

                self.refresh_button = tk.Button(self.recommendation_window, text="Refresh", command=lambda: self.refresh_recommendations(track_id, 'pearson', 0.8, 10))

                self.intro_label.pack()
                self.title_label.pack()
                self.artist_label.pack()
                self.refresh_button.pack()
                # Create recommendation list
                self.create_recommendation(track_id, 'pearson', 0.8, 10)
        else:
            self.no_track_provided_screen()

        return None
    
    def create_recommendation(self, track_id, method, threshold, show_limit):
        rec_list, rec_feats = sa.recommend_from_track(track_id, 20, method, threshold, show_limit)
        self.create_rec_frame(rec_list, rec_feats)
        return None
    
    def create_rec_frame(self, rec_list, rec_feats):
        self.canvas = tk.Canvas(self.recommendation_window)
        self.scrollbar = ttk.Scrollbar(self.recommendation_window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        rec_list = rec_list.sort_values(by='similarity', ascending=False)
        for index in range(1,len(rec_list)-1):
            df = rec_list.iloc[index]
            feat_df = pd.DataFrame(rec_feats.iloc[index]).transpose()
            self.create_track_frame(df['name'],df['artists'][0]['name'],df['duration_ms'],df['similarity'],feat_df)
        
        return None
    
    def create_track_frame(self, title, artist, miliseconds, similarity, features):
        miliseconds = sa.parse_miliseconds(miliseconds)

        self.frame = ttk.Frame(self.scrollable_frame, relief="groove", borderwidth=2, padding=(10, 5))
        self.frame.pack(fill="x", padx=10, pady=5)

        # Song name
        self.song_name_label = ttk.Label(self.frame, text=title, width=40)
        self.song_name_label.grid(row=0, column=0, padx=(10, 0))

        # Analytics button
        self.analytics_button = ttk.Button(self.frame, 
                                    text="Analytics", 
                                    command=lambda f = features, s = similarity: self.load_feature_graph(f, s))
        self.analytics_button.grid(row=0, column=3, sticky="e")

        # Artist
        self.artist_label = ttk.Label(self.frame, text=f"Artist: {artist}", width=40)
        self.artist_label.grid(row=1, column=0, padx=(10, 0))

        # Duration
        self.duration_label = ttk.Label(self.frame, text=f"Duration: {miliseconds}", width=40)
        self.duration_label.grid(row=2, column=0, padx=(10, 0))

        # Load button
        self.load_button = ttk.Button(self.frame, text="Load", command=lambda: self.load_recommendation(title, artist))
        self.load_button.grid(row=2, column=3, sticky="e")

        return None
    
    def load_feature_graph(self, features, similarity):
        self.graph_ui = FeatureGraphUI()
        self.graph_ui.create_graph(features, similarity)
        pass

    def load_recommendation(self, title, artist):
        url = af.search_youtube(title, artist)
        self.url_mediator.set_item(url)
        return None
    
    def no_track_provided_screen(self):
        self.sim_label = tk.Label(self.recommendation_window, text="No track found. Please try again.")
        self.close_button = tk.Button(self.recommendation_window, text='Close', command=self.destroy)
        self.sim_label.pack()
        self.close_button.pack()
        return None

    def refresh_recommendations(self, track_id, method, threshold, show_limit):
        print('Refreshing recommendations...')
        self.canvas.destroy()
        self.scrollbar.destroy()
        self.scrollable_frame.destroy()
        self.create_recommendation(track_id, method, threshold, show_limit)
        print('Recommendations refreshed.')
        pass

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update(self, item):
        pass

    def destroy(self):
        """
        Destroy recommendation window and graph_window if exists
        """
        self.graph_ui.destroy()
        if self.recommendation_window: 
            self.recommendation_window.destroy()
            self.canvas = ''
            self.scrollable_frame = ''
            print('Recommendation destroyed')
        pass