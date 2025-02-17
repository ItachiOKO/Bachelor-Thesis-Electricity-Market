import pandas as pd
import pyomo.environ as pyo

from config import CELL_NAMES

def process_results(df, model, battery_capacity, cycles):
    df = extract_pyo_results_to_df(df, model)
    df = add_calculations_to_df(df)
    df = df.round(3)
    add_prints(df, model, battery_capacity, cycles)
    return df


def extract_pyo_results_to_df(df, model):
    df = df.copy()
    df[CELL_NAMES["buy_volume"]] = [pyo.value(model.buy_volume[t]) for t in model.T]
    df[CELL_NAMES["sell_volume"]] = [pyo.value(model.sell_volume[t]) for t in model.T]
    df[CELL_NAMES["battery_soc"]] = [pyo.value(model.battery_soc[t]) for t in model.T]
    df[CELL_NAMES["aging_cost"]] = [pyo.value(model.aging_cost[t]) for t in model.T]
    return df

def add_calculations_to_df(df):
    df = df.copy()
    df[CELL_NAMES["order_cost"]] = -df[CELL_NAMES["buy_volume"]] * df[CELL_NAMES["market_price"]] + df[CELL_NAMES["sell_volume"]] * df[CELL_NAMES["market_price"]]
    df[CELL_NAMES["profit_calc"]] = df[CELL_NAMES["sell_volume"]] * df[CELL_NAMES["market_price"]] - df[CELL_NAMES["buy_volume"]] * df[CELL_NAMES["market_price"]] - df[CELL_NAMES["aging_cost"]]
    return df

def add_prints(df, model, battery_capacity, cycles):	
    n_cycles = df[CELL_NAMES["buy_volume"]].sum()/battery_capacity
    total_profit_model = pyo.value(model.OBJ)
    profit_per_cycle = total_profit_model/n_cycles


    df.attrs["n Cycles"] = n_cycles
    df.attrs["Total Profit Model"] = total_profit_model
    df.attrs["Profit per Cycle"] = profit_per_cycle
    df.attrs["Profit per Battery"] = profit_per_cycle * cycles
    df.attrs['Order Cost'] = df[CELL_NAMES['order_cost']].sum()
