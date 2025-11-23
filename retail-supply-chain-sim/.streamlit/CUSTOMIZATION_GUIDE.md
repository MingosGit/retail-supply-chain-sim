# 🎨 Guía de Personalización de Colores

Esta guía te ayudará a personalizar la paleta de colores del **Retail Supply Chain Simulator** para adaptarla a la identidad visual de tu empresa.

## 📋 Índice

1. [Paleta Actual](#paleta-actual)
2. [Cómo Cambiar Colores](#cómo-cambiar-colores)
3. [Paletas Pre-definidas](#paletas-pre-definidas)
4. [Verificación de Accesibilidad](#verificación-de-accesibilidad)

---

## 🎨 Paleta Actual

### Tema Principal (config.toml)

```toml
[theme]
primaryColor = "#1E3A8A"              # Azul corporativo oscuro
backgroundColor = "#FFFFFF"            # Blanco
secondaryBackgroundColor = "#F8FAFC"  # Gris muy claro
textColor = "#1E293B"                 # Gris carbón
```

### Colores de Gráficos (app.py)

| Uso | Color | HEX |
|-----|-------|-----|
| Líneas principales | Azul brillante | `#3b82f6` |
| Costes almacenamiento | Cyan | `#06b6d4` |
| Costes pedido | Púrpura claro | `#a78bfa` |
| Costes ruptura | Rojo | `#dc2626` |
| Métricas positivas | Verde | `#10b981` |
| Advertencias | Ámbar | `#f59e0b` |
| Alertas | Rojo | `#dc2626` |

---

## 🔧 Cómo Cambiar Colores

### 1️⃣ Modificar el Tema Principal

**Archivo**: `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#TU_COLOR_PRIMARIO"
backgroundColor = "#TU_COLOR_FONDO"
secondaryBackgroundColor = "#TU_COLOR_FONDO_SECUNDARIO"
textColor = "#TU_COLOR_TEXTO"
font = "sans serif"  # Opciones: "sans serif", "serif", "monospace"
```

**Ejemplo - Tema Verde Corporativo**:
```toml
[theme]
primaryColor = "#047857"              # Verde oscuro
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0FDF4"  # Verde muy claro
textColor = "#064E3B"
```

### 2️⃣ Modificar Colores de Gráficos

**Archivo**: `app.py`

**Buscar y reemplazar los códigos HEX** según tus preferencias:

#### Gradientes de Encabezado (línea ~22, ~53)
```python
# ANTES
background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);

# DESPUÉS (ejemplo verde)
background: linear-gradient(135deg, #047857 0%, #10b981 100%);
```

#### Colores de Métricas (líneas ~535-580)
```python
# Tarjeta de costes de almacenamiento (línea ~546)
background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);

# Tarjeta de costes de pedido (línea ~557)
background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);

# Tarjeta de costes de ruptura (línea ~568)
background: linear-gradient(135deg, #dc2626 0%, #f87171 100%);
```

#### Gráficos Plotly (líneas ~597, ~648, etc.)
```python
# Pie chart (línea ~597)
color_discrete_sequence=['#06b6d4', '#a78bfa', '#f87171']

# Línea de stock (línea ~648)
line=dict(color='#3b82f6', width=2)

# Línea de ROP (línea ~656)
line_color="#dc2626"
```

### 3️⃣ Reiniciar Streamlit

```bash
# Detener la aplicación (Ctrl+C en terminal)
# Volver a ejecutar
streamlit run app.py
```

---

## 🎨 Paletas Pre-definidas

### 🔵 Azul Corporativo (Actual)
```toml
primaryColor = "#1E3A8A"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8FAFC"
textColor = "#1E293B"
```
**Uso**: Empresas tecnológicas, consultoría, finanzas

---

### 🟢 Verde Sostenible
```toml
primaryColor = "#047857"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0FDF4"
textColor = "#064E3B"
```
**Uso**: Empresas eco-friendly, agricultura, salud

---

### 🟣 Púrpura Creativo
```toml
primaryColor = "#7C3AED"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#FAF5FF"
textColor = "#4C1D95"
```
**Uso**: Startups, diseño, educación

---

### 🟠 Naranja Energético
```toml
primaryColor = "#EA580C"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#FFF7ED"
textColor = "#7C2D12"
```
**Uso**: Retail, logística, deportes

---

### ⚫ Gris Minimalista
```toml
primaryColor = "#374151"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F9FAFB"
textColor = "#111827"
```
**Uso**: Luxury brands, arquitectura, legal

---

### 🔴 Rojo Impactante
```toml
primaryColor = "#DC2626"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#FEF2F2"
textColor = "#7F1D1D"
```
**Uso**: Urgencias, alimentación, eventos

---

## ♿ Verificación de Accesibilidad

### Herramientas Recomendadas

1. **[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)**
   - Introduce tu color de texto y fondo
   - Verifica que cumpla **WCAG AA** (ratio ≥ 4.5:1)

2. **[Coolors Palette Generator](https://coolors.co/)**
   - Genera paletas completas
   - Verifica armonía de colores

3. **[Adobe Color](https://color.adobe.com/)**
   - Crea esquemas desde imágenes
   - Exporta códigos HEX

### Ratios Mínimos WCAG AA

| Elemento | Ratio Mínimo | Ejemplo Válido |
|----------|--------------|----------------|
| Texto normal | 4.5:1 | `#1E293B` sobre `#FFFFFF` = 14.7:1 ✅ |
| Texto grande (18pt+) | 3:1 | `#3b82f6` sobre `#FFFFFF` = 4.6:1 ✅ |
| Elementos UI | 3:1 | `#1E3A8A` sobre `#F8FAFC` = 12.1:1 ✅ |

### 🧪 Prueba de Accesibilidad

```python
# Simula daltonismo en Chrome DevTools:
# 1. Abre DevTools (F12)
# 2. Cmd/Ctrl + Shift + P
# 3. Escribe "Emulate vision deficiencies"
# 4. Selecciona tipo (Protanopia, Deuteranopia, etc.)
```

---

## 🎯 Mejores Prácticas

### ✅ Recomendaciones

1. **Coherencia**: Mantén la misma paleta en toda la aplicación
2. **Contraste**: Asegura ratios WCAG AA mínimo
3. **Jerarquía**: Usa color primario para acciones principales
4. **Semántica**: 
   - 🟢 Verde = Éxito, positivo
   - 🟡 Amarillo = Advertencia
   - 🔴 Rojo = Error, crítico
   - 🔵 Azul = Información
5. **Pruebas**: Valida en múltiples dispositivos y navegadores

### ❌ Evitar

1. Demasiados colores primarios (máx. 2-3)
2. Colores muy saturados para fondos
3. Gradientes con colores muy contrastantes
4. Texto gris claro sobre gris claro
5. Dependencia únicamente del color (usar iconos también)

---

## 🔄 Flujo de Personalización Completo

```bash
# 1. Edita config.toml
nano .streamlit/config.toml

# 2. Edita app.py (opcional, si cambias gráficos)
nano app.py

# 3. Verifica accesibilidad
# → Usar WebAIM Contrast Checker

# 4. Reinicia Streamlit
streamlit run app.py

# 5. Prueba en navegador
# → Verifica colores en Chrome, Firefox, Safari

# 6. Exporta paleta (opcional)
# → Documenta códigos HEX en README
```

---

## 📚 Recursos Adicionales

- **[Streamlit Theming Docs](https://docs.streamlit.io/library/advanced-features/theming)**
- **[Material Design Color Tool](https://material.io/resources/color/)**
- **[Paletton](https://paletton.com/)** - Generador de esquemas de color
- **[ColorBox](https://colorbox.io/)** - Generador de paletas accesibles
- **[Color Hunt](https://colorhunt.co/)** - Inspiración de paletas

---

## 🆘 Solución de Problemas

### Problema: Los cambios no se reflejan

**Solución**:
```bash
# 1. Limpia caché de Streamlit
streamlit cache clear

# 2. Reinicia la aplicación
# Ctrl+C en terminal
streamlit run app.py

# 3. Limpia caché del navegador
# Ctrl+Shift+R (hard reload)
```

### Problema: Colores se ven diferentes en otro monitor

**Solución**:
- Usa perfiles de color sRGB (estándar web)
- Prueba en múltiples dispositivos
- Evita colores muy saturados (>80% saturation)

### Problema: Gradientes no se ven suaves

**Solución**:
```css
/* En app.py, añade más pasos al gradiente */
background: linear-gradient(135deg, 
    #1e3a8a 0%, 
    #2563eb 50%,
    #3b82f6 100%);
```

---

**Versión**: 1.0  
**Autor**: Jose Candon Rubio  
**Última actualización**: Noviembre 2025
