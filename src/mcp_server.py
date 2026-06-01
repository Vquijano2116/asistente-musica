import requests
import json

def buscar_artista_musicbrainz(nombre: str) -> dict:
    """Skill MCP: busca información de artistas en MusicBrainz"""
    try:
        headers = {"User-Agent": "AsistenteMusical/1.0 (proyecto-universitario)"}
        
        # Buscar artista
        url = "https://musicbrainz.org/ws/2/artist/"
        params = {
            "query": nombre,
            "limit": 1,
            "fmt": "json"
        }
        respuesta = requests.get(url, params=params, headers=headers, timeout=10)
        
        if respuesta.status_code != 200:
            return {"error": "No se pudo conectar a MusicBrainz"}
        
        datos = respuesta.json()
        artistas = datos.get("artists", [])
        
        if not artistas:
            return {"error": f"No se encontró el artista '{nombre}'"}
        
        artista = artistas[0]
        return {
            "nombre": artista.get("name", nombre),
            "tipo": artista.get("type", "Desconocido"),
            "pais": artista.get("country", "Desconocido"),
            "inicio": artista.get("life-span", {}).get("begin", "Desconocido"),
            "generos": [t["name"] for t in artista.get("tags", [])[:5]],
            "fuente": "MusicBrainz API"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    resultado = buscar_artista_musicbrainz("Bad Bunny")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))