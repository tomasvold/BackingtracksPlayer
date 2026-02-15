# 🎶 BackingtracksPlayer (for Raspberry Pi)

A portable, offline audioplayer with a web-based UI built with Python/Flask. Designed to run on a Raspberry Pi with a touch screen for local control, while remaining accessible via any web browser on the same network.

---

## ✨ Features

* **Dual-Interface Control:**
    * **Local:** Optimized for use with a Raspberry Pi touch screen via the local browser.
    * **Remote:** Accessible from phones, tablets, or PCs on the same network.
* **Portable Architecture:**
    * Uses a **hardware abstraction layer** via `try/except` imports in `app.py`.
    * Automatically switches between the real `Player.py` (Pygame) for deployment and `MockPlayer.py` for easy PC development.
* **Persistent Playlist Management:**
    * Features a clean web interface with drag-and-drop reordering.
    * The playlist order is saved and loaded from a persistent `playlist.txt` file within the music directory.
* **Media Control:**
    * Play, Pause, and Stop functions powered by **Pygame mixer** for reliable, low-latency audio playback.

---

## 🛠️ Tech Stack & Tools

* **Backend Framework:** Python (Flask)
* **Audio Playback:** `pygame.mixer`
* **Front-end:** HTML, CSS, Vanilla JavaScript
* **Hardware:** Raspberry Pi + Raspberry Pi OS + Touch Screen Display

---

## 📂 Project Structure

| File/Folder | Description |
| :--- | :--- |
| `app.py` | Main Flask application and API routing. |
| `Player.py` | Real audio logic using `pygame.mixer`. |
| `MockPlayer.py` | Simulated audio logic for testing on non-Pi hardware. |
| `config.py` | Path configurations for the `MusicFolder`. |
| `templates/` | HTML templates (`index.html`). |
| `static/` | CSS and JS assets. |
| `MusicFolder/` | **(Git Ignored)** Local directory for your MP3/WAV files. |

---

## 💾 Installation and Local Run

### 1. Setup Environment
Clone the repository and prepare the Python environment:

```bash
git clone [https://github.com/tomasvold/BackingtracksPlayer.git](https://github.com/tomasvold/BackingtracksPlayer.git)
cd BackingtracksPlayer

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt