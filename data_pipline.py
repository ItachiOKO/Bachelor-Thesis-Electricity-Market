import time
import pandas as pd
from utils import convert_datetime_to_string
from config import (
    START_DATE,
    END_DATE,
    PATH_DA_AUC_DATA,
    PATH_PRL_DATA,
    PATH_SRL_POWER_DATA,
    PATH_SRL_WORK_DATA,
    PATH_INTRADAY_DATA,
)
from config_column_names import ColumnNamesRaw as CR,  ColumnNamesClean as CC

from dataloader import (
    load_da_auc_data,
    load_id_auc_data,
    load_compared_auc_data,
    load_prl_data,
    load_srl_power_data,
    load_srl_work_data,

)

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_dataframe(start_date, end_date, debug=False):
    df_master = create_master_df(start_date, end_date)

    loader_tasks = [
        (load_compared_auc_data, (PATH_DA_AUC_DATA, PATH_INTRADAY_DATA, CR.ENERGIE_CHARTS_DATE, CR.DA_AUC_PRICE, CC.DA_AUC_PRICE, CR.ID_PRICE_AUC_15min, CR.ID_PRICE_AUC_IDA1_GEKOPPELT, CC.ID_AUC_PRICE)),
        #(load_da_auc_data,      (PATH_DA_AUC_DATA, CR.ENERGIE_CHARTS_DATE, CR.DA_AUC_PRICE, CC.DA_AUC_PRICE)),
        #(load_id_auc_data,      (PATH_INTRADAY_DATA, CR.ENERGIE_CHARTS_DATE, CR.ID_PRICE_AUC_15min, CR.ID_PRICE_AUC_IDA1_GEKOPPELT, CC.ID_AUC_PRICE)),
        (load_prl_data,          (PATH_PRL_DATA, CR.PRL_PRICE, CC.DATE, CC.PRL_PRICE)),
        (load_srl_power_data,    (PATH_SRL_POWER_DATA, CR.SRL_POWER_PRICE, CC.SRL_POWER_PRICE_POS, CC.SRL_POWER_PRICE_NEG)),
        (load_srl_work_data,     (PATH_SRL_WORK_DATA, CC.SRL_WORK_PRICE_NEG, CC.SRL_WORK_PRICE_POS))
    ]

    for loader, args in loader_tasks:
        df = loader(*args)
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
    df = create_dataframe(START_DATE, END_DATE, debug=True)
    print(f"Berechnungszeit: {round(time.time() - start_time, 1)} Sekunden")
    print(df)
    print(len(df))
    # to excel

    formated_df = convert_datetime_to_string(df)       
    formated_df.to_excel("data/market_price_data.xlsx", index=True, sheet_name="Market Price Data")
