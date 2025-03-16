# 📺 Echtzeit-Analyse von Stillständen mit YOLO

## 📌 Projektbeschreibung
Dieses Projekt ermöglicht die **automatische Erkennung und Analyse von Maschinenstillständen** mithilfe von **YOLOv8** und einer **Streamlit-Webanwendung**. Das System verarbeitet **Live-Kamera- oder Videodaten**, erkennt relevante Objekte und klassifiziert Stillstände als **geplant oder ungeplant**.

Die Ergebnisse werden in Echtzeit in der Webanwendung visualisiert und als CSV-Datei gespeichert, um eine weitere Analyse in Excel oder anderen Tools zu ermöglichen.

---

## 🚀 Funktionen
✅ **Live- oder Videoanalyse:** Wähle zwischen Kamera-Stream oder Datei-Upload
✅ **YOLO-basierte Objekterkennung:** Automatische Identifikation von Maschinenzuständen
✅ **Stillstandsanalyse:** Erkennung und Klassifikation in "Geplant" und "Ungeplant"
✅ **Live-Visualisierung:** Echtzeit-Anzeige der Objekterkennung im Video
✅ **Ergebnis-Speicherung:** CSV-Export der erkannten Stillstände und Berechnung der OEE

---

## 🛠️ Installation & Ausführung

### 1️⃣ **Voraussetzungen**  
Stelle sicher, dass du **Python 3.8+** installiert hast.

### 2️⃣ **Repository klonen**

git clone https://github.com/dein-benutzername/stillstandsanalyse.git
cd stillstandsanalyse


### 3️⃣ **Benötigte Pakete installieren**

pip install -r requirements.txt


### 4️⃣ **Start der Anwendung**

streamlit run app.py


---

## 📊 Datenausgabe (CSV-Datei)
Nach der Analyse wird eine CSV-Datei mit folgender Struktur gespeichert:

| Start (s) | Ende (s) | Dauer (s) | Typ     | Gesamt Geplant (s) | Gesamt Ungeplant (s) | Gesamt Stillstandszeit (s) | OEE-Faktor (%) |
|-----------|---------|-----------|---------|--------------------|---------------------|----------------------------|----------------|
| 10.33     | 10.50   | 0.17      | Geplant |                    |                     |                            |                |
| 11.17     | 16.50   | 5.33      | Geplant |                    |                     |                            |                |
|           |         |           | **GESAMT:** | 135.83            | 29.67               | 165.50                     | 68.86          |

Die Datei kann direkt in **Excel oder andere Datenanalyse-Tools** importiert werden.

---

## 🔧 Mögliche Erweiterungen
- **Optimierung der Performance:** Nutzung einer GPU zur schnelleren Analyse
- **Mehr Objekttypen:** Training des YOLO-Modells mit erweiterten Daten
- **Cloud-Anbindung:** Speicherung und Visualisierung der Ergebnisse in einer Web-Datenbank

---

## 📝 Lizenz & Autor
Dieses Projekt wurde von Nicolas Gutsfeld erstellt und steht unter der **MIT-Lizenz**.


