import pandas as pd
import pyomo.environ as pyo
from config import ColumnNamesClean as CC	



import pandas as pd
import pyomo.environ as pyo

# Einfachste Version: sammelt alle Werte in einem dict und baut per from_dict einen DataFrame
# Der anschließende update-Call matched automatisch Index (Timestamp) und Spalten

def add_model_timeseries_results_to_df(df_template, models_by_year):
    vars_map = {
        CC.DA_AUC_BUY_VOL:  lambda m, t: m.v_DA_AUC_BUY_VOL[t],
        CC.DA_AUC_SELL_VOL: lambda m, t: m.v_DA_AUC_SELL_VOL[t],
        CC.BAT_SOC:         lambda m, t: m.v_BAT_SOC[t],
        CC.AGING_COST:      lambda m, t: m.e_AGING_COST[t],
        CC.PRL_POWER:       lambda m, t: m.v_PRL_POWER[t],
        CC.SRL_POWER_NEG:   lambda m, t: m.v_SRL_POWER_NEG[t],
        CC.SRL_POWER_POS:   lambda m, t: m.v_SRL_POWER_POS[t],
    }

    df = df_template.copy()
    data = {}
    for model in models_by_year.values():
        for t in model.T:
            data[t] = {col: pyo.value(fn(model, t)) for col, fn in vars_map.items()}

    var_df = pd.DataFrame.from_dict(data, orient='index')
    df.update(var_df)
    return df




def add_model_atrs_results_to_df(models_by_year):
    attrs = {
        'OBJ':                   lambda m: pyo.value(m.OBJ),
        'TOTAL_REVENUE_SUM':     lambda m: pyo.value(m.e_TOTAL_REVENUE_SUM),
    }

    data = {}
    for year, model in models_by_year.items():
        data[year] = {name: fn(model) for name, fn in attrs.items()}

    df_attrs = pd.DataFrame.from_dict(data, orient='index')
    df_attrs.index.name = 'Year'
    
    return df_attrs




