import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Simulación de Regeneración de Tejidos",
    layout="wide"
)

st.title("Simulación Computacional de Regeneración de Tejidos")
st.markdown("""
Modelo de Autómatas Celulares 2D para simular procesos de proliferación celular, 
angiogénesis y maduración del tejido en tiempo real.
""")

# Sidebar con controles
st.sidebar.header("Parámetros de Simulación")
grid_size = st.sidebar.slider("Tamaño de la Grilla", 20, 100, 50, 5)
steps = st.sidebar.slider("Pasos de Evolución", 5, 200, 50, 5)
oxygen_level = st.sidebar.slider("Nivel de Oxígeno Inicial", 0.1, 1.0, 0.6, 0.05)

# Inicializar estado de la matriz en la sesión si no existe
if 'grid' not in st.session_state or st.session_state.get('grid_size') != grid_size:
    st.session_state.grid_size = grid_size
    # 0: Vacío/Necrótico, 1: Célula en proliferación, 2: Tejido maduro
    st.session_state.grid = np.random.choice([0, 1, 2], size=(grid_size, grid_size), p=[0.5, 0.3, 0.2])

# Botón para reiniciar matriz
if st.sidebar.button("Reiniciar Matriz"):
    st.session_state.grid = np.random.choice([0, 1, 2], size=(grid_size, grid_size), p=[0.5, 0.3, 0.2])

# Función de evolución de autómatas celulares
def evolve_grid(grid, oxygen):
    new_grid = grid.copy()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            neighbors = grid[max(0, r-1):min(rows, r+2), max(0, c-1):min(cols, c+2)]
            active_count = np.sum(neighbors == 1)
            
            if grid[r, c] == 0 and oxygen > 0.4 and active_count >= 2:
                new_grid[r, c] = 1 
            elif grid[r, c] == 1:
                new_grid[r, c] = 2 
    return new_grid

# Área principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Matriz Celular en Vivo")
    
    # Botón para correr la simulación paso a paso
    if st.button("Ejecutar Simulación"):
        progress_bar = st.progress(0)
        for step in range(steps):
            st.session_state.grid = evolve_grid(st.session_state.grid, oxygen_level)
            progress_bar.progress((step + 1) / steps)
        st.success("¡Simulación completada con éxito!")

    st.image(st.session_state.grid * 100, caption="Mapa Térmico de Autómatas Celulares", clamp=True, use_container_width=True)

with col2:
    st.markdown("### Métricas de Tejido")
    healthy_cells = np.sum(st.session_state.grid == 2)
    proliferating_cells = np.sum(st.session_state.grid == 1)
    
    st.metric(label="Tejido Maduro", value=f"{int(healthy_cells)} celdas")
    st.metric(label="Células Activas", value=f"{int(proliferating_cells)} celdas")
    st.metric(label="Oxígeno Disponible", value=f"{oxygen_level * 100:.1f}%")
