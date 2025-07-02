import pandas as pd

# Datei einlesen
df = pd.read_excel("Energy-Charts 2021 bis 2024.xlsx")

# Anzahl fehlender Werte pro Spalte
missing = df.isna().sum().sort_values(ascending=False)

# Anteil fehlender Werte in Prozent
percent = (missing / len(df) * 100).round(2)

# Zusammenfassung als DataFrame
summary = pd.DataFrame({
    "Fehlende Werte": missing,
    "Anteil (%)": percent
})
#write summary to text file
summary_file = "missing_values_summary.txt"
summary.to_csv(summary_file, sep="\t", index=True)
print(summary)
