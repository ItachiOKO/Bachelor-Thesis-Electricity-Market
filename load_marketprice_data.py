import datetime
from dateutil import parser
import pandas as pd
from utils import get_interval_minutes, calculate_period_in_days
from config import START_DATE, END_DATE, CSV_PATH, SKIPROWS, CELL_NAMES


def create_dataframe(csv_path: str, skiprows: int, start_date: str, end_date: str) -> pd.DataFrame:
    df = pd.read_csv(
        csv_path,
        skiprows=skiprows,
        names=[CELL_NAMES["date"], CELL_NAMES["market_price"]]
    )

    df[CELL_NAMES["date"]] = pd.to_datetime(df[CELL_NAMES["date"]], utc=True).dt.tz_localize(None)

    start_date = pd.to_datetime(start_date).tz_localize(None)
    end_date = pd.to_datetime(end_date).tz_localize(None)
    df = df[(df[CELL_NAMES["date"]] >= start_date) & (df[CELL_NAMES["date"]] < end_date)]
    df = df.set_index(CELL_NAMES["date"])

    return df



if __name__ == '__main__':
    df = create_dataframe(CSV_PATH, SKIPROWS, START_DATE, END_DATE)
    interval_minutes = get_interval_minutes(df)
    n_days = calculate_period_in_days(START_DATE, END_DATE)
    print(df)
    print(f"interval_minutes: {interval_minutes}")
    print(f"n_days: {n_days}")
    df.to_csv("market_price_data.csv", index=False)
