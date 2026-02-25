import win32com.client as win32
from pathlib import Path
import pandas as pd

# --- RUTAS ---
DB_PATH = r"C:\Users\Usuario\Desktop\UNIR\TFM\Tabla_Maestra\HH 2017-2024 v250630.mdb"
XLSX_PATH = r"C:\Users\Usuario\Desktop\UNIR\TFM\Tabla_Maestra\EurostatDESI.xlsx"

TABLES = {
    "BrkDwns": "BrkDwns",
    "Units": "Units",
    "Variables": "Variables",
}


def recordset_to_dataframe(rs):
    """Convierte un DAO.Recordset de Access en un pandas.DataFrame"""
    # nombres de columnas
    cols = [rs.Fields(i).Name for i in range(rs.Fields.Count)]
    data = []
    while not rs.EOF:
        row = [rs.Fields(i).Value for i in range(rs.Fields.Count)]
        data.append(row)
        rs.MoveNext()
    return pd.DataFrame(data, columns=cols)


# --- Abrir Access ---
acc = win32.Dispatch("Access.Application")
acc.OpenCurrentDatabase(DB_PATH)
db = acc.CurrentDb()

# --- Leer tablas en dataframes ---
dfs = {}
for sheet_name, table_name in TABLES.items():
    rs = db.OpenRecordset(table_name)
    dfs[sheet_name] = recordset_to_dataframe(rs)
    rs.Close()

# --- Cerrar Access ---
acc.CloseCurrentDatabase()
acc.Quit()

# --- Escribir en Excel ---
xlsx_file = Path(XLSX_PATH)
mode = "a" if xlsx_file.exists() else "w"

with pd.ExcelWriter(XLSX_PATH, engine="openpyxl", mode=mode,
                    if_sheet_exists="replace") as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Diccionarios exportados a:", XLSX_PATH)