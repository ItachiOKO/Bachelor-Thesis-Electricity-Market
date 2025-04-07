import pandas as pd
from config import (
    START_DATE,
    END_DATE,
    PATH_MARKET_DATA,
    PATH_PRL_DATA,
    SKIPROWS,
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
    
    if debug:
        logging.info("Lade Market Price DataFrame")
    df_market_price = load_market_data()
    if debug:
        logging.debug("Market Price Index: Start=%s, Ende=%s, Länge=%d", 
                      df_market_price.index[0], df_market_price.index[-1], len(df_market_price.index))
        logging.debug("Market Price Beispiel:\n%s", df_market_price.head())
    
    if debug:
        logging.info("Lade FCR Price DataFrame")
    df_fcr_price = load_fcr_data()
    if debug:
        logging.debug("FCR Price Index: Start=%s, Ende=%s, Länge=%d", 
                      df_fcr_price.index[0], df_fcr_price.index[-1], len(df_fcr_price.index))
        logging.debug("FCR Price Beispiel:\n%s", df_fcr_price.head())
    
    if debug:
        logging.info("Führe Join der DataFrames durch")
    # Hier wird per join gearbeitet – beachte, dass dafür die Indizes exakt übereinstimmen müssen.
    df_master = df_master.join(df_market_price, how='left')
    df_master = df_master.join(df_fcr_price, how='left')
    
    if debug:
        num_null_market = df_master[CELL_NAMES["market_price"]].isna().sum()
        num_null_fcr = df_master[CELL_NAMES["prl_price"]].isna().sum()
        logging.debug("Anzahl NaN-Werte nach Join: Market Price=%d, FCR Price=%d", 
                      num_null_market, num_null_fcr)
    
    df_master.index.name = CELL_NAMES["date"]
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


def load_fcr_data() -> pd.DataFrame:
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


if __name__ == "__main__":
    df = create_dataframe(START_DATE, END_DATE, debug=True)
    print(df)
    # to excel

    formated_df = convert_datetime_to_string(df)       
    formated_df.to_excel("market_price_data.xlsx", index=True, sheet_name="Market Price Data")
