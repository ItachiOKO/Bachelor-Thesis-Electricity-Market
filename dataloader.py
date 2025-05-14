import pandas as pd
from config import (
    START_DATE,
    END_DATE,
    PATH_MARKET_DATA,
    PATH_PRL_DATA,
    PATH_SRL_DATA,
    ColumnNamesRaw as CR,
    ColumnNamesClean as CC,
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
    
    ## Market Data
    if debug:
        logging.info("Lade Market Price DataFrame")
    df_market_price = load_market_data()
    if debug:
        logging.debug("Market Price Index: Start=%s, Ende=%s, Länge=%d", 
                      df_market_price.index[0], df_market_price.index[-1], len(df_market_price.index))
        logging.debug("Market Price Beispiel:\n%s", df_market_price.head())
    df_master = df_master.join(df_market_price, how='left')
    
    ## PRL Data
    if debug:
        logging.info("Lade FCR Price DataFrame")
    df_prl_price = load_prl_data()
    if debug:
        logging.debug("FCR Price Index: Start=%s, Ende=%s, Länge=%d", 
                      df_prl_price.index[0], df_prl_price.index[-1], len(df_prl_price.index))
        logging.debug("FCR Price Beispiel:\n%s", df_prl_price.head())
    df_master = df_master.join(df_prl_price, how='left')
    
    ## SRL Data
    if debug:
        logging.info("Lade SRL Price DataFrame")
    df_srl_price = load_srl_power_data()
    if debug:
        logging.debug("SRL Price Index: Start=%s, Ende=%s, Länge=%d", 
                      df_srl_price.index[0], df_srl_price.index[-1], len(df_srl_price.index))
        logging.debug("SRL Price Beispiel:\n%s", df_srl_price.head())
    df_master = df_master.join(df_srl_price, how='left')

    if debug:
        num_null_market = df_master[CC.market_price].isna().sum()
        num_null_fcr = df_master[CC.prl_price].isna().sum()
        # Für SRL-Spalten alle SRL_* Spalten zusammenzählen
        srl_cols = [col for col in df_master.columns if col.startswith('SRL_')]
        num_null_srl = df_master[srl_cols].isna().sum().sum()
        logging.debug("Anzahl NaN-Werte nach Join: Market Price=%d, FCR Price=%d, SRL Price=%d", 
                      num_null_market, num_null_fcr, num_null_srl)
    
    df_master.index.name = CC.date
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
        names=[CC.date, CC.market_price],
        parse_dates=[CC.date],
        index_col= [CC.date]
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
    
    df[CC.date] = (
        df["DATE_FROM"].dt.floor("D")  
        + pd.to_timedelta(df["start_hour"], unit="H")
    )

    df[CC.date] = df[CC.date].dt.tz_localize("Europe/Berlin")
    df.set_index(CC.date, inplace=True)

    df = df[[CR.prl_price]]    # <-- echtes DataFrame, kein Python-List-Literal
    # optional: gleich umbenennen
    df.columns = [ CC.prl_price ]

    return df


def load_srl_power_data() -> pd.DataFrame:
    df = pd.read_excel(
        PATH_SRL_DATA,
        parse_dates=['DATE_FROM', 'DATE_TO'],
    )

    parts = df['PRODUCT'].str.split('_', expand=True)
    df['direction']  = parts[0]       # 'POS' oder 'NEG'
    df['start_hour'] = parts[1].astype(int)

    df['timestamp'] = (
        df['DATE_FROM'].dt.normalize()
        + pd.to_timedelta(df['start_hour'], unit='h')
    ).dt.tz_localize('Europe/Berlin')
    df = df.set_index('timestamp')

    # direction als zweites Index-Level hinzunehmen, dann unstacken
    df_wide = (
        df
        .set_index('direction', append=True)[CR.srl_power_price]
        .unstack('direction')
    )

    # Spalten umbenennen
    df_wide.columns = [
       CC.srl_power_price_pos if d == 'POS'
        else CC.srl_power_price_neg
        for d in df_wide.columns
    ]

    return df_wide


def load_srl_energy_data() -> pd.DataFrame:
    df = pd.read_excel(
        PATH_SRL_DATA,
        parse_dates=['DATE_FROM', 'DATE_TO'],
    )

    parts = df['PRODUCT'].str.split('_', expand=True)
    df['direction']  = parts[0]       # 'POS' oder 'NEG'
    df['start_hour'] = parts[1].astype(int)

    df['timestamp'] = (
        df['DATE_FROM'].dt.normalize()
        + pd.to_timedelta(df['start_hour'], unit='h')
    ).dt.tz_localize('Europe/Berlin')
    df = df.set_index('timestamp')

    # direction als zweites Index-Level hinzunehmen, dann unstacken
    df_wide = (
        df
        .set_index('direction', append=True)[CR.srl_power_price]
        .unstack('direction')
    )

    # Spalten umbenennen
    df_wide.columns = [
       CC.srl_power_price_pos if d == 'POS'
        else CC.srl_power_price_neg
        for d in df_wide.columns
    ]

    return df_wide


if __name__ == "__main__":
    df = create_dataframe(START_DATE, END_DATE, debug=False)
    print(df)
    # to excel

    formated_df = convert_datetime_to_string(df)       
    formated_df.to_excel("market_price_data.xlsx", index=True, sheet_name="Market Price Data")
