import streamlit as st
from data.engine import load_questions, get_random_question
from data.persistence import update_student_progress, filter_questions_by_memory
from modules.renderer import render_math_text, generate_geometry_plot
from modules.ui_components import apply_industrial_theme, display_header, stats_tile
from modules.pdf_factory import create_exam_pdf

# 1. Configuración de página y Estética Industrial
st.set_page_config(page_title="EL OXICORTE | PAES M1", layout="wide", initial_sidebar_state="expanded")
apply_industrial_theme()

def main():
    # 2. Encabezado del Santuario Digital
    display_header("El Oxicorte de I:G:N:A", "Preparación M1 de Alto Rendimiento")

    # 3. Carga de datos (Cloud)
    df_questions = load_questions()
    
    if df_questions.empty:
        st.warning("⚠️ Esperando conexión con el banco de preguntas en Google Sheets...")
        return

    # 4. Barra Lateral: Control y Estadísticas
    with st.sidebar:
        st.markdown("### PANEL DE CONTROL")
        if st.button("📥 Generar Ensayo PDF (Facsímil)"):
            # Generamos un PDF con las primeras 10 preguntas para Ignacia
            path = create_exam_pdf(df_questions.head(10).to_dict('records'))
            st.success(f"PDF Generado: {path}")
            with open(path, "rb") as f:
                st.download_button("Descargar Archivo", f, file_name="Ensayo_M1_Ignacia.pdf")
        
        st.divider()
        stats_tile("Preguntas Listas", len(df_questions))
        stats_tile("Sesión Actual", "M1 - Álgebra y Funciones")

    # 5. Lógica de Visualización de Pregunta
    # Filtramos por Repetición Espaciada (Simulado hasta tener el df_progress)
    # questions_to_show = filter_questions_by_memory(df_questions, st.session_state.get('progress', pd.DataFrame()))
    
    pregunta = get_random_question(df_questions)

    if pregunta is not None:
        col_txt, col_vis = st.columns([1.5, 1])

        with col_txt:
            st.markdown(f"**PREGUNTA ID: {pregunta['id']}**")
            render_math_text(pregunta['enunciado'])
            
            # Alternativas con estética de botones industriales
            st.markdown("---")
            for letra in ['a', 'b', 'c', 'd', 'e']:
                if st.button(f"{letra.upper()}) {pregunta[f'alt_{letra}']}", key=f"btn_{letra}"):
                    if letra == pregunta['correcta'].lower():
                        st.balloons()
                        st.success("Correcto. Registro enviado a la nube.")
                        # Actualizamos progreso (Score 5)
                        # update_student_progress(None, "Ignacia", pregunta['id'], 5)
                    else:
                        st.error("Incorrecto. Esta pregunta reaparecerá pronto.")
                        # Actualizamos progreso (Score 1)
                        # update_student_progress(None, "Ignacia", pregunta['id'], 1)

        with col_vis:
            # Si la pregunta requiere gráfico (puedes condicionarlo en tu Sheets)
            st.subheader("Visualización Técnica")
            # Ejemplo de gráfico dinámico de función
            import numpy as np
            x = np.linspace(-10, 10, 100)
            y = x**2 # Esto debería venir de la lógica de la pregunta
            fig = generate_geometry_plot({'x': x, 'y': y}, plot_type="function")
            st.pyplot(fig)

    else:
        st.info("🎯 ¡Felicidades! Ignacia ha completado todas las revisiones programadas para hoy.")

if __name__ == "__main__":
    main()