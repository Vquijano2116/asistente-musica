import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents import consultar
from skill_reporte import generar_reporte_artista

st.set_page_config(
    page_title="Bavafy AI",
    page_icon="🎵",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #000000 !important;
    color: #ffffff !important;
}

.stApp {
    background: linear-gradient(180deg, #1a0a2e 0%, #000000 40%) !important;
}

/* Header */
.bavafy-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 24px 0 8px 0;
}
.bavafy-logo {
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #ffffff;
}

/* Chat messages */
.stChatMessage {
    background-color: #1a1a1a !important;
    border-radius: 12px !important;
    border: 1px solid #2a2a2a !important;
    margin-bottom: 8px !important;
}

[data-testid="stChatMessageContent"] {
    color: #ffffff !important;
}

/* Input */
.stChatInputContainer {
    background-color: #1a1a1a !important;
    border: 1px solid #6b21a8 !important;
    border-radius: 24px !important;
}

.stChatInput textarea {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border-radius: 24px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid #1f1f1f !important;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Botones */
.stButton > button {
    background-color: #7c3aed !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 24px !important;
    font-weight: 600 !important;
    padding: 8px 24px !important;
    transition: background 0.2s !important;
}

.stButton > button:hover {
    background-color: #6d28d9 !important;
}

/* Download button */
.stDownloadButton > button {
    background-color: #1a1a1a !important;
    color: #a855f7 !important;
    border: 1px solid #a855f7 !important;
    border-radius: 24px !important;
    font-weight: 600 !important;
}

/* Text input */
.stTextInput > div > div > input {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 8px !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #7c3aed !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 3px; }

/* Ocultar elementos de Streamlit */
#MainMenu, footer, header { visibility: hidden; }
</style>

<div class="bavafy-header">
    <span style="font-size:32px">🎵</span>
    <span class="bavafy-logo">BAVAFY AI</span>
</div>
<p style="color:#a0a0a0; margin-bottom:24px;">Tu asistente musical inteligente</p>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("##  Herramientas")
    st.markdown("---")
    st.markdown("###  Reporte de Artista")
    nombre_artista = st.text_input("Nombre del artista:", placeholder="Bad Bunny, Beatles...")
    if st.button("Generar PDF"):
        if nombre_artista:
            with st.spinner("Generando reporte..."):
                archivo = generar_reporte_artista(nombre_artista)
            with open(archivo, "rb") as f:
                st.download_button(
                    label="⬇ Descargar PDF",
                    data=f,
                    file_name=os.path.basename(archivo),
                    mime="application/pdf"
                )
            st.success(f" Listo!")
        else:
            st.warning("Escribe el nombre del artista")

# Chat
if "historial" not in st.session_state:
    st.session_state.historial = []

pregunta = st.chat_input("Pregunta sobre música...")

if pregunta:
    with st.spinner("🎵 Buscando..."):
        respuesta = consultar(pregunta)
    st.session_state.historial.append(("user", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)