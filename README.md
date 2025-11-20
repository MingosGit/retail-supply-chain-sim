# 📦 Retail Supply Chain Simulator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![SimPy](https://img.shields.io/badge/SimPy-Discrete%20Event%20Simulation-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20UI-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

### 🎯 Optimiza tu inventario con simulación de eventos discretos

*Toma decisiones basadas en datos. Minimiza costes. Maximiza el nivel de servicio.*

[🚀 Instalación](#-instalación-y-uso-local) • [📊 Características](#-características-principales) • [🛠️ Stack Tecnológico](#️-stack-tecnológico)

</div>

---

## 🌟 ¿Qué es este proyecto?

Una **aplicación web interactiva de última generación** que simula la cadena de suministro de un negocio retail, permitiéndote experimentar con diferentes políticas de inventario sin riesgo financiero real.

### 💡 El Problema

Las empresas retail enfrentan un dilema constante:
- 📈 **Demasiado stock** → Costes de almacenamiento elevados
- 📉 **Poco stock** → Pérdida de ventas y clientes insatisfechos
- ⏱️ **Lead times variables** → Incertidumbre en la reposición
- ⚙️ **Parámetros complejos** → Difícil encontrar la configuración óptima manualmente

### ✅ La Solución

Este simulador te permite:
- 🔬 **Experimentar** con diferentes parámetros de inventario (punto de reorden hasta 250, cantidad de pedido hasta 500, lead time, patrones de demanda)
- 📊 **Visualizar** el impacto financiero en tiempo real con gráficos interactivos organizados en pestañas
- 🎲 **Simular** 365 días de operación en segundos
- 💰 **Optimizar automáticamente** el balance entre costes y servicio al cliente con algoritmo Grid Search
- 📈 **Analizar sensibilidad** de parámetros para identificar rangos óptimos
- 💾 **Exportar reportes** completos en Excel y TXT para presentaciones

---

## 🚀 Características Principales

| Característica | Descripción |
|---------------|-------------|
| 🎲 **Simulación Estocástica Avanzada** | Demanda con 3 distribuciones (Uniforme, Normal, Poisson) + parámetros configurables |
| ⚙️ **Parámetros Configurables** | ROP hasta 250, Q hasta 500, lead time 1-14 días, stock inicial, costes personalizables |
| 🤖 **Optimizador Automático** | Algoritmo Grid Search que encuentra la configuración óptima automáticamente |
| 📊 **Interfaz Multi-Pestaña** | 4 tabs organizadas: Análisis de Costes, Evolución Stock, KPIs, Exportar |
| 📈 **Dashboard de KPIs** | Nivel de servicio, rotación, fill rate, días sin stock, con tarjetas con gradientes |
| 🎯 **Análisis de Sensibilidad** | Gráficos que muestran impacto de ROP/Q en costes totales |
| 💡 **Tooltips Interactivos** | Símbolos de ayuda (ℹ️/❓) en todos los controles y secciones con explicaciones detalladas |
| 💾 **Exportación Avanzada** | Reportes completos en Excel (3 hojas) y TXT para documentación |
| 📉 **Visualizaciones Plotly** | Gráficos interactivos: líneas, barras, histogramas, scatter, pie charts |
| 🎨 **Diseño Profesional** | Gradientes azules coherentes, métricas destacadas, UI moderna |

---

## 🧠 Conceptos Teóricos Aplicados

Este proyecto fusiona **Ingeniería Informática** y **Dirección de Operaciones**:

### 📚 Fundamentos Clave

| Concepto | Implementación |
|----------|----------------|
| **🔄 Discrete Event Simulation** | Motor SimPy para eventos temporales y procesos concurrentes |
| **💰 Optimización de Costes** | Minimización de: Holding + Ordering + Stockout costs |
| **🤖 Grid Search Optimization** | Búsqueda exhaustiva de parámetros óptimos (ROP, Q) con restricciones configurables |
| **📦 Política (Q, R)** | Punto de Reorden (ROP 0-250) + Cantidad Económica (Q 10-500) |
| **🎲 Procesos Estocásticos** | Demanda aleatoria con 3 distribuciones: Uniforme, Normal, Poisson |
| **📊 Análisis de Sensibilidad** | Evaluación del impacto de parámetros en costes mediante gráficos 2D |

### 💡 Fórmula de Costes Totales

```
Total Cost = (Holding Cost × Avg. Inventory) + (Ordering Cost × # Orders) + (Stockout Cost × Lost Sales)
```

---

## 🛠️ Stack Tecnológico

<div align="center">

| Categoría | Tecnología | Uso |
|-----------|-----------|-----|
| 🐍 **Backend** | Python 3.12+ | Lenguaje principal |
| ⚙️ **Simulación** | SimPy | Motor de eventos discretos |
| 📊 **Datos** | Pandas, NumPy | Procesamiento y análisis |
| 📈 **Visualización** | Plotly Express/GO | Gráficos interactivos (líneas, barras, histogramas, scatter, pie) |
| 🌐 **Frontend** | Streamlit | Interfaz web con tabs, popovers, expanders, métricas |
| 💾 **Exportación** | io, openpyxl | Generación de reportes Excel/TXT |
| 🎨 **Estilizado** | Custom CSS | Gradientes, sombras, diseño moderno |

</div>

---

## 📁 Estructura del Proyecto

```
retail-supply-chain-sim/
│
├── 📄 app.py                    # 🎨 Interfaz Streamlit (UI/UX)
├── 📄 simulation.py             # 🧠 Motor de simulación (lógica core)
├── 📄 requirements.txt          # 📦 Dependencias Python
├── 📄 README.md                 # 📖 Este archivo
└── 📄 LICENSE                   # ⚖️ Licencia MIT
```

### 🔍 Descripción de Archivos

- **`app.py`**: Controlador de la interfaz. Gestiona inputs del usuario, ejecuta simulaciones y renderiza resultados (KPIs, gráficos).
- **`simulation.py`**: Núcleo lógico. Define la clase `ClothingStoreSimulation` con procesos de demanda, reposición y observación del sistema.

---

## ⚡ Instalación y Uso Local

### Requisitos Previos
- Python 3.12 o superior
- pip (gestor de paquetes)
- Git

### 🚀 Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/MingosGit/retail-supply-chain-sim.git
   cd retail-supply-chain-sim
   ```

2. **Crear y activar entorno virtual**
   ```bash
   # Crear entorno virtual
   python -m venv venv
   
   # Activar (Windows)
   .\venv\Scripts\activate
   
   # Activar (macOS/Linux)
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación** 🎉
   ```bash
   streamlit run app.py
   ```

5. **Abrir en el navegador**
   
   La aplicación se abrirá automáticamente en `http://localhost:8501`

---

## 🎮 Cómo Usar el Simulador

### 📋 Modo Manual

1. **Ajusta los parámetros** en el panel lateral (todos con tooltips explicativos ℹ️):
   - 📍 **Punto de Reorden (ROP)**: 0-250 unidades (stock crítico)
   - 📦 **Cantidad de Pedido (Q)**: 10-500 unidades (lote económico)
   - ⏱️ **Lead Time**: 1-14 días (tiempo de entrega)
   - 📊 **Patrón de Demanda**: Uniforme, Normal o Poisson
   - 💰 **Costes**: Almacenamiento, pedido, ruptura (personalizables)

2. **Haz clic en "▶️ Ejecutar Simulación"**

3. **Analiza los resultados en 4 pestañas**:
   - **📊 Análisis de Costes**: Desglose en pie chart + tarjetas métricas con gradientes
   - **📈 Evolución Stock**: Gráfico temporal interactivo con eventos de pedidos/rupturas
   - **🎯 KPIs**: Nivel servicio, rotación, fill rate con popovers explicativos
   - **💾 Exportar**: Descarga CSV con datos completos

4. **Visualiza insights adicionales**:
   - 📊 Histograma de distribución de stock
   - 🔥 Días críticos (stock más bajo)
   - 📉 Análisis de sensibilidad (impacto de ROP/Q)

5. **Descarga reportes** completos en Excel (3 hojas) o TXT

### 🤖 Modo Optimizador Automático

1. **Activa el optimizador** en el sidebar
2. **Configura rangos de búsqueda**:
   - ROP: Mínimo, Máximo, Paso
   - Q: Mínimo, Máximo, Paso
3. **Ejecuta Grid Search** → Encuentra automáticamente la configuración con menor coste total
4. **Aplica configuración óptima** con un clic
5. **Analiza tabla comparativa** de todas las combinaciones probadas

---

## 📊 Metodología de Análisis

El simulador modela **365 días de operación** para proporcionar insights accionables:

### KPIs Monitorizados

| Métrica | Descripción | Objetivo |
|---------|-------------|----------|
| 💰 **Coste de Almacenamiento** | Coste por mantener inventario (Holding Cost × Stock Promedio) | Minimizar sin sacrificar servicio |
| 📦 **Coste de Pedidos** | Coste fijo por cada orden al proveedor (Ordering Cost × Núm. Pedidos) | Reducir frecuencia sin desabastecimiento |
| ⚠️ **Coste de Ruptura** | Ventas perdidas por falta de stock (Stockout Cost × Lost Sales) | Eliminar completamente |
| 🎯 **Nivel de Servicio** | % demanda satisfecha desde stock | Maximizar (objetivo: >95%) |
| 🔄 **Rotación de Inventario** | Ventas Totales ÷ Stock Promedio | Mayor rotación = menos capital inmovilizado |
| 📦 **Fill Rate** | % de días con stock disponible | Disponibilidad del producto (objetivo: >98%) |
| ⏱️ **Días de Cobertura** | Stock Promedio ÷ Demanda Diaria Media | Autonomía del inventario |
| 📉 **Días sin Stock** | Total de días con inventario = 0 | Minimizar (afecta satisfacción del cliente) |

### Visualizaciones

- 📈 **Gráfico de Stock vs Tiempo**: Evolución diaria con marcadores de eventos (pedidos, rupturas, ROP)
- 🥧 **Pie Chart de Costes**: Desglose porcentual de almacenamiento/pedidos/rupturas
- 📊 **Histograma de Distribución**: Frecuencia de niveles de stock con bordes y colores profesionales
- 🔥 **Días Críticos**: Scatter plot de los 30 días con menor stock
- 📉 **Análisis de Sensibilidad**: Gráficos de línea mostrando impacto de ROP y Q en coste total
- 📊 **Tabla Comparativa**: Resultados del Grid Search con todas las combinaciones evaluadas
- 💳 **Tarjetas Métricas**: KPIs destacados con gradientes de colores (verde/azul/amarillo) y popovers

---

## 🔬 Caso de Uso Ejemplo

**Escenario**: Tienda de ropa que vende camisetas

```python
# Parámetros de entrada
Punto de Reorden (ROP): 15 unidades (rango: 0-250)
Cantidad de Pedido (Q): 50 unidades (rango: 10-500)
Lead Time: 5 días
Stock Inicial: 50 unidades
Patrón de Demanda: Uniforme (0-5 unidades/día)
Coste Almacenamiento: 1€/ud/día
Coste Pedido: 50€/orden
Coste Ruptura: 10€/venta perdida
```

**Resultados obtenidos** (ejemplo):
- ✅ Nivel de servicio: 98.2%
- 🔄 Rotación: 4.3x/año
- 📦 Fill rate: 97.5%
- 💰 Coste total: 3,245€ (67% almacenamiento, 28% pedidos, 5% rupturas)
- 📊 Número de pedidos: 14 órdenes
- 📉 Días sin stock: 9 días

**Optimizador automático sugiere**: ROP=20, Q=45 → Coste reducido a 2,890€ (-11%)

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el simulador:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Jose Candon Rubio**

- 🐙 GitHub: [@MingosGit](https://github.com/MingosGit)
- 📧 Email: [josecandonrubio@gmail.com]

---

## 🙏 Agradecimientos

- 📚 SimPy Documentation - Por la excelente librería de simulación
- 🎨 Streamlit Team - Por facilitar la creación de aplicaciones web
- 📊 Plotly - Por las visualizaciones interactivas

---

<div align="center">

### ⭐ Si este proyecto te ha sido útil, considera darle una estrella

**[⬆ Volver arriba](#-retail-supply-chain-simulator)**

</div>