import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def load_questions():
    """
    Establece conexión con la Google Sheet privada usando la Service Account
    configurada en los Secrets.
    """
    try:
        # Inicializa la conexión. Streamlit busca automáticamente 
        # las credenciales bajo [connections.gsheets] en los secrets.
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Intentamos leer la pestaña 'secretom'
        # ttl=0 asegura que durante el desarrollo veas los cambios al instante
        df = conn.read(
            spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"],
            worksheet="secretom",
            ttl=0,
            usecols=['id', 'enunciado', 'alt_a', 'alt_b', 'alt_c', 'alt_d', 'alt_e', 'correcta']
        )
        
        if df is None or df.empty:
            st.error("La conexión tuvo éxito pero la hoja 'secretom' parece estar vacía.")
            return pd.DataFrame()

        # LIMPIEZA TÉCNICA:
        # 1. Quitamos espacios en los nombres de las columnas
        df.columns = df.columns.str.strip()
        # 2. Eliminamos filas que no tengan ID o Enunciado
        df = df.dropna(subset=['id', 'enunciado'])
        # 3. Aseguramos que el ID sea tratado como string o int limpio
        df['id'] = df['id'].astype(str)

        return df

    except Exception as e:
        # Si hay un error 400 o de permisos, se capturará aquí
        st.error("🛑 Error Crítico en el Santuario Digital")
        st.info(f"Detalle técnico: {e}")
        return pd.DataFrame()

def get_random_question(df, excludes=[]):
    """
    Selecciona una pregunta del banco de datos.
    """
    if df is None or df.empty:
        return None
        
    # Filtrar preguntas ya vistas si es necesario
    available = df[~df['id'].isin(excludes)]
    
    if available.empty:
        return None
        
    # Retorna una fila aleatoria como Serie de Pandas
    return available.sample(n=1).iloc[0]