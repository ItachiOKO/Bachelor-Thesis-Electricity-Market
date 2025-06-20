import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .load_pkl import load_pkl_results
from config_column_names import ColumnNamesClean as CC

def plot_compare_profit_markets_monthly():
    market_dict = load_pkl_results('market.pkl')   
    prl_dict = load_pkl_results('prl.pkl')         
    srl_dict = load_pkl_results('srl.pkl')
    
    dict_list = [market_dict, prl_dict, srl_dict]
    market_names = ['Energy Market', 'PRL Market', 'SRL Market']
    profit_col = CC.REVENUE_TOTAL

    processed_dfs = []
    for i, data_dict in enumerate(dict_list):
        df_ts = data_dict['timeseries']
        df_ts.columns = df_ts.columns.str.strip()

        if profit_col not in df_ts.columns:
            print(f"FEHLER: Spalte '{profit_col}' in '{market_names[i]}' nicht gefunden. Überspringe...")
            continue 

        weekly_profit = df_ts[profit_col].resample('W').sum().to_frame()
        weekly_profit['Zeitraum'] = weekly_profit.index.strftime('%Y - Woche %U')
        weekly_profit['Markt'] = market_names[i]
        processed_dfs.append(weekly_profit)

    if not processed_dfs:
        print("Keine Daten zum Plotten vorhanden. Verarbeitung wird abgebrochen.")
        return

    combined_df = pd.concat(processed_dfs)
    print(combined_df)

    plt.figure(figsize=(18, 9)) # Etwas grösser für bessere Lesbarkeit
    sns.barplot(data=combined_df, x='Zeitraum', y=profit_col, hue='Markt', palette='viridis')
    
    plt.title(f'Wöchentlicher "{profit_col}"-Vergleich der Märkte', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Zeitraum', fontsize=12)
    plt.ylabel(f'Gesamt-{profit_col} in €', fontsize=12)
    plt.xticks(rotation=60, ha='right') # Rotation angepasst für bessere Lesbarkeit
    plt.legend(title='Märkte', fontsize=10)
    
    plt.show()