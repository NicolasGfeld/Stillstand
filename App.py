import streamlit as st
import os

# 🎬 Titel der App
st.title("📹 Video-Upload für Stillstandserkennung")

# 🌟 Upload-Bereich für Videos
uploaded_file = st.file_uploader("Ziehe dein Video hierher oder wähle eine Datei aus", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Speichere das hochgeladene Video temporär
    video_path = os.path.join("temp_video.mp4")
    
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    # 📽️ Zeige das Video an
    st.video(video_path)

    st.success("✅ Video erfolgreich hochgeladen!")
