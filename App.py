import gdown
from ultralytics import YOLO
import os

# Google Drive Datei-ID (ersetzen mit deiner ID!)
file_id = "https://drive.google.com/file/d/1hzHnlqe3FCQ8fSOwIRY0SPh_UY1cUAoA/view?usp=drive_link"  # <-- Ersetze das mit deiner Datei-ID
output_path = "best.pt"

# Falls die Datei noch nicht existiert, herunterladen
if not os.path.exists(output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)
    print("✅ Modell heruntergeladen!")

# YOLO-Modell laden
model = YOLO(output_path)
print("✅ Modell erfolgreich geladen!")
