import os
import pandas as pd
from utils import get_pickle_path


def load_prl_data(path, cr_prl_price, cc_date, cc_prl_price) -> pd.DataFrame:
    pkl_path = get_pickle_path(path)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    print(f"Loading data from {path}")
    df = pd.read_excel(
        path,
        usecols=["DATE_FROM", "PRODUCTNAME", cr_prl_price],
        parse_dates=["DATE_FROM"],
        engine="openpyxl",           # falls du vorher kein engine explizit hattest
    )

    df["start_hour"] = (
        df["PRODUCTNAME"]
        .str.split("_")
        .str[1]        
        .astype(int)    
    )
    
    df[cc_date] = (
        df["DATE_FROM"].dt.floor("D")  
        + pd.to_timedelta(df["start_hour"], unit="H")
    )

    df[cc_date] = df[cc_date].dt.tz_localize("Europe/Berlin")
    df.set_index(cc_date, inplace=True)

    df = df[[cr_prl_price]]   
    df.columns = [cc_prl_price]
    
    df.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df