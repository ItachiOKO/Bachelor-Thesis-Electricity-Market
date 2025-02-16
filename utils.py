from datetime import datetime
import pandas as pd
from config import SPECIFIC_CHARGE_RATE, CELL_NAMES


def get_interval_minutes(df: pd.DataFrame) -> int:
    df_copy = df.copy()
    df_copy[CELL_NAMES['time']] = pd.to_datetime(df_copy[CELL_NAMES['time']], utc=True)
    diffs = df_copy[CELL_NAMES['time']].diff().dropna()
    time_interval = diffs.mode()[0]
    return int(time_interval.total_seconds() / 60)

def calculate_period_in_days(start_date: str, end_date: str) -> int:
    return (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days

def get_charge_rate(interval_minutes):
    return SPECIFIC_CHARGE_RATE * (interval_minutes/60)
