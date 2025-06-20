import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .load_pkl import load_pkl_results
from .bar_combiner import MarketDataCombiner

# 1) Kombinierer‐Klasse initialisieren
combiner = MarketDataCombiner()

# 2) Quellen dynamisch hinzufügen (beliebig viele Aufrufe möglich)
combiner.add_source(
    data_dict=load_pkl_results('market.pkl'),
    market_name='Energy Market',
    value_col='Total Revenue'
)
combiner.add_source(
    data_dict=load_pkl_results('prl.pkl'),
    market_name='PRL Market',
    value_col='Total Revenue'
)
combiner.add_source(
    data_dict=load_pkl_results('srl.pkl'),
    market_name='SRL Market',
    value_col='Total Revenue'
)

combined_df = combiner.get_combined_df(freq='W')


profit_col = 'Total Revenue'
print(combined_df)

plt.figure(figsize=(18, 9)) # Etwas grösser für bessere Lesbarkeit
sns.barplot(data=combined_df, x='Zeitraum', y=profit_col, hue='Markt', palette='viridis')

plt.title(f'Wöchentlicher "{profit_col}"-Vergleich der Märkte', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Zeitraum', fontsize=12)
plt.ylabel(f'Gesamt-{profit_col} in €', fontsize=12)
plt.xticks(rotation=60, ha='right') # Rotation angepasst für bessere Lesbarkeit
plt.legend(title='Märkte', fontsize=10)

plt.show()