import time
import json
from optimisation_model import setup_model, solve_model
from result_processing import process_results
from result_export import export_results
from load_marketprice_data import create_dataframe
from utils import get_interval_minutes
from config import (
    BATTERY_CAPACITY,
    BATTERY_PRICE,
    CELL_NAMES,
    CSV_PATH,
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


if __name__ == "__main__":
    df = create_dataframe(CSV_PATH, SKIPROWS, START_DATE, END_DATE)
    start_time = time.time()
    model = main_optimisation(df)
    print(f"Berrechnungszeit: {round(time.time() - start_time, 1)} Sekunden")
    df = process_results(df, model, CELL_NAMES, START_DATE, END_DATE, BATTERY_CAPACITY, LIFETIME_CYCLES, BATTERY_PRICE, EFFICIENCY)
    export_results(df, RESULTS_FILE_NAME_EXCEL, RESULTS_FILE_NAME_PICKLE)
    print(df)
    print(json.dumps(df.attrs, indent=4))

