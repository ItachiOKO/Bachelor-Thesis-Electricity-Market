import pandas as pd 
from utils import convert_datetime_to_string
from pathlib import Path
from config import (
    RESULTS_FILE_NAME_EXCEL,
    RESULTS_FILE_NAME_PICKLE,
    RESULTS_DIR
)
def export_results(df, 
                   excel_name: str = RESULTS_FILE_NAME_EXCEL, 
                   pickle_name: str = RESULTS_FILE_NAME_PICKLE,
                   results_dir: Path = RESULTS_DIR):
    # Ordner anlegen, falls nicht vorhanden
    results_dir.mkdir(parents=True, exist_ok=True)

    excel_path = results_dir / excel_name
    pickle_path = results_dir / pickle_name

    df.to_pickle(pickle_path)
    formatted_df = convert_datetime_to_string(df)
    attrs_df = pd.DataFrame(
        list(formatted_df.attrs.items()), 
        columns=['Attribute', 'Value']
    )

    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        attrs_df.to_excel(writer, sheet_name='Attributes', index=False)
        formatted_df.to_excel(writer, sheet_name='Data')