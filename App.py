import streamlit as st
import tempfile

# --- STREAMLIT APP ---
st.title("📹 Video Upload & Wiedergabe")

# --- VIDEO UPLOAD ---
uploaded_file = st.file_uploader(
    "📂 Ziehe dein Video hierher oder wähle eine Datei aus",
    type=["mp4", "avi", "mov"]
)

if uploaded_file is not None:
    # Temporäre Datei speichern
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())
        video_path = temp_file.name

    st.success("✅ Video erfolgreich hochgeladen!")
    st.video(video_path)  # Video in der App anzeigen
