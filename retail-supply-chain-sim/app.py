import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
import io
from datetime import datetime
from simulation import run_simulation, SIMULATION_DAYS
from multi_product_sim import run_multi_product_simulation

st.set_page_config(
    page_title="Supply Chain Simulator", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="📦"
)

# Estilo CSS personalizado con paleta coherente
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 2.5rem; color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">📦 Simulador de Cadena de Suministro</h1>
    <p style="margin-top: 0.5rem; font-size: 1.1rem; color: #F8FAFC; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">Optimiza tu inventario y reduce costes operativos</p>
</div>
""", unsafe_allow_html=True)

# --- BARRA LATERAL CON MEJOR DISEÑO ---
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
            padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
    <h2 style="color: white; margin: 0; font-size: 1.5rem;">⚙️ Configuración</h2>
    <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        Ajusta los parámetros de tu simulación
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🚚 Operaciones & Logística")

# Usar session_state para mantener el valor del slider entre ejecuciones
if 'order_quantity_value' not in st.session_state:
    st.session_state.order_quantity_value = 50

reorder_point = st.sidebar.slider(
    "Punto de Reorden (ROP)", 
    0, 250, 15,
    help="Nivel de inventario crítico. Cuando el stock baja de esta cantidad, se emite automáticamente un nuevo pedido al proveedor. \n\nUn ROP alto protege contra la demanda inesperada (Stock de seguridad), pero aumenta el coste de almacenamiento."
)

order_quantity = st.sidebar.slider(
    "Cantidad de Pedido (Q)", 
    10, 500, st.session_state.order_quantity_value,
    help="Cantidad fija de unidades que se solicitan en cada orden (Lote económico). \n\nSi Q es alto: Se piden pocas veces al año (Bajo coste de pedido) pero se acumula mucho stock (Alto coste de almacenamiento). \nSi Q es bajo: Se pide muchas veces (Alto coste de pedido) pero se mantiene poco stock.",
    key="order_quantity_slider"
)

# Actualizar session_state cuando el slider cambia
st.session_state.order_quantity_value = order_quantity

lead_time = st.sidebar.slider(
    "Tiempo de Entrega (Días)", 
    1, 14, 5,
    help="Tiempo que transcurre desde que se emite la orden de compra hasta que la mercancía llega al almacén. Durante este tiempo, la empresa es vulnerable a roturas de stock."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Patrón de Demanda")

demand_type = st.sidebar.selectbox(
    "Tipo de Distribución",
    ["uniform", "normal", "poisson"],
    format_func=lambda x: {
        "uniform": "🎲 Uniforme (0-5 uds/día)",
        "normal": "📈 Normal (Realista)",
        "poisson": "📊 Poisson (Eventos Raros)"
    }[x],
    help="Distribución estadística de la demanda diaria.\n\nUniforme: Todos los valores tienen la misma probabilidad.\nNormal: Más realista, se concentra alrededor de la media.\nPoisson: Común en retail para productos de baja rotación."
)

demand_mean = 2.5
demand_std = 1.5

if demand_type in ["normal", "poisson"]:
    demand_mean = st.sidebar.slider(
        "Demanda Media (uds/día)",
        0.5, 10.0, 2.5, 0.5,
        help="Demanda promedio esperada por día."
    )
    
    if demand_type == "normal":
        demand_std = st.sidebar.slider(
            "Desviación Estándar",
            0.5, 5.0, 1.5, 0.5,
            help="Variabilidad de la demanda. Mayor valor = mayor incertidumbre."
        )

# ============================================================================
# WHAT-IF INTERACTIVO: Escenarios de Demanda en Tiempo Real
# ============================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Análisis What-If")

demand_multiplier = st.sidebar.slider(
    "📈 Escenario de Demanda",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.05,
    help="Simula cambios en la demanda y observa el impacto inmediato en costes y rentabilidad.\n\n• 1.0 = Demanda Normal (Base)\n• 1.2 = +20% (Campaña Marketing, Black Friday)\n• 0.8 = -20% (Recesión, Temporada Baja)\n\nLos resultados se actualizan automáticamente al ejecutar la simulación."
)

# Visualización del cambio porcentual
demand_change_pct = (demand_multiplier - 1.0) * 100
if demand_change_pct > 0:
    st.sidebar.success(f"📊 Simulando: **+{demand_change_pct:.0f}%** de demanda")
elif demand_change_pct < 0:
    st.sidebar.warning(f"📊 Simulando: **{demand_change_pct:.0f}%** de demanda")
else:
    st.sidebar.info("📊 Escenario: **Base** (sin cambios)")

enable_seasonality = st.sidebar.checkbox(
    "🍃 Estacionalidad",
    help="Activa patrones estacionales que simulan picos y valles de demanda durante el año, como aumentos en Navidad o rebajas de verano. Esto permite analizar cómo afectan las temporadas a la gestión de inventario."
)

seasonality = None
if enable_seasonality:
    st.sidebar.caption("📅 Factores de demanda por mes (1.0 = normal):")
    seasonal_pattern = st.sidebar.selectbox(
        "Patrón de Estacionalidad",
        ["retail_navidad", "verano_alto"],
        format_func=lambda x: {
            "retail_navidad": "🎄 Retail (Pico Navidad)",
            "verano_alto": "☀️ Verano Alto"
        }[x],
        help="Selecciona un patrón predefinido de estacionalidad:\n\n🎄 Retail (Pico Navidad): Simula el comportamiento típico del retail con incremento gradual de demanda hacia fin de año, alcanzando el pico en noviembre-diciembre.\n\n☀️ Verano Alto: Patrón con mayor demanda en los meses de verano (junio-agosto), ideal para productos de temporada estival."
    )
    
    if seasonal_pattern == "retail_navidad":
        # Picos en Nov-Dic (Navidad)
        seasonality = {0: 0.8, 1: 0.7, 2: 0.9, 3: 1.0, 4: 1.0, 5: 1.1, 
                      6: 1.2, 7: 1.1, 8: 1.0, 9: 1.1, 10: 1.5, 11: 1.8}
    elif seasonal_pattern == "verano_alto":
        # Picos en Jun-Ago (Verano)
        seasonality = {0: 0.8, 1: 0.8, 2: 0.9, 3: 1.0, 4: 1.1, 5: 1.4,
                      6: 1.6, 7: 1.5, 8: 1.2, 9: 1.0, 10: 0.9, 11: 0.9}
    elif seasonal_pattern == "uniforme":
        seasonality = None

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Estructura de Costes (€)")

ordering_cost_per_order = st.sidebar.number_input(
    "Coste por Pedido (Logística)", 
    value=50.0,
    min_value=0.0,
    help="Coste fijo incurrido cada vez que se realiza un pedido, independientemente de la cantidad solicitada. Incluye: transporte, recepción, inspección y costes administrativos.\n\nEjemplo: Si cuesta 50€ hacer un pedido (transporte + gestión), ese coste se aplica tanto si pides 10 unidades como 100."
)

holding_cost_per_unit_year = st.sidebar.number_input(
    "Coste de Almacenamiento (Unidad/Año)", 
    value=2.0,
    min_value=0.0,
    help="Coste de mantener una unidad en inventario durante un año completo. Incluye: coste de capital (dinero inmovilizado), alquiler de espacio, seguros, obsolescencia y deterioro.\n\nEjemplo: Si cada unidad almacenada cuesta 2€/año, mantener 100 unidades durante un año cuesta 200€."
)

stockout_cost_per_unit = st.sidebar.number_input(
    "Coste de Oportunidad (Venta Perdida)", 
    value=20.0,
    min_value=0.0,
    help="Coste económico estimado por no tener producto cuando un cliente lo solicita. Incluye: margen de beneficio perdido, deterioro de imagen de marca, pérdida de fidelidad del cliente y posible venta al competidor.\n\nEjemplo: Si pierdes 20€ de beneficio por cada venta perdida, 10 rupturas de stock cuestan 200€."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Asistente Inteligente")

# Inicializar EOQ si no existe
if 'eoq' not in st.session_state:
    st.session_state.eoq = 0

# Cálculo EOQ (dinámico según demanda ajustada y costes actuales)
if demand_type == "uniform":
    annual_demand_estimate = 2.5 * 365 * demand_multiplier
elif demand_type in ["normal", "poisson"]:
    annual_demand_estimate = demand_mean * 365 * demand_multiplier
else:
    annual_demand_estimate = 2.5 * 365 * demand_multiplier

if annual_demand_estimate > 0 and ordering_cost_per_order > 0 and holding_cost_per_unit_year > 0:
    # Fórmula EOQ: √((2 × D × S) / H)
    # D = Demanda anual, S = Coste por pedido, H = Coste almacenamiento
    eoq = math.sqrt((2 * annual_demand_estimate * ordering_cost_per_order) / holding_cost_per_unit_year)
    
    # Mostrar cálculo para debugging
    st.sidebar.caption(f"📐 D={annual_demand_estimate:.0f} | S={ordering_cost_per_order}€ | H={holding_cost_per_unit_year}€")
    
    # Guardar en session state
    st.session_state.eoq = eoq
    
    # Comparar con el valor actual
    diff = abs(order_quantity - eoq)
    diff_percent = (diff / eoq * 100) if eoq > 0 else 0
    
    if diff_percent > 20:
        st.sidebar.warning(f"⚠️ Tu Q ({order_quantity}) difiere {diff_percent:.0f}% del óptimo")
        st.sidebar.metric(
            label="Cantidad Óptima Sugerida (EOQ)",
            value=f"{eoq:.0f} uds",
            delta=f"{int(eoq - order_quantity):+d} vs actual",
            delta_color="inverse"
        )
        
        # Botón destacado para aplicar
        if st.sidebar.button("✨ Usar Valor Óptimo (EOQ)", type="primary", use_container_width=True):
            st.session_state.order_quantity_value = int(eoq)
            st.rerun()
            
    else:
        st.sidebar.success(f"✓ Tu Q está cerca del óptimo")
        st.sidebar.metric(
            label="Cantidad Óptima (EOQ)",
            value=f"{eoq:.0f} uds",
            delta=f"{int(eoq - order_quantity):+d}",
            delta_color="off"
        )
else:
    st.sidebar.warning("⚠️ Configura los costes primero para ver sugerencias")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔬 Herramientas Avanzadas")

enable_optimizer = st.sidebar.checkbox(
    "🤖 Optimizador Automático",
    help="Ejecuta una búsqueda exhaustiva (Grid Search) para encontrar la combinación óptima de ROP y Q que minimiza el coste total. Prueba múltiples configuraciones y te muestra la mejor.\n\nÚtil cuando no sabes qué valores usar o quieres validar tu configuración actual."
)

enable_comparison = st.sidebar.checkbox(
    "🔄 Comparar Múltiples Escenarios",
    help="Ejecuta 3 simulaciones en paralelo con diferentes configuraciones (Conservador, Actual, Agresivo) para que puedas comparar resultados lado a lado.\n\nIdeal para ver el impacto de cambiar tus parámetros de inventario."
)

enable_sensitivity = st.sidebar.checkbox(
    "📉 Análisis de Sensibilidad",
    help="Genera gráficos que muestran cómo varían los costes totales al cambiar ROP o Q gradualmente. Te ayuda a entender qué tan sensible es tu configuración a pequeños cambios.\n\nPerfecto para identificar el rango óptimo de operación y entender los trade-offs."
)

# --- OPTIMIZADOR AUTOMÁTICO ---
if enable_optimizer:
    st.header("🤖 Optimizador Automático")
    st.markdown("**Búsqueda exhaustiva de la configuración óptima (Grid Search)**")
    
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        rop_min = st.number_input(
            "ROP Mínimo", 
            value=5, 
            min_value=0, 
            max_value=250,
            help="Valor mínimo de Punto de Reorden a evaluar en la búsqueda."
        )
        rop_max = st.number_input(
            "ROP Máximo", 
            value=25, 
            min_value=0, 
            max_value=250,
            help="Valor máximo de Punto de Reorden a evaluar en la búsqueda."
        )
        rop_step = st.number_input(
            "Paso ROP", 
            value=5, 
            min_value=1, 
            max_value=10,
            help="Incremento entre valores de ROP (ej: paso=5 evalúa 5, 10, 15, 20, 25)."
        )
    
    with col_opt2:
        q_min = st.number_input(
            "Q Mínimo", 
            value=20, 
            min_value=10, 
            max_value=500,
            help="Valor mínimo de Cantidad de Pedido a evaluar."
        )
        q_max = st.number_input(
            "Q Máximo", 
            value=80, 
            min_value=10, 
            max_value=500,
            help="Valor máximo de Cantidad de Pedido a evaluar."
        )
        q_step = st.number_input(
            "Paso Q", 
            value=10, 
            min_value=5, 
            max_value=20,
            help="Incremento entre valores de Q (ej: paso=10 evalúa 20, 30, 40...)."
        )
    
    total_combinations = len(range(rop_min, rop_max + 1, rop_step)) * len(range(q_min, q_max + 1, q_step))
    st.info(f"📊 Se evaluarán **{total_combinations} combinaciones**")
    
    if st.button("🚀 Iniciar Optimización", type="primary"):
        optimization_results = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_iterations = 0
        for rop_test in range(rop_min, rop_max + 1, rop_step):
            for q_test in range(q_min, q_max + 1, q_step):
                total_iterations += 1
                progress = total_iterations / total_combinations
                progress_bar.progress(progress)
                status_text.text(f"Evaluando ROP={rop_test}, Q={q_test}... ({total_iterations}/{total_combinations})")
                
                df, lost, total, orders = run_simulation(
                    rop_test, q_test, lead_time,
                    demand_type=demand_type, demand_mean=demand_mean, demand_std=demand_std,
                    seasonality=seasonality
                )
                
                avg_inv = df['stock'].mean()
                h_cost = avg_inv * holding_cost_per_unit_year
                o_cost = orders * ordering_cost_per_order
                s_cost = lost * stockout_cost_per_unit
                t_cost = h_cost + o_cost + s_cost
                service = (total / (total + lost) * 100) if (total + lost) > 0 else 0
                
                optimization_results.append({
                    "ROP": rop_test,
                    "Q": q_test,
                    "Coste Total": t_cost,
                    "Nivel Servicio (%)": service,
                    "Ventas Perdidas": lost,
                    "Nº Pedidos": orders,
                    "Inv. Promedio": avg_inv
                })
        
        progress_bar.empty()
        status_text.empty()
        
        opt_df = pd.DataFrame(optimization_results)
        opt_df = opt_df.sort_values("Coste Total")
        
        # Mejor configuración
        best = opt_df.iloc[0]
        st.success(f"✅ **Configuración Óptima Encontrada:**")
        
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            st.metric("ROP Óptimo", f"{int(best['ROP'])}")
        with col_b2:
            st.metric("Q Óptimo", f"{int(best['Q'])}")
        with col_b3:
            st.metric("Coste Total", f"{best['Coste Total']:,.2f}€")
        with col_b4:
            st.metric("Nivel Servicio", f"{best['Nivel Servicio (%)']:.1f}%")
        
        # Mapa de calor
        st.subheader("🔥 Mapa de Calor: Coste Total")
        pivot_table = opt_df.pivot(index="ROP", columns="Q", values="Coste Total")
        
        fig_heatmap = px.imshow(
            pivot_table,
            labels=dict(x="Cantidad de Pedido (Q)", y="Punto de Reorden (ROP)", color="Coste Total (€)"),
            x=pivot_table.columns,
            y=pivot_table.index,
            color_continuous_scale="RdYlGn_r",
            title="Coste Total según combinaciones ROP-Q"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Top 10 configuraciones
        st.subheader("🏆 Top 10 Configuraciones")
        st.dataframe(opt_df.head(10), use_container_width=True, hide_index=True)
    
    st.divider()

# --- COMPARATIVA DE ESCENARIOS ---
if enable_comparison:
    st.header("🔄 Comparativa de Escenarios")
    st.markdown("Compara automáticamente 3 políticas de inventario diferentes:")
    
    scenarios = [
        {"name": "Conservador", "rop": reorder_point + 10, "q": order_quantity, "lt": lead_time},
        {"name": "Actual", "rop": reorder_point, "q": order_quantity, "lt": lead_time},
        {"name": "Agresivo", "rop": max(0, reorder_point - 10), "q": int(st.session_state.get('eoq', order_quantity)), "lt": lead_time}
    ]
    
    comparison_results = []
    
    with st.spinner("Ejecutando simulaciones comparativas..."):
        for scenario in scenarios:
            df, lost, total, orders = run_simulation(
                scenario["rop"], scenario["q"], scenario["lt"],
                demand_type=demand_type, demand_mean=demand_mean, demand_std=demand_std,
                seasonality=seasonality
            )
            
            avg_inv = df['stock'].mean()
            h_cost = avg_inv * holding_cost_per_unit_year
            o_cost = orders * ordering_cost_per_order
            s_cost = lost * stockout_cost_per_unit
            t_cost = h_cost + o_cost + s_cost
            service = (total / (total + lost) * 100) if (total + lost) > 0 else 0
            
            comparison_results.append({
                "Escenario": scenario["name"],
                "ROP": scenario["rop"],
                "Q": scenario["q"],
                "Lead Time": scenario["lt"],
                "Coste Total (€)": f"{t_cost:,.2f}",
                "Nivel Servicio (%)": f"{service:.1f}",
                "Ventas Perdidas": lost,
                "Nº Pedidos": orders
            })
    
    comparison_df = pd.DataFrame(comparison_results)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.divider()

# --- EJECUCIÓN ---

# Validaciones
validation_errors = []
validation_warnings = []

if reorder_point >= order_quantity:
    validation_warnings.append("⚠️ **Advertencia**: El Punto de Reorden es mayor o igual a la Cantidad de Pedido. Esto puede causar pedidos muy frecuentes.")

if lead_time > 7 and reorder_point < 15:
    validation_warnings.append("⚠️ **Advertencia**: Lead Time largo con ROP bajo puede causar rupturas de stock.")

if order_quantity < 10:
    validation_warnings.append("⚠️ **Advertencia**: Cantidad de pedido muy baja puede incrementar excesivamente los costes de pedido.")

if ordering_cost_per_order <= 0 or holding_cost_per_unit_year <= 0 or stockout_cost_per_unit <= 0:
    validation_errors.append("❌ **Error**: Todos los costes deben ser mayores a 0.")

# Mostrar validaciones
for warning in validation_warnings:
    st.warning(warning)

for error in validation_errors:
    st.error(error)

# ============================================================================
# DATOS SEMILLA: Ejecutar simulación automáticamente al inicio (Requisito #1)
# ============================================================================
if 'simulation_results' not in st.session_state:
    # Parámetros por defecto profesionales (caso de éxito demostrable)
    df_results, lost_sales, total_sales, num_orders = run_simulation(
        reorder_point=15, 
        order_quantity=50, 
        lead_time=5,
        demand_type="normal", 
        demand_mean=2.5, 
        demand_std=1.5,
        seasonality=None
    )
    
    # Cálculos económicos con parámetros por defecto
    avg_inventory = df_results['stock'].mean()
    default_holding = 1.0
    default_ordering = 50.0
    default_stockout = 10.0
    
    total_holding_cost = avg_inventory * default_holding
    total_ordering_cost = num_orders * default_ordering
    total_stockout_cost = lost_sales * default_stockout
    total_cost = total_holding_cost + total_ordering_cost + total_stockout_cost
    
    # Guardar resultados iniciales
    st.session_state['simulation_results'] = {
        'df_results': df_results,
        'lost_sales': lost_sales,
        'total_sales': total_sales,
        'num_orders': num_orders,
        'avg_inventory': avg_inventory,
        'total_holding_cost': total_holding_cost,
        'total_ordering_cost': total_ordering_cost,
        'total_stockout_cost': total_stockout_cost,
        'total_cost': total_cost,
        'reorder_point': 15,
        'order_quantity': 50,
        'lead_time': 5,
        'demand_type': "normal",
        'demand_mean': 2.5,
        'demand_multiplier': 1.0,
        'is_demo': True  # Marca para mostrar banner
    }

# Botón de simulación más destacado
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run_button = st.button(
        "🚀 EJECUTAR SIMULACIÓN", 
        disabled=len(validation_errors) > 0,
        type="primary",
        use_container_width=True
    )

if run_button:
    # Aplicar multiplicador What-If a la demanda
    adjusted_demand_mean = demand_mean * demand_multiplier
    
    # Obtenemos el nuevo valor num_orders
    df_results, lost_sales, total_sales, num_orders = run_simulation(
        reorder_point, order_quantity, lead_time,
        demand_type=demand_type, demand_mean=adjusted_demand_mean, demand_std=demand_std,
        seasonality=seasonality
    )
    
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
    
    # GUARDAR EN SESSION STATE para evitar pérdida de datos al descargar
    st.session_state['simulation_results'] = {
        'df_results': df_results,
        'lost_sales': lost_sales,
        'total_sales': total_sales,
        'num_orders': num_orders,
        'avg_inventory': avg_inventory,
        'total_holding_cost': total_holding_cost,
        'total_ordering_cost': total_ordering_cost,
        'total_stockout_cost': total_stockout_cost,
        'total_cost': total_cost,
        'reorder_point': reorder_point,
        'order_quantity': order_quantity,
        'lead_time': lead_time,
        'demand_type': demand_type,
        'demand_mean': adjusted_demand_mean,
        'demand_multiplier': demand_multiplier,
        'is_demo': False  # Simulación manual del usuario
    }

# Mostrar resultados si existen en session_state
if 'simulation_results' in st.session_state:
    results = st.session_state['simulation_results']
    df_results = results['df_results']
    lost_sales = results['lost_sales']
    total_sales = results['total_sales']
    num_orders = results['num_orders']
    avg_inventory = results['avg_inventory']
    total_holding_cost = results['total_holding_cost']
    total_ordering_cost = results['total_ordering_cost']
    total_stockout_cost = results['total_stockout_cost']
    total_cost = results['total_cost']
    sim_reorder_point = results['reorder_point']
    sim_order_quantity = results['order_quantity']
    sim_lead_time = results['lead_time']
    sim_demand_type = results['demand_type']
    sim_demand_mean = results['demand_mean']
    sim_demand_multiplier = results.get('demand_multiplier', 1.0)
    is_demo = results.get('is_demo', False)
    
    # Banner de datos de demostración
    if is_demo:
        st.info("👁️ **Visualización de Demostración** | Estás viendo datos de ejemplo pre-cargados. Ajusta los parámetros en la barra lateral y haz clic en '🚀 EJECUTAR SIMULACIÓN' para ver tus propios resultados.", icon="ℹ️")
    
    # Banner de escenario What-If activo
    if sim_demand_multiplier != 1.0:
        whatif_change = (sim_demand_multiplier - 1.0) * 100
        if whatif_change > 0:
            st.warning(f"🎯 **Escenario What-If Activo**: Estás simulando un **aumento del {whatif_change:.0f}%** en la demanda ({sim_demand_mean/sim_demand_multiplier:.1f} → {sim_demand_mean:.1f} uds/día). Compara los costes con el escenario base para ver el impacto financiero.", icon="📊")
        else:
            st.info(f"🎯 **Escenario What-If Activo**: Estás simulando una **reducción del {abs(whatif_change):.0f}%** en la demanda ({sim_demand_mean/sim_demand_multiplier:.1f} → {sim_demand_mean:.1f} uds/día). Observa cómo se optimizan los costes en baja demanda.", icon="📊")

    # ============================================================================
    # TABLERO FINANCIERO (P&L) - Requisito #3: Valor Financiero
    # ============================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 1.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);">
        <h2 style="color: white; margin: 0 0 1rem 0; font-size: 1.8rem; font-weight: 700;">
            💼 Tablero Financiero (P&L) - Año Completo
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas financieras en formato P&L
    col_pl1, col_pl2, col_pl3 = st.columns([2, 2, 1])
    
    with col_pl1:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #10b981;">
            <p style="margin: 0; color: #6b7280; font-size: 0.85rem; font-weight: 600;">📊 INGRESOS POTENCIALES</p>
        </div>
        """, unsafe_allow_html=True)
        total_demand = total_sales + lost_sales
        potential_revenue = total_demand * 10  # Asumiendo 10€ precio venta
        st.metric("Demanda Total Valorada", f"{potential_revenue:,.0f} €", 
                 help=f"{total_demand} unidades demandadas × precio venta estimado")
    
    with col_pl2:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc2626;">
            <p style="margin: 0; color: #6b7280; font-size: 0.85rem; font-weight: 600;">💸 COSTES OPERATIVOS</p>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Coste Total Anual", f"{total_cost:,.0f} €", 
                 help="Suma de costes de almacenamiento + pedidos + rupturas de stock")
    
    with col_pl3:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; color: #6b7280; font-size: 0.85rem; font-weight: 600;">📈 IMPACTO</p>
        </div>
        """, unsafe_allow_html=True)
        impact_pct = (total_cost / potential_revenue * 100) if potential_revenue > 0 else 0
        st.metric("% Costes/Ingresos", f"{impact_pct:.1f}%",
                 delta=f"-{100-impact_pct:.1f}% margen" if impact_pct < 100 else "⚠️ Pérdidas",
                 delta_color="inverse")
    
    # Desglose de costes en tabla P&L
    st.markdown("""
    <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
        <h4 style="margin: 0 0 1rem 0; color: #1e293b; font-weight: 600;">💶 Desglose de Costes (€)</h4>
    </div>
    """, unsafe_allow_html=True)
    
    pl_cols = st.columns([3, 2, 2, 1])
    
    with pl_cols[0]:
        st.markdown("**Concepto**")
        st.write("📦 Coste Almacenamiento")
        st.write("🚚 Coste Pedidos")
        st.write("⚠️ Coste Rupturas")
        st.markdown("---")
        st.markdown("**💰 COSTE TOTAL**")
    
    with pl_cols[1]:
        st.markdown("**Importe (€)**")
        st.write(f"{total_holding_cost:,.2f} €")
        st.write(f"{total_ordering_cost:,.2f} €")
        st.write(f"{total_stockout_cost:,.2f} €")
        st.markdown("---")
        st.markdown(f"**{total_cost:,.2f} €**")
    
    with pl_cols[2]:
        st.markdown("**% del Total**")
        st.write(f"{(total_holding_cost/total_cost*100):.1f}%" if total_cost > 0 else "0%")
        st.write(f"{(total_ordering_cost/total_cost*100):.1f}%" if total_cost > 0 else "0%")
        st.write(f"{(total_stockout_cost/total_cost*100):.1f}%" if total_cost > 0 else "0%")
        st.markdown("---")
        st.markdown("**100%**")
    
    with pl_cols[3]:
        st.markdown("**Impacto**")
        st.write("📊" if total_holding_cost == max(total_holding_cost, total_ordering_cost, total_stockout_cost) else "")
        st.write("📊" if total_ordering_cost == max(total_holding_cost, total_ordering_cost, total_stockout_cost) else "")
        st.write("⚠️" if total_stockout_cost > 0 else "✅")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================================================
    # ANÁLISIS WHAT-IF: Comparación con Escenario Base (ROI)
    # ============================================================================
    if sim_demand_multiplier != 1.0:
        st.markdown("---")
        st.markdown("### 🔄 Análisis Comparativo: What-If vs Escenario Base")
        
        # Calcular escenario base (demanda sin multiplicador)
        with st.spinner("Calculando impacto del escenario What-If..."):
            base_demand_mean = sim_demand_mean / sim_demand_multiplier
            df_base, lost_base, total_base, orders_base = run_simulation(
                sim_reorder_point, sim_order_quantity, sim_lead_time,
                demand_type=sim_demand_type, demand_mean=base_demand_mean, demand_std=demand_std,
                seasonality=seasonality
            )
            
            avg_inv_base = df_base['stock'].mean()
            h_cost_base = avg_inv_base * holding_cost_per_unit_year
            o_cost_base = orders_base * ordering_cost_per_order
            s_cost_base = lost_base * stockout_cost_per_unit
            total_cost_base = h_cost_base + o_cost_base + s_cost_base
            
            total_demand_base = total_base + lost_base
            potential_revenue_base = total_demand_base * 10
            service_level_base = (total_base / total_demand_base * 100) if total_demand_base > 0 else 0
        
        # Métricas comparativas lado a lado
        st.markdown("""<div style="background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h4 style="color: white; margin: 0; text-align: center;">💡 Impacto Financiero del Cambio en Demanda</h4>
        </div>""", unsafe_allow_html=True)
        
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        
        with comp_col1:
            st.markdown("**📊 Escenario Base**")
            st.metric("Demanda Media", f"{base_demand_mean:.1f} uds/día")
            st.metric("Coste Total", f"{total_cost_base:,.0f} €")
            st.metric("Nivel Servicio", f"{service_level_base:.1f}%")
            st.metric("Ventas Perdidas", f"{lost_base} uds")
        
        with comp_col2:
            whatif_label = f"+{(sim_demand_multiplier-1)*100:.0f}%" if sim_demand_multiplier > 1 else f"{(sim_demand_multiplier-1)*100:.0f}%"
            st.markdown(f"**🎯 Escenario What-If ({whatif_label})**")
            st.metric("Demanda Media", f"{sim_demand_mean:.1f} uds/día", 
                     delta=f"{sim_demand_mean - base_demand_mean:+.1f} uds")
            st.metric("Coste Total", f"{total_cost:,.0f} €",
                     delta=f"{total_cost - total_cost_base:+,.0f} €",
                     delta_color="inverse")
            total_demand_current = total_sales + lost_sales
            service_level_current = (total_sales / total_demand_current * 100) if total_demand_current > 0 else 0
            st.metric("Nivel Servicio", f"{service_level_current:.1f}%",
                     delta=f"{service_level_current - service_level_base:+.1f}%")
            st.metric("Ventas Perdidas", f"{lost_sales} uds",
                     delta=f"{lost_sales - lost_base:+d} uds",
                     delta_color="inverse")
        
        with comp_col3:
            st.markdown("**📈 Impacto en ROI**")
            
            # Cálculo de ROI
            potential_revenue_current = (total_sales + lost_sales) * 10
            revenue_change = potential_revenue_current - potential_revenue_base
            cost_change = total_cost - total_cost_base
            roi_impact = revenue_change - cost_change
            
            st.metric("Δ Ingresos Potenciales", f"{revenue_change:+,.0f} €",
                     help="Cambio en ingresos por variación de demanda")
            st.metric("Δ Costes Operativos", f"{cost_change:+,.0f} €",
                     delta_color="inverse",
                     help="Cambio en costes totales")
            st.metric("ROI Neto Estimado", f"{roi_impact:+,.0f} €",
                     delta=f"{(roi_impact/potential_revenue_base*100):+.1f}%" if potential_revenue_base > 0 else "N/A",
                     help="Impacto neto: (Δ Ingresos - Δ Costes)")
            
            if roi_impact > 0:
                st.success("✅ Escenario rentable")
            elif roi_impact < 0:
                st.error("⚠️ Escenario menos rentable")
            else:
                st.info("➡️ ROI neutro")
        
        # Gráfico comparativo de costes
        st.markdown("#### 📊 Comparación Visual de Costes")
        
        comparison_data = pd.DataFrame([
            {"Escenario": "Base", "Almacenamiento": h_cost_base, "Pedidos": o_cost_base, "Rupturas": s_cost_base},
            {"Escenario": f"What-If ({whatif_label})", "Almacenamiento": total_holding_cost, "Pedidos": total_ordering_cost, "Rupturas": total_stockout_cost}
        ])
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(name='Almacenamiento', x=comparison_data['Escenario'], 
                                       y=comparison_data['Almacenamiento'], marker_color='#06b6d4'))
        fig_comparison.add_trace(go.Bar(name='Pedidos', x=comparison_data['Escenario'], 
                                       y=comparison_data['Pedidos'], marker_color='#a78bfa'))
        fig_comparison.add_trace(go.Bar(name='Rupturas', x=comparison_data['Escenario'], 
                                       y=comparison_data['Rupturas'], marker_color='#f87171'))
        
        fig_comparison.update_layout(
            barmode='group',
            title="Desglose de Costes: Base vs What-If",
            xaxis_title="Escenario",
            yaxis_title="Coste (€)",
            height=400
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Recomendaciones automáticas
        st.markdown("#### 💡 Recomendaciones Estratégicas")
        
        if sim_demand_multiplier > 1.0:
            # Aumento de demanda
            if lost_base > 0 and lost_sales > lost_base * 1.5:
                pct_increase = ((lost_sales/lost_base-1)*100)
                st.warning(f"⚠️ **Alerta**: Las ventas perdidas aumentaron {pct_increase:.0f}% con el incremento de demanda. Considera **aumentar el ROP a {sim_reorder_point + 10}** para mejorar el nivel de servicio.")
            elif lost_sales > 10:
                st.warning(f"⚠️ **Alerta**: {lost_sales} ventas perdidas con el incremento de demanda. Considera **aumentar el ROP a {sim_reorder_point + 10}** para mejorar el nivel de servicio.")
            
            if total_cost_base > 0 and total_cost > total_cost_base * 1.3:
                pct_cost_increase = ((total_cost/total_cost_base-1)*100)
                st.info(f"📊 Los costes aumentaron {pct_cost_increase:.0f}%. Esto es normal con mayor demanda. El ROI neto {'es positivo ✅' if roi_impact > 0 else 'requiere optimización ⚠️'}.")
            
            if service_level_current < 90:
                st.error(f"🎯 **Nivel de servicio crítico**: {service_level_current:.1f}%. Con {whatif_label} de demanda, necesitas más stock de seguridad. Prueba ROP={sim_reorder_point + 15}.")
        else:
            # Reducción de demanda
            if h_cost_base > 0 and total_holding_cost > h_cost_base * 0.8:
                st.info(f"💰 Oportunidad de ahorro: Con {whatif_label} de demanda, puedes reducir el ROP a {max(5, sim_reorder_point - 5)} para optimizar costes de almacenamiento.")
            
            if lost_base > 0 and lost_sales < lost_base * 0.5:
                pct_reduction = abs((lost_sales/lost_base-1)*100)
                st.success(f"✅ Excelente: Las rupturas se redujeron {pct_reduction:.0f}%. El inventario actual está bien dimensionado para demanda baja.")
            elif lost_sales == 0:
                st.success(f"✅ Perfecto: Sin rupturas de stock. El inventario está bien dimensionado para esta demanda.")
        
        st.markdown("---")

    # --- RESULTADOS CON DISEÑO MEJORADO ---
    col_title, col_help = st.columns([4, 1])
    with col_title:
        st.markdown("### 📊 Resultados de la Simulación")
    with col_help:
        st.markdown("")
        st.markdown("")
        with st.expander("ℹ️ ¿Qué muestran estos resultados?"):
            st.markdown("""
            Esta sección presenta el análisis completo de tu simulación de inventario:
            
            - **Métricas Financieras**: Costes totales desglosados por categoría
            - **Análisis Visual**: Gráficos que te ayudan a identificar dónde están tus mayores costes
            - **KPIs Operativos**: Indicadores clave de rendimiento como nivel de servicio y rotación
            - **Opciones de Exportación**: Descarga los datos para análisis posteriores
            """)
    
    # Métricas principales con tarjetas de colores
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem; font-weight: 500;">💰 Coste Total</p>
            <h2 style="color: white; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;">{total_cost:,.0f}€</h2>
        </div>
        """, unsafe_allow_html=True)
        st.caption("💡 Suma de todos los costes operativos (almacenamiento + pedidos + rupturas)")
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem; font-weight: 500;">📦 Almacenamiento</p>
            <h2 style="color: white; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;">{total_holding_cost:,.0f}€</h2>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"💡 Stock promedio: {avg_inventory:.1f} uds × coste anual")
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem; font-weight: 500;">🚚 Pedidos ({num_orders})</p>
            <h2 style="color: white; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;">{total_ordering_cost:,.0f}€</h2>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"💡 {num_orders} pedidos × coste por pedido")
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #dc2626 0%, #f87171 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem; font-weight: 500;">⚠️ Rupturas ({lost_sales})</p>
            <h2 style="color: white; margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 700;">{total_stockout_cost:,.0f}€</h2>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"💡 {lost_sales} ventas perdidas × coste unitario")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # TABS para organizar el contenido
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Análisis de Costes", "📈 Evolución Stock", "🎯 KPIs", "💾 Exportar"])
    
    with tab1:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            cost_breakdown = pd.DataFrame({
                "Tipo de Coste": ["Almacenamiento", "Pedidos", "Ruptura de Stock"],
                "Importe (€)": [total_holding_cost, total_ordering_cost, total_stockout_cost]
            })
            
            fig_pie = px.pie(
                cost_breakdown, 
                values="Importe (€)", 
                names="Tipo de Coste",
                title="Distribución de Costes",
                hole=0.4,
                color_discrete_sequence=['#06b6d4', '#a78bfa', '#f87171']
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_chart2:
            fig_bar = px.bar(
                cost_breakdown,
                x="Tipo de Coste",
                y="Importe (€)",
                title="Comparativa de Costes",
                color="Tipo de Coste",
                color_discrete_sequence=['#06b6d4', '#a78bfa', '#f87171']
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Insights automáticos
        col_insight_title, col_insight_help = st.columns([5, 1])
        with col_insight_title:
            st.markdown("#### 💡 Insights")
        with col_insight_help:
            with st.popover("❓"):
                st.markdown("""
                **Recomendaciones automáticas** basadas en el análisis de tus costes:
                
                - Si el almacenamiento es alto → Reduce inventario (baja Q o ROP)
                - Si los pedidos son altos → Aumenta Q para pedir menos veces
                - Si las rupturas son altas → Aumenta ROP para más stock de seguridad
                """)
        
        max_cost_type = cost_breakdown.loc[cost_breakdown['Importe (€)'].idxmax(), 'Tipo de Coste']
        max_cost_value = cost_breakdown['Importe (€)'].max()
        max_cost_pct = (max_cost_value / total_cost * 100) if total_cost > 0 else 0
        
        if max_cost_type == "Almacenamiento":
            st.info(f"🔍 **{max_cost_pct:.1f}%** de tus costes son de almacenamiento. Considera reducir Q o ROP.")
        elif max_cost_type == "Pedidos":
            st.info(f"🔍 **{max_cost_pct:.1f}%** de tus costes son pedidos. Aumenta Q para reducir órdenes.")
        else:
            st.warning(f"⚠️ **{max_cost_pct:.1f}%** son pérdidas por ruptura. Aumenta ROP para mejorar disponibilidad.")
    
    with tab2:
        # Gráfico de evolución mejorado
        fig_stock = go.Figure()
        
        fig_stock.add_trace(go.Scatter(
            x=df_results['day'],
            y=df_results['stock'],
            mode='lines',
            name='Stock',
            line=dict(color='#3b82f6', width=2),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        fig_stock.add_hline(
            y=sim_reorder_point, 
            line_dash="dash", 
            line_color="#dc2626",
            annotation_text=f"Punto de Reorden ({sim_reorder_point})",
            annotation_position="right"
        )
        
        fig_stock.add_hline(
            y=avg_inventory,
            line_dash="dot",
            line_color="#7c3aed",
            annotation_text=f"Promedio ({avg_inventory:.1f})",
            annotation_position="right"
        )
        
        fig_stock.update_layout(
            title="Evolución del Inventario",
            xaxis_title="Día",
            yaxis_title="Unidades en Stock",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_stock, use_container_width=True)
        
        # Estadísticas
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Stock Máximo", f"{df_results['stock'].max():.0f} uds")
        with col_stat2:
            st.metric("Stock Mínimo", f"{df_results['stock'].min():.0f} uds")
        with col_stat3:
            st.metric("Stock Promedio", f"{avg_inventory:.1f} uds")
        with col_stat4:
            stockout_days = len(df_results[df_results['stock'] == 0])
            st.metric("Días sin Stock", f"{stockout_days}")
    
    with tab3:
        # KPIs operativos
        total_demand = total_sales + lost_sales
        service_level = (total_sales / total_demand * 100) if total_demand > 0 else 0
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #34d399 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h4 style="margin: 0; color: rgba(255,255,255,0.9); font-weight: 500;">✅ Nivel de Servicio</h4>
                <h2 style="margin: 0.5rem 0 0 0; color: white; font-weight: 700;">{service_level:.1f}%</h2>
                <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">{total_sales} de {total_demand} satisfechas</p>
            </div>
            """, unsafe_allow_html=True)
            with st.popover("ℹ️ ¿Qué es?"):
                st.markdown("**Nivel de Servicio** = % de demanda satisfecha con stock disponible. Un 95% significa que solo el 5% de los clientes no encontraron producto.")
        
        with kpi_col2:
            rotation = (total_sales / avg_inventory) if avg_inventory > 0 else 0
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h4 style="margin: 0; color: rgba(255,255,255,0.9); font-weight: 500;">🔄 Rotación</h4>
                <h2 style="margin: 0.5rem 0 0 0; color: white; font-weight: 700;">{rotation:.2f}</h2>
                <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">veces por año</p>
            </div>
            """, unsafe_allow_html=True)
            with st.popover("ℹ️ ¿Qué es?"):
                st.markdown("**Rotación de Inventario** = Ventas ÷ Stock promedio. Indica cuántas veces renuevas tu inventario al año. Mayor rotación = menos capital inmovilizado.")
        
        with kpi_col3:
            fill_rate = ((SIMULATION_DAYS - len(df_results[df_results['stock'] == 0])) / SIMULATION_DAYS * 100)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h4 style="margin: 0; color: rgba(255,255,255,0.9); font-weight: 500;">📦 Fill Rate</h4>
                <h2 style="margin: 0.5rem 0 0 0; color: white; font-weight: 700;">{fill_rate:.1f}%</h2>
                <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">días con stock</p>
            </div>
            """, unsafe_allow_html=True)
            with st.popover("ℹ️ ¿Qué es?"):
                st.markdown("**Fill Rate** = % de días con stock disponible. Un 98% significa que solo 2% de los días (≈7 días/año) no hubo inventario.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabla resumen
        col_resumen_title, col_resumen_help = st.columns([5, 1])
        with col_resumen_title:
            st.markdown("#### 📋 Resumen Ejecutivo")
        with col_resumen_help:
            with st.popover("❓"):
                st.markdown("Tabla con todas las métricas operativas clave de la simulación. Útil para reportes y análisis rápido.")
        summary_data = pd.DataFrame({
            "Métrica": [
                "Ventas Totales",
                "Ventas Perdidas",
                "Número de Pedidos",
                "Stock Promedio",
                "Días de Cobertura"
            ],
            "Valor": [
                f"{total_sales} uds",
                f"{lost_sales} uds",
                f"{num_orders} órdenes",
                f"{avg_inventory:.1f} uds",
                f"{(avg_inventory / sim_demand_mean):.1f} días" if sim_demand_mean > 0 else "N/A"
            ]
        })
        st.dataframe(summary_data, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("#### 💾 Exportar Resultados")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            export_data = df_results.copy()
            export_data["total_sales"] = total_sales
            export_data["lost_sales"] = lost_sales
            export_data["num_orders"] = num_orders
            export_data["total_cost"] = total_cost
            export_data["holding_cost"] = total_holding_cost
            export_data["ordering_cost"] = total_ordering_cost
            export_data["stockout_cost"] = total_stockout_cost
            
            csv = export_data.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f"simulacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"download_csv_main_{id(df_results)}"
            )
        
        with export_col2:
            report_text = f"""SIMULACIÓN DE INVENTARIO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

CONFIGURACIÓN:
  ROP: {sim_reorder_point} | Q: {sim_order_quantity} | Lead Time: {sim_lead_time} días
  Demanda: {sim_demand_type} (Media: {sim_demand_mean})

RESULTADOS ECONÓMICOS:
  Coste Total: {total_cost:,.2f}€
  - Almacenamiento: {total_holding_cost:,.2f}€
  - Pedidos: {total_ordering_cost:,.2f}€ ({num_orders} órdenes)
  - Rupturas: {total_stockout_cost:,.2f}€

OPERACIONES:
  Ventas: {total_sales} uds | Perdidas: {lost_sales} uds
  Nivel Servicio: {service_level:.1f}%
  Stock Promedio: {avg_inventory:.1f} uds
"""
            
            st.download_button(
                label="📝 Descargar Reporte",
                data=report_text,
                file_name=f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                key=f"download_report_main_{id(df_results)}"
            )
    
    # --- GRÁFICOS ADICIONALES ---
    st.divider()
    col_graficos_title, col_graficos_help = st.columns([5, 1])
    with col_graficos_title:
        st.subheader("📊 Gráficos Adicionales")
    with col_graficos_help:
        st.markdown("")
        with st.popover("ℹ️ Info"):
            st.markdown("""
            **Análisis visual complementario:**
            
            - **Distribución de Stock**: Histograma que muestra la frecuencia de cada nivel de inventario
            - **Días Críticos**: Visualización de cuándo el stock estuvo por debajo del punto de reorden
            """)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Histograma de niveles de stock
        fig_hist = px.histogram(
            df_results, 
            x="stock", 
            title="Distribución de Niveles de Stock",
            labels={"stock": "Unidades en Stock", "count": "Frecuencia (días)"},
            nbins=30,
            color_discrete_sequence=['#3b82f6']
        )
        fig_hist.update_traces(marker=dict(line=dict(color='#1e40af', width=1.5)))
        fig_hist.add_vline(x=sim_reorder_point, line_dash="dash", line_color="#dc2626", 
                          annotation_text="ROP", line_width=2)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col_g2:
        # Días críticos (stock bajo)
        df_results['critico'] = df_results['stock'] <= sim_reorder_point
        critical_days = df_results[df_results['critico']].shape[0]
        
        fig_critical = go.Figure()
        fig_critical.add_trace(go.Scatter(
            x=df_results['day'], 
            y=df_results['stock'],
            mode='lines',
            name='Stock',
            line=dict(color='#3b82f6')
        ))
        fig_critical.add_hline(y=sim_reorder_point, line_dash="dash", line_color="#dc2626",
                              annotation_text=f"ROP ({sim_reorder_point})")
        fig_critical.add_hline(y=0, line_color="darkred", line_width=2,
                              annotation_text="Ruptura")
        fig_critical.update_layout(
            title=f"Días Críticos: {critical_days}/{SIMULATION_DAYS}",
            xaxis_title="Día",
            yaxis_title="Stock"
        )
        st.plotly_chart(fig_critical, use_container_width=True)
    
    # --- ANÁLISIS DE SENSIBILIDAD ---
    if enable_sensitivity:
        st.divider()
        col_sens_title, col_sens_help = st.columns([5, 1])
        with col_sens_title:
            st.subheader("📉 Análisis de Sensibilidad")
            st.markdown("**Cómo varían los costes totales al cambiar parámetros:**")
        with col_sens_help:
            st.markdown("")
            st.markdown("")
            with st.popover("ℹ️ Info"):
                st.markdown("""
                **Análisis de sensibilidad:**
                
                Muestra cómo cambian los costes totales cuando modificas gradualmente ROP o Q, manteniendo los demás parámetros fijos.
                
                Los gráficos te ayudan a:
                - Ver si estás cerca del óptimo
                - Entender cuán sensible es tu sistema a cambios
                - Identificar rangos seguros de operación
                """)
        
        with st.spinner("Calculando sensibilidad..."):
            # Sensibilidad de Q (Cantidad de Pedido)
            q_range = range(max(10, sim_order_quantity - 30), sim_order_quantity + 31, 5)
            q_costs = []
            
            for q_test in q_range:
                df_temp, lost_temp, total_temp, orders_temp = run_simulation(
                    sim_reorder_point, q_test, sim_lead_time,
                    demand_type=sim_demand_type, demand_mean=sim_demand_mean, demand_std=demand_std,
                    seasonality=seasonality
                )
                avg_inv_temp = df_temp['stock'].mean()
                total_cost_temp = (avg_inv_temp * holding_cost_per_unit_year + 
                                 orders_temp * ordering_cost_per_order + 
                                 lost_temp * stockout_cost_per_unit)
                q_costs.append({"Q": q_test, "Coste Total": total_cost_temp})
            
            df_q_sensitivity = pd.DataFrame(q_costs)
            
            # Sensibilidad de ROP (Punto de Reorden)
            rop_range = range(max(0, sim_reorder_point - 15), sim_reorder_point + 16, 3)
            rop_costs = []
            
            for rop_test in rop_range:
                df_temp, lost_temp, total_temp, orders_temp = run_simulation(
                    rop_test, sim_order_quantity, sim_lead_time,
                    demand_type=sim_demand_type, demand_mean=sim_demand_mean, demand_std=demand_std,
                    seasonality=seasonality
                )
                avg_inv_temp = df_temp['stock'].mean()
                total_cost_temp = (avg_inv_temp * holding_cost_per_unit_year + 
                                 orders_temp * ordering_cost_per_order + 
                                 lost_temp * stockout_cost_per_unit)
                rop_costs.append({"ROP": rop_test, "Coste Total": total_cost_temp})
            
            df_rop_sensitivity = pd.DataFrame(rop_costs)
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            fig_q_sens = px.line(
                df_q_sensitivity, 
                x="Q", 
                y="Coste Total",
                title="Sensibilidad: Cantidad de Pedido (Q)",
                markers=True
            )
            fig_q_sens.add_vline(x=sim_order_quantity, line_dash="dash", line_color="red",
                                annotation_text="Q actual")
            if 'eoq' in st.session_state and st.session_state.eoq > 0:
                fig_q_sens.add_vline(x=st.session_state.eoq, line_dash="dot", line_color="green",
                                    annotation_text="EOQ")
            st.plotly_chart(fig_q_sens, use_container_width=True)
        
        with col_s2:
            fig_rop_sens = px.line(
                df_rop_sensitivity, 
                x="ROP", 
                y="Coste Total",
                title="Sensibilidad: Punto de Reorden (ROP)",
                markers=True
            )
            fig_rop_sens.add_vline(x=sim_reorder_point, line_dash="dash", line_color="red",
                                  annotation_text="ROP actual")
            st.plotly_chart(fig_rop_sens, use_container_width=True)
        
        # Recomendaciones
        optimal_q = df_q_sensitivity.loc[df_q_sensitivity['Coste Total'].idxmin(), 'Q']
        optimal_rop = df_rop_sensitivity.loc[df_rop_sensitivity['Coste Total'].idxmin(), 'ROP']
        
        st.info(f"🎯 **Recomendaciones basadas en sensibilidad:**\n\n"
                f"- Cantidad de Pedido óptima: **{optimal_q}** unidades\n\n"
                f"- Punto de Reorden óptimo: **{optimal_rop}** unidades")
    
    # --- REPORTE EXPORTABLE ---
    st.divider()
    col_reporte_title, col_reporte_help = st.columns([5, 1])
    with col_reporte_title:
        st.subheader("📄 Generar Reporte Completo")
    with col_reporte_help:
        st.markdown("")
        with st.popover("ℹ️ Info"):
            st.markdown("""
            **Reportes descargables:**
            
            - **Excel**: Incluye 3 hojas (Resumen, Datos diarios, Parámetros)
            - **TXT**: Reporte de texto plano para documentación rápida
            
            Ideal para presentaciones, auditorías o análisis posteriores en otras herramientas.
            """)
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        # Reporte Excel
        buffer_excel = io.BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            # Hoja 1: Resumen Financiero (con símbolo €)
            summary_data = {
                'Métrica': ['💰 Coste Total', '📦 Coste Almacenamiento', '🚚 Coste Pedidos', 
                           '⚠️ Coste Ruptura', '✅ Nivel de Servicio', '📊 Ventas Totales', 
                           '❌ Ventas Perdidas', '📋 Número de Pedidos', '📈 Stock Promedio'],
                'Valor': [f"{total_cost:,.2f} €", f"{total_holding_cost:,.2f} €", 
                         f"{total_ordering_cost:,.2f} €", f"{total_stockout_cost:,.2f} €",
                         f"{service_level:.1f}%", f"{total_sales} uds", f"{lost_sales} uds", 
                         f"{num_orders} órdenes", f"{avg_inventory:.2f} uds"]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Resumen Financiero', index=False)
            
            # Hoja 2: Datos diarios
            export_data.to_excel(writer, sheet_name='Datos Diarios', index=False)
            
            # Hoja 3: Parámetros
            params_data = {
                'Parámetro': ['Punto de Reorden (ROP)', 'Cantidad de Pedido (Q)', 
                             'Lead Time', 'Tipo Demanda', 'Demanda Media', 
                             'Coste Pedido', 'Coste Almacenamiento/año', 'Coste Ruptura'],
                'Valor': [f"{sim_reorder_point} uds", f"{sim_order_quantity} uds", 
                         f"{sim_lead_time} días", sim_demand_type, 
                         f"{sim_demand_mean} uds/día", f"{ordering_cost_per_order:.2f} €", 
                         f"{holding_cost_per_unit_year:.2f} €", f"{stockout_cost_per_unit:.2f} €"]
            }
            pd.DataFrame(params_data).to_excel(writer, sheet_name='Parámetros', index=False)
        
        buffer_excel.seek(0)
        
        st.download_button(
            label="📊 Descargar Reporte Excel",
            data=buffer_excel,
            file_name=f"reporte_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel_report"
        )
    
    with col_r2:
        # Reporte de texto
        report_text = f"""
REPORTE DE SIMULACIÓN DE INVENTARIO
{'='*50}
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PARÁMETROS DE CONFIGURACIÓN
{'-'*50}
Punto de Reorden (ROP): {sim_reorder_point} unidades
Cantidad de Pedido (Q): {sim_order_quantity} unidades
Lead Time: {sim_lead_time} días
Tipo de Demanda: {sim_demand_type}
Demanda Media: {sim_demand_mean} uds/día

COSTES
{'-'*50}
Coste por Pedido: {ordering_cost_per_order:.2f} €
Coste Almacenamiento/año: {holding_cost_per_unit_year:.2f} €
Coste por Ruptura: {stockout_cost_per_unit:.2f} €

RESULTADOS
{'-'*50}
Coste Total: {total_cost:,.2f} €
  - Almacenamiento: {total_holding_cost:,.2f} €
  - Pedidos: {total_ordering_cost:,.2f} €
  - Rupturas: {total_stockout_cost:,.2f} €

OPERACIONES
{'-'*50}
Ventas Totales: {total_sales} unidades
Ventas Perdidas: {lost_sales} unidades
Nivel de Servicio: {service_level:.2f}%
Número de Pedidos: {num_orders}
Stock Promedio: {avg_inventory:.2f} unidades

{'='*50}
"""
        
        st.download_button(
            label="📝 Descargar Reporte TXT",
            data=report_text,
            file_name=f"reporte_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_txt_report"
        )