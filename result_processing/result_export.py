from pathlib import Path
import pandas as pd 
import pickle
from utils import convert_datetime_to_string
from config import (
    RESULTS_FILE_NAME_EXCEL,
    RESULTS_FILE_NAME_PICKLE,
    RESULTS_DIR
)

def export_results(df_timeseries: pd.DataFrame,
                   df_attrs: pd.DataFrame,
                   results_dir: Path = RESULTS_DIR,
                   excel_name: str = RESULTS_FILE_NAME_EXCEL,
                   pickle_name: str = RESULTS_FILE_NAME_PICKLE):

    excel_path = results_dir / excel_name
    pickle_path = results_dir / pickle_name

    export_to_pickle(df_timeseries, df_attrs, pickle_path)
    export_to_excel(df_timeseries, df_attrs, excel_path)


def export_to_pickle(df_timeseries: pd.DataFrame,
                     df_attrs: pd.DataFrame,
                     path: Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'timeseries': df_timeseries,
        'attributes': df_attrs
    }
    with open(path, 'wb') as f:
        pickle.dump(payload, f)


def export_to_excel(df_timeseries: pd.DataFrame,
                    df_attrs: pd.DataFrame,
                    path: Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    df_ts_fmt = convert_datetime_to_string(df_timeseries)

    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        df_ts_fmt.to_excel(writer, sheet_name='Data')
        df_attrs.to_excel(writer, sheet_name='Attributes', index=True)


