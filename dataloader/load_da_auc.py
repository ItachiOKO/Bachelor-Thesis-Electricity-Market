import os
import locale
import pandas as pd
from utils import get_pickle_path


def load_da_auc_data(path, cr_energie_charts_date, cr_da_auc_price, cc_da_auc_price) -> pd.DataFrame:
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    pkl_path = get_pickle_path(path)
    if os.path.exists(pkl_path):
        #print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    df = pd.read_excel(
        path,
        usecols=[cr_energie_charts_date, cr_da_auc_price],
        index_col=0,
        parse_dates=[0],
        date_format="%d.%m.%Y, %H:%M",
        engine="openpyxl",
        thousands='.',    # Punkt als Tausender
        decimal=','       # Komma als Dezimaltrennzeichen
    )

    df.index = (
        df.index
          .tz_localize('UTC')
          .tz_convert('Europe/Berlin')
    )
    # fillna(0) falls es Lücken gibt
    df[cc_da_auc_price] = df[cr_da_auc_price].fillna(0)

    df_clean = df[[cc_da_auc_price]]
    df_clean.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df_clean
