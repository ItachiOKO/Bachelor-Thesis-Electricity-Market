import pandas as pd
import pyomo.environ as pyo
from config import ColumnNamesClean as CC


def extract_pyo_results_to_df(df, model):
    df = df.copy()
    df[CC.DA_AUC_BUY_VOL] = [pyo.value(model.v_DA_AUC_BUY_VOL[t]) for t in model.T]
    df[CC.DA_AUC_SELL_VOL] = [pyo.value(model.v_DA_AUC_SELL_VOL[t]) for t in model.T]
    df[CC.BAT_SOC] = [pyo.value(model.v_BAT_SOC[t]) for t in model.T]
    df[CC.AGING_COST] = [pyo.value(model.e_AGING_COST[t]) for t in model.T]
    df[CC.PRL_POWER] = [pyo.value(model.v_PRL_POWER[t]) for t in model.T]
    df[CC.SRL_POWER_NEG] = [pyo.value(model.v_SRL_POWER_NEG[t]) for t in model.T]
    df[CC.SRL_POWER_POS] = [pyo.value(model.v_SRL_POWER_POS[t]) for t in model.T]
    return df