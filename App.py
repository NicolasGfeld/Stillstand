import streamlit as st
import tempfile

st.title("📂 Video Upload und Anzeige")

uploaded_file = st.file_uploader("Lade dein Video hoch", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # ✅ Temporäre Datei speichern
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())
        video_path = temp_file.name  # Pfad zur Datei
    
    st.success("✅ Video erfolgreich hochgeladen!")
    st.video(video_path)  # ✅ Video abspielen
