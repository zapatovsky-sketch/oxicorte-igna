import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def load_questions():
    try:
        # La librería buscará automáticamente 'service_account' en los secrets
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(
            spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"],
            worksheet="secretom", 
            ttl=0  # TTL 0 para pruebas iniciales y ver cambios en tiempo real
        )
        return df
    except Exception as e:
        st.error(f"Error de acceso privado: {e}")
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