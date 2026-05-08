import matplotlib.pyplot as plt
import streamlit as st

def set_industrial_style():
    """
    Configura el estilo visual de las gráficas para que coincida con
    la estética minimalista e industrial de 'El Oxicorte'.
    """
    plt.rcParams.update({
        "text.usetex": False, # Usamos el motor mathtext de MPL por compatibilidad
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial"],
        "axes.edgecolor": "#444444",
        "axes.labelcolor": "#333333",
        "xtick.color": "#444444",
        "ytick.color": "#444444",
        "grid.color": "#E0E0E0",
        "figure.facecolor": "white",
        "axes.facecolor": "#F9F9F9"
    })

def render_math_text(text):
    """
    Procesa enunciados que contienen LaTeX. 
    Streamlit maneja esto nativamente con st.latex o st.markdown,
    pero este wrapper permite limpieza previa si el JSON/Sheets viene con errores.
    """
    if "$" in text:
        st.markdown(text) # Markdown de Streamlit soporta $...$ para LaTeX inline
    else:
        st.write(text)

def generate_geometry_plot(data_coords, plot_type="function"):
    """
    Genera un gráfico dinámico para preguntas de Geometría o Funciones M1.
    """
    set_industrial_style()
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Dibujar ejes cartesianos (Estética facsímil oficial)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.6)

    if plot_type == "function":
        # Ejemplo: data_coords podría ser una lista de puntos o una función
        ax.plot(data_coords['x'], data_coords['y'], color='#1A1A1A', linewidth=2)
    
    ax.set_aspect('equal')
    plt.tight_layout()
    
    return fig