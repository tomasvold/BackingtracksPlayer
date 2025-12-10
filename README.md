# 🎶 BackingtracksPlayer (Raspberry Pi Edition)

A portable, web-controlled media player built with Python/Flask and the Pygame mixer. This application is designed to run on a headless Raspberry Pi, allowing you to manage and play local backing tracks via any web browser on your network.

---

## ✨ Features

* **Portable Architecture:**
    * Uses a **hardware abstraction layer** via `try/except` imports in `app.py`.
    * Automatically switches between the real `Player.py` (with Pygame) and `MockPlayer.py` (simulated playback) for easy development on a PC.
    * Uses `MockGPIOClass.py` for testing hardware interaction logic without RPi.GPIO dependencies.
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

---

## 💾 Installation and Local Run

### 1. Requirements

Dependencies are listed in the `requirements.txt` file, which includes:

```text
Flask
pygame
python-dotenv
# RPi.GPIO (Pi-only - needed on the Raspberry Pi for hardware control)
# gunicorn (Recommended for production deployment on Linux/Pi)

git clone [https://github.com/tomasvold/BackingtracksPlayer.git](https://github.com/tomasvold/BackingtracksPlayer.git)
cd BackingtracksPlayer

### 🚀 Final Push Plan

Since you created the README manually on GitHub, we need to handle this carefully to avoid conflicts when you push from your local machine.

The most straightforward way is to push the local changes (`requirements.txt`) first, then pull the remote changes (`README.md`), and push again.

**Please confirm you have updated the local `README.md` file (in VS Code) with the final corrected text.** Then, we can run the final Git commands!
