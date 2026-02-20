# Construcción de un Índice Sintético de Digitalización Educativa (ISDE) mediante Análisis Exploratorio de Datos, Aprendizaje Automático no Supervisado y Analítica Visual

**Autores:** Rocío Noriega Bustelo, Jose Miguel Martínez Martín  
**TFM — UNIR (Máster Universitario en Análisis y Visualización de Datos Masivos/ Visual Analytics and Big Data)**  
**Año:** 2026

---

## Resumen
La transformación digital constituye uno de los ejes vertebradores de las políticas educativas contemporáneas, redefiniendo la manera en que los sistemas de enseñanza aprenden, gestionan y se relacionan con el conocimiento (UNESCO, 2023). En el contexto europeo y global, el grado de digitalización de los centros educativos se ha convertido en un indicador clave de la calidad, equidad y sostenibilidad de los sistemas de educación secundaria (European Commission, 2022). Sin embargo, persisten desigualdades relevantes entre países, regiones y centros escolares en términos de acceso, infraestructura, competencia digital docente y uso pedagógico de las TIC.

Este Trabajo de Fin de Máster aborda el análisis internacional de la digitalización educativa a partir de indicadores TIC, complementándolo con la **construcción de un índice sintético de digitalización educativa (ISDE)** que permita comparar niveles de desarrollo digital entre territorios y tipologías de centros. Como parte aplicada, el proyecto incorpora un **cuestionario de campo (Google Forms)** en español e inglés destinado a docentes, técnicos y responsables educativos de Educación Secundaria, con el propósito de explorar la percepción profesional sobre el uso de las TIC, la capacitación digital, las estrategias pedagógicas y las barreras institucionales.

Aunque el número de respuestas obtenidas hasta el momento es limitado (45 participantes), el cuestionario se plantea como un instrumento de observación empírica que se pretende continuar y ampliar. De este modo, la investigación combina un componente **analítico-macro** (indicadores internacionales, EDA y modelización) con un componente **empírico-micro** (cuestionario estructurado), aportando una doble dimensión: diagnóstica y prospectiva.

El trabajo se alinea con las estrategias europeas de educación digital (European Commission, 2021), los marcos de competencia digital docente (DigCompEdu; Redecker & Punie, 2017) y modelos de autoevaluación institucional (SELFIE), ofreciendo una contribución metodológica orientada a la evaluación cuantitativa, reproducible y comparativa de la digitalización en educación secundaria.

---

## Objetivos
- **O1.** Analizar comparativamente el grado de digitalización educativa mediante indicadores TIC.
- **O2.** Construir el **Índice Sintético de Digitalización Educativa (ISDE)** integrando múltiples dimensiones.
- **O3.** Aplicar **aprendizaje automático no supervisado** para identificar patrones/agrupaciones (clustering) entre territorios.
- **O4.** Complementar el análisis con evidencia empírica a través de un cuestionario de percepción docente y organizativa.

---

## Estructura del repositorio
Este repositorio incluye la **memoria** y **dos notebooks** (EDA y ML no supervisado):

```
.
├── docs/
│   └── memoria_tfm.pdf
├── notebooks/
│   ├── 01_EDA_ISDE.ipynb
│   └── 02_ML_NoSupervisado_ISDE.ipynb
└── README.md
```

> Ajusta los nombres de archivos/carpetas si difieren de tu estructura final.

---

## Datos
Por motivos de licencia y redistribución, este repositorio **no incluye** los datasets originales (p. ej., TALIS/OECD u otras fuentes).  
Los notebooks contienen la metodología, transformaciones y análisis necesarios para reproducir el trabajo **si se dispone de los datos por vías legítimas**.

---

## Metodología (alto nivel)
1. **Preparación y limpieza (ETL):** normalización de países, diccionario de ítems, tratamiento de faltantes/NA y estandarización de variables.
2. **EDA:** análisis descriptivo y comparativo, exploración de distribuciones y relaciones, y analítica visual.
3. **Construcción del ISDE:** integración de dimensiones (infraestructura, competencia digital docente, uso pedagógico, etc.) en un indicador sintético.
4. **ML no supervisado:** clustering (p. ej., K-Means) y validación (p. ej., silhouette) para segmentación de perfiles.
5. **Comunicación de resultados:** tablas, gráficos y mapas para interpretación y discusión.

---

## Cómo ejecutar
### Requisitos
- Python **3.10+**
- Jupyter Notebook / JupyterLab

### Instalación (si aplica)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

### Ejecución
1) Lanzar Jupyter:
```bash
jupyter lab
```

2) Ejecutar notebooks en orden:
- `notebooks/01_EDA_ISDE.ipynb`
- `notebooks/02_ML_NoSupervisado_ISDE.ipynb`

> Si los notebooks esperan rutas locales, revisa la celda inicial de configuración (p. ej., `BASE_PATH`, `PATHS`) y actualiza la ruta a tu entorno.

---

## Limitaciones
- **Comparabilidad internacional:** depende de la cobertura y consistencia de los indicadores por territorio.
- **Índice sintético:** el ISDE está condicionado por decisiones metodológicas (selección de variables, normalización/ponderación y supuestos).
- **Cuestionario empírico:** la muestra actual (45 respuestas) limita la generalización; se plantea como instrumento prospectivo para ampliaciones posteriores.

---

## Licencia
- **Código (notebooks/scripts):** MIT License (ver `LICENSE`)
- **Memoria y contenido escrito (PDF, texto, figuras propias):** Creative Commons **CC BY-NC-ND 4.0**

---

## Cita
Si utilizas este trabajo, por favor cita:

```bibtex
@mastersthesis{martinez2026isde,
  title   = {Construcción de un Índice Sintético de Digitalización Educativa (ISDE) mediante Análisis Exploratorio de Datos, Aprendizaje Automático no Supervisado y Analítica Visual},
  authors  = {Noriega Bustelo, Rocío and Martínez Martín, Jose Miguel},
  school  = {UNIR},
  year    = {2026}
}
```

---
