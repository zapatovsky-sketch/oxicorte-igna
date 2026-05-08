import streamlit as st
import json
import time
import unicodedata
import re
import matplotlib.pyplot as plt
from fpdf import FPDF

# 1. Identidad de la Obra
st.set_page_config(page_title="El Oxicorte de I:G:N:A", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1, h2, h3 { color: #FF4B2B !important; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button { background-color: #FF4B2B; color: white; border-radius: 5px; font-weight: bold; width: 100%; }
    .stExpander { background-color: #1E1E1E; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. Gestión de Estados
if 'fase' not in st.session_state: st.session_state.fase = "CONFIG"
if 'respuestas_ignacia' not in st.session_state: st.session_state.respuestas_ignacia = {}
if 'preguntas_seleccionadas' not in st.session_state: st.session_state.preguntas_seleccionadas = []

# 3. Ductos de Datos (Lectura)
def cargar_inventario():
    try:
        with open("preguntas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except: return []

# 4. Motor de Limpieza (Blindaje para PDF)
def limpiar_para_pdf(texto):
    if not texto: return ""
    texto = str(texto)
    # Purga de basura de código
    texto = re.sub(r'\\?\$', '', texto)
    texto = texto.replace("~", " ").replace("\\n", " ").replace("\n", " ")
    texto = re.sub(r'(\^)?\{\\?wedge\}', '^', texto)
    # Traducción simplificada
    texto = texto.replace("\\frac", "").replace("{", "(").replace("}", ")").replace("\\", "")
    # Codificación básica para evitar caídas
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('ascii')
    return texto.strip()

# 5. Prensa PDF (Reconstrucción desde cero)
def generar_pdf_fiel(preguntas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EL OXICORTE DE I:G:N:A", ln=1, align='C')
    pdf.ln(10)
    
    for p in preguntas:
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 8, f"PIEZA: {p['uid']} | {p['eje']}")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, limpiar_para_pdf(p['enunciado_latex']))
        pdf.ln(2)
        # Listado vertical de alternativas
        for k, v in p['opciones'].items():
            pdf.set_x(20)
            pdf.cell(0, 6, f"{k.upper()}) {limpiar_para_pdf(v)}", ln=1)
        pdf.ln(5); pdf.cell(0, 0, "", "T"); pdf.ln(5)
    return bytes(pdf.output())

# --- FLUJO DE OPERACIÓN ---
inventario = cargar_inventario()

if st.session_state.fase == "CONFIG":
    st.title("⚙️ El Oxicorte de I:G:N:A")
    st.subheader("Configuración de Jornada")
    
    col1, col2 = st.columns(2)
    with col1:
        ejes = sorted(list(set([p['eje'] for p in inventario])))
        eje_sel = st.selectbox("Eje Temático:", ["Todos"] + ejes)
    with col2:
        modo_m2 = st.toggle("Activar Modo M2", value=False)
    
    filtrado = [p for p in inventario if (eje_sel == "Todos" or p['eje'] == eje_sel)]
    
    if filtrado:
        cant = st.slider("Piezas a procesar:", 1, len(filtrado), min(len(filtrado), 5))
        if st.button("🚀 COMENZAR OXICORTE"):
            st.session_state.preguntas_seleccionadas = filtrado[:cant]
            st.session_state.fase = "VERIFICACION" # Salto directo para agilizar
            st.rerun()

elif st.session_state.fase == "VERIFICACION":
    st.title("📝 Grilla de Respuestas")
    
    # Barra lateral para el PDF (Separación de preocupaciones)
    with st.sidebar:
        st.header("Herramientas")
        pdf_bytes = generar_pdf_fiel(st.session_state.preguntas_seleccionadas)
        st.download_button("📥 Descargar Guía PDF", data=pdf_bytes, file_name="oxicorte_igna.pdf")
        if st.button("🏁 Finalizar y Evaluar"):
            st.session_state.fase = "METACOGNICION"; st.rerun()

    # Grilla Principal
    for i, p in enumerate(st.session_state.preguntas_seleccionadas):
        with st.container(border=True):
            c_text, c_graph = st.columns([2, 1])
            with c_text:
                st.write(f"**P{p['uid']}**")
                st.write(p['enunciado_latex'])
                # Mostrar alternativas
                for k, v in p['opciones'].items():
                    st.write(f"*{k.upper()})* {v}")
            
            with c_graph:
                if "grafico_script" in p and p["grafico_script"]:
                    try: exec(p["grafico_script"])
                    except: st.caption("Gráfico no disponible")

            # Control de respuesta al final del contenedor
            opciones = [k.upper() for k in p['opciones'].keys()]
            st.segmented_control("Tu respuesta:", opciones, key=f"ans_{i}")

elif st.session_state.fase == "METACOGNICION":
    st.title("🔍 Autopsia del Error")
    aciertos = 0
    total = len(st.session_state.preguntas_seleccionadas)
    
    for i, p in enumerate(st.session_state.preguntas_seleccionadas):
        resp = st.session_state.get(f"ans_{i}", "").lower()
        correcta = p['correcta'].lower()
        
        with st.expander(f"Pieza {p['uid']}: {'✅' if resp == correcta else '❌'}"):
            st.write(f"**Tu respuesta:** {resp.upper()} | **Correcta:** {correcta.upper()}")
            st.info(f"**Análisis:** {p['explicacion']}")
            if resp == correcta: aciertos += 1
            
    st.divider()
    st.metric("PRECISIÓN", f"{(aciertos/total)*100:.1f}%")
    if st.button("🔄 NUEVA JORNADA"):
        st.session_state.clear(); st.rerun()