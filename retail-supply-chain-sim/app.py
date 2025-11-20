import streamlit as st
import plotly.express as px
from simulation import run_simulation

st.set_page_config(page_title="Supply Chain Sim", layout="wide")

st.title("Simulador de Cadena de Suministro: Análisis de Costes")
st.markdown("""
### Contexto del Simulador
Esta herramienta permite analizar el impacto de las políticas de inventario en la rentabilidad de una empresa de retail. 
El objetivo es encontrar el **equilibrio óptimo (Trade-off)** entre minimizar los costes operativos y maximizar el nivel de servicio al cliente.

Utilice los controles de la izquierda para definir la política de reposición y los parámetros económicos.
""")

# --- BARRA LATERAL ---
st.sidebar.header("1. Operaciones (Logística)")

reorder_point = st.sidebar.slider(
    "Punto de Reorden (ROP)", 
    0, 50, 15,
    help="Nivel de inventario crítico. Cuando el stock baja de esta cantidad, se emite automáticamente un nuevo pedido al proveedor. \n\nUn ROP alto protege contra la demanda inesperada (Stock de seguridad), pero aumenta el coste de almacenamiento."
)

order_quantity = st.sidebar.slider(
    "Cantidad de Pedido (Q)", 
    10, 100, 50,
    help="Cantidad fija de unidades que se solicitan en cada orden (Lote económico). \n\nSi Q es alto: Se piden pocas veces al año (Bajo coste de pedido) pero se acumula mucho stock (Alto coste de almacenamiento). \nSi Q es bajo: Se pide muchas veces (Alto coste de pedido) pero se mantiene poco stock."
)

lead_time = st.sidebar.slider(
    "Tiempo de Entrega (Días)", 
    1, 14, 5,
    help="Tiempo que transcurre desde que se emite la orden de compra hasta que la mercancía llega al almacén. Durante este tiempo, la empresa es vulnerable a roturas de stock."
)

st.sidebar.markdown("---")
st.sidebar.header("2. Economía (Costes)")

ordering_cost_per_order = st.sidebar.number_input(
    "Coste por Pedido (Logística)", 
    value=50.0,
    help="Coste fijo incurrido cada vez que se realiza un pedido, independientemente de la cantidad solicitada. Incluye: transporte, recepción, inspección y costes administrativos."
)

holding_cost_per_unit_year = st.sidebar.number_input(
    "Coste de Almacenamiento (Unidad/Año)", 
    value=2.0,
    help="Coste de mantener una unidad en inventario durante un año completo. Incluye: coste de capital (dinero inmovilizado), alquiler de espacio, seguros y obsolescencia."
)

stockout_cost_per_unit = st.sidebar.number_input(
    "Coste de Oportunidad (Venta Perdida)", 
    value=20.0,
    help="Coste económico estimado por no tener producto cuando un cliente lo quiere comprar. Incluye: margen de beneficio perdido y pérdida de imagen/fidelidad del cliente."
)

# --- EJECUCIÓN ---
if st.button("Ejecutar Simulación"):
    # Obtenemos el nuevo valor num_orders
    df_results, lost_sales, total_sales, num_orders = run_simulation(reorder_point, order_quantity, lead_time)
    
    # --- CÁLCULOS ECONÓMICOS ---
    avg_inventory = df_results['stock'].mean()
    
    # 1. Coste de Almacenamiento
    total_holding_cost = avg_inventory * holding_cost_per_unit_year
    
    # 2. Coste de Pedidos
    total_ordering_cost = num_orders * ordering_cost_per_order
    
    # 3. Coste de Rotura
    total_stockout_cost = lost_sales * stockout_cost_per_unit
    
    # Coste Total
    total_cost = total_holding_cost + total_ordering_cost + total_stockout_cost

    # --- RESULTADOS ---
    st.subheader("Resultados Financieros")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Coste Total Operativo", f"{total_cost:,.2f}€", delta_color="inverse", help="Suma de costes de almacenamiento, pedidos y rotura de stock.")
    with col2:
        st.metric("Coste Almacenamiento", f"{total_holding_cost:,.2f}€", help=f"Inventario Promedio: {avg_inventory:.1f} uds")
    with col3:
        st.metric("Coste Pedidos", f"{total_ordering_cost:,.2f}€", help=f"Se realizaron {num_orders} pedidos al proveedor.")
    with col4:
        st.metric("Coste Oportunidad", f"{total_stockout_cost:,.2f}€", help=f"Se perdieron {lost_sales} ventas por falta de stock.")

    st.divider()
    st.subheader("Métricas Operativas")
    op_col1, op_col2 = st.columns(2)
    with op_col1:
        st.metric("Ventas Totales", f"{total_sales} uds")
    with op_col2:
        total_demand = total_sales + lost_sales
        service_level = (total_sales / total_demand * 100) if total_demand > 0 else 0
        st.metric("Nivel de Servicio", f"{service_level:.1f}%", help="Porcentaje de demanda que fue satisfecha con stock disponible.")

    # Gráfico
    st.plotly_chart(px.line(df_results, x="day", y="stock", title="Evolución de Stock"), use_container_width=True)