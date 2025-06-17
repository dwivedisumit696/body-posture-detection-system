# Body Posture Detection System 🧍‍♂️🟢🔴

A desktop application that monitors your sitting or standing posture in real time using a webcam, Google Mediapipe’s pose-estimation model, and OpenCV.
If you slouch or tilt, the app flashes a red “Bad Posture” warning and plays a spoken reminder so you can correct yourself immediately.


## ✨ Key Features

| Capability | Details |
|------------|---------|
| **Real-time pose tracking** | Uses **Mediapipe Pose** to locate shoulders & nose every frame |
| **Good / Bad posture classifier** | Simple heuristics:<br>• Shoulder misalignment > 10 % of frame height<br>• Nose ≥ 10 % in front of shoulder line |
| **Instant feedback** | GUI banner turns green or red; optional TTS reminder (“Bad posture detected”) |
| **Minimal GUI	** | Built with Tkinter – one-click Start Detection, Stop, and Exit|
| **Cross-platform** | Tested on Windows 10, macOS 14, Ubuntu 22.04 – just needs a webcam|


## 📦 Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/<your-handle>/body-posture-detection-system.git
   cd body-posture-detection-system

   
2. **Create a virtual environment (recommended)**

    ```bash
        python -m venv .venv
        # On Linux/macOS:
        source .venv/bin/activate
        # On Windows (PowerShell):
        .venv\Scripts\Activate
        
3. **Install dependencies**
   
        pip install -r requirements.txt
   
   requirements.txt
   
        opencv-python
        mediapipe
        pyttsx3
        Pillow
        
# 🚀 Usage

    - python main.py
  1. Allow webcam permission when prompted.
  2. Click Start Body Posture – the live feed appears.
  3. A green label means “Good Posture”; a red label + voice alert means fix your posture.
  4. Stop Detection pauses processing; Close exits cleanly (releases the camera).

   
# 🗂️ Project Structure

      ├── Final_year_Project/
      │   ├── main.py            # Tkinter GUI + Mediapipe posture logic
      │   └── README.md          # ← you are here
      └── requirements.txt


## 🤖 How It Works

1. **Pose Landmark Detection**  
   The webcam stream is piped into **MediaPipe Pose**, which returns 33 body‐landmark coordinates (x, y, z, visibility) for every video frame.

2. **Feature Extraction**  
   From those landmarks we compute two ergonomic signals:  
   - `shoulder_alignment = |y_left_shoulder − y_right_shoulder|` &nbsp;→ detects torso tilt  
   - `nose_to_shoulder = mean(y_shoulders) − y_nose` &nbsp;→ detects forward head posture (slouch)

3. **Rule-Based Classification**  
   ```text
   if shoulder_alignment > 0.10  OR  nose_to_shoulder < -0.10:
       posture = "bad"
   else:
       posture = "good"

      

---

## 🛠️ Roadmap/ideas

| Status | Feature/Task | Notes |
|--------|--------------|-------|
| ✅ | **Real-time posture detection (v1.0)** | CPU-friendly, 30 FPS on 720p |
| ✅ | GUI alerts + TTS | Tkinter banners + `pyttsx3` voice prompts |
| ⬜ | Daily posture report (CSV/JSON) | Summarize good/bad minutes per day |
| ⬜ | Sensitivity slider | Adjust detection thresholds at runtime |
| ⬜ | Dark-mode UI | Use `ttk` themes or custom CSS (ttkthemes) |
| ⬜ | Mobile port | Kivy / React Native camera pipeline |
| ⬜ | One-click installer | PyInstaller or Briefcase bundle for Win/macOS/Linux |

*Legend: `✅` done &nbsp;`⬜` planned &nbsp;`⚙️` in progress*

---

---

## 🤝 Contributing

Pull requests are welcome! To get started:

 1. fork the repository and create a feature branch:
  
        git checkout -b feature/awesome
 2. Commit your changes:
    
        git commit -m "Add awesome feature"
 5. Push to your branch:

        git push origin feature/awesome
 7. Open a Pull Request describing your fix or feature.
 ### Code Style
 Please run the formatters and linters before committing:

 black .
 ruff --fix .

## 🙏 Acknowledgements

- **[Google Mediapipe](https://mediapipe.dev)** – real-time ML pipelines  
- **[OpenCV](https://opencv.org)** – computer-vision backbone  
- **[Pillow](https://python-pillow.org)** – image handling in Tkinter  
- The **Python community** for the awesome ecosystem 🤍








