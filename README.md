#  Asistente Musical Inteligente

Asistente conversacional especializado en música que integra RAG, multiagentes, MCP y Skills.

**Integrantes:** [Tu nombre] y [Nombre de tu pareja]  
**Curso:** Introducción a la Inteligencia Artificial – UTP 2026

##  Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Vquijano2116/asistente-musica.git
cd asistente-musica
```

2. Crea y activa el entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
copy .env.example .env
```

##  Uso

1. Primero indexa los documentos (solo la primera vez):
```bash
python src/ingest.py
```

2. Lanza la interfaz:
```bash
streamlit run src/app.py
```

##  Arquitectura

- **LLM:** Llama 3.1 8B via Groq API
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
- **Base vectorial:** ChromaDB
- **RAG:** LangChain con chunking y búsqueda por similitud
- **Multiagentes:** LangGraph (Agente Buscador + Agente Redactor)
- **MCP:** MusicBrainz API
- **Skill:** Generación de reportes PDF
- **Interfaz:** Streamlit

##  Estructura
```
asistente-musica/
├── src/
│   ├── ingest.py        # Pipeline RAG
│   ├── agents.py        # Multiagentes con LangGraph
│   ├── mcp_server.py    # MCP con MusicBrainz
│   ├── skill_reporte.py # Skill de reporte PDF
│   └── app.py           # Interfaz Streamlit
├── data/                # Corpus de 15 documentos
├── docs/                # Diagramas y documentación
├── tests/
├── .env.example
└── requirements.txt
``` 
