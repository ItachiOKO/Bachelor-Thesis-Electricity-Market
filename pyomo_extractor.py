import pandas as pd
import pyomo.environ as pyo


def extract_pyo_results_to_df(df, model, cell_names):
    df = df.copy()
    df[cell_names["buy_volume"]] = [pyo.value(model.buy_volume[t]) for t in model.T]
    df[cell_names["sell_volume"]] = [pyo.value(model.sell_volume[t]) for t in model.T]
    df[cell_names["battery_soc"]] = [pyo.value(model.battery_soc[t]) for t in model.T]
    df[cell_names["aging_cost"]] = [pyo.value(model.aging_cost[t]) for t in model.T]
    df[cell_names["prl_capacity"]] = [pyo.value(model.prl_power[t]) for t in model.T]
    df[cell_names["srl_power_pos"]] = [pyo.value(model.srl_power_pos[t]) for t in model.T]
    df[cell_names["srl_power_neg"]] = [pyo.value(model.srl_power_neg[t]) for t in model.T]
    return df