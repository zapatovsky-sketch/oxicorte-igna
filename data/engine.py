import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def load_questions():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Ajustamos el nombre de la worksheet a 'Hoja 1' que es el estándar de Google
        df = conn.read(
            spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"],
            worksheet="secretom", # Si en tu Google Sheets le cambiaste el nombre a 'secretom', cámbialo aquí
            ttl=600
        )
        
        # Limpieza de nombres de columnas (quita espacios en blanco)
        df.columns = df.columns.str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error en el Santuario: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error de conexión al Santuario Digital: {e}")
        return pd.DataFrame()

def get_random_question(df, excludes=[]):
    """
    Selecciona una pregunta aleatoria que no esté en la lista de excluidas
    (Útil para el motor de repetición espaciada).
    """
    available_questions = df[~df['id'].isin(excludes)]
    if available_questions.empty:
        return None
    return available_questions.sample(n=1).iloc[0]