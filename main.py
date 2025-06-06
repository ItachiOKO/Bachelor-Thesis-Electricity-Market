import logging
logging.getLogger('pyomo').setLevel(logging.WARNING)

import time
import pandas as pd
import pyomo.environ as pyo
from model.model_builder import setup_model, solve_model
from model.pyomo_extractor import extract_pyo_results_to_df
from model.result_export import export_results
from data_pipline import create_dataframe
from config import (
    RESULTS_FILE_NAME_EXCEL,
    RESULTS_FILE_NAME_PICKLE,
    START_DATE,
    END_DATE,
)


def main_optimisation(df_data_period):
    model = setup_model(df_data_period)
    solve_model(model)
    print(pyo.value(model.OBJ))
    return model


def optimize_by_year(df_data):
    yearly_results = []
    models = []  
    
    for year, df_data_year in df_data.groupby(pd.Grouper(freq='Y')):
        if df_data_year.empty:
            print(f"Keine Daten für {year}")
            continue
        
        print(f"Optimierung {df_data_year.index[0]} bis {df_data_year.index[-1]}")
        model_year = main_optimisation(df_data_year)
        models.append(model_year)  
        
        df_extracted_year = extract_pyo_results_to_df(df_data_year, model_year)
        yearly_results.append(df_extracted_year)
    
    final_df_extracted = pd.concat(yearly_results)
    return final_df_extracted, models 


if __name__ == "__main__":
    df = create_dataframe(START_DATE, END_DATE, debug=False)
    print(df)
    start_time = time.time()
    final_df_extracted, models = optimize_by_year(df)
    print(final_df_extracted)
    export_results(final_df_extracted, RESULTS_FILE_NAME_EXCEL, RESULTS_FILE_NAME_PICKLE)



