# 📁 Carpeta `.streamlit/` - Índice de Documentación

Bienvenido a la configuración visual profesional del **Retail Supply Chain Simulator**.

---

## 📚 Archivos Disponibles

### ⚙️ Configuración Activa

| Archivo | Descripción | Prioridad |
|---------|-------------|-----------|
| **[`config.toml`](config.toml)** | Configuración del tema Streamlit (colores, fuentes, servidor) | ⭐⭐⭐⭐⭐ |

### 📖 Documentación

| Archivo | Descripción | Audiencia | Páginas |
|---------|-------------|-----------|---------|
| **[`README.md`](README.md)** | Introducción al diseño visual, paleta, principios | Todos | ~200 líneas |
| **[`CUSTOMIZATION_GUIDE.md`](CUSTOMIZATION_GUIDE.md)** | Guía paso a paso para personalizar colores | Desarrolladores | ~450 líneas |
| **[`COLOR_REFERENCE.md`](COLOR_REFERENCE.md)** | Referencia completa de paleta con códigos HEX/RGB | Diseñadores | ~400 líneas |
| **[`BEFORE_AFTER.md`](BEFORE_AFTER.md)** | Comparativa visual antes/después del refinamiento | Stakeholders | ~500 líneas |
| **[`SUMMARY.md`](SUMMARY.md)** | Resumen ejecutivo de cambios implementados | Gestores | ~300 líneas |
| **[`INDEX.md`](INDEX.md)** | Este archivo (índice de navegación) | Todos | - |

---

## 🚀 Inicio Rápido

### 🎯 ¿Qué archivo leer primero?

**Según tu perfil**:

| Perfil | Archivo Recomendado | Tiempo |
|--------|---------------------|--------|
| 👨‍💼 **Gerente/Decisor** | [`SUMMARY.md`](SUMMARY.md) | 5 min |
| 👨‍💻 **Desarrollador** | [`README.md`](README.md) → [`CUSTOMIZATION_GUIDE.md`](CUSTOMIZATION_GUIDE.md) | 15 min |
| 🎨 **Diseñador** | [`COLOR_REFERENCE.md`](COLOR_REFERENCE.md) → [`BEFORE_AFTER.md`](BEFORE_AFTER.md) | 10 min |
| 📊 **Analista/Consultor** | [`BEFORE_AFTER.md`](BEFORE_AFTER.md) | 8 min |
| 🆕 **Nuevo Usuario** | [`README.md`](README.md) | 10 min |

### ⚡ Acciones Rápidas

```bash
# Ver configuración actual del tema
cat .streamlit/config.toml

# Cambiar color primario (ejemplo: verde corporativo)
nano .streamlit/config.toml
# Editar: primaryColor = "#047857"

# Reiniciar aplicación con nuevo tema
streamlit run app.py

# Leer documentación completa
ls .streamlit/*.md
```

---

## 📂 Contenido Detallado

### 1️⃣ `config.toml` (⚙️ Configuración)

**Qué contiene**:
- Tema de colores (`[theme]`)
- Configuración del servidor (`[server]`)
- Configuración del cliente (`[client]`)
- Configuración del runner (`[runner]`)

**Cuándo editarlo**:
- ✅ Cambiar paleta de colores corporativa
- ✅ Ajustar configuración de servidor
- ✅ Modificar comportamiento de la UI

**Ejemplo de edición**:
```toml
[theme]
primaryColor = "#1E3A8A"  # Cambiar a tu color
```

**Líneas**: ~60  
**Formato**: TOML  
**Documentación oficial**: https://docs.streamlit.io/library/advanced-features/configuration

---

### 2️⃣ `README.md` (📖 Introducción)

**Qué contiene**:
- Paleta de colores con tabla visual
- Guía de modificación de colores
- Principios de diseño (Profesionalismo, Claridad, Confianza)
- Ratios de contraste WCAG AA/AAA
- Características visuales implementadas
- Optimizaciones de UX
- Recursos adicionales

**Para quién**:
- Desarrolladores que quieren entender el diseño
- Colaboradores del proyecto
- Usuarios que quieren personalizar

**Líneas**: ~200  
**Formato**: Markdown

---

### 3️⃣ `CUSTOMIZATION_GUIDE.md` (🔧 Personalización)

**Qué contiene**:
- Paleta actual (tema + gráficos)
- Instrucciones paso a paso para cambiar colores
- 6 paletas pre-definidas listas para usar:
  - 🔵 Azul Corporativo (actual)
  - 🟢 Verde Sostenible
  - 🟣 Púrpura Creativo
  - 🟠 Naranja Energético
  - ⚫ Gris Minimalista
  - 🔴 Rojo Impactante
- Verificación de accesibilidad WCAG
- Mejores prácticas de diseño
- Solución de problemas comunes
- Flujo de personalización completo

**Para quién**:
- Usuarios técnicos que quieren adaptar colores
- Diseñadores que integran branding empresarial
- Desarrolladores que forkean el proyecto

**Líneas**: ~450  
**Formato**: Markdown  
**Nivel**: Intermedio

---

### 4️⃣ `COLOR_REFERENCE.md` (🎨 Referencia)

**Qué contiene**:
- Referencia completa de todos los colores
- Códigos HEX, RGB y ubicaciones exactas en el código
- Tabla de gradientes con inicio/fin
- Ratios de contraste calculados
- Jerarquía de colores
- Variables CSS recomendadas
- Exportación para Adobe/Figma/PowerPoint
- Checklist de validación en dispositivos
- Troubleshooting de visualización

**Para quién**:
- Diseñadores gráficos
- Equipos de marketing
- Creadores de presentaciones
- Desarrolladores que necesitan códigos exactos

**Líneas**: ~400  
**Formato**: Markdown  
**Nivel**: Técnico/Diseño

---

### 5️⃣ `BEFORE_AFTER.md` (🔄 Comparativa)

**Qué contiene**:
- Comparación visual antes/después del refinamiento
- Transformación del tema principal
- Análisis de elementos específicos:
  - Botones y sliders
  - Sidebar
  - Encabezado principal
  - Tarjetas de métricas
  - Gráficos Plotly
  - Pie charts
- Contraste de accesibilidad (mejoras WCAG)
- Coherencia visual (unificación de paleta)
- Percepción profesional (evaluación cualitativa)
- Casos de uso (presentaciones, reportes, accesibilidad)
- Métricas finales de mejora

**Para quién**:
- Stakeholders que quieren ver ROI
- Gestores de proyecto
- Usuarios que evalúan adoptar el proyecto
- Documentación de portfolio

**Líneas**: ~500  
**Formato**: Markdown  
**Nivel**: Ejecutivo/Visual

---

### 6️⃣ `SUMMARY.md` (📋 Resumen Ejecutivo)

**Qué contiene**:
- Resumen de archivos creados/modificados
- Mejoras aplicadas (tema, servidor, documentación)
- Impacto visual antes/después
- Checklist de validación (profesionalismo, accesibilidad, documentación)
- Instrucciones de aplicación para usuarios/desarrolladores
- Métricas de mejora (contraste +149%, coherencia +100%)
- Beneficios empresariales
- Paleta corporativa final
- Próximos pasos opcionales

**Para quién**:
- Gerentes de proyecto
- Decisores técnicos
- Documentación interna
- Changelog del proyecto

**Líneas**: ~300  
**Formato**: Markdown  
**Nivel**: Ejecutivo

---

## 🎯 Flujos de Trabajo Recomendados

### 🆕 Nuevo Usuario del Simulador

```
1. Leer README.md (10 min)
   ↓
2. Ejecutar: streamlit run app.py
   ↓
3. Ver diseño aplicado
   ↓
4. (Opcional) Leer BEFORE_AFTER.md para contexto
```

---

### 🎨 Personalizar Colores (Primera Vez)

```
1. Leer CUSTOMIZATION_GUIDE.md (15 min)
   ↓
2. Elegir paleta pre-definida O crear propia
   ↓
3. Editar config.toml
   ↓
4. (Opcional) Editar colores en app.py (gráficos)
   ↓
5. Verificar accesibilidad (WebAIM Contrast Checker)
   ↓
6. Reiniciar: streamlit run app.py
   ↓
7. Probar en múltiples dispositivos
```

---

### 🏢 Integrar Branding Empresarial

```
1. Obtener paleta corporativa (HEX codes)
   ↓
2. Consultar COLOR_REFERENCE.md (ubicaciones exactas)
   ↓
3. Editar config.toml (tema principal)
   ↓
4. Editar app.py (gradientes, gráficos)
   ↓
5. Verificar contraste WCAG AA (mínimo 4.5:1)
   ↓
6. Documentar cambios en README.md personalizado
   ↓
7. Exportar paleta para presentaciones (PowerPoint/Figma)
```

---

### 📊 Evaluar Proyecto (Stakeholder)

```
1. Leer SUMMARY.md (5 min)
   ↓
2. Revisar BEFORE_AFTER.md (métricas de mejora)
   ↓
3. Ejecutar demo: streamlit run app.py
   ↓
4. Evaluar profesionalismo visual
   ↓
5. Decisión: Adoptar/Rechazar/Personalizar
```

---

### 🐛 Resolver Problemas Visuales

```
1. Identificar problema (colores incorrectos, contraste bajo, etc.)
   ↓
2. Consultar CUSTOMIZATION_GUIDE.md → Sección "Solución de Problemas"
   ↓
3. Si es sobre colores específicos: COLOR_REFERENCE.md
   ↓
4. Si es configuración: Verificar config.toml
   ↓
5. Limpiar caché: streamlit cache clear
   ↓
6. Reiniciar app + hard reload navegador (Ctrl+Shift+R)
```

---

## 📈 Métricas de Documentación

| Archivo | Líneas | Palabras | Tiempo Lectura |
|---------|--------|----------|----------------|
| `config.toml` | ~60 | ~400 | 2 min |
| `README.md` | ~200 | ~1,500 | 10 min |
| `CUSTOMIZATION_GUIDE.md` | ~450 | ~3,200 | 20 min |
| `COLOR_REFERENCE.md` | ~400 | ~2,800 | 15 min |
| `BEFORE_AFTER.md` | ~500 | ~3,500 | 18 min |
| `SUMMARY.md` | ~300 | ~2,000 | 12 min |
| `INDEX.md` | ~250 | ~1,800 | 10 min |
| **TOTAL** | **~2,160** | **~15,200** | **~87 min** |

---

## 🔗 Enlaces Útiles

### Documentación Oficial

- **[Streamlit Theming](https://docs.streamlit.io/library/advanced-features/theming)** - Configuración de temas
- **[Streamlit Configuration](https://docs.streamlit.io/library/advanced-features/configuration)** - Todas las opciones de config.toml
- **[WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)** - Estándares de accesibilidad

### Herramientas de Diseño

- **[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)** - Verificar contraste WCAG
- **[Coolors](https://coolors.co/)** - Generador de paletas
- **[Adobe Color](https://color.adobe.com/)** - Esquemas de color
- **[Paletton](https://paletton.com/)** - Generador avanzado
- **[ColorBox](https://colorbox.io/)** - Paletas accesibles

### Recursos del Proyecto

- **[README Principal](../README.md)** - Documentación general del simulador
- **[app.py](../app.py)** - Código de la aplicación
- **[simulation.py](../simulation.py)** - Motor de simulación

---

## 🆘 Soporte

### Problemas Comunes

| Problema | Solución Rápida | Archivo |
|----------|-----------------|---------|
| Colores no cambian | Reiniciar Streamlit + hard reload | `CUSTOMIZATION_GUIDE.md` |
| Contraste bajo | Verificar en WebAIM Contrast Checker | `COLOR_REFERENCE.md` |
| Gradientes no visibles | Revisar compatibilidad CSS del navegador | `BEFORE_AFTER.md` |
| Tema inconsistente | Verificar config.toml + app.py coherencia | `README.md` |

### Contacto

**Autor**: Jose Candon Rubio  
**Email**: josecandonrubio@gmail.com  
**GitHub**: [@MingosGit](https://github.com/MingosGit)  
**Repositorio**: [retail-supply-chain-sim](https://github.com/MingosGit/retail-supply-chain-sim)

---

## 📝 Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| **1.0** | Nov 23, 2025 | Implementación inicial del refinamiento visual |
| | | - config.toml con tema azul corporativo |
| | | - 6 documentos de diseño completos |
| | | - Paleta coherente en toda la aplicación |
| | | - Accesibilidad WCAG AA completa |

---

## 🎯 Próximos Pasos

### Recomendaciones

1. **Leer documentación relevante** según tu perfil (ver tabla arriba)
2. **Ejecutar la aplicación** para ver el diseño aplicado
3. **Personalizar colores** si es necesario (CUSTOMIZATION_GUIDE.md)
4. **Verificar accesibilidad** con WebAIM Contrast Checker
5. **Compartir feedback** para mejorar la documentación

### Contribuciones

Si encuentras errores o tienes sugerencias:
1. Abre un **Issue** en GitHub
2. Propón un **Pull Request** con mejoras
3. Comparte en redes sociales con **#RetailSupplyChainSim**

---

**Última actualización**: Noviembre 23, 2025  
**Mantenido por**: Jose Candon Rubio  
**Licencia**: MIT
