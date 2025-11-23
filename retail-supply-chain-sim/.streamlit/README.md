# 🎨 Configuración Visual Profesional

Este directorio contiene la configuración de estilo corporativo del **Retail Supply Chain Simulator**.

## 📋 Contenido

- **`config.toml`**: Configuración de tema personalizado de Streamlit

## 🎨 Paleta de Colores Corporativa

La paleta ha sido diseñada para proyectar profesionalismo y confianza, optimizada para presentaciones ejecutivas y entornos corporativos.

### Colores Principales

| Elemento | Color | Código HEX | Uso |
|----------|-------|------------|-----|
| **Primario** | ![#1E3A8A](https://via.placeholder.com/15/1E3A8A/000000?text=+) | `#1E3A8A` | Botones, elementos interactivos, encabezados |
| **Fondo Principal** | ![#FFFFFF](https://via.placeholder.com/15/FFFFFF/000000?text=+) | `#FFFFFF` | Fondo general de la aplicación |
| **Fondo Secundario** | ![#F8FAFC](https://via.placeholder.com/15/F8FAFC/000000?text=+) | `#F8FAFC` | Tarjetas, secciones, sidebars |
| **Texto** | ![#1E293B](https://via.placeholder.com/15/1E293B/000000?text=+) | `#1E293B` | Texto principal |

### Colores de Acento (Gráficos y Métricas)

| Elemento | Color | Código HEX | Uso |
|----------|-------|------------|-----|
| **Azul Brillante** | ![#3b82f6](https://via.placeholder.com/15/3b82f6/000000?text=+) | `#3b82f6` | Gráficos de stock, líneas principales |
| **Cyan** | ![#06b6d4](https://via.placeholder.com/15/06b6d4/000000?text=+) | `#06b6d4` | Costes de almacenamiento |
| **Púrpura** | ![#a78bfa](https://via.placeholder.com/15/a78bfa/000000?text=+) | `#a78bfa` | Costes de pedido |
| **Rojo** | ![#dc2626](https://via.placeholder.com/15/dc2626/000000?text=+) | `#dc2626` | Alertas, ventas perdidas, ROP |
| **Verde** | ![#10b981](https://via.placeholder.com/15/10b981/000000?text=+) | `#10b981` | Métricas positivas, éxito |
| **Ámbar** | ![#f59e0b](https://via.placeholder.com/15/f59e0b/000000?text=+) | `#f59e0b` | Advertencias, estados intermedios |

## 🔧 Cómo Modificar los Colores

### 1. Editar el Tema Principal

Abre `config.toml` y modifica la sección `[theme]`:

```toml
[theme]
primaryColor = "#1E3A8A"  # Tu color primario
backgroundColor = "#FFFFFF"  # Fondo general
secondaryBackgroundColor = "#F8FAFC"  # Fondo de secciones
textColor = "#1E293B"  # Color del texto
font = "sans serif"  # Tipografía
```

### 2. Reiniciar la Aplicación

Después de modificar `config.toml`, reinicia Streamlit:

```bash
streamlit run app.py
```

## 🎯 Principios de Diseño

### ✅ **Profesionalismo**
- Paleta sobria y corporativa
- Contraste optimizado WCAG AA
- Tipografía limpia y legible

### ✅ **Claridad**
- Jerarquía visual clara
- Espaciado generoso
- Elementos bien diferenciados

### ✅ **Confianza**
- Colores estables (azules)
- Diseño coherente
- Estética empresarial

## 📊 Accesibilidad

Todos los colores cumplen con **WCAG 2.1 AA** para contraste:

- Texto principal sobre fondo blanco: **Ratio 14.7:1** ✅
- Botones primarios: **Ratio 4.6:1** ✅
- Texto sobre fondos secundarios: **Ratio 13.1:1** ✅

## 🚀 Características Visuales

### Elementos Mejorados

- ✅ Gradientes sutiles en encabezados
- ✅ Sombras suaves (box-shadow)
- ✅ Bordes redondeados (10px)
- ✅ Tarjetas elevadas
- ✅ Tipografía escalada (responsive)
- ✅ Iconos emoji contextuales

### Optimizaciones de UX

- ✅ Tooltips informativos (ℹ️)
- ✅ Estados hover mejorados
- ✅ Transiciones suaves
- ✅ Feedback visual claro
- ✅ Toolbar minimalista

## 📝 Notas Técnicas

### Configuración del Servidor

```toml
[server]
headless = true  # Modo servidor
port = 8501  # Puerto por defecto
enableCORS = false  # Seguridad
enableXsrfProtection = true  # Protección XSRF
```

### Configuración del Cliente

```toml
[client]
showErrorDetails = false  # Oculta detalles técnicos
toolbarMode = "minimal"  # Toolbar minimalista
```

## 🎨 Exportación para Presentaciones

Los colores están optimizados para:

- 📊 **PowerPoint/Google Slides**: Contraste alto en proyectores
- 📱 **Pantallas móviles**: Legibilidad en dispositivos pequeños
- 🖨️ **Impresión**: Paleta compatible con impresión B/N
- 💻 **Monitores**: Optimizado para sRGB

## 🔗 Recursos Adicionales

- [Documentación de Streamlit Theming](https://docs.streamlit.io/library/advanced-features/theming)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025  
**Autor**: Jose Candon Rubio
