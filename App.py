import gdown
from ultralytics import YOLO
import os
import streamlit as st  # ✅ Streamlit importieren
import cv2
import tempfile  # ✅ Temporäre Datei-Speicherung

# --- GOOGLE DRIVE MODELL UND YAML LADEN ---
model_file_id = "1hzHnlqe3FCQ8fSOwIRY0SPh_UY1cUAoA"  # ID für das YOLO Modell
yaml_file_id = "15clenJ6DdHJ9mwYXFeveTt15AbMnxg8g"   # ID für die YAML-Datei

# Modell herunterladen
model_output_path = "best.pt"
if not os.path.exists(model_output_path):
    url = f"https://drive.google.com/uc?id={model_file_id}"
    gdown.download(url, model_output_path, quiet=False)
    print("✅ Modell heruntergeladen!")

# YAML-Datei herunterladen
yaml_output_path = "data.yaml"
if not os.path.exists(yaml_output_path):
    url = f"https://drive.google.com/uc?id={yaml_file_id}"
    gdown.download(url, yaml_output_path, quiet=False)
    print("✅ YAML-Datei heruntergeladen!")

# YOLO-Modell laden
model = YOLO(model_output_path, data=yaml_output_path)
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

    # --- Stillstandserkennung --- 
    cap = cv2.VideoCapture(video_path)  # Video mit OpenCV öffnen
    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Frames pro Sekunde des Videos

    # Wir erstellen ein Display für jedes Frame im Video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO-Modell auf das aktuelle Frame anwenden
        results = model(frame)  # YOLO Vorhersage auf diesem Frame

        # Ergebnisse visualisieren
        for result in results.xywh[0]:
            x, y, w, h, conf, cls = result  # Extrahiere x, y, Breite, Höhe, Konfidenz und Klasse
            if conf > 0.5:  # Filtere nach einer minimalen Konfidenz
                x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Rechteck um erkannte Objekte
                cv2.putText(frame, f"{model.names[int(cls)]} {conf:.2f}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Frame anzeigen
        st.image(frame, channels="BGR", use_column_width=True)  # Anzeigen des aktuellen Frames in der App
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Video freigeben, wenn wir fertig sind
