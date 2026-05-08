import streamlit as st

def apply_industrial_theme():
    """
    Inyecta CSS personalizado para establecer la estética de ingeniería/industrial.
    """
    st.markdown("""
        <style>
        /* Fondo y tipografía general */
        .main {
            background-color: #0e1117;
            color: #e0e0e0;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* Contenedor de la pregunta */
        .question-box {
            padding: 25px;
            border-left: 5px solid #00ff41;
            background-color: #1a1c23;
            border-radius: 0px 10px 10px 0px;
            margin-bottom: 25px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
        }

        /* Estilo de los botones (Alternativas) */
        .stButton>button {
            width: 100%;
            border-radius: 0px;
            border: 1px solid #444;
            background-color: #161b22;
            color: #e0e0e0;
            font-family: 'Courier New', Courier, monospace;
            text-align: left;
            padding: 15px;
            transition: all 0.2s ease;
        }

        .stButton>button:hover {
            border: 1px solid #00ff41;
            color: #00ff41;
            background-color: #1f242d;
            transform: translateX(5px);
        }

        /* Títulos y Headers */
        h1, h2, h3 {
            color: #00ff41 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* Sidebar industrial */
        [data-testid="stSidebar"] {
            background-color: #0b0d11;
            border-right: 1px solid #333;
        }
        
        /* Stats tiles */
        .status-tile {
            padding: 10px;
            border: 1px solid #333;
            background-color: #101218;
            border-radius: 4px;
            text-align: center;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def display_header(title, subtitle):
    """
    Renderiza el encabezado principal del sistema.
    """
    st.title(f"⚡ {title}")
    st.markdown(f"**Módulo:** {subtitle} | **Status:** `High Performance Mode`")
    st.divider()

def stats_tile(label, value):
    """
    Muestra un indicador métrico con estilo industrial en la barra lateral.
    """
    st.markdown(f"""
        <div class="status-tile">
            <small style="color: #888;">{label.upper()}</small><br>
            <strong style="color: #00ff41; font-size: 1.2rem;">{value}</strong>
        </div>
    """, unsafe_allow_html=True)

def feedback_success():
    """
    Efecto visual/emoji para aciertos.
    """
    st.markdown("### 🎯 ¡OBJETIVO ALCANZADO!")
    st.toast("Progreso guardado en secretom", icon="💾")

def feedback_error():
    """
    Efecto visual para errores.
    """
    st.markdown("### ⚠️ DESVIACIÓN DETECTADA")
    st.toast("Revisión programada para re-calibración", icon="🔧")