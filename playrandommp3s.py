import os
import random
import shutil
from playsound import playsound

# Directory containing MP3 files
MP3_FOLDER = 'day1'
destination_folder = 'burntfiles'

def get_mp3_files(folder_path):
    """Get a list of all MP3 files in the given folder."""
    return [f for f in os.listdir(folder_path) if f.lower().endswith('.mp3')]

def play_mp3_files(folder_path):
    """Play all MP3 files in the folder in a random order."""
    mp3_files = get_mp3_files(folder_path)
    if not mp3_files:
        print("No MP3 files found in the directory.")
        return

    random.shuffle(mp3_files)  # Shuffle the list to randomize the order
    
    # Create the destination folder if it does not exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        
    for mp3_file in mp3_files:
        #print(f"Playing: {mp3_files[1]}")
        mp3_path = os.path.join(folder_path, mp3_file)
        # move file to burnt folder once its burnt
        destination_file = os.path.join(destination_folder, mp3_file)
        print(f"Playing: {mp3_file}")
        # try:
            # playsound(mp3_path)
        # except Exception as e:
            # print(f"Failed to play {mp3_file}: {e}")
        
        if os.path.isfile(mp3_path):
            shutil.move(mp3_path, destination_file)
            print(f"Moved '{mp3_file}' to '{destination_folder}'")
        else:
            print(f"'{mp3_file}' is not a file, skipping.")
        
        

if __name__ == "__main__":
    play_mp3_files(MP3_FOLDER)
