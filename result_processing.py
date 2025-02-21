import pandas as pd
import pyomo.environ as pyo

from utils import calculate_period_in_days


def export_results(df, results_file_name_excel, results_file_name_pickle):
    df.to_pickle(results_file_name_pickle)
    attrs_df = pd.DataFrame(list(df.attrs.items()), columns=['Attribute', 'Value'])
    with pd.ExcelWriter(results_file_name_excel, engine='xlsxwriter') as writer:
        attrs_df.to_excel(writer, sheet_name='Attributes', index=False)
        df.to_excel(writer, sheet_name='Data')

def process_results(df, model, cell_names, start_date, end_date, battery_capacity, cycles, battery_price, efficiency):
    df = extract_pyo_results_to_df(df, model, cell_names)
    df = add_calculations_to_df(df, cell_names)
    df = df.round(3)
    add_attrs_to_df(df, model, cell_names, start_date, end_date,  battery_capacity, cycles, battery_price, efficiency)
    return df

def extract_pyo_results_to_df(df, model, cell_names):
    df = df.copy()
    df[cell_names["buy_volume"]] = [pyo.value(model.buy_volume[t]) for t in model.T]
    df[cell_names["sell_volume"]] = [pyo.value(model.sell_volume[t]) for t in model.T]
    df[cell_names["battery_soc"]] = [pyo.value(model.battery_soc[t]) for t in model.T]
    df[cell_names["aging_cost"]] = [pyo.value(model.aging_cost[t]) for t in model.T]
    df[cell_names["prl_capacity"]] = [pyo.value(model.prl_capacity[t]) for t in model.T]
    return df

def add_calculations_to_df(df, cell_names):
    df = df.copy()
    df[cell_names["order_cost"]] = -df[cell_names["buy_volume"]] * df[cell_names["market_price"]] + df[cell_names["sell_volume"]] * df[cell_names["market_price"]]
    df[cell_names["profit_calc"]] = df[cell_names["sell_volume"]] * df[cell_names["market_price"]] - df[cell_names["buy_volume"]] * df[cell_names["market_price"]] - df[cell_names["aging_cost"]] + df[cell_names["prl_capacity"]] * df[cell_names["prl_price"]]
    return df

def add_attrs_to_df(df, model, cell_names, start_date, end_date, battery_capacity, cycles, battery_price, efficiency):	
    n_cycles = df[cell_names["buy_volume"]].sum() * efficiency/battery_capacity
    order_cost = df[cell_names["order_cost"]].sum()
    total_profit_simulation = pyo.value(model.OBJ)
    profit_per_cycle = total_profit_simulation/n_cycles
    profit_per_battery = profit_per_cycle * cycles
    days = calculate_period_in_days(start_date, end_date)
    amortization_years = battery_price / total_profit_simulation * days/365
    battery_lifetime = cycles/n_cycles

    df.attrs["n Cycles"] = n_cycles
    df.attrs['Order Cost'] = order_cost
    df.attrs["Total Profit Model"] = total_profit_simulation
    df.attrs["Profit per Cycle"] = profit_per_cycle
    df.attrs["Profit per Battery"] = profit_per_battery
    df.attrs["Amortization Years"] = amortization_years
    df.attrs["Battery Lifetime"] = battery_lifetime
    
