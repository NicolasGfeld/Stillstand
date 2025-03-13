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
        
        # Video abspielen
        st.video(str(file_path))

if __name__ == "__main__":
    main()

