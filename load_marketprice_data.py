import datetime
from dateutil import parser
import numpy as np
import pandas as pd
from utils import get_interval_minutes, calculate_period_in_days
from config import START_DATE, END_DATE, PATH_MARKET_DATA, PATH_PRL_DATA, SKIPROWS, CELL_NAMES


def create_dataframe(csv_path: str, skiprows: int, start_date: str, end_date: str) -> pd.DataFrame:
    df = pd.read_csv(
        csv_path,
        skiprows=skiprows,
        names=[CELL_NAMES["date"], CELL_NAMES["market_price"]]
    )

    df[CELL_NAMES["date"]] = pd.to_datetime(df[CELL_NAMES["date"]], utc=True)

    start_date = pd.to_datetime(start_date).tz_localize('UTC')
    end_date = pd.to_datetime(end_date).tz_localize('UTC')
    df = df[(df[CELL_NAMES["date"]] >= start_date) & (df[CELL_NAMES["date"]] < end_date)]
    df = df.set_index(CELL_NAMES["date"])

    #mask = ~df.index.floor('4H').duplicated()
    #df[CELL_NAMES["prl_price"]] = 0
    #df.loc[mask, CELL_NAMES["prl_price"]] = PRL_PRICE
    df_prl_data = read_prl_price_data()
    df = df.join(
        df_prl_data[['GERMANY_SETTLEMENTCAPACITY_PRICE_[EUR/MW]']], 
        how='left'
    )
    df = df.fillna(0)
    return df


def read_prl_price_data():
    df = pd.read_excel(PATH_PRL_DATA)
    df['DATE_FROM'] = pd.to_datetime(df['DATE_FROM'], dayfirst=True)
    df['DATE_TO']   = pd.to_datetime(df['DATE_TO'],   dayfirst=True)

    df[['start_hour','end_hour']] = (
        df['PRODUCTNAME']
        .str.extract(r'_(\d{2})_(\d{2})')  # Regex fängt die zwei Stunden-Angaben ab
        .astype(int)
    )
    df['start_time_local'] = df.apply(
        lambda row: row['DATE_FROM'] + pd.Timedelta(hours=row['start_hour']), 
        axis=1
    )
    df['start_time_local'] = df['start_time_local'].dt.tz_localize('Europe/Berlin')
    df['start_time_utc']   = df['start_time_local'].dt.tz_convert('UTC')
    df = df.set_index('start_time_utc')
    df.drop(['start_time_local', 'start_hour', 'end_hour'], axis=1, inplace=True)
    return df



if __name__ == '__main__':
    df = create_dataframe(PATH_MARKET_DATA, SKIPROWS, START_DATE, END_DATE)
    interval_minutes = get_interval_minutes(df)
    n_days = calculate_period_in_days(START_DATE, END_DATE)
    print(df)
    print(f"interval_minutes: {interval_minutes}")
    print(f"n_days: {n_days}")
    df.to_csv("market_price_data.csv", index=True)
