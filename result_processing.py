import pandas as pd
import pyomo.environ as pyo

from config import CELL_NAMES

def process_results(df, model, battery_capacity, cycles):
    extract_pyo_results_to_df(df, model)
    add_calculations_to_df(df)
    add_prints(df, model, battery_capacity, cycles)

def extract_pyo_results_to_df(df, model):
    df[CELL_NAMES["buy_volume"]] = [pyo.value(model.buy_volume[t]) for t in model.T]
    df[CELL_NAMES["sell_volume"]] = [pyo.value(model.sell_volume[t]) for t in model.T]
    df[CELL_NAMES["battery_soc"]] = [pyo.value(model.battery_soc[t]) for t in model.T]
    df[CELL_NAMES["aging_cost"]] = [pyo.value(model.aging_cost[t]) for t in model.T]
    return df

def add_calculations_to_df(df):
    df[CELL_NAMES["order_cost"]] = -df[CELL_NAMES["buy_volume"]] * df[CELL_NAMES["market_price"]] + df[CELL_NAMES["sell_volume"]] * df[CELL_NAMES["market_price"]]
    df[CELL_NAMES["profit_calc"]] = df[CELL_NAMES["sell_volume"]] * df[CELL_NAMES["market_price"]] - df[CELL_NAMES["buy_volume"]] * df[CELL_NAMES["market_price"]] - df[CELL_NAMES["aging_cost"]]
    return df

def add_prints(df, model, battery_capacity, cycles):	
    n_cycles = df[CELL_NAMES["buy_volume"]].sum()/battery_capacity
    total_profit_model = pyo.value(model.OBJ)
    profit_per_cycle = total_profit_model/n_cycles
    print(f"{n_cycles}: Ladezyklen")
    print(f"Order Profit: {df[CELL_NAMES['order_cost']].sum()} €")
    print(f"Gesamtprofit_model: {total_profit_model} €")
    print(f"Profit pro Zyklus: {profit_per_cycle} €")
    print(f"Profit pro Battery: {profit_per_cycle * cycles} €")
