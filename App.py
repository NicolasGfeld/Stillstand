import streamlit as st
import os
from pathlib import Path

def save_uploaded_file(uploaded_file):
    save_path = Path("uploads")
    save_path.mkdir(exist_ok=True)
    file_path = save_path / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    st.title("Video Uploader App")
    
    uploaded_file = st.file_uploader("Lade ein Video hoch", type=["mp4", "mov", "avi", "mkv"])
    
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        st.success(f"Datei gespeichert unter: {file_path}")
        st.write(f"Gespeicherter Pfad: {file_path}")
        
        # Video abspielen (alternative Methoden für bessere Kompatibilität)
        try:
            with open(file_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)
        except Exception as e:
            st.error(f"Fehler beim Abspielen des Videos: {e}")

if __name__ == "__main__":
    main()
