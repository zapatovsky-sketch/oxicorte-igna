import streamlit as st

def apply_industrial_theme():
    """
    Inyecta CSS personalizado para transformar la interfaz de Streamlit 
    en un entorno de alto rendimiento industrial.
    """
    industrial_css = """
    <style>
        /* Fondo y tipografía principal */
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1A1A1A;
        }

        /* Estética de la barra lateral (Notebook View) */
        [data-testid="stSidebar"] {
            background-color: #F0F0F0;
            border-right: 1px solid #D1D1D1;
        }

        /* Títulos y Headers con look técnico */
        h1, h2, h3 {
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
            letter-spacing: -0.5px;
            font-weight: 700;
            color: #000000;
            border-left: 5px solid #FF4B4B; /* Acento de advertencia industrial */
            padding-left: 15px;
        }

        /* Contenedores de preguntas (Tarjetas) */
        div.stButton > button {
            border-radius: 0px;
            border: 2px solid #1A1A1A;
            background-color: white;
            color: #1A1A1A;
            font-family: 'JetBrains Mono', monospace;
            transition: 0.3s;
            width: 100%;
        }

        div.stButton > button:hover {
            background-color: #1A1A1A;
            color: white;
            border-color: #1A1A1A;
        }

        /* Bloques de LaTeX e Información */
        .stAlert {
            border-radius: 0px;
            border: 1px solid #D1D1D1;
            background-color: #FAFAFA;
        }

        /* Esconder menús innecesarios para el estudiante */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
    st.markdown(industrial_css, unsafe_allow_html=True)

def display_header(title, subtitle):
    """
    Renderiza un encabezado minimalista con metadatos del proyecto.
    """
    st.markdown(f"### {title}")
    st.caption(f"**Módulo:** {subtitle} | **Status:** High Performance Mode")
    st.divider()

def stats_tile(label, value):
    """
    Un indicador de progreso minimalista para el rendimiento de Ignacia.
    """
    st.markdown(
        f"""
        <div style="border: 1px solid #000; padding: 10px; background: #FFF;">
            <small style="text-transform: uppercase; color: #666;">{label}</small>
            <div style="font-size: 24px; font-weight: bold; font-family: 'JetBrains Mono';">{value}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )