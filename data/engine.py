import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def load_questions():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Esto nos dirá qué hojas ve la cuenta de servicio
        # Puedes imprimirlo en pantalla con st.write(conn.client.open_by_url(...).worksheets())
        df = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"])
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

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