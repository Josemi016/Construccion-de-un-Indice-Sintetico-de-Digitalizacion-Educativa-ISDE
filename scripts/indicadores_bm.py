# -*- coding: utf-8 -*-
from pathlib import Path
import win32com.client as win32
import pandas as pd

DB_PATH = r"C:\Users\Usuario\Desktop\UNIR\TFM\Tabla_Maestra\HH 2017-2024 v250630.mdb"
OUT_CSV = Path(DB_PATH).with_name("EurostatNUEVO.csv")
OUT_XLSX = Path(DB_PATH).with_name("EurostatNUEVO.xlsx")

PERIOD = "2024A00"
TABLE = "[1_View AllData]"

sql = f"""
SELECT [ExpPeriod],[ExpCountry],[ExpVariable],[ExpBrkDwn],[ExpUnit],[Value]
FROM {TABLE}
WHERE [ExpPeriod]='{PERIOD}'
ORDER BY [ExpCountry], [ExpVariable], [ExpBrkDwn]
"""

print("Conectando a Access...")
acc = win32.Dispatch("Access.Application")
acc.OpenCurrentDatabase(DB_PATH)
db = acc.CurrentDb()

print("Ejecutando consulta...")
rs = db.OpenRecordset(sql)

print("Extrayendo todos los datos (GetRows)...")
rs.MoveLast()
total_rows = rs.RecordCount
rs.MoveFirst()

raw_data = rs.GetRows(total_rows)
rs.Close()

acc.CloseCurrentDatabase()
acc.Quit()
print("Access cerrado.")

print(f"Procesando {total_rows:,} filas...")
field_names = ["ExpPeriod", "ExpCountry", "ExpVariable", "ExpBrkDwn", "ExpUnit", "Value"]

data = list(zip(*raw_data))
df = pd.DataFrame(data, columns=field_names)

print(f"Total filas: {len(df):,}")
print(f"Total países: {df['ExpCountry'].nunique()}")
print(f"¿Está NO? {'SÍ' if 'NO' in df['ExpCountry'].values else 'NO'}")

# Opción 1: Exportar a CSV (sin límites)
print(f"\nExportando a CSV...")
df.to_csv(OUT_CSV, index=False, encoding='utf-8-sig')
print(f"CSV guardado: {OUT_CSV}")

# Opción 2: Exportar a Excel en múltiples hojas
print(f"\nExportando a Excel (múltiples hojas)...")
MAX_ROWS = 1000000  # Dejar margen bajo el límite de Excel

with pd.ExcelWriter(OUT_XLSX, engine='openpyxl') as writer:
    for i, start in enumerate(range(0, len(df), MAX_ROWS)):
        chunk = df.iloc[start:start + MAX_ROWS]
        sheet_name = f"Datos_{i+1}"
        chunk.to_excel(writer, index=False, sheet_name=sheet_name)
        print(f"  Hoja '{sheet_name}': {len(chunk):,} filas")

print(f"\n{'='*50}")
print(f"¡COMPLETADO!")
print(f"CSV: {OUT_CSV}")
print(f"XLSX: {OUT_XLSX} (múltiples hojas)")
print(f"{'='*50}")