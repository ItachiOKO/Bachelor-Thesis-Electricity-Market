import time
import json
import pandas as pd
import pyomo.environ as pyo
from optimisation_model import setup_model, solve_model
from result_processing import process_results 
from extraction_model import extract_pyo_results_to_df
from result_export import export_results
from load_marketprice_data import create_dataframe
from utils import get_interval_minutes
from config import (
    BATTERY_CAPACITY,
    BATTERY_PRICE,
    CELL_NAMES,
    PATH_MARKET_DATA,
    EFFICIENCY,
    LIFETIME_CYCLES,
    RESULTS_FILE_NAME_EXCEL,
    RESULTS_FILE_NAME_PICKLE,
    SKIPROWS,
    SPECIFIC_CHARGE_RATE,
    START_DATE,
    END_DATE,
)


def main_optimisation(df):
    charge_rate = SPECIFIC_CHARGE_RATE * (get_interval_minutes(df)/60)
    time_points = df.index.tolist()
    market_price_dict = df[CELL_NAMES["market_price"]].to_dict()
    prl_price_dict = df[CELL_NAMES["prl_price"]].to_dict()
    model = setup_model(time_points, market_price_dict, prl_price_dict, charge_rate)
    solve_model(model)
    return model


def optimize_by_month(df):
    monthly_results = []
    models = []  
    
    for month, df_month in df.groupby(pd.Grouper(freq='M')):
        if df_month.empty:
            print(f"Keine Daten für {month}")
            continue
        
        print(f"Optimierung für {month.strftime('%Y-%m')}")
        model = main_optimisation(df_month)
        models.append(model)  
        
        df_extracted_month = extract_pyo_results_to_df(df_month, model, CELL_NAMES)
        monthly_results.append(df_extracted_month)
    
    final_df_extracted = pd.concat(monthly_results)
    return final_df_extracted, models 


if __name__ == "__main__":
    df = create_dataframe(PATH_MARKET_DATA, SKIPROWS, START_DATE, END_DATE)
    start_time = time.time()
    final_df_extracted, models = optimize_by_month(df)
    print(f"Berechnungszeit: {round(time.time() - start_time, 1)} Sekunden")
    if models:
        total_profit_model = sum(pyo.value(m.OBJ) for m in models)
    else:
        raise ValueError("Keine Modelle vorhanden")

    final_df_results = process_results(
        final_df_extracted, 
        total_profit_model=total_profit_model,  # Ein Modell wird mitgegeben
        cell_names=CELL_NAMES, 
        start_date=START_DATE, 
        end_date=END_DATE, 
        battery_capacity=BATTERY_CAPACITY, 
        cycles=LIFETIME_CYCLES, 
        battery_price=BATTERY_PRICE, 
        efficiency=EFFICIENCY
    )
    export_results(final_df_results, RESULTS_FILE_NAME_EXCEL, RESULTS_FILE_NAME_PICKLE)
    print(final_df_results)
    print(json.dumps(final_df_results.attrs, indent=4))
