import pandas as pd
from config import COLUMN_NAMES_CLEAN




def load_srl_data() -> pd.DataFrame:
    PATH_SRL_DATA = "data\Leistung_Ergebnisse_SRL_2023-01-01_2023-12-31.xlsx"
    # 1. Excel einlesen
    df = pd.read_excel(
        PATH_SRL_DATA,
        parse_dates=["DATE_FROM", "DATE_TO"],
    )

    # 2. PRODUCT in Richtung + Stunden splitten
    df[['direction', 'start_hour', 'end_hour']] = (
        df['PRODUCT']
          .str.split('_', expand=True)
    )
    df['start_hour'] = df['start_hour'].astype(int)

    # 3. Zeitindex bauen und timezone setzen
    df['timestamp'] = (
        df['DATE_FROM'].dt.normalize() +
        pd.to_timedelta(df['start_hour'], unit='h')
    ).dt.tz_localize("Europe/Berlin")
    df.set_index('timestamp', inplace=True)

    # 4. Pivot für alle drei Preis-Spalten gleichzeitig
    df_wide = df.pivot_table(
        index=df.index,
        columns='direction',
        values=[
            'TOTAL_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]',
            'TOTAL_MIN_CAPACITY_PRICE_[(EUR/MW)/h]',
            'TOTAL_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]'
        ]
    )

    # 5. MultiIndex flattenen und Spalten umbenennen
    #    aus (Metrik, Richtung) → SRL_<METRIK>_<POS/NEG>
    df_wide.columns = [
        f"SRL_{metric.split('_')[1]}_{direction}"
        for metric, direction in df_wide.columns
    ]

    # 6. Achsenname entfernen (war vorher "direction" bzw. der Name der oberen Ebene)
    df_wide.columns.name = None

    return df_wide




df = load_srl_data()
print(df)
# to csv
df.to_csv("srl_data.csv", index=True, sep=";")
