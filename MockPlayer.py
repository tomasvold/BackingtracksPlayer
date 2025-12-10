# MockPlayer.py
import os

_playback_state = "stopped"
_current_track = None

def _is_audio_file(filename):
    """Helper function to check if a file has a supported audio extension."""
    return filename.lower().endswith(('.mp3', '.wav'))

def get_all_files(music_folder):
    """Returns a list of all supported audio files in the music folder."""
    files = [f for f in os.listdir(music_folder) if os.path.isfile(os.path.join(music_folder, f))]
    return [f for f in files if _is_audio_file(f)]

def get_playlist_order(music_folder):
    """Loads the playlist order from a file, or creates one if it doesn't exist."""
    playlist_file = os.path.join(music_folder, "playlist.txt")
    
    if os.path.exists(playlist_file):
        with open(playlist_file, 'r') as f:
            # Filter the loaded files to ensure they are valid audio files
            return [line.strip() for line in f.readlines() if _is_audio_file(line.strip())]
    else:
        # If no playlist file exists, get files from the folder and save a new list
        files = get_all_files(music_folder)
        save_playlist_order(music_folder, files)
        return files

def save_playlist_order(music_folder, file_list):
    """Saves the current playlist order to a text file."""
    playlist_file = os.path.join(music_folder, "playlist.txt")
    with open(playlist_file, 'w') as f:
        for file in file_list:
            f.write(f"{file}\n")
    print("MockPlayer: Playlist order saved.")

def get_playlist(music_folder):
    """Returns the ordered list of files from the playlist file."""
    return get_playlist_order(music_folder)

def play_pause(filename=None):
    global _playback_state
    global _current_track
    if filename:
        _current_track = filename
        _playback_state = "playing"
        print(f"MockPlayer: Started playing '{_current_track}'.")
    elif _playback_state == "stopped" or _playback_state == "paused":
        _playback_state = "playing"
        print(f"MockPlayer: Started playing '{_current_track}'.")
    elif _playback_state == "playing":
        _playback_state = "paused"
        print(f"MockPlayer: Paused playback of '{_current_track}'.")
    return _playback_state

def stop():
    global _playback_state
    global _current_track
    _playback_state = "stopped"
    _current_track = None
    print("MockPlayer: Stopped playback.")
    return _playback_state

def remove_from_playlist(music_folder, filename):
    """Removes a file from the playlist, but not from the hard drive."""
    playlist_order = get_playlist_order(music_folder)
    if filename in playlist_order:
        playlist_order.remove(filename)
        save_playlist_order(music_folder, playlist_order)
        print(f"MockPlayer: Removed '{filename}' from the playlist.")
        return True
    return False

def add_to_playlist(music_folder, filename):
    """Adds a file to the end of the playlist."""
    playlist_order = get_playlist_order(music_folder)
    if filename not in playlist_order:
        playlist_order.append(filename)
        save_playlist_order(music_folder, playlist_order)
        print(f"MockPlayer: Added '{filename}' to the playlist.")
        return True
    return False