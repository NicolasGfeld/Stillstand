import gdown
import cv2
import os
from ultralytics import YOLO
import numpy as np
import streamlit as st
import tempfile

# --- GOOGLE DRIVE MODEL UND YAML LADEN ---
model_file_id = "1hzHnlqe3FCQ8fSOwIRY0SPh_UY1cUAoA"  # ID für das YOLO Modell
yaml_file_id = "1hzHnlqe3FCQ8fSOwIRY0SPh_UY1cUAoB"   # ID für die YAML-Datei

# Download des YOLO-Modells und der YAML-Datei von Google Drive
def download_file_from_drive(file_id, output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)

# YOLO-Modell und YAML-Datei herunterladen
model_output_path = "best.pt"
yaml_output_path = "data.yaml"

if not os.path.exists(model_output_path):
    download_file_from_drive(model_file_id, model_output_path)

if not os.path.exists(yaml_output_path):
    download_file_from_drive(yaml_file_id, yaml_output_path)

# YOLO-Modell laden
model = YOLO(model_output_path, data=yaml_output_path)
st.title("🔍 Stillstandserkennung mit YOLO")  # Titel der App

# --- VIDEO UPLOAD ---
uploaded_file = st.file_uploader("📂 Lade dein Video hoch", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Temporäre Datei speichern
    temp_dir = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_dir.write(uploaded_file.read())
    video_path = temp_dir.name

    st.success("✅ Video erfolgreich hochgeladen!")  # Erfolgsmeldung
    st.video(video_path)  # Zeige Video in der App an

    # 2⃣ Video öffnen
    cap = cv2.VideoCapture(video_path)

    # 3⃣ Ergebnisse-Ordner erstellen
    output_dir = "Ergebnisse"
    os.makedirs(output_dir, exist_ok=True)

    # 4⃣ Video speichern
    output_path = os.path.join(output_dir, "output_detected.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = 1280, 720  # Kleinere Auflösung
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 5⃣ Stillstand-Tracking
    stillstand_aktiv = False
    stillstand_start = None

    geplanter_stillstand = False
    ungeplanter_stillstand = False

    bewegungs_puffer = []  # Speichert die letzten Bewegungswerte
    bewegungs_grenze = 2.0  # Schwellwert für Bewegung

    prev_gray = None  # Vorheriges Graustufenbild für Bewegungserkennung

    # 6⃣ Objekterkennung für jedes Frame
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        frame = cv2.resize(frame, (width, height))  # Video verkleinern
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # In Graustufen konvertieren
        
        # Initialisierung des ersten Frames
        if prev_gray is None:
            prev_gray = gray
            continue
        
        # YOLOv8 auf das aktuelle Frame anwenden
        results = model(frame, conf=0.3)
        detected_labels = [model.names[int(box.cls)] for box in results[0].boxes]

        # Bewegungserkennung
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        movement = np.sum(np.abs(flow))  # Summierte Bewegung
        bewegungs_puffer.append(movement)
        if len(bewegungs_puffer) > 10:
            bewegungs_puffer.pop(0)
        
        bewegung_mittelwert = np.mean(bewegungs_puffer)
        prev_gray = gray  # Setze das aktuelle Frame als vorheriges Frame
        
        # **Stillstandserkennung**
        if "Tür_offen" in detected_labels:
            if any(obj in detected_labels for obj in ["Zange", "Messschieber", "Einstellwerkzeug", "Werkzeugkalibrierung"]):
                if not geplanter_stillstand:
                    geplanter_stillstand = True
                    stillstand_start = time.time()
            elif "Späneentferner" in detected_labels:
                if not ungeplanter_stillstand:
                    ungeplanter_stillstand = True
                    stillstand_start = time.time()
            elif bewegung_mittelwert < bewegungs_grenze:
                if not ungeplanter_stillstand:
                    ungeplanter_stillstand = True
                    stillstand_start = time.time()
        
        # **Stillstand beenden**
        if geplanter_stillstand and not any(obj in detected_labels for obj in ["Zange", "Messschieber", "Einstellwerkzeug", "Werkzeugkalibrierung"]):
            geplanter_stillstand = False
        
        if ungeplanter_stillstand and not ("Tür_offen" in detected_labels and ("Späneentferner" in detected_labels or bewegung_mittelwert < bewegungs_grenze)):
            ungeplanter_stillstand = False

        # **Anzeige im Video**
        stillstand_text = "Geplant: {} | Ungeplant: {}".format(
            "Ja" if geplanter_stillstand else "Nein", 
            "Ja" if ungeplanter_stillstand else "Nein"
        )
        cv2.putText(frame, stillstand_text, (10, height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        # Ergebnisse anzeigen & speichern
        annotated_frame = results[0].plot()
        out.write(annotated_frame)
        st.image(annotated_frame, channels="BGR", use_column_width=True)  # Zeige Frame im Streamlit

    # 7⃣ Alles freigeben
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    st.success(f"✅ Ergebnis-Video gespeichert in {output_path}")
