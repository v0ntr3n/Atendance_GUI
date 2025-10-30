<div align="center" markdown="1">

<h1>➤ Attendance&nbsp;GUI</h1>

<p><b>Face-recognition attendance tracker built with PyQt5 &amp; OpenCV</b></p>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3670A0?logo=python&logoColor=white)](#-requirements)
[![PyQt5](https://img.shields.io/badge/PyQt5-Widget_UI-41CD52?logo=qt)](#-run-it)
[![OpenCV](https://img.shields.io/badge/OpenCV-LBPH_Face-5C3EE8?logo=opencv&logoColor=white)](#-register-students)
[![SQLite](https://img.shields.io/badge/SQLite-students.db-044A64?logo=sqlite&logoColor=white)](#-data-flow)

</div>

---

## ✨ Highlights
- Live preview with face detection overlays, attendance list, and capture progress ring.
- Register new students straight from the UI; faces auto-save and retrain the recogniser.
- Lightweight storage: on-disk SQLite (`students.db`) plus LBPH model (`data/recognition.yml`).
- Works with RTSP streams or a direct webcam (set `RTSP_URL = 0`).

## ⚙️ Requirements

| Dependency | Notes |
|------------|-------|
| Python 3.8+ | Tested on Windows; PyQt5/OpenCV support required on Linux/macOS too. |
| `opencv-contrib-python` | Needed for `cv2.face.LBPHFaceRecognizer_create`. |
| `PyQt5`, `numpy` | Listed explicitly; install via `pip`. |
| Camera source | RTSP endpoint or local webcam index. |

## 🚀 Quick Start

```bash
# Optional, but keeps dependencies isolated
python -m venv .venv

# Activate
# PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install PyQt5 opencv-contrib-python numpy
```

<details>
<summary><b>💡 Version pin suggestion</b></summary>

```
PyQt5==5.15.10
opencv-contrib-python==4.9.0.80
numpy==1.26.4
```

</details>

## 🧭 Configure Before Launch
1. Open `config/config.py`.
2. Update the following:
   - `RTSP_URL`: stream URL (`rtsp://user:pass@ip:port/route`) **or** `0` for a USB webcam.
   - `IMAGES_PATH`: folder that will hold captured faces (default `"images"`).
   - `CASCADE_PATH` / `LBPHFACE_PATH`: update if you move model files.
   - `MAX_SAMPLES`: number of images to capture per student (default `50`).
3. Ensure directories exist:
   ```bash
   mkdir images
   ```
   `data/` already contains the Haar cascade and a starter recogniser file.

## ▶️ Run It
```bash
python GUI.py
```
You’ll get a window with the video feed on the left and controls + attendance list on the right.

## 🧑‍🎓 Register Students
1. Click **Add Student**.
2. Provide Student ID, Name, and Class (stored in `students.db`).
3. Capture thread starts automatically:
   - Faces save to `images/<student_id>/`.
   - Circular progress shows capture count until `MAX_SAMPLES`.
   - LBPH retrains and overwrites `data/recognition.yml` + `labels.txt`.
4. A confirmation dialog appears and the video thread reloads the new model.

## 🔁 Data Flow
- **During recognition** (`Start` button):
  - Frames pass through `utils/pre_process.py` for grayscale, equalise, blur.
  - Haar cascade locates faces, LBPH predicts label → student info is fetched from SQLite.
  - Overlay shows ID, name, class, confidence, and timestamp.
  - Each recognised ID emits once per session to update the attendance list.
- **Need persistence?** Extend `VideoThread.update_attendance_signal` to write rows to CSV/DB.

## 🔧 Troubleshooting
- **Camera won’t open**: confirm `RTSP_URL`, credentials, and firewall. Test with `RTSP_URL = 0`.
- **`cv2.face` missing**: install `opencv-contrib-python`, not `opencv-python`.
- **No faces detected**: check lighting and confirm `data/haarcascade_frontalface_default.xml` exists.
- **Model never updates**: delete `data/recognition.yml` + `labels.txt` to rebuild after capturing new faces.

## 🗂 Project Layout
```
GUI.py                     # PyQt main window & threads wiring
config/config.py           # Stream URL, model paths, capture constants
utils/db_utils.py          # SQLite helpers (init, CRUD)
utils/pre_process.py       # Image preprocessing pipeline
widgets/CaptureFacesThread # Thread for capturing faces & retraining
widgets/VideoCapture       # Live recognition + attendance updates
widgets/*                  # Custom widgets (progress, dialogs)
data/                      # Haar cascade & LBPH model artifacts
labels.txt                 # Pipe-separated labels synced with the LBPH model
students.db                # Auto-created SQLite database
images/                    # Created at runtime; per-student face samples
```

## 🔮 Next Steps
1. Generate a `requirements.txt` or lockfile for reproducible installs.
2. Package with PyInstaller or fbs for distribution on Windows/macOS/Linux.
3. Persist attendance logs (SQLite table or CSV) for reporting.
