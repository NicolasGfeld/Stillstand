import cv2
import os
import time
import streamlit as st
import pandas as pd
from ultralytics import YOLO
import numpy as np

# 1⃣ Streamlit UI – Auswahl zwischen Datei-Upload und Kamera
st.title("📺 Echtzeit-Analyse von Stillständen mit YOLO")
option = st.radio("Wähle eine Quelle:", ("📎 Video hochladen", "🎥 Live-Kamera"))

if option == "📎 Video hochladen":
    uploaded_file = st.file_uploader("Lade ein Video hoch", type=["mp4", "avi", "mov"])
    if uploaded_file:
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        cap = cv2.VideoCapture(video_path)
    else:
        st.warning("Bitte lade ein Video hoch.")
        st.stop()
else:
    cap = cv2.VideoCapture(0)  # Live-Kamera

# 2⃣ Modell laden
model = YOLO("dataset/runs/detect/train2/weights/best.pt")

# 3⃣ Ergebnisse-Ordner erstellen
output_dir = "Ergebnisse"
os.makedirs(output_dir, exist_ok=True)

# 4⃣ Video-Setup
fps = int(cap.get(cv2.CAP_PROP_FPS))
width, height = 1280, 720
output_path = os.path.join(output_dir, "output_detected.mp4")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 5⃣ Stillstand-Tracking
stillstand_fälle = []
gesamt_geplanter_stillstand = 0
gesamt_ungeplanter_stillstand = 0
stillstand_aktiv = False
stillstand_start = None

prev_gray = None
bewegungs_puffer = []
bewegungs_grenze = 2.0

frame_count = 0
sample_rate = 5  # Nur jeder 5. Frame wird analysiert

# 6⃣ Streamlit-Video-Output
frame_window = st.image([])  
stillstand_df = st.empty()  # Platzhalter für Stillstandsdaten

# Zustand für Pause initialisieren
if "paused" not in st.session_state:
    st.session_state.paused = False

def toggle_pause():
    st.session_state.paused = not st.session_state.paused

# 7⃣ Video durchlaufen
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is None:
        prev_gray = gray
        continue

    if frame_count % sample_rate == 0:
        results = model(frame, conf=0.3)
        detected_labels = [model.names[int(box.cls)] for box in results[0].boxes]

        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        movement = np.sum(np.abs(flow))
        bewegungs_puffer.append(movement)
        if len(bewegungs_puffer) > 10:
            bewegungs_puffer.pop(0)

        bewegung_mittelwert = np.mean(bewegungs_puffer)
        prev_gray = gray

        aktuelle_zeit = frame_count / fps  

        stillstand_typ = None
        if "Werkzeugkalibrierung" in detected_labels or (
            "Tür_offen" in detected_labels and any(obj in detected_labels for obj in ["Zange", "Messschieber", "Einstellwerkzeug"])):
            stillstand_typ = "Geplant"
        elif "Späneentferner" in detected_labels or bewegung_mittelwert < bewegungs_grenze:
            stillstand_typ = "Ungeplant"

        if stillstand_typ:
            if not stillstand_aktiv:
                stillstand_aktiv = True
                stillstand_start = aktuelle_zeit
                stillstand_aktuelle_art = stillstand_typ
        elif stillstand_aktiv:
            stillstand_dauer = aktuelle_zeit - stillstand_start
            stillstand_fälle.append({
                "Start (s)": round(stillstand_start, 2),
                "Ende (s)": round(aktuelle_zeit, 2),
                "Dauer (s)": round(stillstand_dauer, 2),
                "Typ": stillstand_aktuelle_art
            })

            if stillstand_aktuelle_art == "Geplant":
                gesamt_geplanter_stillstand += stillstand_dauer
            else:
                gesamt_ungeplanter_stillstand += stillstand_dauer

            stillstand_aktiv = False

    frame_count += 1
    annotated_frame = results[0].plot()
    out.write(annotated_frame)
    frame_window.image(annotated_frame, channels="BGR")

    if stillstand_fälle:
        df = pd.DataFrame(stillstand_fälle)
        stillstand_df.dataframe(df)

    if st.session_state.paused:
        st.warning("⏸️ Analyse pausiert. Klicke auf den Button, um fortzufahren.")
        time.sleep(0.1)
        continue

    time.sleep(0.1)

cap.release()
out.release()
cv2.destroyAllWindows()

# 11⃣ CSV-Datei speichern
csv_path = os.path.join(output_dir, "stillstand.csv")
df = pd.DataFrame(stillstand_fälle)

gesamt_stillstandszeit = round(gesamt_geplanter_stillstand + gesamt_ungeplanter_stillstand, 2)
video_länge = round(frame_count / fps, 2)
oee_faktor = round(1 - (gesamt_stillstandszeit / video_länge), 4) * 100

gesamtwerte_df = pd.DataFrame([{
    "Start (s)": "", 
    "Ende (s)": "",
    "Dauer (s)": "",
    "Typ": "GESAMT:",
    "Gesamt Geplant (s)": round(gesamt_geplanter_stillstand, 2),
    "Gesamt Ungeplant (s)": round(gesamt_ungeplanter_stillstand, 2),
    "Gesamt Stillstandszeit (s)": gesamt_stillstandszeit,
    "Theoretisch mögliche Produktionszeit (s)": video_länge,
    "OEE-Faktor (%)": oee_faktor
}])

df = pd.concat([df, pd.DataFrame([{}]), gesamtwerte_df], ignore_index=True)
df.to_csv(csv_path, index=False, sep=";", quoting=1, float_format="%.2f")

st.success("✅ Analyse abgeschlossen! CSV gespeichert.")
st.download_button("📥 CSV-Datei herunterladen", data=open(csv_path, "rb"), file_name="stillstand.csv", mime="text/csv")
