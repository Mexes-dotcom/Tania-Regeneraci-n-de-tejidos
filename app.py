import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Simulación de Regeneración de Tejidos",
    layout="wide"
)

st.title("Simulación Computacional de Regeneración de Tejidos")
st.markdown("""
Modelo de Autómatas Celulares 2D para simular procesos de proliferación celular, 
angiogénesis y maduración del tejido.
""")

# Sidebar con controles
st.sidebar.header("Parámetros de Simulación")
grid_size = st.sidebar.slider("Tamaño de la Grilla", 20, 100, 50, 5)
steps = st.sidebar.slider("Pasos de Simulación", 10, 200, 50, 10)
oxygen_level = st.sidebar.slider("Nivel de Oxígeno Inicial", 0.1, 1.0, 0.5, 0.05)

st.sidebar.info("Ajustá los parámetros y observá el comportamiento de la matriz celular.")

# Área principal
st.subheader("Estado de la Matriz Celular")
col1, col2 = st.columns([2, 1])

with col1:
    # Generador simple de matriz de prueba para la visualización inicial
    matrix = np.random.choice([0, 1, 2], size=(grid_size, grid_size), p=[0.7, 0.2, 0.1])
    st.write(f"Grilla generada de **{grid_size}x{grid_size}** celdas.")
    st.image(matrix * 100, caption="Mapa de Celdas (Matriz 2D)", clamp=True, use_container_width=True)

with col2:
    st.markdown("### Métricas")
    st.metric(label="Paso Actual", value=f"0 / {steps}")
    st.metric(label="Oxígeno Promedio", value=f"{oxygen_level * 100:.1f}%")
    st.metric(label="Células Activas", value="Estable")
