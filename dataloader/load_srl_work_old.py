import os
import pandas as pd
from utils import get_pickle_path


def load_srl_work_data(path, cr_srl_work_price_neg, cr_srl_work_price_pos, cc_srl_work_price_neg, cc_srl_work_price_pos):
    pkl_path = get_pickle_path(path)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    path = 'data/SRL Arbeitspreise berechnet 2021 bis 2024.xlsx'

    print(f"Loading data from {path}")
    df = pd.read_excel(
        path,
        index_col='Datum',
        usecols=['Datum', cr_srl_work_price_neg, cr_srl_work_price_pos],
        engine="openpyxl",
        thousands='.',    # Punkt als Tausender
        decimal=','       # Komma als Dezimaltrennzeichen
    )

    df.index = pd.to_datetime(df.index, utc=True)
    df.index = df.index.tz_convert('Europe/Berlin')

    new_names = {
        cr_srl_work_price_neg: cc_srl_work_price_neg,
        cr_srl_work_price_pos: cc_srl_work_price_pos
    }
    df.rename(columns=new_names, inplace=True)

    df.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df



