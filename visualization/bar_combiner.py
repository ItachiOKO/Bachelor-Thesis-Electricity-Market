import pandas as pd

class MarketDataCombiner:
    
    def __init__(self):
        self._sources = []

    def add_source(self, data_dict: dict, market_name: str, value_col: str):
        if 'timeseries' in data_dict and isinstance(data_dict['timeseries'], pd.DataFrame):
            source_info = {
                'data': data_dict['timeseries'],
                'market_name': market_name,
                'value_col': value_col
            }
            self._sources.append(source_info)
            print(f"Quelle '{market_name}' erfolgreich hinzugefügt.")
        else:
            print(f"WARNUNG: Quelle für '{market_name}' konnte nicht hinzugefügt werden. "
                  "Das Dictionary enthält keinen 'timeseries'-DataFrame.")

    def get_combined_df(self, freq: str = 'W') -> pd.DataFrame:
        if not self._sources:
            print("Keine Quellen hinzugefügt. Gebe leeren DataFrame zurück.")
            return pd.DataFrame()

        processed_dfs_generator = (
            source['data'][source['value_col']]
            .resample(freq).sum()
            .to_frame()
            .assign(
                Zeitraum=lambda df: df.index.strftime('%Y - Woche %U'),
                Markt=source['market_name']
            )
            .rename(columns={source['value_col']: 'Wert'}) # Spalten vereinheitlichen
            for source in self._sources
            if source['value_col'] in source['data'].columns
        )

        try:
            combined_df = pd.concat(processed_dfs_generator)
            print("Kombinierter DataFrame erfolgreich erstellt.")
            return combined_df
        except ValueError:
            print("Konnte keinen kombinierten DataFrame erstellen (möglicherweise keine validen Daten).")
            return pd.DataFrame()