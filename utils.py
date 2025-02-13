def get_interval_time():
    df = get_market_price_data()  
    df['date'] = pd.to_datetime(df['date'])  
    time_interval = df['date'].diff().dropna().mode()[0]  
    return int(time_interval.total_seconds() / 60)
