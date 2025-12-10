# 🎶 BackingtracksPlayer (for Raspberry Pi)

A portable, offline web-controlled audioplayer built with Python/Flask. Built to run on a headless Raspberry Pi to manage and play local backing tracks via any web browser.

---

## ✨ Features

* **Portable Architecture:**
    * Uses a **hardware abstraction layer** via `try/except` imports in `app.py`.
    * Automatically switches between the real `Player.py` (Pygame) for deployment and `MockPlayer.py`/`MockGPIOClass.py` for easy PC development and testing.
* **Persistent Playlist Management:**
    * Features a clean web interface built with HTML, CSS, and vanilla JavaScript.
    * Supports drag-and-drop reordering of tracks within the playlist.
    * The playlist order is saved and loaded from a persistent `playlist.txt` file within the music directory.
* **Media Control:**
    * Play, Pause, and Stop functions for the selected track.
    * Uses the powerful **Pygame mixer** for reliable, low-latency audio playback on the Raspberry Pi.

---

## 🛠️ Tech Stack & Tools

* **Backend Framework:** Python (Flask)
* **Audio Playback:** `pygame.mixer`
* **Portability:** Custom `MockPlayer.py` and `MockGPIOClass.py` modules.
* **Configuration:** Simple relative path configuration via `config.py` for easy project relocation.
* **Front-end:** HTML, CSS, JavaScript (for UI updates and drag-and-drop).
* **Hardware:** Designed for a Raspberry Pi running Raspberry Pi OS.

---

## 📂 Project Structure

The application is structured for portability and clear separation of concerns:

| File/Folder | Description |
| :--- | :--- |
| `app.py` | Main Flask application, handles routing and manages the `Player` import logic. |
| `Player.py` | **Real** player module using `pygame.mixer` for Raspberry Pi deployment. |
| `MockPlayer.py` | **Mock** player module with print statements for PC development and testing. |
| `MockGPIOClass.py` | Mock module for hardware interaction testing on a PC. |
| `config.py` | Configuration file containing the relative path to the `MusicFolder`. |
| `templates/` | Stores the main HTML template (`index.html`) rendered by Flask. |
| `static/` | Stores static assets like CSS (`style.css`) and JavaScript (`script.js`). |
| `MusicFolder/` | **(Excluded by .gitignore)** The dedicated directory for MP3/WAV backing tracks. |
| `venv/` | **(Excluded by .gitignore)** The Python virtual environment. |

---

## 💾 Installation and Local Run

```bash
# The first step is always to clone the repository and set up the environment on the Raspberry Pi:
git clone [https://github.com/tomasvold/BackingtracksPlayer.git](https://github.com/tomasvold/BackingtracksPlayer.git)
cd BackingtracksPlayer

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Add your backing tracks (MP3 or WAV) to the 'MusicFolder' directory.

# Start the Flask application
python app.py (or go to http://127.0.0.1:5000 in your web browswer)
