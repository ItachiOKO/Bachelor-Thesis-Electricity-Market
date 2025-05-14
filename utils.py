from datetime import datetime
import pandas as pd
from config import SYSTEM_POWER


def get_interval_minutes(df: pd.DataFrame) -> int:
    diffs = df.index.to_series().diff().dropna()
    time_interval = diffs.mode()[0]
    return int(time_interval.total_seconds() / 60)

def calculate_period_in_days(start_date: str, end_date: str) -> int:
    return (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days

def get_charge_rate(interval_minutes):
    return SYSTEM_POWER * (interval_minutes/60)


def convert_datetime_to_string(df: pd.DataFrame) -> pd.DataFrame:
    formated_df = df.copy()
    formatted_index = []
    for idx in formated_df.index:
        timestamp_str = idx.strftime("%Y-%m-%d %H:%M:%S%z")
        if timestamp_str[-5:]:  # If there's a timezone offset
            formatted_str = timestamp_str[:-2] + ":" + timestamp_str[-2:]
            formatted_index.append(formatted_str)
        else:
            formatted_index.append(timestamp_str)
    
    formated_df.index = formatted_index
    return formated_df