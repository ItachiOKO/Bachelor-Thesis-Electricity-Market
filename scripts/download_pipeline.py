import os
import time
from datetime import timedelta
import pandas as pd
from api.entsoe.loader.affr_cbmp_loader import AffrCbmpLoader
from api.exceptions import LoaderError


START_DATE = "2023-01-01"
END_DATE = "2023-01-04"
RAW_DATA_PATH = "data/raw/entsoe"


LOADERS_TO_RUN = {
    "AffrCbmpLoader": AffrCbmpLoader,
}


if __name__ == "__main__":
    api_key = '382100ed-6229-44cd-87c1-3726801cc157'


    for loader_name, LoaderClass in LOADERS_TO_RUN.items():
        print(f"\n--- Verarbeitung von: {loader_name} ---")
        output_dir = os.path.join(RAW_DATA_PATH, loader_name)
        os.makedirs(output_dir, exist_ok=True)
        loader = LoaderClass(api_key=api_key)

        for day in pd.date_range(start=START_DATE, end=END_DATE, freq='D'):
            day_str = day.strftime('%Y-%m-%d')
            output_filepath = os.path.join(output_dir, f"{day_str}.csv")

            if os.path.exists(output_filepath):
                continue

            print(f"Lade {day_str}...")
            try:
                period_start = day.strftime('%Y%m%d0000')
                period_end = (day + timedelta(days=1)).strftime('%Y%m%d0000')
                
                daily_df = loader.load(period_start=period_start, period_end=period_end)
                daily_df.to_pickle(output_filepath)
                time.sleep(0.5)
            except LoaderError as e:
                print(f"FEHLER bei {day_str}: {e}")