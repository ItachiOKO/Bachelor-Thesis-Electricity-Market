import pandas as pd
import pyomo.environ as pyo


def process_results(df, model, battery_capacity, cycles):
    extract_pyo_results_to_df(df, model)
    add_calculations_to_df(df)
    add_prints(df, model, battery_capacity, cycles)

def extract_pyo_results_to_df(df, model):
    df["buy_volume"] = [pyo.value(model.buy_volume[t]) for t in model.T]
    df["sell_volume"] = [pyo.value(model.sell_volume[t]) for t in model.T]
    df["battery_soc"] = [pyo.value(model.battery_soc[t]) for t in model.T]
    df["aging_cost"] = [pyo.value(model.aging_cost[t]) for t in model.T]
    return df

def add_calculations_to_df(df):
    df["order_cost"] = -df["buy_volume"] * df["market_price"] + df["sell_volume"] * df["market_price"]
    df["profit_calc"] = df["sell_volume"] * df["market_price"] - df["buy_volume"] * df["market_price"] - df["aging_cost"]
    return df

def add_prints(df, model, battery_capacity, cycles):	
    n_cycles = df["buy_volume"].sum()/battery_capacity
    total_profit_model = pyo.value(model.OBJ)
    profit_per_cycle = total_profit_model/n_cycles
    print(f"{n_cycles}: Ladezyklen")
    print(f"Order Profit: {df['order_cost'].sum()} €")
    print(f"Gesamtprofit_model: {total_profit_model} €")
    print(f"Profit pro Zyklus: {profit_per_cycle} €")
    print(f"Profit pro Battery: {profit_per_cycle * cycles} €")
