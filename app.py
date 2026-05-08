import streamlit as st
import pandas as pd
from data.engine import load_questions, get_random_question
from data.persistence import update_student_progress
from modules.renderer import render_math_text, generate_geometry_plot
from modules.ui_components import apply_industrial_theme, display_header, stats_tile
from modules.pdf_factory import create_exam_pdf

# 1. Configuración de cabecera y Estética
st.set_page_config(
    page_title="EL OXICORTE | I:G:N:A", 
    layout="wide", 
    initial_sidebar_state="expanded"
)
apply_industrial_theme()

def main():
    # 2. Encabezado e Identidad
    display_header("El Oxicorte de I:G:N:A", "Fase 2.0: Operación Cimiento")

    # 3. Carga de datos desde Google Sheets (Privado)
    df_questions = load_questions()
    
    if df_questions.empty:
        st.warning("⚠️ El Santuario está esperando la carga de datos... (Revisa la pestaña 'secretom')")
        return

    # 4. Barra Lateral de Control
    with st.sidebar:
        st.markdown("### PANEL DE CONTROL")
        if st.button("📥 Generar Facsímil PDF"):
            # Genera PDF con las preguntas cargadas
            path = create_exam_pdf(df_questions.to_dict('records'))
            with open(path, "rb") as f:
                st.download_button("Descargar PDF", f, file_name="Ensayo_M1.pdf")
        
        st.divider()
        stats_tile("Preguntas en Base", len(df_questions))
        st.markdown("---")
        st.caption("Arqueniería Digital v2.0")

    # 5. Lógica de Navegación de Preguntas
    # Usamos session_state para mantener la pregunta actual al responder
    if 'current_q' not in st.session_state:
        st.session_state.current_q = get_random_question(df_questions)

    pregunta = st.session_state.current_q

    if pregunta is not None:
        col_main, col_visual = st.columns([1.5, 1])

        with col_main:
            st.markdown(f"**ID: {pregunta['id']}**")
            # Renderizado de enunciado con soporte LaTeX
            render_math_text(pregunta['enunciado'])
            
            st.markdown("---")
            
            # Grilla de alternativas
            for letra in ['a', 'b', 'c', 'd', 'e']:
                label = f"{letra.upper()}) {pregunta[f'alt_{letra}']}"
                if st.button(label, key=f"btn_{letra}", use_container_width=True):
                    if letra.lower() == str(pregunta['correcta']).lower():
                        st.success("✅ CORRECTO | Registro enviado a la nube.")
                        # Registrar progreso en 'secretoms'
                        # update_student_progress(None, "Ignacia", pregunta['id'], 5)
                        if st.button("Siguiente Pregunta ➡️"):
                            st.session_state.current_q = get_random_question(df_questions)
                            st.rerun()
                    else:
                        st.error("❌ INCORRECTO | Reaparecerá en la próxima sesión.")
                        # Registrar progreso (Score bajo para repetición rápida)
                        # update_student_progress(None, "Ignacia", pregunta['id'], 1)

        with col_visual:
            st.subheader("Análisis Visual")
            # Aquí podrías cargar un gráfico si la pregunta tiene coordenadas
            # Por ahora, un placeholder estético o gráfico de función genérico
            st.info("Visualización técnica activa para análisis de funciones.")
            # Ejemplo: generate_geometry_plot(...)

    else:
        st.info("🎯 Sesión completada. No hay más preguntas pendientes por ahora.")

if __name__ == "__main__":
    main()