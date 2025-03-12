import gdown
from ultralytics import YOLO
import os

# ✅ Richtig: Nur die Datei-ID einfügen
file_id = "1hzHnlqe3FCQ8fSOwIRY0SPh_UY1cUAoA"  
output_path = "best.pt"

# Falls die Datei noch nicht existiert, herunterladen
if not os.path.exists(output_path):
    url = f"https://drive.google.com/uc?id={file_id}"  # ✅ Korrekte Download-URL
    gdown.download(url, output_path, quiet=False)
    print("✅ Modell heruntergeladen!")

# YOLO-Modell laden
model = YOLO(output_path)
print("✅ Modell erfolgreich geladen!")
