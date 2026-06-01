from fpdf import FPDF
from mcp_server import buscar_artista_musicbrainz
from datetime import datetime
import os

def generar_reporte_artista(nombre_artista: str) -> str:
    """Skill: genera un reporte PDF con información del artista"""
    
    info = buscar_artista_musicbrainz(nombre_artista)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 15, "Reporte Musical", ln=True, align="C")
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, f"Artista: {info.get('nombre', nombre_artista)}", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Informacion General", ln=True)
    pdf.set_draw_color(200, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 12)
    campos = [
        ("Nombre", info.get("nombre", "N/A")),
        ("Tipo", info.get("tipo", "N/A")),
        ("Pais de origen", info.get("pais", "N/A")),
        ("Inicio de carrera", info.get("inicio", "N/A")),
        ("Generos", ", ".join(info.get("generos", [])) or "N/A"),
        ("Fuente", info.get("fuente", "N/A")),
    ]
    
    for campo, valor in campos:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(55, 9, f"{campo}:", ln=False)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 9, valor, ln=True)

    os.makedirs("reportes", exist_ok=True)
    nombre_archivo = f"reportes/reporte_{nombre_artista.replace(' ', '_')}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo

if __name__ == "__main__":
    archivo = generar_reporte_artista("Bad Bunny")
    print(f"✅ Reporte generado: {archivo}")