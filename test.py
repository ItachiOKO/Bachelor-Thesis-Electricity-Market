import requests
import pandas as pd

# 1) Parameter
filter_code = "123456789"  # Beispiel-Filtercode, anpassen!
region      = "DE"
resolution  = "hour"

# 2) Index abrufen
url_index   = f"https://www.smard.de/app/chart_data/{filter_code}/{region}/index_{resolution}.json"
resp_index  = requests.get(url_index, timeout=60)
resp_index.raise_for_status()
index_data  = resp_index.json()            # Dict mit key 'timestamps'

# 3) Letzten Timestamp wählen
latest_ts   = index_data['timestamps'][-1]
print(latest_ts)
# 4) Series abrufen
url_series  = (
    f"https://www.smard.de/app/chart_data/"
    f"{filter_code}/{region}/"
    f"{filter_code}_{region}_{resolution}_{latest_ts}.json"
)
resp_series = requests.get(url_series, timeout=60)
resp_series.raise_for_status()
series_data = resp_series.json()           # Dict mit keys 'meta_data' und 'series'



df = pd.DataFrame(series_data['series'])

# 2) Erste Spalte als Zeitindex umwandeln …
ts_col = df.columns[0]
df.index = pd.to_datetime(df[ts_col], unit='ms')
df.index.name = 'Zeitpunkt'

# 3) … und falls Du die ursprüngliche Timestamp-Spalte nicht mehr brauchst, entfernen
df = df.drop(columns=ts_col)

print(df.head())