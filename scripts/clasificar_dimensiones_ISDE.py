"""
================================================================================
SCRIPT: Clasificación de Indicadores por Dimensiones ISDE
================================================================================
TFM: Índice Sintético de Digitalización Educativa
Autores: José Miguel Martínez Martín & Rocío Noriega Bustelo
Fecha: Enero 2026

Este script:
1. Lee los 4 datasets (TALIS, Eurydice, UNESCO, Eurostat/DESI)
2. Clasifica cada fila en una dimensión ISDE (D1-D5)
3. Crea una hoja "dimensiones" como diccionario de referencia
4. Guarda los archivos transformados en la carpeta Dimensiones
================================================================================
"""

import pandas as pd
import os
from pathlib import Path

# ==============================================================================
# CONFIGURACIÓN DE RUTAS
# ==============================================================================

BASE_PATH = Path(r"C:\Users\Usuario\Desktop\UNIR\TFM\Tablas")
OUTPUT_PATH = BASE_PATH / "Dimensiones"

# Crear carpeta de salida si no existe
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# DEFINICIÓN DE DIMENSIONES ISDE
# ==============================================================================

DIMENSIONES_DESC = {
    'D1': 'Infraestructura Digital',
    'D2': 'Competencia Digital Docente',
    'D3': 'Pedagogía Digital / Uso Pedagógico TIC',
    'D4': 'Liderazgo y Política Institucional',
    'D5': 'Equidad Digital'
}

# ==============================================================================
# REGLAS DE CLASIFICACIÓN POR DATASET
# ==============================================================================

# -----------------------------------------------------------------------------
# TALIS 2024: Clasificación por tipo de pregunta
# -----------------------------------------------------------------------------
TALIS_CLASIFICACION = {
    # D2 - Competencia Digital Docente
    'Actividades de desarrollo profesional': 'D2',
    'Temas incluidos en el desarrollo profesional': 'D2',
    'Impacto global del desarrollo profesional': 'D2',
    'Importancia de características del desarrollo profesional': 'D2',
    'Lo que puedes hacer en tu enseñanza': 'D2',
    'Tareas que puedes hacer con recursos/herramientas digitales': 'D2',
    
    # D3 - Pedagogía Digital
    'Frecuencia con la que el profesor': 'D3',
    'Opiniones sobre el uso de recursos/herramientas digitales': 'D3',
}

# -----------------------------------------------------------------------------
# EURYDICE 2023: Clasificación por tipo de ítem
# -----------------------------------------------------------------------------
EURYDICE_CLASIFICACION = {
    # D3 - Pedagogía Digital (integración curricular)
    'Asignatura separada obligatoria': 'D3',
    'Informática como asignatura separada y obligatoria': 'D3',
    'Informática como asignatura separada, optativa': 'D3',
    'Informática no se imparte como asignatura separada': 'D3',
    'Integrada en otras materias obligatorias': 'D3',
    'No incluida en currículo': 'D3',
    'Otras (p. ej., optativa)': 'D3',
    'Transversal (cross-curricular)': 'D3',
    
    # D4 - Liderazgo y Política Institucional
    'Autonomía centro/local': 'D4',
    'Autonomía del centro/autoridad local': 'D4',
    'Criterios de educación digital en marcos de evaluación externa': 'D4',
    'Designación de coordinador/a digital en los centros': 'D4',
    'Hay requisitos de nivel superior obligatorios de las competencias específicas digitales para algunos profesores': 'D4',
    'Hay requisitos de nivel superior obligatorios de las competencias específicas digitales para todo el profesorado': 'D4',
    'No hay ningún requisito de nivel superior obligatorio de las competencias específicas digitales del profesorado': 'D4',
    'Plan digital de centro como documento específico': 'D4',
    'Plan digital integrado en el plan de centro': 'D4',
}

# -----------------------------------------------------------------------------
# UNESCO UIS: Todos son D1 (Infraestructura)
# -----------------------------------------------------------------------------
UNESCO_CLASIFICACION = {
    'Proporción de centros de Educación Secundaria Superior con acceso a ordenadores con fines pedagógicos (%)': 'D1',
    'Proporción de centros de Educación Secundaria Superior con acceso a Internet con fines pedagógicos (%)': 'D1',
    'Proporción de centros de Educación Secundaria con acceso a ordenadores con fines pedagógicos (%)': 'D1',
    'Proporción de centros de Educación Secundaria con acceso a Internet con fines pedagógicos (%)': 'D1',
    'Proporción de centros de Educación Secundaria Inferior con acceso a Internet con fines pedagógicos (%)': 'D1'
}

# -----------------------------------------------------------------------------
# EUROSTAT/DESI: Clasificación por código de variable y descripción
# -----------------------------------------------------------------------------
# Palabras clave para clasificar variables de Eurostat/DESI

EUROSTAT_KEYWORDS = {
    'D1': [  # Infraestructura
        'broadband', 'internet', 'connectivity', 'coverage', 'network',
        'banda ancha', 'conexión', 'conectividad', 'cobertura', 'red',
        'fiber', 'fibra', '5g', '4g', 'mobile', 'móvil',
        'ICT infrastructure', 'digital infrastructure'
    ],
    'D2': [  # Competencia Digital
        'skill', 'competence', 'training', 'education', 'learning',
        'habilidad', 'competencia', 'formación', 'educación', 'aprendizaje',
        'digital skills', 'basic digital', 'above basic', 'software',
        'ICT specialist', 'ICT user', 'e-skill', 'computer',
        'programming', 'programación', 'literacy', 'alfabetización'
    ],
    'D3': [  # Pedagogía (uso)
        'use of', 'using', 'usage', 'activities', 'online services',
        'uso de', 'usando', 'actividades', 'servicios en línea',
        'e-commerce', 'e-government', 'e-health', 'social media',
        'online shopping', 'internet banking', 'cloud', 'video call'
    ],
    'D4': [  # Liderazgo/Política
        'policy', 'strategy', 'plan', 'governance', 'regulation',
        'política', 'estrategia', 'gobernanza', 'regulación',
        'enterprise', 'business', 'SME', 'empresa', 'negocio', 'PYME'
    ],
    'D5': [  # Equidad
        'gap', 'divide', 'inequality', 'access', 'inclusion',
        'brecha', 'desigualdad', 'acceso', 'inclusión',
        'rural', 'urban', 'age', 'gender', 'income',
        'edad', 'género', 'ingreso', 'vulnerable'
    ]
}


def clasificar_eurostat(variable_desc, variable_codigo):
    """
    Clasifica una variable de Eurostat/DESI en una dimensión ISDE
    basándose en palabras clave en la descripción y código.
    """
    texto = f"{variable_desc} {variable_codigo}".lower()
    
    # Prioridad: D1 > D2 > D3 > D4 > D5
    for dim in ['D1', 'D2', 'D3', 'D4', 'D5']:
        for keyword in EUROSTAT_KEYWORDS[dim]:
            if keyword.lower() in texto:
                return dim
    
    # Por defecto, si no coincide con nada, asignar D2 (competencia general)
    return 'D2'


# ==============================================================================
# FUNCIONES DE PROCESAMIENTO
# ==============================================================================

def crear_hoja_dimensiones(clasificacion_dict, columna_origen, nombre_dataset):
    """
    Crea un DataFrame con el diccionario de dimensiones para la hoja de referencia.
    """
    rows = []
    for valor, dimension in clasificacion_dict.items():
        rows.append({
            columna_origen: valor,
            'Dimension_ISDE': dimension,
            'Dimension_Nombre': DIMENSIONES_DESC.get(dimension, 'Sin clasificar'),
            'Dataset': nombre_dataset
        })
    
    df_dim = pd.DataFrame(rows)
    return df_dim


def procesar_talis():
    """Procesa el dataset TALIS 2024."""
    print("\n" + "="*60)
    print("📊 Procesando TALIS 2024...")
    print("="*60)
    
    # Leer archivo
    talis = pd.read_csv(BASE_PATH / 'TALIS_2024.csv', encoding='utf-8-sig')
    print(f"   Filas originales: {len(talis):,}")
    
    # Clasificar cada fila
    talis['Dimension_ISDE'] = talis['Pregunta'].map(TALIS_CLASIFICACION)
    talis['Dimension_Nombre'] = talis['Dimension_ISDE'].map(DIMENSIONES_DESC)
    
    # Verificar clasificación
    sin_clasificar = talis['Dimension_ISDE'].isna().sum()
    if sin_clasificar > 0:
        print(f"   ⚠️  Filas sin clasificar: {sin_clasificar}")
        print(f"   Preguntas no clasificadas: {talis[talis['Dimension_ISDE'].isna()]['Pregunta'].unique()}")
    
    # Crear hoja de dimensiones
    df_dimensiones = crear_hoja_dimensiones(TALIS_CLASIFICACION, 'Pregunta', 'TALIS 2024')
    
    # Guardar como Excel con dos hojas
    output_file = OUTPUT_PATH / 'TALIS_2024_DIMENSIONES.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        talis.to_excel(writer, sheet_name='Datos', index=False)
        df_dimensiones.to_excel(writer, sheet_name='dimensiones', index=False)
    
    print(f"   ✓ Guardado: {output_file.name}")
    print(f"   Distribución de dimensiones:")
    print(talis['Dimension_ISDE'].value_counts().to_string(header=False))
    
    return talis


def procesar_eurydice():
    """Procesa el dataset Eurydice 2023."""
    print("\n" + "="*60)
    print("📊 Procesando EURYDICE 2023...")
    print("="*60)
    
    # Leer archivo
    eurydice = pd.read_excel(BASE_PATH / 'Eurydice.xlsx', sheet_name='Eurydice')
    print(f"   Filas originales: {len(eurydice):,}")
    
    # Clasificar cada fila
    eurydice['Dimension_ISDE'] = eurydice['Ítem'].map(EURYDICE_CLASIFICACION)
    eurydice['Dimension_Nombre'] = eurydice['Dimension_ISDE'].map(DIMENSIONES_DESC)
    
    # Verificar clasificación
    sin_clasificar = eurydice['Dimension_ISDE'].isna().sum()
    if sin_clasificar > 0:
        print(f"   ⚠️  Filas sin clasificar: {sin_clasificar}")
        print(f"   Ítems no clasificados: {eurydice[eurydice['Dimension_ISDE'].isna()]['Ítem'].unique()}")
    
    # Crear hoja de dimensiones
    df_dimensiones = crear_hoja_dimensiones(EURYDICE_CLASIFICACION, 'Ítem', 'Eurydice 2023')
    
    # Guardar como Excel con dos hojas
    output_file = OUTPUT_PATH / 'Eurydice_DIMENSIONES.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        eurydice.to_excel(writer, sheet_name='Datos', index=False)
        df_dimensiones.to_excel(writer, sheet_name='dimensiones', index=False)
    
    print(f"   ✓ Guardado: {output_file.name}")
    print(f"   Distribución de dimensiones:")
    print(eurydice['Dimension_ISDE'].value_counts().to_string(header=False))
    
    return eurydice


def procesar_unesco():
    """Procesa el dataset UNESCO UIS."""
    print("\n" + "="*60)
    print("📊 Procesando UNESCO UIS...")
    print("="*60)
    
    # Leer archivo
    unesco = pd.read_excel(BASE_PATH / 'UNESCO.xlsx', sheet_name='Datos')
    print(f"   Filas originales: {len(unesco):,}")
    
    # Clasificar cada fila (todos son D1 - Infraestructura)
    unesco['Dimension_ISDE'] = unesco['Indicador'].map(UNESCO_CLASIFICACION)
    unesco['Dimension_Nombre'] = unesco['Dimension_ISDE'].map(DIMENSIONES_DESC)
    
    # Verificar clasificación
    sin_clasificar = unesco['Dimension_ISDE'].isna().sum()
    if sin_clasificar > 0:
        print(f"   ⚠️  Filas sin clasificar: {sin_clasificar}")
        print(f"   Indicadores no clasificados: {unesco[unesco['Dimension_ISDE'].isna()]['Indicador'].unique()}")
    
    # Crear hoja de dimensiones
    df_dimensiones = crear_hoja_dimensiones(UNESCO_CLASIFICACION, 'Indicador', 'UNESCO UIS')
    
    # Guardar como Excel con dos hojas
    output_file = OUTPUT_PATH / 'UNESCO_DIMENSIONES.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        unesco.to_excel(writer, sheet_name='Datos', index=False)
        df_dimensiones.to_excel(writer, sheet_name='dimensiones', index=False)
    
    print(f"   ✓ Guardado: {output_file.name}")
    print(f"   Distribución de dimensiones:")
    print(unesco['Dimension_ISDE'].value_counts().to_string(header=False))
    
    return unesco


def procesar_eurostat():
    """Procesa el dataset Eurostat/DESI 2024."""
    print("\n" + "="*60)
    print("📊 Procesando EUROSTAT/DESI 2024...")
    print("="*60)
    
    # Leer archivo transformado
    eurostat_path = BASE_PATH / 'EuroStatDESI_TRANSFORMADO2.xlsx'
    
    if not eurostat_path.exists():
        print(f"   ⚠️  Archivo no encontrado: {eurostat_path}")
        print("   El script está preparado para procesarlo cuando esté disponible.")
        return None
    
    eurostat = pd.concat(
    [pd.read_excel(eurostat_path, sheet_name=s) for s in pd.ExcelFile(eurostat_path).sheet_names if s.startswith('Datos_Transformados')],
    ignore_index=True
    )
    print(f"   Filas originales: {len(eurostat):,}")
    
    # Clasificar cada fila usando la función de palabras clave
    eurostat['Dimension_ISDE'] = eurostat.apply(
        lambda row: clasificar_eurostat(
            str(row.get('Variable_Descripcion', '')), 
            str(row.get('Variable_Codigo', ''))
        ), axis=1
    )
    eurostat['Dimension_Nombre'] = eurostat['Dimension_ISDE'].map(DIMENSIONES_DESC)
    
    # Crear diccionario de clasificación para la hoja de referencia
    clasificacion_eurostat = eurostat.groupby(['Variable_Codigo', 'Variable_Descripcion'])['Dimension_ISDE'].first().reset_index()
    clasificacion_eurostat['Dimension_Nombre'] = clasificacion_eurostat['Dimension_ISDE'].map(DIMENSIONES_DESC)
    clasificacion_eurostat['Dataset'] = 'Eurostat/DESI 2024'
    
    # Guardar como Excel con dos hojas
    output_file = OUTPUT_PATH / 'EuroStatDESI_DIMENSIONES.xlsx'
    MAX_ROWS = 1000000
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for i, start in enumerate(range(0, len(eurostat), MAX_ROWS)):
            chunk = eurostat.iloc[start:start + MAX_ROWS]
            sheet_name = f"Datos_{i+1}" if len(eurostat) > MAX_ROWS else "Datos"
            chunk.to_excel(writer, sheet_name=sheet_name, index=False)
        clasificacion_eurostat.to_excel(writer, sheet_name='dimensiones', index=False)
    
    print(f"   ✓ Guardado: {output_file.name}")
    print(f"   Distribución de dimensiones:")
    print(eurostat['Dimension_ISDE'].value_counts().to_string(header=False))
    
    return eurostat


def crear_resumen_global():
    """Crea un archivo Excel resumen con todas las dimensiones."""
    print("\n" + "="*60)
    print("📋 Creando resumen global de dimensiones...")
    print("="*60)
    
    # DataFrame con descripción de dimensiones
    df_descripcion = pd.DataFrame([
        {'Dimension': 'D1', 'Nombre': 'Infraestructura Digital', 
         'Descripción': 'Acceso a dispositivos, conectividad, equipamiento TIC en centros educativos',
         'Fuentes': 'UNESCO, Eurostat/DESI'},
        {'Dimension': 'D2', 'Nombre': 'Competencia Digital Docente', 
         'Descripción': 'Formación, habilidades y capacitación del profesorado en TIC',
         'Fuentes': 'TALIS, Eurostat/DESI'},
        {'Dimension': 'D3', 'Nombre': 'Pedagogía Digital', 
         'Descripción': 'Uso pedagógico de TIC, integración curricular, metodologías activas',
         'Fuentes': 'TALIS, Eurydice'},
        {'Dimension': 'D4', 'Nombre': 'Liderazgo y Política Institucional', 
         'Descripción': 'Planes digitales, coordinación, políticas de centro, gobernanza',
         'Fuentes': 'Eurydice'},
        {'Dimension': 'D5', 'Nombre': 'Equidad Digital', 
         'Descripción': 'Brecha digital, acceso equitativo, inclusión',
         'Fuentes': 'UNESCO (parcial), Eurostat/DESI (parcial)'},
    ])
    
    # Guardar resumen
    output_file = OUTPUT_PATH / 'RESUMEN_DIMENSIONES_ISDE.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_descripcion.to_excel(writer, sheet_name='Dimensiones_ISDE', index=False)
        
        # Añadir hoja con palabras clave de Eurostat
        keywords_rows = []
        for dim, keywords in EUROSTAT_KEYWORDS.items():
            for kw in keywords:
                keywords_rows.append({'Dimension': dim, 'Keyword': kw})
        df_keywords = pd.DataFrame(keywords_rows)
        df_keywords.to_excel(writer, sheet_name='Keywords_Eurostat', index=False)
    
    print(f"   ✓ Resumen guardado: {output_file.name}")


# ==============================================================================
# EJECUCIÓN PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║     CLASIFICACIÓN DE INDICADORES POR DIMENSIONES ISDE                        ║
║     TFM: Índice Sintético de Digitalización Educativa                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"📂 Ruta de entrada: {BASE_PATH}")
    print(f"📂 Ruta de salida:  {OUTPUT_PATH}")
    
    # Procesar cada dataset
    try:
        talis = procesar_talis()
    except Exception as e:
        print(f"   ❌ Error procesando TALIS: {e}")
    
    try:
        eurydice = procesar_eurydice()
    except Exception as e:
        print(f"   ❌ Error procesando Eurydice: {e}")
    
    try:
        unesco = procesar_unesco()
    except Exception as e:
        print(f"   ❌ Error procesando UNESCO: {e}")
    
    try:
        eurostat = procesar_eurostat()
    except Exception as e:
        print(f"   ❌ Error procesando Eurostat/DESI: {e}")
    
    # Crear resumen global
    try:
        crear_resumen_global()
    except Exception as e:
        print(f"   ❌ Error creando resumen: {e}")
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║     ✅ PROCESO COMPLETADO                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"""
📁 Archivos generados en {OUTPUT_PATH}:
   • TALIS_2024_DIMENSIONES.xlsx
   • Eurydice_DIMENSIONES.xlsx
   • UNESCO_DIMENSIONES.xlsx
   • EuroStatDESI_DIMENSIONES.xlsx
   • RESUMEN_DIMENSIONES_ISDE.xlsx

📋 Cada archivo Excel contiene:
   • Hoja 'Datos': Dataset original + columnas Dimension_ISDE y Dimension_Nombre
   • Hoja 'dimensiones': Diccionario de referencia con la clasificación

📊 Dimensiones ISDE:
   • D1: Infraestructura Digital
   • D2: Competencia Digital Docente
   • D3: Pedagogía Digital
   • D4: Liderazgo y Política Institucional
   • D5: Equidad Digital
    """)
