import datetime
from dateutil import parser
import pandas as pd
from utils import get_interval_minutes, calculate_period_in_days
from config import START_DATE, END_DATE, CSV_PATH, SKIPROWS, CELL_NAMES



def create_dataframe(csv_path: str, skiprows: int, start_date: str, end_date: str) -> pd.DataFrame:
    # CSV einlesen, wobei "date" als String bleibt
    df = pd.read_csv(
        csv_path,
        skiprows=skiprows,
        names=[CELL_NAMES['date'], CELL_NAMES['market_price']]
    )
    df['time'] = df['date'].apply(lambda x: x.split("T")[1])  
    df['date'] = df['date'].apply(lambda x: parser.parse(x, ignoretz=True).date())
    mask = (df["date"] >= pd.to_datetime(start_date).date()) & (df["date"] < pd.to_datetime(end_date).date())
    filtered_df = df.loc[mask]
    filtered_df = filtered_df[['date', 'time', CELL_NAMES['market_price']]]

    return filtered_df








if __name__ == '__main__':
    df = create_dataframe(CSV_PATH, SKIPROWS, START_DATE, END_DATE)
    #interval_minutes = get_interval_minutes(df)
    #n_days = calculate_period_in_days(START_DATE, END_DATE)
    print(df)
    #print(f"interval_minutes: {interval_minutes}")
    #print(f"n_days: {n_days}")

    df.to_excel("market_price_data.xlsx")
