import pandas as pd

START_DATE = "2023-07-07"
END_DATE = "2023-07-08"

def get_market_price_data():
    data_file_path = "energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
    df = pd.read_csv(data_file_path, skiprows=2, names=["date", "market_price", "buy_volume", "charge_volume", "sell_volume", "discharge_volume" "battery_soc"])
    df['date'] = pd.to_datetime(df['date'], utc=True)
    start_date = pd.to_datetime(START_DATE, utc=True)
    end_date = pd.to_datetime(END_DATE, utc=True)
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return filtered_df

def get_interval_time():
    df = get_market_price_data()  
    df['date'] = pd.to_datetime(df['date'])  
    time_interval = df['date'].diff().dropna().mode()[0]  
    return int(time_interval.total_seconds() / 60)


if __name__ == '__main__':
    df = get_market_price_data()
    interval_time = get_interval_time()
    print(df)
    print(interval_time)