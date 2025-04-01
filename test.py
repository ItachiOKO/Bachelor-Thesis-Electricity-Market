import pandas as pd
from config import PATH_MARKET_DATA, SKIPROWS


def load_market_price_data():
    df_market_price = pd.read_csv(
        PATH_MARKET_DATA,
        sep=";",
        skiprows=SKIPROWS,
    )
    return df_market_price


df_market_price = load_market_price_data()
print(df_market_price)