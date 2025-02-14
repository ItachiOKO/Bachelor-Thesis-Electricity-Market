import pandas as pd
from utils import get_interval_minutes, calculate_period_in_days
from config import START_DATE, END_DATE


def get_market_price_data():
    data_file_path = "energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
    df = pd.read_csv(data_file_path, skiprows=2, names=["date", "market_price", "buy_volume", "sell_volume", "battery_soc"])
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['date'] = df['date'].dt.tz_localize(None)
    filtered_df = df[(df['date'] >= START_DATE) & (df['date'] < END_DATE)].copy()
    return filtered_df

if __name__ == '__main__':


    df = get_market_price_data()
    #interval_minutes = get_interval_minutes(df)
    #n_days = calculate_period_in_days(START_DATE, END_DATE)
    print(df)
    #print(f"interval_minutes: {interval_minutes}")
    #print(f"n_days: {n_days}")

