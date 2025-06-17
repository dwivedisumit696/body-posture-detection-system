import cv2
import mediapipe as mp
import pyttsx3
import tkinter as tk
from tkinter import Label, Frame, messagebox
from PIL import Image, ImageTk
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

prev_posture = "Good Posture"

def check_posture(landmarks):
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    nose = landmarks[mp_pose.PoseLandmark.NOSE]

    shoulder_alignment = abs(left_shoulder.y - right_shoulder.y)
    nose_to_shoulder = (left_shoulder.y + right_shoulder.y) / 2 - nose.y

    bad_alignment_threshold = 0.1
    slouching_threshold = -0.1

    if shoulder_alignment > bad_alignment_threshold or nose_to_shoulder < slouching_threshold:
        return "Bad Posture"
    return "Good Posture"

class PostureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Body Posture Detection System")
        self.root.geometry("1000x800")
        self.root.configure(bg="#F0F0F0")

        Label(root, text="Body Posture Detection System", font=("Arial", 24, "bold"), bg="#F0F0F0").pack(pady=10)
        self.status_label = Label(root, text="Please allow camera access to start.", font=("Arial", 18, "bold"), bg="#F0F0F0")
        self.status_label.pack(pady=20)

        self.camera_permission_button = tk.Button(root, text="Allow Camera Access", font=("Arial", 14), command=self.request_camera_permission)
        self.camera_permission_button.pack(pady=10)

        self.check_posture_button = None
        self.stop_button = None
        self.close_button = None
        self.cap = None
        self.is_running = False
        self.last_check_time = time.time()
        self.prev_posture = "Good Posture"
        self.spoken_warning = False

    def request_camera_permission(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            messagebox.showerror("Camera Access", "Camera permission is denied. Please allow camera access.")
        else:
            self.camera_permission_button.pack_forget()
            self.status_label.config(text="Camera access granted. You can now check posture.")
            self.show_posture_buttons()

    def show_posture_buttons(self):
        self.check_posture_button = tk.Button(self.root, text="Check Body Posture", font=("Arial", 14), command=self.check_body_posture)
        self.check_posture_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Detection", font=("Arial", 14), command=self.stop_posture_check)
        self.stop_button.pack(pady=10)

        self.close_button = tk.Button(self.root, text="Close", font=("Arial", 14), command=self.close_app)
        self.close_button.pack(pady=10)

    def check_body_posture(self):
        if self.cap is None or not self.cap.isOpened():
            self.request_camera_permission()
            return
        self.is_running = True
        self.process_frame()

    def process_frame(self):
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="Camera disconnected. Reconnecting...")
            self.cap.release()
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            return

        frame = cv2.resize(frame, (640, 480))
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        posture_status = "Good Posture"

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            posture_status = check_posture(results.pose_landmarks.landmark)

            if posture_status == "Bad Posture" and self.prev_posture == "Good Posture":
                self.speak_warning()
                self.spoken_warning = True
            elif posture_status == "Good Posture":
                self.spoken_warning = False

        color = (0, 255, 0) if posture_status == "Good Posture" else (0, 0, 255)
        cv2.putText(frame, posture_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        if hasattr(self, 'video_label'):
            self.video_label.config(image=img)
            self.video_label.image = img
        else:
            self.video_label = Label(self.root, image=img)
            self.video_label.image = img
            self.video_label.pack()

        self.status_label.config(text=f"Posture: {posture_status}", fg="green" if posture_status == "Good Posture" else "red")
        self.prev_posture = posture_status
        self.root.after(30, self.process_frame)

    def speak_warning(self):
        if not self.spoken_warning:
            engine.say("Bad posture detected")
            engine.runAndWait()
            self.spoken_warning = True

    def stop_posture_check(self):
        self.is_running = False
        self.status_label.config(text="Posture detection stopped.")

    def close_app(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PostureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
