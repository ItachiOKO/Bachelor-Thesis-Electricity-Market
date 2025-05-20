import pandas as pd
import pyomo.environ as pyo
from config import ColumnNamesClean as CC


def extract_pyo_results_to_df(df, model):
    df = df.copy()
    df[CC.BUY_VOL] = [pyo.value(model.buy_volume[t]) for t in model.T]
    df[CC.SELL_VOL] = [pyo.value(model.sell_volume[t]) for t in model.T]
    df[CC.BAT_SOC] = [pyo.value(model.battery_soc[t]) for t in model.T]
    df[CC.AGING_COST] = [pyo.value(model.aging_cost[t]) for t in model.T]
    df[CC.PRL_POWER] = [pyo.value(model.prl_power[t]) for t in model.T]
    df[CC.SRL_POWER_NEG] = [pyo.value(model.srl_power_neg[t]) for t in model.T]
    df[CC.SRL_POWER_POS] = [pyo.value(model.srl_power_pos[t]) for t in model.T]
    return df