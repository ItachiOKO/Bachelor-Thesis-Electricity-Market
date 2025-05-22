import time
import locale
import pandas as pd
from config import (
    START_DATE,
    END_DATE,
    PATH_DA_AUC_DATA,
    PATH_PRL_DATA,
    PATH_SRL_POWER_DATA,
    PATH_SRL_WORK_DATA,
    PATH_INTRADAY_DATA,
    ColumnNamesClean as CC,
)
from dataloader import (
    load_da_auc_price_data,
    load_id_data,
    load_prl_data,
    load_srl_power_data,
    load_srl_work_data,
)
from utils import convert_datetime_to_string, get_pickle_path

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_dataframe(start_date, end_date, debug=False):
    df_master = create_master_df(start_date, end_date)
    loader_tasks = [
        (load_da_auc_price_data,   PATH_DA_AUC_DATA),     # Day-Ahead
        (load_id_data,             PATH_INTRADAY_DATA),   # Intraday
        (load_prl_data,            PATH_PRL_DATA),        # PRL
        (load_srl_power_data,      PATH_SRL_POWER_DATA),  # SRL Power
        (load_srl_work_data,       PATH_SRL_WORK_DATA),   # SRL Energy
    ]

    for loader, path in loader_tasks:
        df = loader(path)
        if debug:
            logging.debug(
                "Joining %s: %s bis %s (%d)",
                loader.__name__, df.index.min(), df.index.max(), len(df)
            )
        df_master = df_master.join(df, how="left")

    df_master.fillna(0, inplace=True)
    df_master.index.name = CC.DATE
    if debug:
        logging.info("Finaler Master-DataFrame: Shape=%s", df_master.shape)
    return df_master


def create_master_df(start_date, end_date):
    master_index = pd.date_range(start=start_date, end=end_date, freq='15T', tz='Europe/Berlin', inclusive='left')
    df = pd.DataFrame(index=master_index)
    return df


if __name__ == "__main__":
    # mesure time
    start_time = time.time()
    df = create_dataframe(START_DATE, END_DATE, debug=False)
    print(f"Berechnungszeit: {round(time.time() - start_time, 1)} Sekunden")
    print(df)
    # to excel

    formated_df = convert_datetime_to_string(df)       
    formated_df.to_excel("market_price_data.xlsx", index=True, sheet_name="Market Price Data")
