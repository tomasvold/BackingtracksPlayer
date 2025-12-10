# app.py
from flask import Flask, render_template, request, jsonify
import os
import subprocess # NEW: import subprocess for executing commands

# --- Configuration ---
try:
    from config import MUSIC_FOLDER
except ImportError:
    MUSIC_FOLDER = "mock_music"
    print("No config.py found. Using mock_music folder.")

# Make sure the music folder exists
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)
    if MUSIC_FOLDER == "mock_music":
        open(os.path.join(MUSIC_FOLDER, "track1.wav"), "a").close()
        open(os.path.join(MUSIC_FOLDER, "track2.mp3"), "a").close()

# --- Player & GPIO Library Selection ---
# This block will attempt to import the real RPi.GPIO and Player libraries.
# If it fails, it will fall back to our mock versions for PC development.
try:
    import RPi.GPIO as GPIO
    from Player import get_playlist, play_pause, stop, remove_from_playlist, save_playlist_order, get_all_files, add_to_playlist, get_playlist_order
    print("Running on Raspberry Pi with real GPIO and Player.")
except ImportError:
    import MockGPIOClass as GPIO
    from MockPlayer import get_playlist, play_pause, stop, remove_from_playlist, save_playlist_order, get_all_files, add_to_playlist
    print("Running on PC with MockPlayer and MockGPIO.")

# Configure GPIO using the selected library
GPIO.setmode(GPIO.BCM)
# Add your specific GPIO setup here for buttons, LEDs, etc.
# GPIO.setup(your_pin, GPIO.IN)

app = Flask(__name__)

# This line ensures the playlist is loaded on startup
if MUSIC_FOLDER:
    try:
        get_playlist_order(MUSIC_FOLDER)
    except NameError:
        # This will happen on the PC, as MockPlayer does not have get_playlist_order
        print("MockPlayer does not have get_playlist_order. Skipping initialization.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/playlist', methods=['GET'])
def get_playlist_api():
    files = get_playlist(MUSIC_FOLDER)
    return jsonify({'files': files})

@app.route('/api/available_tracks', methods=['GET'])
def get_available_tracks_api():
    all_files = get_all_files(MUSIC_FOLDER)
    playlist_files = get_playlist(MUSIC_FOLDER)
    available_tracks = [f for f in all_files if f not in playlist_files]
    return jsonify({'files': available_tracks})

@app.route('/api/play_pause', methods=['POST'])
def play_pause_api():
    data = request.json
    filename = data.get('filename')
    state = play_pause(filename)
    return jsonify({'state': state})

@app.route('/api/stop', methods=['POST'])
def stop_api():
    state = stop()
    return jsonify({'state': state})

@app.route('/api/remove_file', methods=['POST'])
def remove_file_api():
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'Filename not provided'}), 400
    
    if remove_from_playlist(MUSIC_FOLDER, filename):
        return jsonify({'status': 'success', 'message': f'File {filename} removed from playlist'}), 200
    else:
        return jsonify({'error': 'File not found in playlist'}), 500

@app.route('/api/reorder_playlist', methods=['POST'])
def reorder_playlist_api():
    data = request.json
    new_order = data.get('new_order')
    if not new_order:
        return jsonify({'error': 'New order not provided'}), 400
    
    save_playlist_order(MUSIC_FOLDER, new_order)
    return jsonify({'status': 'success', 'message': 'Playlist order saved'}), 200

@app.route('/api/add_track', methods=['POST'])
def add_track_api():
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'Filename not provided'}), 400

    if add_to_playlist(MUSIC_FOLDER, filename):
        return jsonify({'status': 'success', 'message': f'File {filename} added to playlist'}), 200
    else:
        return jsonify({'error': 'File not added to playlist'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)