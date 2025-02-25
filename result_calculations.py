import math
import pyomo.environ as pyo
from utils import calculate_period_in_days
from config import PRL_DAILY_CYCLES


def add_column_calculations_to_df(df, cell_names):
    df = df.copy()

    df[cell_names["order_cost"]] = (
        (df[cell_names["sell_volume"]] - df[cell_names["buy_volume"]]) * df[cell_names["market_price"]]
    )

    df[cell_names["profit_calc"]] = (
        (df[cell_names["sell_volume"]] - df[cell_names["buy_volume"]]) * df[cell_names["market_price"]]
        + df[cell_names["prl_capacity"]] * df[cell_names["prl_price"]]
        - df[cell_names["aging_cost"]]
    )
    return df

def add_attrs_calculations_to_df(df, model, cell_names, start_date, end_date, battery_capacity, cycles, battery_price, efficiency):	
    #exchange
    n_cycles_exchange = df[cell_names["buy_volume"]].sum() * efficiency/battery_capacity
    net_order_value = df[cell_names["order_cost"]].sum()
    #prl
    n_cycles_prl = df[cell_names["prl_capacity"]].sum() / battery_capacity * PRL_DAILY_CYCLES
    net_prl_value = sum(df[cell_names["prl_capacity"]] * df[cell_names["prl_price"]])
    #profit calculation
    total_profit_simulation = pyo.value(model.OBJ)
    profit_per_cycle = total_profit_simulation/(n_cycles_exchange + n_cycles_prl)
    profit_per_battery = profit_per_cycle * cycles
    days = calculate_period_in_days(start_date, end_date)
    amortization_years = battery_price / total_profit_simulation * days/365 #years
    battery_lifetime = cycles/(n_cycles_exchange + n_cycles_prl) * days/365 #years


    df = df.copy()
    df.attrs["n Cycles exchange"] = n_cycles_exchange
    df.attrs['Net order Value'] = net_order_value
    df.attrs["n Cycles PRL"] = n_cycles_prl
    df.attrs['Net PRL Value'] = net_prl_value
    df.attrs["Total Profit"] = total_profit_simulation
    df.attrs["Profit per Cycle"] = profit_per_cycle
    df.attrs["Profit per Battery"] = profit_per_battery
    df.attrs["Amortization Years"] = amortization_years
    df.attrs["Battery Lifetime"] = battery_lifetime
    return df

def test_results(df, cell_names):
    total_profit_model = df.attrs['Total Profit']
    total_profit_calculated = df[cell_names["profit_calc"]].sum()
    if math.isclose(total_profit_model, total_profit_calculated, rel_tol=1e-3):
        pass
    else:
        raise ValueError("Total Profit Model: {} != Total Profit Calculated: {}".format(total_profit_model, total_profit_calculated))
