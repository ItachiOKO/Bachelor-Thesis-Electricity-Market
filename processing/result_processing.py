import pandas as pd
import pyomo.environ as pyo
from result_calculations import add_column_calculations_to_df, add_attrs_calculations_to_df, test_results


def process_results(df, total_profit_model, cell_names, start_date, end_date, battery_capacity, cycles, battery_price, efficiency):
    #df = add_column_calculations_to_df(df, cell_names)
    #df = add_attrs_calculations_to_df(df, total_profit_model, cell_names, start_date, end_date,  battery_capacity, cycles, battery_price, efficiency)
    #df = sort_columns_df(df, cell_names)
    #df = df.round(2)
    #df = round_attrs_df(df)
    #test_results(df, cell_names)	
    return df


def round_attrs_df(df):
    df = df.copy()
    df.attrs = {key: round(value, 1) for key, value in df.attrs.items()}
    return df
    
def sort_columns_df(df, cell_names):
    columns_order = [
        #cell_names["date"] Index
        cell_names["market_price"], 
        cell_names["prl_price"], 
        cell_names["buy_volume"], 
        cell_names["sell_volume"], 
        cell_names["order_cost"], 
        cell_names["battery_soc"], 
        cell_names["prl_capacity"], 
        cell_names["aging_cost"], 
        cell_names["profit_calc"],
    ]
    df = df.copy()
    df = df[columns_order]
    return df