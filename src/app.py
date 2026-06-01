import streamlit as st
from agents import consultar

st.set_page_config(
    page_title="🎵 Asistente Musical",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Asistente Musical Inteligente")
st.markdown("Pregúntame sobre géneros, artistas, historia musical y más.")

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