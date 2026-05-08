import streamlit as st

def apply_industrial_theme():
    st.markdown("""
        <style>
        /* Estética de Laboratorio de Destinos / Santuario Digital */
        .main {
            background-color: #0e1117;
            color: #e0e0e0;
            font-family: 'Courier New', Courier, monospace;
        }
        .stButton>button {
            width: 100%;
            border-radius: 0px;
            border: 1px solid #444;
            background-color: #1a1c23;
            color: #00ff41; /* Verde Matrix/Terminal */
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #00ff41;
            color: #000;
            border: 1px solid #00ff41;
        }
        .question-box {
            padding: 20px;
            border-left: 4px solid #00ff41;
            background-color: #161b22;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def display_question_card(pregunta):
    with st.container():
        st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
        st.subheader(f"PREGUNTA {pregunta['id']}")
        st.markdown(f"### {pregunta['enunciado']}")
        st.markdown('</div>', unsafe_allow_html=True)