import datetime
import pandas as pd
from utils import get_interval_minutes, calculate_period_in_days
from config import START_DATE, END_DATE


def create_time_indexed_dataframe(start_date: str, end_date: str, step_interval: str) -> pd.DataFrame:
    date_index = pd.date_range(
        start=start_date,
        end=end_date,
        freq=step_interval,
        inclusive='left'     
    )
    return pd.DataFrame(index=date_index)

def load_raw_data_from_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(
        csv_path,
        skiprows=2,
        names=["date", "market_price"]
    )

    def parse_and_remove_offset(date_str):
        dt_with_tz = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M%z")
        return dt_with_tz.replace(tzinfo=None)
    df['date'] = df['date'].apply(parse_and_remove_offset)

    return df

def merge_time_index_with_data(time_df: pd.DataFrame, raw_df: pd.DataFrame,
                               start_date: str, end_date: str) -> pd.DataFrame:
    mask = (raw_df['date'] >= start_date) & (raw_df['date'] < end_date)
    filtered_df = raw_df.loc[mask].copy()
    filtered_df.set_index('date', inplace=True)
    merged_df = time_df.merge(filtered_df, how='left', left_index=True, right_index=True)
    return merged_df

def create_dataframe(start_date: str,
                     end_date: str,
                     csv_path: str = "energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
                    ) -> pd.DataFrame:

    time_df = create_time_indexed_dataframe(start_date, end_date, step_interval="15min")	
    raw_df = load_raw_data_from_csv(csv_path)
    final_df = merge_time_index_with_data(time_df, raw_df, start_date, end_date)
    return final_df




if __name__ == '__main__':
    df = create_dataframe(START_DATE, END_DATE)
    interval_minutes = get_interval_minutes(df)
    n_days = calculate_period_in_days(START_DATE, END_DATE)
    print(df)
    print(f"interval_minutes: {interval_minutes}")
    print(f"n_days: {n_days}")

