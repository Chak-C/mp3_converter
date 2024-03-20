import os
from mutagen.easyid3 import EasyID3

def reset_album_metadata(folder_path):
    # Iterate over all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                
                audio = EasyID3(file_path)
                
                audio['album'] = ['']
                
                audio.save()
                
                print(f"Reset album metadata for: {file_path}")

# Specify the folder containing the audio files
folder_path = "C:/Users/Alvis/Desktop/Music"

# Call the function to reset the album metadata
reset_album_metadata(folder_path)