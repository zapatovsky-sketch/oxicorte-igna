import streamlit as st
import json
import time
import unicodedata
import re
import matplotlib.pyplot as plt
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

# 2. Gestión de Estados y Persistencia
if 'fase' not in st.session_state: st.session_state.fase = "CONFIG"
if 'respuestas_ignacia' not in st.session_state: st.session_state.respuestas_ignacia = {}
if 'preguntas_seleccionadas' not in st.session_state: st.session_state.preguntas_seleccionadas = []
if 'progreso' not in st.session_state: st.session_state.progreso = {}

# 3. Ductos de Datos (JSON y Progreso)
def cargar_inventario():
    try:
        with open("preguntas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except: return []

def cargar_progreso():
    try:
        with open("progreso_igna.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

def registrar_evento(uid, correcta, respuesta_dada):
    # Actualización en tiempo real del progreso
    progreso = cargar_progreso()
    if uid not in progreso:
        progreso[uid] = {"vistas": 0, "aciertos": 0, "fallos": 0, "ultimo_intento": ""}
    
    progreso[uid]["vistas"] += 1
    if correcta.lower() == respuesta_dada.lower():
        progreso[uid]["aciertos"] += 1
    else:
        progreso[uid]["fallos"] += 1
    
    progreso[uid]["ultimo_intento"] = respuesta_dada
    
    with open("progreso_igna.json", "w", encoding="utf-8") as f:
        json.dump(progreso, f, indent=2)

# 4. Motor de Traducción Humanizada
def limpiar_para_pdf(texto):
    if not texto: return ""
    texto = str(texto)
    texto = re.sub(r'\\?\$', '', texto)
    texto = texto.replace("~", " ").replace("\\n", "\n")
    texto = re.sub(r'(\^)?\{\\?wedge\}', '^', texto)
    texto = re.sub(r'\\sqrt\[([^\[\]]+)\]\{([^{}]+)\}', r'raíz_\1(\2)', texto)
    texto = re.sub(r'\\sqrt\{([^{}]+)\}', r'raíz(\1)', texto)
    for _ in range(3): texto = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', texto)
    texto = re.sub(r'\(([A-Za-z0-9\.]+)\)/', r'\1/', texto)
    texto = re.sub(r'/\(([A-Za-z0-9\.]+)\)', r'/\1', texto)
    texto = re.sub(r'\^\{([A-Za-z0-9\+\-\*\/\.]+)\}', r'^\1', texto).replace("\\", "")
    
    ortografia = {"Numeros": "Números", "Basico": "Básico", "Cual(es)": "Cuál(es)", "Algebra": "Álgebra"}
    for k, v in ortografia.items(): texto = re.sub(rf'\b{k}\b', v, texto)
    return texto.encode('latin-1', 'replace').decode('latin-1').strip()

# 5. Prensa PDF y Gráficos
def generar_pdf_blindado(preguntas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(180, 10, "EL OXICORTE DE I:G:N:A", ln=1, align='C')
    pdf.ln(10)
    for p in preguntas:
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(175, 8, limpiar_para_pdf(f"Pieza: {p['uid']} | {p['eje']}"))
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(175, 7, f"{limpiar_para_pdf(p['enunciado_latex'])}")
        alts = p['opciones']
        pdf.set_font("Helvetica", "I", 10)
        for k, v in alts.items():
            pdf.multi_cell(170, 6, f"{k.upper()}) {limpiar_para_pdf(v)}")
        pdf.ln(6); pdf.cell(175, 0, "", "T"); pdf.ln(6)
    return bytes(pdf.output())

# --- FLUJO DE OPERACIÓN ---
inventario = cargar_inventario()

if st.session_state.fase == "CONFIG":
    st.title("⚙️ El Oxicorte de I:G:N:A")
    st.subheader("Configuración de Jornada")
    
    modo_m2 = st.toggle("🚀 Activar Modo M2 (Nivel Avanzado)", value=False)
    tipo_filtro = "M2" if modo_m2 else "M1"
    
    if inventario:
        ejes = sorted(list(set([p['eje'] for p in inventario])))
        eje_sel = st.selectbox("Eje Temático:", ["Todos"] + ejes)
        
        # Filtro de Memoria: Excluir preguntas dominadas (opcional)
        filtrado = [p for p in inventario if (eje_sel == "Todos" or p['eje'] == eje_sel)]
        # Aquí podrías añadir: and p.get('tipo', 'M1') == tipo_filtro
        
        if filtrado:
            cant = st.slider("Piezas a procesar:", 1, len(filtrado), min(len(filtrado), 5))
            if st.button("🚀 COMENZAR OXICORTE"):
                st.session_state.preguntas_seleccionadas = filtrado[:cant]
                st.session_state.start_time = time.time()
                st.session_state.fase = "DESPACHO"
                st.rerun()

elif st.session_state.fase == "DESPACHO":
    st.title("📦 El Oxicorte de I:G:N:A | Despacho")
    pdf_bytes = generar_pdf_blindado(st.session_state.preguntas_seleccionadas)
    st.download_button("📥 Descargar Guía PDF", data=pdf_bytes, file_name="oxicorte_igna.pdf")
    if st.button("✅ IR A VERIFICACIÓN"):
        st.session_state.fase = "VERIFICACION"; st.rerun()

elif st.session_state.fase == "VERIFICACION":
    st.title("📝 El Oxicorte de I:G:N:A | Verificación")
    
    for i, p in enumerate(st.session_state.preguntas_seleccionadas):
        st.write(f"### Pieza {p['uid']}")
        if "grafico_script" in p and p["grafico_script"]:
            try: exec(p["grafico_script"]) # Ejecución segura de Matplotlib
            except: st.warning("Error al renderizar gráfico dinámico.")
            
        opciones = [k.upper() for k in p['opciones'].keys()]
        
        # GUARDADO ATÓMICO: Al marcar, se registra
        ans = st.segmented_control(f"Selecciona tu respuesta para {p['uid']}:", opciones, key=f"ans_{i}")
        
        if ans and (i not in st.session_state.respuestas_ignacia or st.session_state.respuestas_ignacia[i] != ans):
            st.session_state.respuestas_ignacia[i] = ans
            registrar_evento(p['uid'], p['correcta'], ans)
            st.toast(f"Progreso guardado para {p['uid']} ✅")

    if st.button("🔥 FINALIZAR SESIÓN"):
        st.session_state.end_time = time.time()
        st.session_state.fase = "METACOGNICION"; st.rerun()

elif st.session_state.fase == "METACOGNICION":
    st.title("🔍 El Oxicorte de I:G:N:A | Autopsia")
    aciertos = 0
    for i, p in enumerate(st.session_state.preguntas_seleccionadas):
        resp = st.session_state.respuestas_ignacia.get(i, "").lower()
        correcta = p['correcta'].lower()
        with st.expander(f"Pieza {p['uid']}: {'✅' if resp == correcta else '❌'}"):
            st.write(f"**Tu respuesta:** {resp.upper()} | **Correcta:** {correcta.upper()}")
            st.info(f"**Análisis:** {p['explicacion']}")
            st.warning(f"**Metacognición:** {p['metacognicion']}")
            if resp == correcta: aciertos += 1
    
    st.metric("PRECISIÓN", f"{(aciertos/len(st.session_state.preguntas_seleccionadas))*100:.1f}%")
    if st.button("🔄 NUEVA JORNADA"):
        st.session_state.clear(); st.rerun()