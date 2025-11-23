# 🎨 Paleta de Colores - Retail Supply Chain Simulator

## Referencia Visual Completa

Esta guía proporciona una referencia rápida de todos los colores utilizados en el simulador.

---

## 🎯 Tema Principal (Streamlit)

### Configuración en `config.toml`

```toml
[theme]
primaryColor = "#1E3A8A"              # Azul corporativo oscuro
backgroundColor = "#FFFFFF"            # Blanco nítido
secondaryBackgroundColor = "#F8FAFC"  # Gris claro elegante
textColor = "#1E293B"                 # Gris carbón
font = "sans serif"
```

### Vista Previa

| Color | HEX | RGB | Uso |
|-------|-----|-----|-----|
| ![#1E3A8A](https://via.placeholder.com/50x30/1E3A8A/FFFFFF?text=+) | `#1E3A8A` | `rgb(30, 58, 138)` | Botones, sliders, elementos interactivos |
| ![#FFFFFF](https://via.placeholder.com/50x30/FFFFFF/000000?text=+) | `#FFFFFF` | `rgb(255, 255, 255)` | Fondo general |
| ![#F8FAFC](https://via.placeholder.com/50x30/F8FAFC/000000?text=+) | `#F8FAFC` | `rgb(248, 250, 252)` | Fondos de tarjetas, sidebar |
| ![#1E293B](https://via.placeholder.com/50x30/1E293B/FFFFFF?text=+) | `#1E293B` | `rgb(30, 41, 59)` | Texto principal |

---

## 📊 Paleta de Gráficos

### Gradientes de Encabezados

| Gradiente | Inicio | Fin | Uso |
|-----------|--------|-----|-----|
| **Encabezado Principal** | ![#1E3A8A](https://via.placeholder.com/30x30/1E3A8A/FFFFFF?text=+) `#1E3A8A` | ![#3b82f6](https://via.placeholder.com/30x30/3b82f6/FFFFFF?text=+) `#3b82f6` | Título principal app |
| **Sidebar Header** | ![#1E3A8A](https://via.placeholder.com/30x30/1E3A8A/FFFFFF?text=+) `#1E3A8A` | ![#3b82f6](https://via.placeholder.com/30x30/3b82f6/FFFFFF?text=+) `#3b82f6` | Encabezado configuración |

### Tarjetas de Métricas (KPIs)

| Métrica | Gradiente Inicio | Gradiente Fin | Ubicación |
|---------|------------------|---------------|-----------|
| **Coste Total** | ![#1E40AF](https://via.placeholder.com/30x30/1E40AF/FFFFFF?text=+) `#1E40AF` | ![#3b82f6](https://via.placeholder.com/30x30/3b82f6/FFFFFF?text=+) `#3b82f6` | Línea ~535 |
| **Holding Cost** | ![#0891B2](https://via.placeholder.com/30x30/0891B2/FFFFFF?text=+) `#0891B2` | ![#06b6d4](https://via.placeholder.com/30x30/06b6d4/FFFFFF?text=+) `#06b6d4` | Línea ~546 |
| **Ordering Cost** | ![#7C3AED](https://via.placeholder.com/30x30/7C3AED/FFFFFF?text=+) `#7C3AED` | ![#a78bfa](https://via.placeholder.com/30x30/a78bfa/FFFFFF?text=+) `#a78bfa` | Línea ~557 |
| **Stockout Cost** | ![#DC2626](https://via.placeholder.com/30x30/DC2626/FFFFFF?text=+) `#DC2626` | ![#f87171](https://via.placeholder.com/30x30/f87171/FFFFFF?text=+) `#f87171` | Línea ~568 |

### Tarjetas de KPIs (Tab KPIs)

| KPI | Gradiente Inicio | Gradiente Fin | Semántica |
|-----|------------------|---------------|-----------|
| **Nivel Servicio** | ![#10B981](https://via.placeholder.com/30x30/10B981/FFFFFF?text=+) `#10B981` | ![#34d399](https://via.placeholder.com/30x30/34d399/FFFFFF?text=+) `#34d399` | Verde = Positivo |
| **Rotación** | ![#3b82f6](https://via.placeholder.com/30x30/3b82f6/FFFFFF?text=+) `#3b82f6` | ![#60a5fa](https://via.placeholder.com/30x30/60a5fa/FFFFFF?text=+) `#60a5fa` | Azul = Información |
| **Fill Rate** | ![#F59E0B](https://via.placeholder.com/30x30/F59E0B/FFFFFF?text=+) `#F59E0B` | ![#fbbf24](https://via.placeholder.com/30x30/fbbf24/FFFFFF?text=+) `#fbbf24` | Ámbar = Precaución |

### Gráficos Plotly

| Elemento | Color | HEX | RGB | Uso |
|----------|-------|-----|-----|-----|
| **Stock Line** | ![#3b82f6](https://via.placeholder.com/30x30/3b82f6/FFFFFF?text=+) | `#3b82f6` | `rgb(59, 130, 246)` | Línea principal stock |
| **ROP Line** | ![#DC2626](https://via.placeholder.com/30x30/DC2626/FFFFFF?text=+) | `#DC2626` | `rgb(220, 38, 38)` | Línea punto reorden |
| **Border Histogram** | ![#1E40AF](https://via.placeholder.com/30x30/1E40AF/FFFFFF?text=+) | `#1E40AF` | `rgb(30, 64, 175)` | Bordes histograma |

### Pie Chart - Distribución de Costes

| Segmento | Color | HEX | RGB |
|----------|-------|-----|-----|
| **Holding** | ![#06b6d4](https://via.placeholder.com/30x30/06b6d4/FFFFFF?text=+) | `#06b6d4` | `rgb(6, 182, 212)` |
| **Ordering** | ![#a78bfa](https://via.placeholder.com/30x30/a78bfa/FFFFFF?text=+) | `#a78bfa` | `rgb(167, 139, 250)` |
| **Stockout** | ![#f87171](https://via.placeholder.com/30x30/f87171/FFFFFF?text=+) | `#f87171` | `rgb(248, 113, 113)` |

---

## 🎨 Códigos CSS Completos

### Gradiente Encabezado Principal

```css
background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
padding: 2rem;
border-radius: 10px;
margin-bottom: 2rem;
color: white;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
```

### Gradiente Sidebar

```css
background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
padding: 1.5rem;
border-radius: 10px;
margin-bottom: 1.5rem;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
```

### Tarjeta Métrica (Template)

```css
background: linear-gradient(135deg, #COLOR_INICIO 0%, #COLOR_FIN 100%);
padding: 1.5rem;
border-radius: 10px;
color: white;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
text-align: center;
```

---

## 📐 Especificaciones Técnicas

### Ratios de Contraste (WCAG AA)

| Combinación | Ratio | Cumple AA | Cumple AAA |
|-------------|-------|-----------|------------|
| `#1E293B` / `#FFFFFF` | 14.7:1 | ✅ | ✅ |
| `#1E3A8A` / `#FFFFFF` | 9.2:1 | ✅ | ✅ |
| `#3b82f6` / `#FFFFFF` | 4.6:1 | ✅ | ❌ |
| `#1E293B` / `#F8FAFC` | 13.8:1 | ✅ | ✅ |
| `#DC2626` / `#FFFFFF` | 5.9:1 | ✅ | ✅ |

### Jerarquía de Colores

```
Importancia    Color               Uso
═══════════    ═════               ═══════════════════════════
Crítico        #DC2626 (Rojo)      Errores, alertas, rupturas
Advertencia    #F59E0B (Ámbar)     Precauciones, estados intermedios
Información    #3b82f6 (Azul)      Datos generales, gráficos
Éxito          #10B981 (Verde)     Confirmaciones, métricas positivas
Neutral        #1E293B (Gris)      Texto, fondos, bordes
```

---

## 🔄 Variables CSS Recomendadas

Si deseas centralizar los colores, puedes crear variables CSS en `app.py`:

```python
st.markdown("""
<style>
    :root {
        /* Colores principales */
        --primary-dark: #1E3A8A;
        --primary-light: #3b82f6;
        --cyan: #06b6d4;
        --purple: #a78bfa;
        --red: #dc2626;
        --green: #10b981;
        --amber: #f59e0b;
        
        /* Fondos */
        --bg-main: #FFFFFF;
        --bg-secondary: #F8FAFC;
        
        /* Texto */
        --text-primary: #1E293B;
        --text-light: #64748B;
        
        /* Sombras */
        --shadow-sm: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.15);
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-light) 100%);
        box-shadow: var(--shadow-sm);
    }
</style>
""", unsafe_allow_html=True)
```

---

## 🎨 Exportar Paleta

### Para Adobe Illustrator / Photoshop

```
Swatch 1: #1E3A8A (Azul Oscuro)
Swatch 2: #3b82f6 (Azul Brillante)
Swatch 3: #06b6d4 (Cyan)
Swatch 4: #a78bfa (Púrpura)
Swatch 5: #dc2626 (Rojo)
Swatch 6: #10b981 (Verde)
Swatch 7: #f59e0b (Ámbar)
Swatch 8: #F8FAFC (Gris Claro)
Swatch 9: #1E293B (Gris Oscuro)
```

### Para Figma

```json
{
  "colors": {
    "primary-dark": "#1E3A8A",
    "primary-light": "#3b82f6",
    "cyan": "#06b6d4",
    "purple": "#a78bfa",
    "red": "#dc2626",
    "green": "#10b981",
    "amber": "#f59e0b",
    "bg-secondary": "#F8FAFC",
    "text-primary": "#1E293B"
  }
}
```

### Para PowerPoint

| Color | R | G | B |
|-------|---|---|---|
| Azul Oscuro | 30 | 58 | 138 |
| Azul Brillante | 59 | 130 | 246 |
| Cyan | 6 | 182 | 212 |
| Púrpura | 167 | 139 | 250 |
| Rojo | 220 | 38 | 38 |
| Verde | 16 | 185 | 129 |
| Ámbar | 245 | 158 | 11 |

---

## 📱 Pruebas en Dispositivos

### Checklist de Validación

- [ ] **Desktop Chrome** - Verificar gradientes y sombras
- [ ] **Desktop Firefox** - Comprobar compatibilidad CSS
- [ ] **Desktop Safari** - Validar colores sRGB
- [ ] **Mobile Chrome (Android)** - Contraste en pantallas OLED
- [ ] **Mobile Safari (iOS)** - Verificar en modo claro/oscuro
- [ ] **Tablet** - Comprobar responsive design
- [ ] **Modo Alto Contraste** - Accesibilidad Windows
- [ ] **Simulación Daltonismo** - Chrome DevTools

---

## 🆘 Troubleshooting

### Problema: Gradientes se ven "bañados"

**Causa**: Monitor con bajo gamut de color

**Solución**: 
```css
/* Añade más pasos intermedios */
background: linear-gradient(135deg, 
    #1e3a8a 0%, 
    #2563eb 33%,
    #3b82f6 66%,
    #60a5fa 100%);
```

### Problema: Colores muy saturados en OLED

**Causa**: Pantallas AMOLED oversaturan colores

**Solución**:
```toml
# Reduce saturación ligeramente
primaryColor = "#2E4A9A"  # En vez de #1E3A8A
```

---

**Autor**: Jose Candon Rubio  
**Versión**: 1.0  
**Fecha**: Noviembre 2025
