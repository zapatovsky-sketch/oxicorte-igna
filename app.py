import streamlit as st
import json
import time
import unicodedata
import re
from fpdf import FPDF

# 1. Identidad y Estética Industrial
st.set_page_config(page_title="El Oxicorte de I:G:N:A", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1, h2, h3 { color: #FF4B2B !important; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button { background-color: #FF4B2B; color: white; border-radius: 0px; font-weight: bold; width: 100%; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border: 1px solid #FF4B2B; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Gestión de Estados
if 'fase' not in st.session_state: st.session_state.fase = "CONFIG"
if 'respuestas_ignacia' not in st.session_state: st.session_state.respuestas_ignacia = {}
if 'preguntas_seleccionadas' not in st.session_state: st.session_state.preguntas_seleccionadas = []

# 3. Ducto de Suministro JSON
def cargar_inventario():
    try:
        with open("preguntas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error en el suministro: {e}")
        return []

# 4. Protocolo de Traducción Humanizada Definitiva (Fuerza Bruta Regex)
def limpiar_para_pdf(texto):
    if not texto: return ""
    texto = str(texto)
    
    # FASE 1: Purga Agresiva de Delimitadores y Basura de Espaciado
    texto = re.sub(r'\\?\$', '', texto) # Aniquila dólares ($ y \$)
    texto = texto.replace("~", " ")     # Aniquila virgulillas
    texto = texto.replace("\\n", "\n")
    
    # FASE 2: Traducción Natural de Potencias y Raíces
    texto = re.sub(r'(\^)?\{\\?wedge\}', '^', texto) # Caza ^{\wedge} y variantes
    texto = texto.replace("^{\\wedge}", "^").replace("^{\wedge}", "^")
    texto = texto.replace("\\wedge", "^")
    texto = texto.replace("^{*}", "*")
    
    texto = re.sub(r'\\sqrt\[([^\[\]]+)\]\{([^{}]+)\}', r'raíz_\1(\2)', texto)
    texto = re.sub(r'\\sqrt\{([^{}]+)\}', r'raíz(\1)', texto)
    texto = texto.replace("\\sqrt", "raíz").replace("root", "raíz").replace("raiz", "raíz")
    
    # FASE 3: Lógica Inteligente de Fracciones
    for _ in range(3):
        texto = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', texto)
    texto = texto.replace("\\frac", "")
    
    # Libera paréntesis si el contenido es un número (incluso con puntos) o una variable simple
    texto = re.sub(r'\(([A-Za-z0-9\.]+)\)/', r'\1/', texto)
    texto = re.sub(r'/\(([A-Za-z0-9\.]+)\)', r'/\1', texto)
    
    # FASE 4: Exponentes y Subíndices limpios
    texto = re.sub(r'\^\{([A-Za-z0-9\+\-\*\/\.]+)\}', r'^\1', texto)
    texto = re.sub(r'\_\{([A-Za-z0-9\+\-\*\/\.]+)\}', r'_\1', texto)
    texto = re.sub(r'log\_\s*\\?\_?\(([^()]+)\)', r'log_(\1)', texto)
    
    # FASE 5: Homologación de Signos PAES
    reemplazos_math = {
        "\\cdot": " * ", "\\times": " x ", "\\pi": "pi",
        "\\le": " <= ", "\\ge": " >= ", "\\neq": " != ", "\\approx": " aprox ",
        "\\log_": "log_", "\\log": "log", "\\{": "{", "\\}": "}"
    }
    for k, v in reemplazos_math.items():
        texto = texto.replace(k, v)
        
    texto = texto.replace("{", "(").replace("}", ")")
    texto = texto.replace("\\", "")
    
    # FASE 6: INYECCIÓN DE ORTOGRAFÍA PAES
    ortografia = {
        "Numeros": "Números", "Basico": "Básico", "Cual(es)": "Cuál(es)",
        "¿Cual": "¿Cuál", "numero": "número", "erroneamente": "erróneamente",
        "Cuantos": "Cuántos", "¿Cuantos": "¿Cuántos", "Geometria": "Geometría",
        "Algebra": "Álgebra", "Intermedio": "Intermedio", "Avanzado": "Avanzado"
    }
    for k, v in ortografia.items():
        texto = re.sub(rf'\b{k}\b', v, texto)
        
    texto = re.sub(r' +', ' ', texto) # Limpia espacios dobles accidentales
    
    # Codificación de alta fidelidad
    return texto.encode('latin-1', 'replace').decode('latin-1').strip()

# 5. Prensa PDF (Diseño Pedagógico)
def generar_pdf_blindado(preguntas):
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(180, 10, "GUIA DE TRABAJO - EL OXICORTE DE I:G:N:A", ln=1, align='C')
        pdf.ln(10)
        
        margin_x, safe_width = 15, 175
        for p in preguntas:
            pdf.set_x(margin_x)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(safe_width, 8, limpiar_para_pdf(f"Pieza: {p['uid']} | Eje: {p['eje']} | Nivel: {p['dificultad']}"))
            
            pdf.set_x(margin_x)
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(safe_width, 7, f"{limpiar_para_pdf(p['enunciado_latex'])}")
            pdf.ln(3)
            
            alts = p['opciones']
            pdf.set_font("Helvetica", "I", 10)
            for k, v in alts.items():
                pdf.set_x(margin_x + 5)
                pdf.multi_cell(safe_width - 5, 6, f"{k.upper()}) {limpiar_para_pdf(v)}")
            
            pdf.ln(6); pdf.set_x(margin_x); pdf.cell(safe_width, 0, "", "T"); pdf.ln(6)
            
        return bytes(pdf.output())
    except Exception as e:
        return bytes(f"Error en prensa: {str(e)}", 'utf-8')

# --- FLUJO DE OPERACIÓN ---
inventario = cargar_inventario()

if st.session_state.fase == "CONFIG":
    st.title("⚙️ El Oxicorte de I:G:N:A | Configuración")
    
    if inventario:
        ejes = sorted(list(set([p['eje'] for p in inventario])))
        dificultades = sorted(list(set([p['dificultad'] for p in inventario])))
        
        c1, c2 = st.columns(2)
        eje_sel = c1.selectbox("Eje Temático:", ["Todos"] + ejes)
        dif_sel = c2.selectbox("Nivel de Dificultad:", ["Todos"] + dificultades)
        
        filtrado = [p for p in inventario if 
                    (eje_sel == "Todos" or p['eje'] == eje_sel) and 
                    (dif_sel == "Todos" or p['dificultad'] == dif_sel)]
        
        if filtrado:
            if len(filtrado) > 1:
                cant = st.slider("Piezas a procesar:", 1, len(filtrado), min(len(filtrado), 5))
            else:
                st.info("Solo hay 1 pieza disponible con este calibre.")
                cant = 1
                
            if st.button("🚀 COMENZAR OXICORTE"):
                st.session_state.preguntas_seleccionadas = filtrado[:cant]
                st.session_state.start_time = time.time()
                st.session_state.fase = "DESPACHO"
                st.rerun()
        else:
            st.warning("No hay material con esos filtros. Ajusta el soplete.")
    else:
        st.warning("No hay material cargado en 'preguntas.json'.")

elif st.session_state.fase == "DESPACHO":
    st.title("📦 El Oxicorte de I:G:N:A | Despacho Offline")
    pdf_bytes = generar_pdf_blindado(st.session_state.preguntas_seleccionadas)
    st.download_button("📥 Descargar Guía PDF", data=pdf_bytes, file_name="oxicorte_igna.pdf")
    if st.button("✅ IR A VERIFICACIÓN"):
        st.session_state.fase = "VERIFICACION"
        st.rerun()

elif st.session_state.fase == "VERIFICACION":
    st.title("📝 El Oxicorte de I:G:N:A | Grilla de Respuestas")
    for i, p in enumerate(st.session_state.preguntas_seleccionadas):
        opciones_teclas = [k.upper() for k in p['opciones'].keys()]
        st.session_state.respuestas_ignacia[i] = st.segmented_control(
            f"Pieza {p['uid']}", opciones_teclas, key=f"ans_{i}"
        )
    if st.button("🔥 REVELAR RESULTADOS"):
        st.session_state.end_time = time.time()
        st.session_state.fase = "METACOGNICION"
        st.rerun()

elif st.session_state.fase == "METACOGNICION":
    st.title("🔍 El Oxicorte de I:G:N:A | Autopsia del Error")
    aciertos = 0
    for i, p in enumerate(st.session_state.preguntas_seleccionadas):
        resp = st.session_state.respuestas_ignacia.get(i, "")
        resp = resp.lower() if resp else ""
        correcta = p['correcta'].lower()
        
        with st.expander(f"Pieza {p['uid']}: {'✅' if resp == correcta else '❌'}"):
            st.write(f"**Tu respuesta:** {resp.upper() if resp else 'N/A'} | **Correcta:** {correcta.upper()}")
            st.info(f"**Análisis Oficial:** {p['explicacion']}")
            st.warning(f"**Metacognición:** {p['metacognicion']}")
            if resp == correcta: aciertos += 1
    
    t_total = (st.session_state.end_time - st.session_state.start_time) / 60
    st.metric("PRECISIÓN", f"{(aciertos/len(st.session_state.preguntas_seleccionadas))*100:.1f}%")
    st.metric("TIEMPO TOTAL", f"{t_total:.1f} min")
    
    if st.button("🔄 NUEVA JORNADA"):
        st.session_state.clear()
        st.rerun()
