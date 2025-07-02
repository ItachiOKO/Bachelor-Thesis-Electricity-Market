from pathlib import Path
import pandas as pd

from config import RESULTS_DIR, RESULTS_FILE_NAME_PICKLE
from visualization.compare_revenue_markets_seperated  import plot_compare_profit_markets_monthly
from visualization.compare_revenue_markets_together import plot_weekly_revenue_lines



def create_plots():
    plots_dir = Path(RESULTS_DIR) / "plots"
    plots_dir.mkdir(exist_ok=True)

    # create plots
    plot_compare_profit_markets_monthly()
    plot_weekly_revenue_lines()


if __name__ == "__main__":
    create_plots()

