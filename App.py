import os
import requests
from ultralytics import YOLO

# GitHub Raw URL zum Modell (ersetze durch deine tatsächliche URL)
GITHUB_MODEL_URL = "https://raw.githubusercontent.com/NicolasGfeld/Stillstand/best.pt"
LOCAL_MODEL_PATH = "best.pt"

# Prüfen, ob das Modell bereits existiert, wenn nicht -> herunterladen
if not os.path.exists(LOCAL_MODEL_PATH):
    print("🔽 YOLO-Modell wird heruntergeladen...")
    response = requests.get(GITHUB_MODEL_URL, stream=True)
    with open(LOCAL_MODEL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("✅ Download abgeschlossen!")
else:
    print("✅ Modell bereits vorhanden.")

# YOLO-Modell laden
model = YOLO(LOCAL_MODEL_PATH)

# Jetzt kannst du das Modell normal weiterverwenden
# Beispiel: model.predict("test_image.jpg")
