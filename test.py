from config import PATH_PRL_DATA
import pandas as pd

import pandas as pd

def read_prl_price_data():

    df = pd.read_excel(PATH_PRL_DATA)
    df['DATE_FROM'] = pd.to_datetime(df['DATE_FROM'], dayfirst=True)
    df['DATE_TO']   = pd.to_datetime(df['DATE_TO'],   dayfirst=True)

    df[['start_hour','end_hour']] = (
        df['PRODUCTNAME']
        .str.extract(r'_(\d{2})_(\d{2})')  # Regex fängt die zwei Stunden-Angaben ab
        .astype(int)
    )
    df['start_time_local'] = df.apply(
        lambda row: row['DATE_FROM'] + pd.Timedelta(hours=row['start_hour']), 
        axis=1
    )
    df['start_time_local'] = df['start_time_local'].dt.tz_localize('Europe/Berlin')
    df['start_time_utc']   = df['start_time_local'].dt.tz_convert('UTC')
    df = df.set_index('start_time_utc')
    df.drop(['start_time_local', 'start_hour', 'end_hour'], axis=1, inplace=True)

    df["GERMANY_SETTLEMENTCAPACITY_PRICE_[EUR/MW]"] = df["GERMANY_SETTLEMENTCAPACITY_PRICE_[EUR/MW]"].str.replace(',', '.').astype(float)