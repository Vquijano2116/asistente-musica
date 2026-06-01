import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def ingestar_documentos():
    print(" Cargando documentos...")
    loader = DirectoryLoader(
        "data/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documentos = loader.load()
    print(f" {len(documentos)} documentos cargados")

    print(" Dividiendo en chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documentos)
    print(f" {len(chunks)} chunks creados")

    print(" Generando embeddings y guardando en ChromaDB...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="data/chroma_db"
    )
    print(" Base vectorial lista en data/chroma_db/")

if __name__ == "__main__":
    ingestar_documentos()