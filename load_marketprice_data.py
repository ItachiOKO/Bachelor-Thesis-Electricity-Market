import pandas as pd

from config import (
    START_DATE,
    END_DATE,
    PATH_MARKET_DATA,
    PATH_PRL_DATA,
    SKIPROWS,
    CELL_NAMES,
)

def create_dataframe(start_date, end_date):
    df_master = create_master_df(start_date, end_date)
    df_market_price = load_market_price_data()
    df_prl_price = load_prl_price_data()
    df = df_master.join(df_market_price, how='left')
    df = df.join(df_prl_price, how='left')
    return df

def create_master_df(start_date, end_date):
    master_index = pd.date_range(start=start_date, end=end_date, freq='15T')
    df_master = pd.DataFrame(index=master_index)
    return df_master

def load_market_price_data():
    df_market_price = pd.read_csv(
        PATH_MARKET_DATA,
        sep=";",
        skiprows=SKIPROWS,
        parse_dates=["timestamp"],
        index_col="timestamp",
    )
    return df_market_price

def load_prl_price_data():
    df_prl_price = pd.read_csv(
        PATH_PRL_DATA,
        sep=";",
        skiprows=SKIPROWS,
        parse_dates=["timestamp"],
        index_col="timestamp",
    )
    return df_prl_price

if __name__ == "__main__":
    df = create_dataframe(START_DATE, END_DATE)
    print(df)