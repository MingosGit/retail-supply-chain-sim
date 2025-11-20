import streamlit as st
import plotly.express as px
from simulation import run_simulation

# Configuración de la página
st.set_page_config(page_title="Supply Chain Sim", layout="wide")

st.title("Simulador de Cadena de Suministro: Retail")
st.markdown("""
Esta herramienta simula la gestión de inventario de un producto (ej. Camisetas) durante un año (365 días).
Ajuste los parámetros de **Operaciones** en la barra lateral para optimizar el stock.
""")

# --- BARRA LATERAL (Controles) ---
st.sidebar.header("Parámetros de Gestión")

# Param 1: Punto de Reorden (ROP)
# Cuando el stock baja de este número, se hace un pedido.
reorder_point = st.sidebar.slider(
    "Punto de Reorden (ROP)", 
    min_value=0, 
    max_value=50, 
    value=10,
    help="Nivel de stock que activa un nuevo pedido al proveedor."
)

# Param 2: Cantidad de Pedido (Q)
# Cuántas unidades pedimos cada vez.
order_quantity = st.sidebar.slider(
    "Cantidad de Pedido (Q)", 
    min_value=10, 
    max_value=100, 
    value=50,
    help="Cantidad de unidades solicitadas en cada pedido."
)

# Param 3: Lead Time
# Tiempo que tarda el proveedor en entregar.
lead_time = st.sidebar.slider(
    "Tiempo de Entrega (Días)", 
    min_value=1, 
    max_value=14, 
    value=5,
    help="Días que tardan en llegar los productos desde que se piden."
)

# --- EJECUCIÓN DE LA SIMULACIÓN ---
if st.button("Ejecutar Simulación"):
    # Llamamos a la función que creamos en simulation.py
    df_results, lost_sales, total_sales = run_simulation(reorder_point, order_quantity, lead_time)
    
    # --- KPIs (Indicadores Clave) ---
    col1, col2, col3 = st.columns(3)
    
    total_demand = total_sales + lost_sales
    service_level = (total_sales / total_demand * 100) if total_demand > 0 else 0
    
    with col1:
        st.metric("Ventas Totales", f"{total_sales} uds")
    with col2:
        st.metric("Ventas Perdidas (Stockout)", f"{lost_sales} uds", delta_color="inverse")
    with col3:
        st.metric("Nivel de Servicio", f"{service_level:.1f}%")

    # --- VISUALIZACIÓN ---
    st.subheader("Evolución del Inventario")
    
    # Gráfico de línea con Plotly
    fig = px.line(df_results, x="day", y="stock", title="Nivel de Stock Diario")
    
    # Añadir línea roja para el Punto de Reorden
    fig.add_hline(y=reorder_point, line_dash="dash", line_color="red", annotation_text="ROP")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar datos crudos (opcional)
    with st.expander("Ver datos detallados"):
        st.dataframe(df_results)

else:
    st.info("Pulse el botón 'Ejecutar Simulación' para comenzar.")