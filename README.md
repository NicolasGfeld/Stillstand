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
```sh
git clone https://github.com/dein-benutzername/stillstandsanalyse.git
cd stillstandsanalyse
```

### 3️⃣ **Benötigte Pakete installieren**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Start der Anwendung**
```sh
streamlit run app.py
```

---

## 📜 Code-Struktur & Funktionsweise

### **1️⃣ Benutzeroberfläche (Streamlit)**
Das System nutzt **Streamlit**, um eine interaktive Oberfläche bereitzustellen. Der Benutzer kann wählen zwischen:
- **Live-Kamera-Analyse** (direkter Zugriff auf die Webcam)
- **Video-Upload** (Verarbeitung einer hochgeladenen Datei)

### **2️⃣ Objekterkennung mit YOLOv8**
Das **YOLOv8-Modell** wird geladen und verwendet, um Objekte innerhalb des Videos zu erkennen. Das Modell sucht nach vordefinierten Klassen wie:
- **Maschinenwerkzeuge** (z. B. Zange, Messschieber)
- **Geöffnete Türen** (z. B. Tür_offen)
- **Späneentferner** (Indikator für ungeplante Stillstände)

### **3️⃣ Bewegungserkennung mit Optical Flow**
Neben der Objekterkennung wird ein **Optical Flow Algorithmus (Farneback-Methode)** aus OpenCV verwendet, um Bewegungen im Video zu analysieren:
- Falls **wenig Bewegung erkannt wird**, wird ein ungeplanter Stillstand registriert.
- Falls ein Werkzeug erkannt wird, kann dies auf einen **geplanten Stillstand** hinweisen.

### **4️⃣ Stillstandsanalyse & Klassifikation**
- Falls bestimmte Objekte erkannt werden (**Werkzeugkalibrierung, Tür_offen**), wird ein **geplanter Stillstand** aufgezeichnet.
- Falls kaum Bewegung erkannt wird oder andere Störungen auftreten, wird ein **ungeplanter Stillstand** registriert.

### **5️⃣ Echtzeit-Anzeige & Datenspeicherung**
- Die Videoanalyse läuft **framebasiert** ab (jeder 5. Frame wird verarbeitet, um Performance zu optimieren).
- Stillstände werden live in einer **Tabelle** in Streamlit aktualisiert.
- Eine **CSV-Datei mit den Ergebnissen** wird generiert und kann heruntergeladen werden.

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
- **Echtzeit-Dashboard:** Dynamische Grafiken zur besseren Analyse der OEE-Daten

---

## 📝 Lizenz & Autor
Dieses Projekt wurde von Nicolas Gutsfeld erstellt und steht unter der **MIT-Lizenz**.



