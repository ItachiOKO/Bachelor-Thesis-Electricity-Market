import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .load_pkl import load_pkl_results
from config_column_names import ColumnNamesClean as CC

def plot_weekly_revenue_lines():
    data_dict = load_pkl_results('all.pkl')
    df = data_dict['timeseries']

    revenue_cols = [CC.REVENUE_MARKET, CC.REVENUE_PRL, CC.REVENUE_SRL, CC.REVENUE_TOTAL]
    
    if not all(col in df.columns for col in revenue_cols):
        print(f"FEHLER: Nicht alle benötigten Spalten {revenue_cols} im DataFrame gefunden.")
        return
        
    df_rev = df[revenue_cols]
    df_weekly = df_rev.resample('W').sum()

    df_long = df_weekly.reset_index().melt(
        id_vars='index', 
        value_vars=revenue_cols,
        var_name='Markt',        
        value_name='Wochenertrag' 
    )
    df_long.rename(columns={'index': 'Woche'}, inplace=True)

    plt.figure(figsize=(16, 8))
    
    sns.lineplot(data=df_long, x='Woche', y='Wochenertrag', hue='Markt', marker='o', palette='tab10')
    
    plt.title('Wöchentlicher Ertragsvergleich der Märkte', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Datum (Wochenbeginn)', fontsize=12)
    plt.ylabel('Summierter Wochenertrag in €', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(title='Märkte', frameon=True, shadow=True)
    plt.tight_layout()
    plt.show()