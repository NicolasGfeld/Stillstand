import streamlit as st

st.title("📹 Video-Uploader & Player")

uploaded_file = st.file_uploader("Lade ein Video hoch", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    # Workaround: Video als Bytes lesen und erneut übergeben
    video_bytes = uploaded_file.read()
    st.video(video_bytes)
