from fpdf import FPDF
import datetime

class FacsimilPDF(FPDF):
    def header(self):
        # Estética Industrial: Línea superior y metadatos
        self.set_font("Courier", "B", 10)
        self.cell(0, 10, "PROYECTO: EL OXICORTE DE I:G:N:A // CONTROL PAES M1", ln=True, align="L")
        self.set_draw_color(0, 0, 0)
        self.line(10, 20, 200, 20)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cell(0, 10, f"Generado en Santuario Digital - {fecha} - Pág {self.page_no()}", align="C")

def create_exam_pdf(questions_list, output_path="ensayo_ignacia.pdf"):
    """
    Toma una lista de preguntas (dict) y genera el archivo PDF.
    """
    pdf = FacsimilPDF()
    pdf.add_page()
    
    # IMPORTANTE: Para soporte total de símbolos, se recomienda cargar una fuente externa
    # pdf.add_font('Roboto', '', 'fonts/Roboto-Regular.ttf', uni=True)
    
    pdf.set_font("Arial", size=11)
    
    for i, q in enumerate(questions_list, 1):
        # Número de pregunta y enunciado
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 7, f"Pregunta {i}:")
        
        pdf.set_font("Arial", "", 11)
        # Limpiamos el LaTeX para el PDF (fpdf no renderiza LaTeX nativo, 
        # por lo que aquí se recomienda usar texto plano o exportar el render de Matplotlib)
        enunciado_limpio = q['enunciado'].replace('$', '') 
        pdf.multi_cell(0, 7, enunciado_limpio)
        
        # Alternativas
        pdf.ln(2)
        for letra in ['a', 'b', 'c', 'd', 'e']:
            opcion = f"{letra.upper()}) {q[f'alt_{letra}']}".replace('$', '')
            pdf.cell(0, 7, f"    {opcion}", ln=True)
        
        pdf.ln(10) # Espaciado entre preguntas
        
        # Si la página está por terminar, saltamos
        if pdf.get_y() > 250:
            pdf.add_page()

    pdf.output(output_path)
    return output_path