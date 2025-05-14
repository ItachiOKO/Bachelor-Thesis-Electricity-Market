import logging
logging.getLogger('pyomo').setLevel(logging.WARNING)

import time
import pandas as pd
import pyomo.environ as pyo
from model_builder import setup_model, solve_model
from pyomo_extractor import extract_pyo_results_to_df
from result_export import export_results
from dataloader import create_dataframe
from utils import get_interval_minutes
from config import (
    COLUMN_NAMES_CLEAN,
    RESULTS_FILE_NAME_EXCEL,
    RESULTS_FILE_NAME_PICKLE,
    SYSTEM_POWER,
    START_DATE,
    END_DATE,
)


def main_optimisation(df_data_period):
    time_points = df_data_period.index.tolist()
    market_price_dict = df_data_period[COLUMN_NAMES_CLEAN["market_price"]].to_dict()
    prl_price_dict = df_data_period[COLUMN_NAMES_CLEAN["prl_price"]].to_dict()
    srl_price_pos_dict = df_data_period[COLUMN_NAMES_CLEAN["srl_price_pos"]].to_dict()
    srl_price_neg_dict = df_data_period[COLUMN_NAMES_CLEAN["srl_price_neg"]].to_dict()
    charge_rate = SYSTEM_POWER * (get_interval_minutes(df_data_period)/60)

    model = setup_model(time_points, market_price_dict, prl_price_dict, srl_price_pos_dict, srl_price_neg_dict, charge_rate)
    solve_model(model)
    return model


def optimize_by_year(df_data):
    yearly_results = []
    models = []  
    
    for year, df_data_year in df_data.groupby(pd.Grouper(freq='12M')):
        if df_data_year.empty:
            print(f"Keine Daten für {year}")
            continue
        
        print(f"Optimierung für {year.strftime('%Y')}")
        model_year = main_optimisation(df_data_year)
        models.append(model_year)  
        
        df_extracted_year = extract_pyo_results_to_df(df_data_year, model_year, COLUMN_NAMES_CLEAN)
        yearly_results.append(df_extracted_year)
    
    final_df_extracted = pd.concat(yearly_results)
    return final_df_extracted, models 


if __name__ == "__main__":
    df = create_dataframe(START_DATE, END_DATE, debug=False)

    start_time = time.time()
    final_df_extracted, models = optimize_by_year(df)
    print(f"Berechnungszeit: {round(time.time() - start_time, 1)} Sekunden")
    if models:
        total_profit_model = sum(pyo.value(m.OBJ) for m in models)
    else:
        raise ValueError("Keine Modelle vorhanden")
    
    print(final_df_extracted)
    export_results(final_df_extracted, RESULTS_FILE_NAME_EXCEL, RESULTS_FILE_NAME_PICKLE)


"""
    final_df_results = process_results(
        final_df_extracted, 
        total_profit_model=total_profit_model,  # Ein Modell wird mitgegeben
        cell_names=COLUMN_NAMES_CLEAN, 
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
"""



