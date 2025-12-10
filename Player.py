# Player.py
import os
import pygame

# Initialize the pygame mixer for audio playback
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Pygame mixer failed to initialize: {e}")

_playback_state = "stopped"
_current_track_index = -1
_current_playlist = []
_music_folder = ""

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
    global _current_playlist
    global _music_folder

    if os.path.exists(playlist_file):
        with open(playlist_file, 'r') as f:
            _current_playlist = [line.strip() for line in f.readlines() if _is_audio_file(line.strip())]
    else:
        _current_playlist = get_all_files(music_folder)
        save_playlist_order(music_folder, _current_playlist)
    
    _music_folder = music_folder
    return _current_playlist

def save_playlist_order(music_folder, file_list):
    """Saves the current playlist order to a text file."""
    playlist_file = os.path.join(music_folder, "playlist.txt")
    with open(playlist_file, 'w') as f:
        for file in file_list:
            f.write(f"{file}\n")
    print("Player: Playlist order saved.")

def get_playlist(music_folder):
    """Returns the ordered list of files from the playlist file."""
    return get_playlist_order(music_folder)

def play_pause(filename=None):
    global _playback_state
    global _current_track_index

    if not pygame.mixer.get_init():
        print("Error: Pygame mixer not initialized. Cannot play audio.")
        _playback_state = "stopped"
        return _playback_state

    if filename:
        try:
            full_path = os.path.join(_music_folder, filename)
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
            
            if filename in _current_playlist:
                _current_track_index = _current_playlist.index(filename)
            else:
                _current_track_index = -1
            
            _playback_state = "playing"
            print(f"Player: Started playing new track '{filename}'.")
        except (pygame.error, ValueError) as e:
            print(f"Player: Error loading or playing file: {e}")
            _playback_state = "stopped"
    
    else:
        if _playback_state == "playing":
            pygame.mixer.music.pause()
            _playback_state = "paused"
            print("Player: Paused playback.")
        elif _playback_state == "paused":
            pygame.mixer.music.unpause()
            _playback_state = "playing"
            print("Player: Resumed playback.")
        elif _playback_state == "stopped" and _current_track_index != -1:
            filename = _current_playlist[_current_track_index]
            try:
                full_path = os.path.join(_music_folder, filename)
                pygame.mixer.music.load(full_path)
                _playback_state = "playing"
                pygame.mixer.music.play()
                print(f"Player: Started playing '{filename}'.")
            except pygame.error as e:
                print(f"Player: Error loading or playing file: {e}")
                _playback_state = "stopped"
            
    return _playback_state

def stop():
    global _playback_state
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
    _playback_state = "stopped"
    print("Player: Stopped playback.")
    return _playback_state

def remove_from_playlist(music_folder, filename):
    """Removes a file from the playlist, but not from the hard drive."""
    global _current_playlist
    if filename in _current_playlist:
        _current_playlist.remove(filename)
        save_playlist_order(music_folder, _current_playlist)
        print(f"Player: Removed '{filename}' from the playlist.")
        return True
    return False

def add_to_playlist(music_folder, filename):
    """Adds a file to the end of the playlist."""
    global _current_playlist
    if filename not in _current_playlist:
        _current_playlist.append(filename)
        save_playlist_order(music_folder, _current_playlist)
        print(f"Player: Added '{filename}' to the playlist.")
        return True
    return False