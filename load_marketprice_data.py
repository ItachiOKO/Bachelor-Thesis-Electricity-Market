import pandas as pd
from config import (
    START_DATE,
    END_DATE,
    PATH_MARKET_DATA,
    PATH_PRL_DATA,
    CELL_NAMES,
)
from utils import convert_datetime_to_string

import logging

# Konfiguration des Loggings – falls noch nicht geschehen
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_dataframe(start_date, end_date, debug=False):
    if debug:
        logging.info("Erstelle Master-DataFrame von %s bis %s", start_date, end_date)
    df_master = create_master_df(start_date, end_date)
    if debug:
        logging.debug("Master-Index: Start=%s, Ende=%s, Länge=%d", 
                      df_master.index[0], df_master.index[-1], len(df_master.index))
    
    # Market Data
    if debug:
        logging.info("Lade Market Price DataFrame")
    df_market_price = load_market_data()
    if debug:
        logging.debug("Market Price Index: Start=%s, Ende=%s, Länge=%d", 
                      df_market_price.index[0], df_market_price.index[-1], len(df_market_price.index))
        logging.debug("Market Price Beispiel:\n%s", df_market_price.head())
    df_master = df_master.join(df_market_price, how='left')
    
    # PRL Data
    if debug:
        logging.info("Lade FCR Price DataFrame")
    df_fcr_price = load_prl_data()
    if debug:
        logging.debug("FCR Price Index: Start=%s, Ende=%s, Länge=%d", 
                      df_fcr_price.index[0], df_fcr_price.index[-1], len(df_fcr_price.index))
        logging.debug("FCR Price Beispiel:\n%s", df_fcr_price.head())
    df_master = df_master.join(df_fcr_price, how='left')
    
    # SRL Data
    if debug:
        logging.info("Lade SRL Price DataFrame")
    df_srl_price = load_srl_data()
    if debug:
        logging.debug("SRL Price Index: Start=%s, Ende=%s, Länge=%d", 
                      df_srl_price.index[0], df_srl_price.index[-1], len(df_srl_price.index))
        logging.debug("SRL Price Beispiel:\n%s", df_srl_price.head())
    df_master = df_master.join(df_srl_price, how='left')

    if debug:
        num_null_market = df_master[CELL_NAMES['market_price']].isna().sum()
        num_null_fcr = df_master[CELL_NAMES['prl_price']].isna().sum()
        # Für SRL-Spalten alle SRL_* Spalten zusammenzählen
        srl_cols = [col for col in df_master.columns if col.startswith('SRL_')]
        num_null_srl = df_master[srl_cols].isna().sum().sum()
        logging.debug("Anzahl NaN-Werte nach Join: Market Price=%d, FCR Price=%d, SRL Price=%d", 
                      num_null_market, num_null_fcr, num_null_srl)
    
    df_master.index.name = CELL_NAMES['date']
    df_master.fillna(0, inplace=True)
    
    if debug:
        logging.info("Finaler DataFrame: Shape=%s", df_master.shape)
        logging.debug("Vorschau des finalen DataFrames:\n%s", df_master.head())
    
    return df_master



def create_master_df(start_date, end_date):
    master_index = pd.date_range(start=start_date, end=end_date, freq='15T', tz='Europe/Berlin', inclusive='left')
    df = pd.DataFrame(index=master_index)
    return df

def load_market_data():
    df = pd.read_csv(
        PATH_MARKET_DATA,
        skiprows=2,
        names=[CELL_NAMES["date"], CELL_NAMES["market_price"]],
        parse_dates=[CELL_NAMES["date"]],
        index_col= [CELL_NAMES["date"]]
    )
    df.index = pd.to_datetime(df.index, utc=True).tz_convert("Europe/Berlin")
    return df


def load_prl_data() -> pd.DataFrame:
    df = pd.read_excel(
        PATH_PRL_DATA,
        parse_dates=["DATE_FROM", "DATE_TO"],
    )
    
    df["start_hour"] = (
        df["PRODUCTNAME"]
        .str.split("_")
        .str[1]        
        .astype(int)    
    )
    
    df[CELL_NAMES['date']] = (
        df["DATE_FROM"].dt.floor("D")  
        + pd.to_timedelta(df["start_hour"], unit="H")
    )

    df[CELL_NAMES['date']] = df[CELL_NAMES['date']].dt.tz_localize("Europe/Berlin")
    df.set_index(CELL_NAMES['date'], inplace=True)
    df = df[[CELL_NAMES['prl_price']]]
    return df

def load_srl_data() -> pd.DataFrame:
    PATH_SRL_DATA = 'data/Leistung_Ergebnisse_SRL_2023-01-01_2023-12-31.xlsx'
    # 1. Excel einlesen
    df = pd.read_excel(
        PATH_SRL_DATA,
        parse_dates=['DATE_FROM', 'DATE_TO'],
    )

    # 2. PRODUCT in Richtung + Stunden splitten
    df[['direction', 'start_hour', 'end_hour']] = (
        df['PRODUCT']
          .str.split('_', expand=True)
    )
    df['start_hour'] = df['start_hour'].astype(int)

    # 3. Zeitindex bauen und timezone setzen
    df['timestamp'] = (
        df['DATE_FROM'].dt.normalize()
        + pd.to_timedelta(df['start_hour'], unit='h')
    ).dt.tz_localize('Europe/Berlin')
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
    df_wide.columns = [
        f"SRL_{metric.split('_')[1]}_{direction}"
        for metric, direction in df_wide.columns
    ]

    # 6. Achsenname entfernen
    df_wide.columns.name = None

    return df_wide


if __name__ == "__main__":
    df = create_dataframe(START_DATE, END_DATE, debug=False)
    print(df)
    # to excel

    formated_df = convert_datetime_to_string(df)       
    formated_df.to_excel("market_price_data.xlsx", index=True, sheet_name="Market Price Data")
