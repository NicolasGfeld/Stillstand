import gdown
from ultralytics import YOLO
import os
import streamlit as st  # ✅ Streamlit importieren
import cv2
import tempfile  # ✅ Temporäre Datei-Speicherung

# --- GOOGLE DRIVE MODELL LADEN ---
file_id = "1hzHnlqe3FCQ8fSOwIRY0SPh_UY1cUAoA"
output_path = "best.pt"

if not os.path.exists(output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)
    print("✅ Modell heruntergeladen!")

# YOLO-Modell laden
model = YOLO(output_path)
print("✅ Modell erfolgreich geladen!")

# --- STREAMLIT APP ---
st.title("🔍 Stillstandserkennung mit YOLO")  # Titel der App

# --- VIDEO UPLOAD ---
uploaded_file = st.file_uploader("📂 Lade dein Video hoch", type=["mp4", "avi", "mov"])  # ✅ Benutzer kann Video hochladen

if uploaded_file is not None:
    # ✅ Temporäre Datei speichern
    temp_dir = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_dir.write(uploaded_file.read())
    video_path = temp_dir.name

    st.success("✅ Video erfolgreich hochgeladen!")  # Erfolgsmeldung
    st.video(video_path)  # ✅ Video in der App anzeigen

