
import pygame
import requests
import tkinter as tk
import os
from tkinter import ttk, messagebox

import spotify_analysis as sa

class SpotifyPlayback():
    def __init__(self):
        self.play_window = tk.Toplevel()
        self.play_window.title('Sample playback')
        self.play_window.protocol('WM_DELETE_WINDOW', self.destroy)

        self.pgame = pygame.init()

        self.playing = False
        self.found_track = False
        self.song_length = 0
        self.audio_url = ''

        self.play_button = tk.Button(self.play_window, text = 'Play', command = self.toggle_play)
    
    def start_playbackUI(self, audio_url, start_play):
        """
        If you want to start window with music playing, start_play true, else false
        """
        self.audio_url = audio_url
        self.playing = not start_play # inverse start_play to toggle later
        # Remove audio file if exists
        if os.path.exists('audio.mp3'):
            os.remove('audio.mp3')
        
        # Initiate mixer if disabled / quitted
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.progress_bar = ttk.Progressbar(self.play_window, orient="horizontal", mode = 'determinate', length = 200)
        self.duration_label = tk.Label(self.play_window, text = "00:00/00:00")
        self.volume_label = tk.Label(self.play_window, text = "Volume")
        self.volume_scale = ttk.Scale(self.play_window, from_=0, to=100, orient= 'horizontal', command=self.update_volume)
        
        # grid layout
        self.play_button.grid(row=0, column=0, padx=10, pady=10)
        self.progress_bar.grid(row=0, column=1, padx=10, pady=10)
        self.duration_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.volume_label.grid(row=2, column=0, padx=10, pady=10)
        self.volume_scale.grid(row=2, column=1, padx=10, pady=10)

        self.play_track()
        if self.found_track:
            self.update_progress_bar()
        else:
            self.duration_label.config(text='Track not found. Please try a different track.')

        pass
    
    def play_track(self):
        """
        Make request to audio url and plays the track with pygame.
        Return: False if unsucessful, true otherwise
        """
        # request track url
        try:
            response = requests.get(self.audio_url)
        except:
            messagebox.showwarning("Sorry, ", "this track does not have a preview URL")
        if response.status_code == 200:
            self.found_track = True
            with open('audio.mp3', 'wb') as f:
                f.write(response.content)
        else:
            print("Track url not found")
            return
        
        self.song_length = pygame.mixer.Sound('audio.mp3').get_length()
        pygame.mixer.music.load('audio.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.3)
        
        self.toggle_play()
        return
    
    def toggle_play(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.play_button.config(text='Play')
        else:
            pygame.mixer.music.unpause()
            self.play_button.config(text="Pause")
        self.playing = not self.playing
        pass

    def update_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)
        pass
    
    def update_progress_bar(self):
        current_ms = pygame.mixer.music.get_pos()
        current_time = sa.parse_miliseconds(current_ms)
        track_duration = sa.parse_miliseconds(self.song_length * 1000)
        self.duration_label.config(text=f"{current_time} / {track_duration}")

        progress = ((current_ms / 1000) / self.song_length) * 100
        self.progress_bar['value'] = progress

        if progress >= 90:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            self.start_playbackUI(self.audio_url, False)
            return
        
        self.play_window.after(500, self.update_progress_bar)
        pass

    def destroy(self):
        self.play_window.destroy()
        pygame.quit()
        # Remove audio file if exists
        if os.path.exists('audio.mp3'):
            os.remove('audio.mp3')
            
        print("Playback destroyed")
        