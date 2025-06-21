import os
import locale
import pandas as pd
from config_column_names import (
    ColumnNamesRaw as CR,
    ColumnNamesClean as CC,
)
from utils import get_pickle_path


def load_da_auc_price_data(path_data):
    pkl_path = get_pickle_path(path_data)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)

    df = pd.read_csv(
        path_data,
        skiprows=2,
        names=[CC.DATE, CC.DA_PRICE],
        parse_dates=[CC.DATE],
        index_col= [CC.DATE]
    )
    df.index = pd.to_datetime(df.index, utc=True).tz_convert("Europe/Berlin")
    df.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df


def load_id_data(path_data):
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    pkl_path = get_pickle_path(path_data)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    df = pd.read_excel(
        path_data,
        usecols=["Datum und Uhrzeit (UTC)", CR.ID_PRICE],
        index_col=0,
        parse_dates=[0],
        date_format="%d.%m.%Y, %H:%M",
        engine="openpyxl",
        converters={CR.ID_PRICE: locale.atof}  # liest "1.234,56" korrekt als 1234.56
    )

    df.index = (
        df.index
          .tz_localize('UTC')
          .tz_convert('Europe/Berlin')
    )
    df: pd.DataFrame = df[[CR.ID_PRICE]].rename(
        columns={CR.ID_PRICE: CC.ID_PRICE}
)
    df.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df

    
def load_prl_data(path_data) -> pd.DataFrame:
    pkl_path = get_pickle_path(path_data)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    df = pd.read_excel(
        path_data,
        usecols=["DATE_FROM", "PRODUCTNAME", CR.PRL_PRICE],
        parse_dates=["DATE_FROM"],
        engine="openpyxl",           # falls du vorher kein engine explizit hattest
    )

    df["start_hour"] = (
        df["PRODUCTNAME"]
        .str.split("_")
        .str[1]        
        .astype(int)    
    )
    
    df[CC.DATE] = (
        df["DATE_FROM"].dt.floor("D")  
        + pd.to_timedelta(df["start_hour"], unit="H")
    )

    df[CC.DATE] = df[CC.DATE].dt.tz_localize("Europe/Berlin")
    df.set_index(CC.DATE, inplace=True)

    df = df[[CR.PRL_PRICE]]   
    df.columns = [ CC.PRL_PRICE ]
    
    df.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df


def load_srl_power_data(path_data) -> pd.DataFrame:
    pkl_path = get_pickle_path(path_data)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    df = pd.read_excel(
        path_data,
        usecols=['DATE_FROM', 'DATE_TO', 'PRODUCT', CR.SRL_POWER_PRICE],
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
        .set_index('direction', append=True)[CR.SRL_POWER_PRICE]
        .unstack('direction')
    )

    df_wide.columns = [
       CC.SRL_POWER_PRICE_POS if d == 'POS'
        else CC.SRL_POWER_PRICE_NEG
        for d in df_wide.columns
    ]

    df_wide.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df_wide



def load_srl_work_data(path_data):
    pkl_path = get_pickle_path(path_data)
    if os.path.exists(pkl_path):
        print(f"Loading data from {pkl_path}")
        return pd.read_pickle(pkl_path)
    
    df = pd.read_excel(
        path_data,
        usecols=['DELIVERY_DATE', 'PRODUCT', CR.SRL_WORK_PRICE_NEG],
        )
    
    df['DELIVERY_DATE'] = pd.to_datetime(df['DELIVERY_DATE'], dayfirst=True)
    df['date_local'] = df['DELIVERY_DATE'].dt.tz_localize(
        'Europe/Berlin',
        ambiguous='infer',
        nonexistent='shift_forward'
    )
    
    # PRODUCT zerlegen
    df[['direction', 'step']] = df['PRODUCT'].str.split('_', expand=True)
    df['step'] = df['step'].astype(int)
    
    # 15-Minuten-Offset berechnen
    df['time_offset'] = pd.to_timedelta((df['step'] - 1) * 15, unit='minutes')
    df['datetime'] = df['date_local'] + df['time_offset']
    
    df_wide = df.pivot(
        index='datetime',
        columns='direction',
        values=CR.SRL_WORK_PRICE_NEG
    )
    
    df_wide = df_wide.rename(
        columns={
            'NEG': CC.SRL_WORK_PRICE_NEG,
            'POS': CC.SRL_WORK_PRICE_POS
        }
    )
    
    df_wide = df_wide[[CC.SRL_WORK_PRICE_NEG, CC.SRL_WORK_PRICE_POS]]
    
    df_wide.to_pickle(pkl_path)
    print(f"Data saved to {pkl_path}")
    return df_wide