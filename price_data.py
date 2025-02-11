import pandas as pd


def get_market_price_data():
    data_file_path = "energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
    df = pd.read_csv(data_file_path, skiprows=2, names=["date", "market_price", "buy_volume", "buy_invest" "sell_volume", "sell_invest", "profit"])
    df['date'] = pd.to_datetime(df['date'], utc=True)
    start_date = pd.to_datetime("2023-07-07", utc=True)
    end_date = pd.to_datetime("2023-07-08", utc=True)
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return filtered_df


if __name__ == '__main__':
    df = get_market_price_data()
    print(df)