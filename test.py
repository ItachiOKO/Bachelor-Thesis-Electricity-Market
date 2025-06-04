import pandas as pd

from config import PATH_PRL_DATA

df = pd.read_excel('data/market_price_data.xlsx', index_col=0, parse_dates=True)

# Ermitteln, welche Index-Werte mehrfach vorkommen
dups = df.index[df.index.duplicated()]

if len(dups) > 0:
    # Einzigartige Duplikate anzeigen
    print("Folgende Datumswerte sind doppelt vorhanden:")
    for datum in sorted(set(dups)):
        print(datum.date())
else:
    print("Keine doppelten Datumswerte gefunden.")
