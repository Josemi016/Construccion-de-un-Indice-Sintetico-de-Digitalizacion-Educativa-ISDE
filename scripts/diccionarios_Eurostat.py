# -*- coding: utf-8 -*-
"""
Unifica varios CSVs de dimensiones en un único dataset.

- Lee:
  * Eurydice_DIMENSIONES_datos.csv       -> Estudio = "Eurydice"
  * TALIS_2024_DIMENSIONES_datos.csv     -> Estudio = "TALIS"
  * UNESCO_DIMENSIONES_datos.csv         -> Estudio = "UNESCO"
  * EuroStatDESI_DIMENSIONES_datos.csv   -> Estudio = "EuroStat"

- Guarda:
  * tabla_maestra.csv      (UTF-8-SIG)
  * tabla_maestra.parquet  (si hay pyarrow)

NOVEDADES:
- Normaliza las distintas columnas de país en una sola ('Pais').
- Traduce los códigos ISO2 y ISO3 a nombres completos de los países.
- FILTRA las filas para incluir ÚNICAMENTE los países del diccionario.
- Elimina columnas innecesarias definidas en la lista COLUMNAS_A_ELIMINAR.
"""

import csv
from pathlib import Path
from typing import List, Tuple

import pandas as pd


# =========================
# Configuración (RUTAS Y DICCIONARIOS)
# =========================
OUTPUT_DIR = Path(r"C:\Users\Usuario\Desktop\UNIR\TFM\Tablas\Dimensiones")

SOURCES = [
    {
        "path": r"C:\Users\Usuario\Desktop\UNIR\TFM\Tablas\Dimensiones\Eurydice_DIMENSIONES_datos.csv",
        "type": "csv",
        "estudio": "Eurydice",
    },
    {
        "path": r"C:\Users\Usuario\Desktop\UNIR\TFM\Tablas\Dimensiones\TALIS_2024_DIMENSIONES_datos.csv",
        "type": "csv",
        "estudio": "TALIS",
    },
    {
        "path": r"C:\Users\Usuario\Desktop\UNIR\TFM\Tablas\Dimensiones\UNESCO_DIMENSIONES_datos.csv",
        "type": "csv",
        "estudio": "UNESCO",
    },
    {
        "path": r"C:\Users\Usuario\Desktop\UNIR\TFM\Tablas\Dimensiones\EuroStatDESI_DIMENSIONES_datos.csv",
        "type": "csv",
        "estudio": "EuroStat",
    },
]

OUTPUT_CSV = OUTPUT_DIR / "tabla_maestra.csv"
OUTPUT_PARQUET = OUTPUT_DIR / "tabla_maestra.parquet"

COLUMNAS_A_ELIMINAR = [
    'Año', 'Calificador', 'Código_ISO', 'Desagregación_Codigo', 'Desagregacion_Codigo', 'Pais_Descripcion', 'Respuesta'
    'Desagregacion_Descripcion', 'ID_Indicador', 'Indicador', 
    'Magnitud', 'Nivel_Educación', 'Periodo', 'Tipo_Recurso', 
    'Unidad_Codigo', 'Unidad_Descripcion', 'Variable_Codigo', 
    'Variable_Descripcion'
]

# Diccionario unificado para mapear tanto ISO2 como ISO3 al nombre del país
ISO_A_PAIS = {
    'AL': 'Albania', 'ALB': 'Albania',
    'AT': 'Austria', 'AUT': 'Austria',
    'BG': 'Bulgaria', 'BGR': 'Bulgaria',
    'CZ': 'Chequia', 'CZE': 'Chequia',
    'CY': 'Chipre', 'CYP': 'Chipre',
    'HR': 'Croacia', 'HRV': 'Croacia',
    'DK': 'Dinamarca', 'DNK': 'Dinamarca',
    'SK': 'Eslovaquia', 'SVK': 'Eslovaquia',
    'SI': 'Eslovenia', 'SVN': 'Eslovenia',
    'ES': 'España', 'ESP': 'España',
    'EE': 'Estonia', 'EST': 'Estonia',
    'FI': 'Finlandia', 'FIN': 'Finlandia',
    'FR': 'Francia', 'FRA': 'Francia',
    'HU': 'Hungría', 'HUN': 'Hungría',
    'IT': 'Italia', 'ITA': 'Italia',
    'LV': 'Letonia', 'LVA': 'Letonia',
    'LT': 'Lituania', 'LTU': 'Lituania',
    'MK': 'Macedonia del Norte', 'MKD': 'Macedonia del Norte',
    'MT': 'Malta', 'MLT': 'Malta',
    'ME': 'Montenegro', 'MNE': 'Montenegro',
    'NO': 'Noruega', 'NOR': 'Noruega',
    'NL': 'Países Bajos', 'NLD': 'Países Bajos',
    'PL': 'Polonia', 'POL': 'Polonia',
    'PT': 'Portugal', 'PRT': 'Portugal',
    'RO': 'Rumanía', 'ROU': 'Rumanía',
    'RS': 'Serbia', 'SRB': 'Serbia',
    'SE': 'Suecia', 'SWE': 'Suecia',
    'TR': 'Turquía', 'TUR': 'Turquía'
}

# Lista maestra de países válidos (los valores únicos del diccionario)
PAISES_VALIDOS = set(ISO_A_PAIS.values())


# =========================
# Utilidades
# =========================
def detect_sep_and_encoding(path: str, sample_size: int = 200_000) -> Tuple[str, str]:
    for enc in ("utf-8-sig", "utf-8", "latin1"):
        try:
            with open(path, "r", encoding=enc, errors="ignore") as f:
                sample = f.read(sample_size)
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            return dialect.delimiter, enc
        except Exception:
            continue
    return ",", "utf-8-sig"


def csv_header(path: str) -> List[str]:
    sep, enc = detect_sep_and_encoding(path)
    df0 = pd.read_csv(path, sep=sep, encoding=enc, nrows=0, engine="python")
    return [str(c).strip().replace("\ufeff", "") for c in df0.columns]


def compute_union_columns(sources: list) -> List[str]:
    """Calcula la unión de columnas simulando los descartes y mapeos."""
    cols = set()
    variaciones_pais = {'Pais', 'País', 'País_Descripcion'}
    columnas_eliminar_set = set(COLUMNAS_A_ELIMINAR)

    for s in sources:
        p = s["path"]
        headers = csv_header(p)
        
        has_country = any(c in variaciones_pais for c in headers)
        headers_filtrados = [c for c in headers if c not in columnas_eliminar_set and c not in variaciones_pais]
        
        if has_country:
            headers_filtrados.append('Pais')

        cols.update(headers_filtrados)

    cols.discard("Estudio")
    return ["Estudio"] + sorted(cols)


def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica la normalización de columnas, unificación de país, filtrado y borrado."""
    # 1. Normalizar nombres de columnas
    df.columns = [str(c).strip().replace("\ufeff", "") for c in df.columns]

    # 2. Unificar País
    variaciones = ['Pais', 'País', 'País_Descripcion']
    cols_presentes = [c for c in variaciones if c in df.columns]

    if cols_presentes:
        df['Pais_Temp'] = df[cols_presentes[0]]
        for col in cols_presentes[1:]:
            df['Pais_Temp'] = df['Pais_Temp'].fillna(df[col])
        
        # Mapeamos usando el diccionario
        df['Pais'] = df['Pais_Temp'].replace(ISO_A_PAIS)
        
        # Limpiamos las columnas antiguas y la temporal
        cols_a_borrar = [c for c in cols_presentes if c != 'Pais']
        df.drop(columns=cols_a_borrar + ['Pais_Temp'], errors='ignore', inplace=True)

    # 3. Filtrar por países válidos
    if 'Pais' in df.columns:
        # Se queda solo con las filas donde el país está en nuestra lista maestra
        df = df[df['Pais'].isin(PAISES_VALIDOS)]

    # 4. Eliminar columnas no deseadas
    df.drop(columns=COLUMNAS_A_ELIMINAR, errors='ignore', inplace=True)

    return df


# =========================
# Writer Parquet
# =========================
class ParquetStreamWriter:
    def __init__(self, out_path: Path, schema):
        self.out_path = out_path
        self.schema = schema
        self._writer = None
        self._pa = None
        self._pq = None

    def _lazy_init(self):
        import pyarrow.parquet as pq
        self._pq = pq
        self._writer = pq.ParquetWriter(str(self.out_path), self.schema)

    def write(self, df: pd.DataFrame):
        if df.empty:
            return
        if self._writer is None:
            self._lazy_init()

        df_str = df.astype("string")
        import pyarrow as pa
        self._pa = pa

        table = pa.Table.from_pandas(df_str, schema=self.schema, preserve_index=False, safe=False)
        self._writer.write_table(table)

    def close(self):
        if self._writer is not None:
            self._writer.close()
            self._writer = None


# =========================
# Pipeline
# =========================
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("[INFO] Calculando unión de columnas (para normalizar)...")
    union_cols = compute_union_columns(SOURCES)
    print(f"[INFO] Total columnas finales (incluye 'Estudio'): {len(union_cols)}")

    if OUTPUT_CSV.exists():
        OUTPUT_CSV.unlink()
    if OUTPUT_PARQUET.exists():
        OUTPUT_PARQUET.unlink()

    parquet_writer = None
    parquet_enabled = False
    try:
        import pyarrow as pa
        parquet_schema = pa.schema([(c, pa.string()) for c in union_cols])
        parquet_writer = ParquetStreamWriter(OUTPUT_PARQUET, parquet_schema)
        parquet_enabled = True
    except Exception:
        print("[WARN] No se pudo importar 'pyarrow'. Solo CSV.")

    csv_header_written = False

    for s in SOURCES:
        p = s["path"]
        estudio = s["estudio"]
        print(f"\n[INFO] Procesando: {estudio}  |  {p}")

        sep, enc = detect_sep_and_encoding(p)
        print(f"[INFO] CSV detectado: sep='{sep}'  encoding='{enc}'")

        chunksize = 250_000
        for i, chunk in enumerate(
            pd.read_csv(p, sep=sep, encoding=enc, engine="python", chunksize=chunksize)
        ):
            # --- TRANSFORMACIONES ---
            chunk = transformar_datos(chunk)

            if chunk.empty:
                continue

            chunk.insert(0, "Estudio", estudio)
            chunk = chunk.reindex(columns=union_cols)

            chunk.to_csv(OUTPUT_CSV, mode="a", index=False, header=not csv_header_written, encoding="utf-8-sig")
            csv_header_written = True

            if parquet_enabled and parquet_writer is not None:
                parquet_writer.write(chunk)

            if i == 0:
                print(f"[INFO] Primer chunk filas válidas: {len(chunk):,} (de bloque={chunksize:,})")
            elif (i + 1) % 10 == 0:
                print(f"[INFO] Chunks procesados: {i+1}")

        print(f"[INFO] CSV completado para {estudio}.")

    if parquet_enabled and parquet_writer is not None:
        parquet_writer.close()

    print("\n" + "=" * 80)
    print(f"✓ CSV generado:     {OUTPUT_CSV}   (UTF-8-SIG)")
    if parquet_enabled:
        print(f"✓ Parquet generado: {OUTPUT_PARQUET}")
    print("=" * 80)


if __name__ == "__main__":
    main()