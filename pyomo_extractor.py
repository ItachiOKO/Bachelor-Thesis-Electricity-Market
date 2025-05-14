import pandas as pd
import pyomo.environ as pyo
from config import ColumnNamesClean as CC


def extract_pyo_results_to_df(df, model):
    df = df.copy()
    df[CC.buy_volume] = [pyo.value(model.buy_volume[t]) for t in model.T]
    df[CC.sell_volume] = [pyo.value(model.sell_volume[t]) for t in model.T]
    df[CC.battery_soc] = [pyo.value(model.battery_soc[t]) for t in model.T]
    df[CC.aging_cost] = [pyo.value(model.aging_cost[t]) for t in model.T]
    df[CC.prl_capacity] = [pyo.value(model.prl_power[t]) for t in model.T]
    df[CC.srl_power_pos] = [pyo.value(model.srl_power_pos[t]) for t in model.T]
    df[CC.srl_power_neg] = [pyo.value(model.srl_power_neg[t]) for t in model.T]
    return df