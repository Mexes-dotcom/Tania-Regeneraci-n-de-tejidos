import numpy as np
import streamlit as st

# Configuración de la página
st.set_page_config(
page_title="Simulación de Regeneración de Tejidos",
page_layout="wide",
)

st.title("Simulación Computacional de Regeneración de Tejidos (Necrosis)")
st.markdown(
    "Modelo de Autómatas Celulares 2D para visualizar proliferación celular,"
    " angiogénesis y maduración del tejido."
)

# Sidebar con controles
st.sidebar.header("Parámetros de Simulación")
grid_size = st.sidebar.slider("Tamaño de la Grilla", 30, 100, 50, 5)
steps = st.sidebar.slider("Pasos de Simulación", 10, 200, 50, 10)
oxygen_level = st.sidebar.slider(
    "Nivel de Oxígeno / Angiogénesis", 0.1, 1.0, 0.5, 0.05
)

# Estados celulares: 0 = Sano, 1 = Necrótico, 2 = Regenerando/Proliferando
# Inicializamos la grilla con tejido sano y un núcleo de necrosis en el centro
if "grid" not in st.session_state or st.sidebar.button(
    "Reiniciar Simulación"
):
  grid = np.zeros((grid_size, grid_size), dtype=int)
  # Crear zona necrótica central
  c = grid_size // 2
  grid[c - 5 : c + 5, c - 5 : c + 5] = 1
  st.session_state.grid = grid
  st.session_state.step_count = 0


def update_grid(grid, o2):
  new_grid = grid.copy()
  rows, cols = grid.shape

  for r in range(rows):
    for c in range(cols):
      state = grid[r, c]

      # Célula Necrótica (1) intenta sanar si hay suficiente oxígeno o vecinos regenerando
      if state == 1:
        # Contar vecinos regenerando (estado 2) o sanos (0)
        neighbors = grid[
            max(0, r - 1) : min(rows, r + 2), max(0, c - 1) : min(cols, c + 2)
        ]
        reg_count = np.sum(neighbors == 2)

        # Probabilidad de transición a regeneración basada en oxígeno y vecinos
        if np.random.rand() < (o2 * 0.3 + reg_count * 0.1):
          new_grid[r, c] = 2

      # Célula Regenerando (2) madura a Sana (0) con el tiempo
      elif state == 2:
        if np.random.rand() < 0.4:
          new_grid[r, c] = 0

  return new_grid


# Visualización
col1, col2 = st.columns([2, 1])

with col1:
  # Mapeo de colores para la matriz (Sano=Verde, Necrótico=Rojo, Regenerando=Amarillo)
  # Traducimos a valores visuales para streamlit (0: Sano, 1: Necrótico, 2: Regenerando)
  fig_display = st.empty()

with col2:
  st.subheader("Estado Actual")
  metric_placeholder = st.empty()


# Botón para correr un paso o la simulación completa
if st.button("Avanzar Simulación"):
  st.session_state.grid = update_grid(st.session_state.grid, oxygen_level)
  st.session_state.step_count += 1

# Mostrar matriz usando texto estilizado o gráficos simples con Streamlit
grid_mapped = np.array(
    st.session_state.grid, dtype=object
)  # Preparar para render
st.write(f"Paso actual: {st.session_state.step_count}")

# Dibujar la grilla con un mapa de calor simple usando st.dataframe o st.image
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 6))
cax = ax.imshow(
    st.session_state.grid, cmap="YlOrRd", vmin=0, vmax=2
)  # Visualizador rápido
ax.set_xticks([])
ax.set_yticks([])
col1.pyplot(fig)
