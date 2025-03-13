import streamlit as st

# Titel der App
st.title("📹 Video-Uploader & Player")

# Video hochladen
uploaded_file = st.file_uploader("Lade ein Video hoch", type=["mp4", "avi", "mov", "mkv"])

# Wenn eine Datei hochgeladen wurde, anzeigen
if uploaded_file is not None:
    st.video(uploaded_file)
