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
    df_market_price = load_market_data()
    df_fcr_price = load_fcr_data()
    df_master = df_master.join(df_market_price, how='left')
    df_master = df_master.join(df_fcr_price, how='left')
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
    df = create_dataframe(START_DATE, END_DATE)
    print(df)
