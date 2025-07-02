import pandas as pd
import re
from pathlib import Path
import glob

# 1) Normalisierungsfunktion
def normalize_col(col: str) -> str:
    col = col.lower()
    col = re.sub(r"\s*\(.*?\)", "", col)  # alles in () entfernen
    return col.strip()

# 2) Excel-Dateien sammeln
files = sorted(glob.glob("Energy-Charts - *.xlsx"))

# 3) Header und Mapping original→normalisiert einlesen
norm_cols_by_file = {}   # Dateistem → Liste normierter Spalten
orig_map_by_file = {}    # Dateistem → Dict(normiert → [Originalnamen])

for file in files:
    stem = Path(file).stem
    df = pd.read_excel(file, nrows=0)
    norms = []
    mapping = {}
    for orig in df.columns:
        norm = normalize_col(orig)
        norms.append(norm)
        mapping.setdefault(norm, []).append(orig)
    norm_cols_by_file[stem] = norms
    orig_map_by_file[stem] = mapping

# 4) Gemeinsame, alle und unterschiedliche Spalten ermitteln
sets = [set(cols) for cols in norm_cols_by_file.values()]
common = set.intersection(*sets)
all_cols = set.union(*sets)
diff = all_cols - common

# 5) Ausgabe
print("=== Normalisierte Spalten in ALLEN Dateien ===")
for c in sorted(common):
    print(f"  {c}")
    for stem in norm_cols_by_file:
        origs = orig_map_by_file[stem].get(c, [])
        print(f"    {stem}: {origs}")

print("\n=== Normalisierte Spalten NICHT in allen Dateien ===")
for c in sorted(diff):
    print(f"  {c}")
    for stem, cols in norm_cols_by_file.items():
        if c in cols:
            origs = orig_map_by_file[stem][c]
            print(f"    {stem}: {origs}")
