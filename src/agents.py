from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langgraph.graph import StateGraph, END
from typing import TypedDict

load_dotenv()

# Estado compartido entre agentes
class EstadoAsistente(TypedDict):
    pregunta: str
    documentos_recuperados: str
    respuesta_final: str

# Cargar vectorstore
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

# Agente 1: Buscador
def agente_buscador(estado: EstadoAsistente) -> EstadoAsistente:
    print("🔍 Agente Buscador: buscando información...")
    docs = vectorstore.similarity_search(estado["pregunta"], k=3)
    contexto = "\n\n".join([f"[Fuente: {doc.metadata.get('source', 'desconocida')}]\n{doc.page_content}" for doc in docs])
    return {"documentos_recuperados": contexto}

# Agente 2: Redactor
def agente_redactor(estado: EstadoAsistente) -> EstadoAsistente:
    print("✍️ Agente Redactor: generando respuesta...")
    prompt = f"""Eres un asistente experto en música. Usa el siguiente contexto para responder la pregunta.
Cita las fuentes que usaste al final de tu respuesta.

Contexto:
{estado["documentos_recuperados"]}

Pregunta: {estado["pregunta"]}

Respuesta:"""
    respuesta = llm.invoke(prompt)
    return {"respuesta_final": respuesta.content}

# Construir el grafo de agentes
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
    respuesta = consultar("¿Cuál es la historia del jazz?")
    print("\n🎵 Respuesta:\n", respuesta)