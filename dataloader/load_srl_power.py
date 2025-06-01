import os
import pandas as pd
from utils import get_pickle_path



def load_srl_power_data(path, cr_srl_power_price, cc_srl_power_price_pos, cc_srl_power_price_neg) -> pd.DataFrame:
    pkl_path = get_pickle_path(path)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    df = pd.read_excel(
        path,
        usecols=['DATE_FROM', 'DATE_TO', 'PRODUCT', cr_srl_power_price],
        parse_dates=['DATE_FROM', 'DATE_TO'],
        engine='openpyxl',
    )


    parts = df['PRODUCT'].str.split('_', expand=True)
    df['direction']  = parts[0]       # 'POS' oder 'NEG'
    df['start_hour'] = parts[1].astype(int)

    df['timestamp'] = (
        df['DATE_FROM'].dt.normalize()
        + pd.to_timedelta(df['start_hour'], unit='h')
    ).dt.tz_localize('Europe/Berlin')
    df = df.set_index('timestamp')

    df_wide = (
        df
        .set_index('direction', append=True)[cr_srl_power_price]
        .unstack('direction')
    )

    df_wide.columns = [
       cc_srl_power_price_pos if d == 'POS'
        else cc_srl_power_price_neg
        for d in df_wide.columns
    ]

    df_wide.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df_wide