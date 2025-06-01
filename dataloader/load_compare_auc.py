import numpy as np
import pandas as pd
from dataloader.load_da_auc import load_da_auc_data
from dataloader.load_id_auc import load_id_auc_data
from config import (
    PATH_DA_AUC_DATA,
    PATH_INTRADAY_DATA,
    ColumnNamesRaw as CR,
    ColumnNamesClean as CC
)


def compare_da_id_prices(da_df: pd.DataFrame, id_df: pd.DataFrame) -> pd.DataFrame:

    df = pd.concat([da_df, id_df], axis=1)
    higher = df[[CC.DA_AUC_PRICE, CC.ID_AUC_PRICE]].max(axis=1)
    lower  = df[[CC.DA_AUC_PRICE, CC.ID_AUC_PRICE]].min(axis=1)

    higher_market = np.where(df[CC.DA_AUC_PRICE] >= df[CC.ID_AUC_PRICE], CC.DA_AUC_PRICE, CC.ID_AUC_PRICE) # (condition, x, y) -> if condition then x else y
    lower_market  = np.where(df[CC.DA_AUC_PRICE] <  df[CC.ID_AUC_PRICE], CC.DA_AUC_PRICE, CC.ID_AUC_PRICE)

    result = pd.DataFrame({
        CC.HiGHER_MARKET_PRICE: higher,
        CC.MARKET_HI: higher_market,
        CC.LOWER_MARKET_PRICE: lower,
        CC.MARKET_LO: lower_market
    }, index=df.index)

    return result


def load_compared_auc_data(path_da, path_id, cr_energie_charts_date, cr_da_auc_price, cc_da_auc_price, cr_id_price_auc_15min, cr_id_price_auc_ida1_gekoppelt, cc_id_auc_price) -> pd.DataFrame:

    da_df = load_da_auc_data(path_da, cr_energie_charts_date, cr_da_auc_price, cc_da_auc_price)
    id_df = load_id_auc_data(path_id, cr_energie_charts_date, cr_id_price_auc_15min, cr_id_price_auc_ida1_gekoppelt, cc_id_auc_price )

    return compare_da_id_prices(da_df, id_df)


if __name__ == "__main__":

    da = load_da_auc_data(PATH_DA_AUC_DATA,
                        CR.ENERGIE_CHARTS_DATE,
                        CR.DA_AUC_PRICE,
                        CC.DA_AUC_PRICE)

    id = load_id_auc_data(PATH_INTRADAY_DATA,
                        CR.ENERGIE_CHARTS_DATE,
                        CR.ID_PRICE_AUC_15min,
                        CR.ID_PRICE_AUC_IDA1_GEKOPPELT,
                        CC.ID_AUC_PRICE)

    df_compare = compare_da_id_prices(da, id)
    print(df_compare.head())

