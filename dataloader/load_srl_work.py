import os
import pandas as pd
from utils import get_pickle_path


def load_srl_work_data(path, cc_srl_work_price_neg, cc_srl_work_price_pos):
    pkl_path = get_pickle_path(path)
    if os.path.exists(pkl_path):
        #print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    df = pd.read_excel(
        path,
        index_col=0,
        parse_dates=True,
        engine='openpyxl',
    )
    df.index = df.index.tz_localize('UTC').tz_convert('Europe/Berlin')

    df.columns = [cc_srl_work_price_neg, cc_srl_work_price_pos]

    df.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df



