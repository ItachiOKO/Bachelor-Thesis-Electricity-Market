from pathlib import Path
import pandas as pd
from config import (
    RESULTS_DIR,
    RESULTS_FILE_NAME_PICKLE
)

def load_pkl_results(pfkl_file_name: str = RESULTS_FILE_NAME_PICKLE) -> pd.DataFrame:
    results_dir = Path(RESULTS_DIR)
    pkl_file = results_dir / pfkl_file_name

    if not pkl_file.exists():
        raise FileNotFoundError(f"{RESULTS_FILE_NAME_PICKLE} does not exist.")
    
    df = pd.read_pickle(pkl_file)
    return df