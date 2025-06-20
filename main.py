import logging
logging.getLogger('pyomo').setLevel(logging.WARNING)

import time
import pandas as pd
from typing import Dict
import pyomo.environ as pyo
from model.model_builder import setup_model, solve_model
from result_processing.pyomo_extractor import add_model_timeseries_results_to_df, add_model_atrs_results_to_df
from result_processing.result_export import export_results
from data_pipline import create_dataframe
from config import (
    START_DATE,
    END_DATE,
)
from utils import get_config_as_dict


def main_optimisation(df_data_period):
    model = setup_model(df_data_period)
    solve_model(model)
    print(f" profit: {pyo.value(model.OBJ)}")
    return model


def build_models_by_year(df_data: pd.DataFrame) -> Dict[int, object]:

    models_by_year = {}
    for year_timestamp, df_data_year in df_data.groupby(pd.Grouper(freq='Y')):
        if df_data_year.empty:
            continue

        year = year_timestamp.year
        print(f"Baue Modell für Jahr {year} ({df_data_year.index[0].date()} bis {df_data_year.index[-1].date()})")
        #measure
        start_time = time.time()
        model_year = main_optimisation(df_data_year)
        print(f"{year}:  {time.time() - start_time:.2f} Sekunden")
        models_by_year[year] = model_year

    return models_by_year


if __name__ == "__main__":
    df = create_dataframe(START_DATE, END_DATE, debug=False)
    models_by_year = build_models_by_year(df)

    df_timeseries = add_model_timeseries_results_to_df(df, models_by_year)
    df_attrs = add_model_atrs_results_to_df(models_by_year)

    #print(df_timeseries)
    print(df_attrs)
    config_data = get_config_as_dict()
    export_results(df_timeseries, df_attrs, config_data)



