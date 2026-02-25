# -*- coding: utf-8 -*-
import os, csv
import pandas as pd

BASE_PATH = r"C:\Users\Usuario\Desktop\UNIR\TFM\Tabla_Maestra"
SOURCE_CSV = os.path.join(BASE_PATH, "ttgintt4.csv")
OUTPUT_CSV = os.path.join(BASE_PATH, "TALIS_2024.csv")

COUNTRIES = {
    "ALB", "ARE", "AUS", "AUT", "AZE", "BEL", "BFL", "BFR", "BGR", "BHR", "BRA",
    "CAB", "CHL", "COL", "CRI", "CSH", "CYP", "CZE", "DNK", "ESP", "EST", "FIN",
    "FRA", "HRV", "HUN", "ISL", "ISR", "ITA", "JPN", "KAZ", "KOR", "LTU", "LVA",
    "MAR", "MKD", "MLT", "MNE", "NLD", "NOR", "NZL", "POL", "PRT", "ROU", "SAU",
    "SGP", "SRB", "SVK", "SVN", "SWE", "TUR", "DEU"
}


# ---------- 1) Diccionario programático (igual que antes) ----------
def build_dictionary_df() -> pd.DataFrame:
    rows = []
    def add_rows(pregunta, item, item_opcion, pairs):
        for code, label in pairs:
            rows.append({
                "Pregunta": pregunta,
                "Item": item.upper(),
                "Item_opción": item_opcion,
                "Valor_codigo": int(code),
                "Valor_etiqueta": label
            })

    scale_20 = [(1,"Sí presencial"),(2,"Sí virtual online"),(3,"Sí mixta"),(4,"No"),(9,"NA")]
    yes_no  = [(1,"Sí"),(2,"No"),(9,"NA")]
    scale_1_4 = [(1,"Nada"),(2,"En cierta medida"),(3,"Bastante"),(4,"Mucho"),(9,"NA")]
    agree_4 = [(1,"Muy en desacuerdo"),(2,"En desacuerdo"),(3,"De acuerdo"),(4,"Muy de acuerdo"),(9,"NA")]
    freq_4 = [(1,"Nunca o casi nunca"),(2,"Ocasionalmente"),(3,"Frecuentemente"),(4,"Siempre"),(9,"NA")]

    actividades = [
        ("TT4G20A","Cursos/seminarios/talleres"),
        ("TT4G20B","Conferencias educativas de los docentes u otros"),
        ("TT4G20B2","Conferencias educativas de los docentes u otros"),  # por si existe
        ("TT4G20C","Programa de cualificación formal"),
        ("TT4G20D","Visitas a otras escuelas para informar sobre mi enseñanza"),
        ("TT4G20E","Visitas a locales comerciales, organizaciones públicas u ONG relacionadas con mi enseñanza"),
        ("TT4G20F","Reflexiones sobre las observaciones de la lección"),
        ("TT4G20G","Coaching como parte de un acuerdo escolar formal"),
        ("TT4G20H","Redes formales o informales de profesores para la formación profesional"),
        ("TT4G20I","Actividades de aprendizaje por iniciativa propia"),
        ("TT4G20J","Otro"),
    ]
    for col, txt in actividades:
        add_rows("Actividades de desarrollo profesional", col, txt, scale_20)

    add_rows("Temas incluidos en el desarrollo profesional","TT4G21E",
             "Competencias pedagógicas para incorporar recursos y herramientas digitales en la enseñanza", yes_no)
    add_rows("Temas incluidos en el desarrollo profesional","TT4G21F",
             "Competencias técnicas para el uso de recursos y herramientas digitales", yes_no)
    add_rows("Temas incluidos en el desarrollo profesional","TT4G21M",
             "Análisis y utilización de las evaluaciones de los alumnos", yes_no)

    add_rows("Impacto global del desarrollo profesional","TT4G22",
             "Impacto positivo del desarrollo profesional", scale_1_4)

    add_rows("Importancia de características del desarrollo profesional","TT4G23A",
             "Se basa en mis conocimientos previos", scale_1_4)
    add_rows("Importancia de características del desarrollo profesional","TT4G23F",
             "Ofrece oportunidades para el intercambio colaborativo de ideas", scale_1_4)

    add_rows("Lo que puedes hacer en tu enseñanza","TT4G27M",
             "Apoyar el aprendizaje de los estudiantes a través del uso de recursos y herramientas digitales", scale_1_4)

    add_rows("Tareas que puedes hacer con recursos/herramientas digitales","TT4G33A",
             "Identificar recursos y herramientas digitales para apoyar el tema(s) que enseño", scale_1_4)
    add_rows("Tareas que puedes hacer con recursos/herramientas digitales","TT4G33G",
             "Aprender a usar la tecnología que es nueva para mí", scale_1_4)

    add_rows("Opiniones sobre el uso de recursos/herramientas digitales","TT4G34A",
             "El uso de recursos y herramientas digitales ayuda a los estudiantes a desarrollar un mayor interés en el aprendizaje", agree_4)
    add_rows("Opiniones sobre el uso de recursos/herramientas digitales","TT4G34C",
             "El uso de recursos y herramientas digitales ayuda a mejorar el rendimiento académico de los estudiantes", agree_4)

    add_rows("Frecuencia con la que el profesor","TT4G55B",
             "Indica a los alumnos diferentes materiales didácticos en función de sus necesidades", freq_4)
    add_rows("Frecuencia con la que el profesor","TT4G55D",
             "Adapta sus métodos de enseñanza a las necesidades de los alumnos", freq_4)
    add_rows("Frecuencia con la que el profesor","TT4G56A",
             "Revisa múltiples ejemplos para practicar los pasos de un procedimiento o habilidad", freq_4)
    add_rows("Frecuencia con la que el profesor","TT4G56B",
             "Selecciona tareas cuya dificultad aumenta gradualmente", freq_4)
    add_rows("Frecuencia con la que el profesor","TT4G56C",
             "Prepara a los estudiantes para las dificultades que pueden ocurrir durante la práctica", freq_4)

    return pd.DataFrame(rows).drop_duplicates()

DICT_DF = build_dictionary_df()
ITEMS_UP = sorted(DICT_DF["Item"].unique())

# ---------- 2) Detección robusta de separador/codificación y header ----------
def detect_sep_and_encoding(path):
    # intenta leer con utf-8-sig; si falla, latin1
    for enc in ("utf-8-sig", "latin1"):
        try:
            with open(path, "r", encoding=enc, errors="ignore") as f:
                sample = f.read(100000)
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            return dialect.delimiter, enc
        except Exception:
            continue
    # por defecto
    return ",", "utf-8-sig"

sep, enc = detect_sep_and_encoding(SOURCE_CSV)

# lee sólo cabecera
hdr = pd.read_csv(SOURCE_CSV, sep=sep, nrows=0, encoding=enc)
# normaliza cabeceras
norm_cols = {c: c.strip().strip('"').strip("'").upper() for c in hdr.columns}

# intenta localizar columna país entre varias alternativas
country_candidates = {"CNTRY","IDCNTRY","CNT","CNTRYID","CNTRY3"}
country_col_original = None
for orig, up in norm_cols.items():
    if up in country_candidates:
        country_col_original = orig
        break
if country_col_original is None:
    raise RuntimeError(f"No encuentro columna de país. Cabeceras detectadas (primeras 15): {list(hdr.columns)[:15]}")

# mapea qué ítems están realmente en el CSV
available_map = {}  # original -> UPPER deseado
for orig, up in norm_cols.items():
    if up in ITEMS_UP:
        available_map[orig] = up

available_items_original = list(available_map.keys())
if not available_items_original:
    raise RuntimeError(
        "Ninguna columna del diccionario está en el CSV de origen.\n"
        f"Delimitador detectado: '{sep}', encoding: {enc}\n"
        f"Ejemplo de columnas disponibles: {list(hdr.columns)[:30]}"
    )

print(f"[INFO] Delimitador='{sep}'  encoding='{enc}'")
print(f"[INFO] Columna país detectada: '{country_col_original}'")
print(f"[INFO] Ítems presentes: {len(available_items_original)} de {len(ITEMS_UP)}")
if len(available_items_original) != len(ITEMS_UP):
    present_up = set(available_map.values())          # ítems del diccionario que sí aparecen en el CSV (en UPPER)
    missing = [it for it in ITEMS_UP if it not in present_up]
    print(f"[WARN] Faltan {len(missing)} ítems del diccionario en el CSV: {missing}")


usecols = [country_col_original] + available_items_original

# Preparativos para merge
MAP_DF = (DICT_DF[["Item","Valor_codigo","Pregunta","Item_opción","Valor_etiqueta"]]
          .drop_duplicates())

# ---------- 3) ETL por chunks ----------
chunk_size = 200_000
parts = []

for chunk in pd.read_csv(SOURCE_CSV, sep=sep, encoding=enc, usecols=usecols,
                         dtype=str, chunksize=chunk_size):
    # normaliza nombres en el chunk
    chunk.columns = [c.strip().strip('"').strip("'").upper() for c in chunk.columns]
    # renombra país a CNTRY (estándar interno)
    if "CNTRY" not in chunk.columns:
        # encuentra la que detectamos antes
        up_country = norm_cols[country_col_original]  # su versión upper
        chunk.rename(columns={up_country: "CNTRY"}, inplace=True)

    # filtra países
    chunk = chunk[chunk["CNTRY"].isin(COUNTRIES)]
    if chunk.empty:
        continue

    # asegura tipos numéricos en ítems
    for col in ITEMS_UP:
        if col in chunk.columns:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce").astype("Int64")

    # pasa a long sólo con los ítems que existan
    present_items = [c for c in ITEMS_UP if c in chunk.columns]
    long_df = chunk.melt(id_vars=["CNTRY"], value_vars=present_items,
                         var_name="Item", value_name="Valor_codigo")

    # une diccionario
    tmp = long_df.merge(MAP_DF, how="left", on=["Item","Valor_codigo"])
    tmp = tmp.dropna(subset=["Pregunta","Item_opción","Valor_etiqueta"])  # excluye NA/9 y no mapeados

    if not tmp.empty:
        grp = (tmp.groupby(["CNTRY","Pregunta","Item","Item_opción","Valor_etiqueta"], observed=True)
                  .size().rename("n").reset_index())
        parts.append(grp)

if not parts:
    raise RuntimeError("No hay registros tras el filtrado (revisa países o columnas).")

counts = pd.concat(parts, ignore_index=True)

tot = counts.groupby(["CNTRY","Item"], observed=True)["n"].sum().rename("total").reset_index()
res = counts.merge(tot, on=["CNTRY","Item"], how="left")
res["Porcentaje"] = (res["n"] / res["total"] * 100).round(2)

# --- salida base ---
out = (res.rename(columns={"CNTRY":"Pais",
                           "Valor_etiqueta":"Valor",
                           "Item_opción":"Respuesta"})
          [["Pais","Pregunta","Respuesta","Valor","Porcentaje"]]
          .sort_values(["Pais","Pregunta","Respuesta","Valor"])
          .reset_index(drop=True))

# --- diagnóstico opcional de duplicados (puedes dejarlo comentado) ---
# dups = (out.groupby(["Pais","Pregunta","Respuesta","Valor"], observed=True)
#            .size().reset_index(name="dup_count"))
# print(dups[dups["dup_count"] > 1].head(20))

# --- NUEVO: consolidar filas idénticas sumando porcentajes ---
out = (out.groupby(["Pais","Pregunta","Respuesta","Valor"], observed=True, as_index=False)
           ["Porcentaje"].sum())

# redondeo final
out["Porcentaje"] = out["Porcentaje"].round(2)

out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"✓ Archivo generado: {OUTPUT_CSV}  |  Filas: {len(out):,}")

