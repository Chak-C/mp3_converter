import tkinter as tk
import pygame
from tkinter import ttk
import requests

# testing
audio_url = 'https://p.scdn.co/mp3-preview/3bd133cbf1fb988c0235d0a383fffcf05f5756e8?cid=49b8247f173447b3a2bf1bda588153c4.mp3'

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        
        # Initialize pygame
        pygame.init()
        
        # Initialize variables
        self.playing = False
        self.song_length = 0
        
        # Create widgets
        self.play_button = tk.Button(root, text="Play", command=self.toggle_play)
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=200)
        self.duration_label = tk.Label(root, text="00:00 / 00:00")
        self.volume_label = tk.Label(root, text="Volume")
        self.volume_scale = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=self.update_volume)
        
        # Grid layout
        self.play_button.grid(row=0, column=0, padx=10, pady=10)
        self.progress_bar.grid(row=0, column=1, padx=10, pady=10)
        self.duration_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.volume_label.grid(row=2, column=0, padx=10, pady=10)
        self.volume_scale.grid(row=2, column=1, padx=10, pady=10)
        
        # Load music file
        audio_url = 'https://p.scdn.co/mp3-preview/3bd133cbf1fb988c0235d0a383fffcf05f5756e8?cid=49b8247f173447b3a2bf1bda588153c4.mp3'

        response = requests.get(audio_url)
        with open('audio.mp3', 'wb') as f:
            f.write(response.content)

        pygame.mixer.music.load('audio.mp3')
        pygame.mixer.music.play()
        self.song_length = pygame.mixer.Sound('audio.mp3').get_length()
        
        # Update progress bar
        self.update_progress_bar()
        
    def toggle_play(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.play_button.config(text="Play")
        else:
            pygame.mixer.music.unpause()
            self.play_button.config(text="Pause")
        self.playing = not self.playing
    
    def update_progress_bar(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        current_time_formatted = self.format_time(current_time)
        total_time_formatted = self.format_time(self.song_length)
        self.duration_label.config(text=f"{current_time_formatted} / {total_time_formatted}")
        
        progress = (current_time / self.song_length) * 100
        self.progress_bar["value"] = progress
        
        self.root.after(1000, self.update_progress_bar)
    
    def update_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)
        
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
