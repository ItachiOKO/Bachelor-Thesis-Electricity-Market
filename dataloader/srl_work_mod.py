import os
import locale
import pandas as pd
from config_column_names import ColumnNamesRaw as CR,  ColumnNamesClean as CC



def load_srl_work_data1(path_data, cr_srl_work_price, cc_srl_work_price_pos, cc_srl_work_price_neg) -> pd.DataFrame:

    df = pd.read_excel(
        path_data,
        usecols=['DELIVERY_DATE', 'PRODUCT', cr_srl_work_price],
        parse_dates=['DELIVERY_DATE'],
        engine='openpyxl',
    )

    parts = df['PRODUCT'].str.split('_', expand=True)
    df['direction'] = parts[0]
    df['start_hour'] = parts[1].astype(int)

    df['timestamp'] = (
        df['DELIVERY_DATE'].dt.normalize()
        + pd.to_timedelta(df['start_hour'], unit='h')
    ).dt.tz_localize('Europe/Berlin', ambiguous='infer', nonexistent='shift_forward')

    df_wide = df.pivot(
        index='timestamp',
        columns='direction',
        values=cr_srl_work_price
    )

    df_wide = df_wide.resample('15T').ffill()

    df_wide.columns = [
        cc_srl_work_price_pos if d == 'POS' else cc_srl_work_price_neg
        for d in df_wide.columns
    ]

    return df_wide


def load_srl_work_data2(path_data, cr_srl_work_price, cc_srl_work_price_pos, cc_srl_work_price_neg):
    
    df = pd.read_excel(
        path_data,
        usecols=['DELIVERY_DATE', 'PRODUCT', cr_srl_work_price],
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
        values=cr_srl_work_price
    )
    
    df_wide = df_wide.rename(
        columns={
            'NEG': cc_srl_work_price_neg,
            'POS': cc_srl_work_price_pos
        }
    )
    
    df_wide = df_wide[[cc_srl_work_price_neg, cc_srl_work_price_pos]]
    
    return df_wide

if __name__ == "__main__":
    path1 = 'data/Sekundär Arbeit Ergebnisse 2021 bis 2024 (1).xlsx'
    path2 = 'data/Sekundär Arbeit Ergebnisse 2021 bis 2024 (2).xlsx'
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    
    df1 = load_srl_work_data1(
        path1,
        CR.SRL_WORK_PRICE_NEG,
        CC.SRL_WORK_PRICE_POS,
        CC.SRL_WORK_PRICE_NEG
    )

    df2 = load_srl_work_data2(
        path2,
        CR.SRL_WORK_PRICE_NEG,
        CC.SRL_WORK_PRICE_POS,
        CC.SRL_WORK_PRICE_NEG
    )

    # contact = pd.concat([df1, df2])
    df1 = df1.sort_index()
    df2 = df2.sort_index()
    contact_df = pd.concat([df1, df2])
    # utc no timezones
    contact_df.index = contact_df.index.tz_convert('UTC').tz_localize(None)	

    print(contact_df)
    # to excel
    contact_df.to_excel("data/Sekundär Arbeit Ergebnisse 2021 bis 2024.xlsx", index=True)

   
