# Decisiones Técnicas

## 1. LLM: Groq + Llama 3.1 8B
**Contexto:** Se necesitaba un LLM gratuito y rápido para el prototipo.  
**Decisión:** Usar Groq API con llama-3.1-8b-instant.  
**Consecuencias:** Respuestas en menos de 2 segundos, sin costo, con límite de tokens por minuto.

## 2. Base vectorial: ChromaDB
**Contexto:** Se requería almacenar embeddings del corpus de 15 documentos localmente.  
**Decisión:** Usar ChromaDB por su simplicidad y persistencia en disco.  
**Consecuencias:** Setup en una sola línea, sin servidor externo, ideal para prototipos.

## 3. Embeddings: sentence-transformers/all-MiniLM-L6-v2
**Contexto:** Se necesitaba un modelo de embeddings gratuito y local.  
**Decisión:** Usar all-MiniLM-L6-v2 por su balance entre velocidad y calidad.  
**Consecuencias:** Modelo liviano (80MB), buena recuperación semántica en español e inglés.