import datetime
import pandas as pd
from utils import get_interval_minutes, calculate_period_in_days
from config import START_DATE, END_DATE, CSV_PATH, SKIPROWS, CELL_NAMES, DAYS



def create_dataframe(csv_path: str, skiprows: int, days) -> pd.DataFrame:
    df = pd.read_csv(
        csv_path,
        skiprows=skiprows,
        nrows=days*60/15*24+skiprows,
        names=[CELL_NAMES['date'], CELL_NAMES['market_price']],
    )
    return df



if __name__ == '__main__':
    df = create_dataframe(CSV_PATH, SKIPROWS, DAYS)
    #interval_minutes = get_interval_minutes(df)
    #n_days = calculate_period_in_days(START_DATE, END_DATE)
    print(df)
    #print(f"interval_minutes: {interval_minutes}")
    #print(f"n_days: {n_days}")

    df.to_excel("market_price_data.xlsx")
