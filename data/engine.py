import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def load_questions():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(
            spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"],
            worksheet="secretom",
            ttl=0
        )
        
        # 1. Limpieza de nombres de columnas (por si hay espacios invisibles)
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # 2. Diagnóstico temporal: ¿Qué está viendo pandas realmente?
        # st.write("Raw data shape:", df.shape) 
        
        # 3. Filtro optimizado: Solo eliminamos si TODA la fila está vacía
        df = df.dropna(how='all')
        
        # 4. Asegurar que el ID sea string
        if 'id' in df.columns:
            df['id'] = df['id'].astype(str)
            
        return df

    except Exception as e:
        st.error(f"Error en el Santuario: {e}")
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