from optimisation_model import setup_model, solve_model
from result_processing import process_results
from load_marketprice_data import create_dataframe
from config import START_DATE, END_DATE, BATTERY_CAPACITY, LIFETIME_CYCLES, SPECIFIC_CHARGE_RATE, CSV_PATH, STEP_INTERVAL, SKIPROWS, EFFICIENCY, RESULTS_FILE_NAME
from utils import get_interval_minutes


def main_optimisation(df):
    charge_rate = SPECIFIC_CHARGE_RATE * (get_interval_minutes(df)/60)
    time_points = df.index.tolist()
    market_price_dict = df['market_price'].to_dict()
    model = setup_model(time_points, market_price_dict, charge_rate)
    solve_model(model)
    return model

if __name__ == "__main__":
    df = create_dataframe(START_DATE, END_DATE, CSV_PATH, STEP_INTERVAL, SKIPROWS)
    model = main_optimisation(df)
    process_results(df, model, BATTERY_CAPACITY, LIFETIME_CYCLES)
    print(df)
    df.to_excel(RESULTS_FILE_NAME)
