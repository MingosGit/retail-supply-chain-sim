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

Una **aplicación web interactiva** que simula la cadena de suministro de un negocio retail, permitiéndote experimentar con diferentes políticas de inventario sin riesgo financiero real.

### 💡 El Problema

Las empresas retail enfrentan un dilema constante:
- 📈 **Demasiado stock** → Costes de almacenamiento elevados
- 📉 **Poco stock** → Pérdida de ventas y clientes insatisfechos
- ⏱️ **Lead times variables** → Incertidumbre en la reposición

### ✅ La Solución

Este simulador te permite:
- 🔬 **Experimentar** con diferentes parámetros de inventario (punto de reorden, cantidad de pedido, lead time)
- 📊 **Visualizar** el impacto financiero en tiempo real
- 🎲 **Simular** 365 días de operación en segundos
- 💰 **Optimizar** el balance entre costes y servicio al cliente

---

## 🚀 Características Principales

| Característica | Descripción |
|---------------|-------------|
| 🎲 **Simulación Estocástica** | Demanda diaria aleatoria para modelar la realidad del mercado |
| ⚙️ **Parámetros Configurables** | Ajusta punto de reorden, cantidad de pedido y lead time |
| 📈 **KPIs en Tiempo Real** | Visualiza costes de almacenamiento, pedidos y rupturas de stock |
| 🎯 **Nivel de Servicio** | Mide el % de demanda satisfecha desde inventario |
| 📊 **Gráficos Interactivos** | Evolución del stock durante 365 días con Plotly |
| 💻 **Interfaz Intuitiva** | Streamlit para una experiencia de usuario fluida |

---

## 🧠 Conceptos Teóricos Aplicados

Este proyecto fusiona **Ingeniería Informática** y **Dirección de Operaciones**:

### 📚 Fundamentos Clave

| Concepto | Implementación |
|----------|----------------|
| **🔄 Discrete Event Simulation** | Motor SimPy para eventos temporales y procesos concurrentes |
| **💰 Optimización de Costes** | Minimización de: Holding + Ordering + Stockout costs |
| **📦 Política (Q, R)** | Punto de Reorden (ROP) + Cantidad Económica (EOQ) |
| **🎲 Procesos Estocásticos** | Demanda aleatoria con distribución uniforme |

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
| 📈 **Visualización** | Plotly Express | Gráficos interactivos |
| 🌐 **Frontend** | Streamlit | Interfaz web responsive |

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

1. **Ajusta los parámetros** en el panel lateral:
   - 📍 **Punto de Reorden (ROP)**: Stock mínimo antes de hacer un nuevo pedido
   - 📦 **Cantidad de Pedido (Q)**: Unidades a pedir cada vez
   - ⏱️ **Lead Time**: Días que tarda el proveedor en entregar

2. **Haz clic en "Ejecutar Simulación"**

3. **Analiza los resultados**:
   - 💵 Costes totales desglosados
   - 📊 Nivel de servicio (%)
   - 📈 Gráfico de evolución del stock

4. **Experimenta** con diferentes combinaciones para encontrar el óptimo

---

## 📊 Metodología de Análisis

El simulador modela **365 días de operación** para proporcionar insights accionables:

### KPIs Monitorizados

| Métrica | Descripción | Objetivo |
|---------|-------------|----------|
| 💰 **Coste de Almacenamiento** | Coste por mantener inventario | Minimizar sin sacrificar servicio |
| 📦 **Coste de Pedidos** | Coste fijo por cada orden al proveedor | Reducir frecuencia sin desabastecimiento |
| ⚠️ **Coste de Ruptura** | Ventas perdidas por falta de stock | Eliminar completamente |
| 🎯 **Nivel de Servicio** | % demanda satisfecha desde stock | Maximizar (objetivo: >95%) |

### Visualizaciones

- 📈 **Gráfico de Stock vs Tiempo**: Observa los ciclos de inventario, puntos de pedido y periodos críticos
- 💡 **Desglose de Costes**: Identifica qué componente impacta más tu cuenta de resultados

---

## 🔬 Caso de Uso Ejemplo

**Escenario**: Tienda de ropa que vende camisetas

```python
# Parámetros de entrada
Punto de Reorden (ROP): 15 unidades
Cantidad de Pedido (Q): 50 unidades
Lead Time: 5 días
Stock Inicial: 50 unidades

# Demanda diaria: Aleatoria entre 0-5 unidades
```

**Resultado esperado**:
- Nivel de servicio: ~98%
- Costes optimizados
- Identificación de mejoras en la política de inventario

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