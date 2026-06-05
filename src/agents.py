import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langgraph.graph import StateGraph, END
from typing import TypedDict
from mcp_server import buscar_artista_musicbrainz

load_dotenv()

class EstadoAsistente(TypedDict):
    pregunta: str
    documentos_recuperados: str
    info_externa: str
    respuesta_final: str

def cargar_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings
    )

vectorstore = cargar_vectorstore()
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

# Agente 1: Buscador (RAG + MCP)
def agente_buscador(estado: EstadoAsistente) -> EstadoAsistente:
    print("🔍 Agente Buscador: buscando en corpus local...")
    docs = vectorstore.similarity_search(estado["pregunta"], k=3)
    contexto = "\n\n".join([f"[Fuente: {doc.metadata.get('source', 'desconocida')}]\n{doc.page_content}" for doc in docs])

    # Intentar enriquecer con MusicBrainz
    palabras = estado["pregunta"].split()
    info_externa = ""
    for i in range(len(palabras)):
        for j in range(i+1, min(i+4, len(palabras)+1)):
            termino = " ".join(palabras[i:j])
            if len(termino) > 4:
                resultado = buscar_artista_musicbrainz(termino)
                if "nombre" in resultado:
                    info_externa = f"[MusicBrainz] Artista: {resultado['nombre']}, País: {resultado['pais']}, Inicio: {resultado['inicio']}, Géneros: {', '.join(resultado['generos'])}"
                    print(f" MCP encontró: {resultado['nombre']}")
                    break
        if info_externa:
            break

    return {
        "documentos_recuperados": contexto,
        "info_externa": info_externa
    }

# Agente 2: Redactor
def agente_redactor(estado: EstadoAsistente) -> EstadoAsistente:
    print(" Agente Redactor: generando respuesta...")
    contexto_completo = estado["documentos_recuperados"]
    if estado.get("info_externa"):
        contexto_completo += f"\n\nInformación adicional de MusicBrainz:\n{estado['info_externa']}"

    prompt = f"""Eres un asistente experto en música. Usa el siguiente contexto para responder la pregunta.
Cita las fuentes que usaste al final de tu respuesta.

Contexto:
{contexto_completo}

Pregunta: {estado["pregunta"]}

Respuesta:"""
    respuesta = llm.invoke(prompt)
    return {"respuesta_final": respuesta.content}

def construir_grafo():
    grafo = StateGraph(EstadoAsistente)
    grafo.add_node("buscador", agente_buscador)
    grafo.add_node("redactor", agente_redactor)
    grafo.set_entry_point("buscador")
    grafo.add_edge("buscador", "redactor")
    grafo.add_edge("redactor", END)
    return grafo.compile()

app_grafo = construir_grafo()

def consultar(pregunta: str) -> str:
    resultado = app_grafo.invoke({"pregunta": pregunta})
    return resultado["respuesta_final"]

if __name__ == "__main__":
    respuesta = consultar("¿Quién es Bad Bunny?")
    print("\n Respuesta:\n", respuesta)