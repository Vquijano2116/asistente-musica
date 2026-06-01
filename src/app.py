import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents import consultar
from skill_reporte import generar_reporte_artista

st.set_page_config(
    page_title="🎵 Asistente Musical",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Asistente Musical Inteligente")
st.markdown("Pregúntame sobre géneros, artistas, historia musical y más.")

# Sidebar con la Skill de reporte
with st.sidebar:
    st.header("🛠️ Herramientas")
    st.subheader("📄 Generar Reporte PDF")
    nombre_artista = st.text_input("Nombre del artista:")
    if st.button("Generar PDF"):
        if nombre_artista:
            with st.spinner("Generando reporte..."):
                archivo = generar_reporte_artista(nombre_artista)
            with open(archivo, "rb") as f:
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=f,
                    file_name=os.path.basename(archivo),
                    mime="application/pdf"
                )
            st.success(f"✅ Reporte de {nombre_artista} listo!")
        else:
            st.warning("Escribe el nombre del artista")

# Chat principal
if "historial" not in st.session_state:
    st.session_state.historial = []

pregunta = st.chat_input("Escribe tu pregunta sobre música...")

if pregunta:
    with st.spinner("🔍 Buscando y redactando respuesta..."):
        respuesta = consultar(pregunta)
    st.session_state.historial.append(("user", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)