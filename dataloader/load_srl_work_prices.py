import pandas as pd
from config import (
    PATH_SRL_WORK_DATA,
    SPECIFIC_AGING_COST,
    PROFIT_FACTOR_SRL_POS,
    PROFIT_FACTOR_SRL_NEG,
)
from config_column_names import (
    ColumnNamesRaw as CR,
    ColumnNamesClean as CC,
)



def load_srl_work_cbmp_data(path, specific_aging_cost, cr_srl_neg_work_cbmp, cr_srl_pos_work_cbmp, cc_srl_neg_work_cbmp, cc_srl_pos_work_cbmp):
    df = pd.read_pickle(path)
    df.fillna(0, inplace=True)
    df[cc_srl_neg_work_cbmp] = 0.0
    df[cc_srl_pos_work_cbmp] = 0.0


    mask_neg = (-df[cr_srl_neg_work_cbmp] > specific_aging_cost * PROFIT_FACTOR_SRL_NEG) & (df[cr_srl_pos_work_cbmp] == 0)
    df.loc[mask_neg, cc_srl_neg_work_cbmp] = df.loc[mask_neg, cr_srl_neg_work_cbmp]


    mask_pos = (df[cr_srl_pos_work_cbmp] > specific_aging_cost * PROFIT_FACTOR_SRL_POS) & (df[cr_srl_neg_work_cbmp] == 0)
    df.loc[mask_pos, cc_srl_pos_work_cbmp] = df.loc[mask_pos, cr_srl_pos_work_cbmp] 



    df.drop(columns=[cr_srl_neg_work_cbmp, cr_srl_pos_work_cbmp, 'position'], inplace=True)

    df = df.resample('15min').mean()


    return df
    

if __name__ == "__main__":
    cr_p_neg = CR.SRL_NEG_WORK_CBMP
    cr_p_pos = CR.SRL_POS_WORK_CBMP
    cc_p_neg = CC.SRL_NEG_WORK_CBMP
    cc_p_pos = CC.SRL_POS_WORK_CBMP
    df = load_srl_work_cbmp_data(PATH_SRL_WORK_DATA, SPECIFIC_AGING_COST, cr_p_neg, cr_p_pos, cc_p_neg, cc_p_pos)
    print(df)

    df = df.loc['2023-01-01':'2023-01-02']
    df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
    df.to_excel('srl_work_pricewedwedwedwedwedwedweds.xlsx', index=True)

