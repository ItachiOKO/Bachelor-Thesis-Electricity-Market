import pandas as pd
import pyomo.environ as pyo
from config import ColumnNamesClean as CC	



import pandas as pd
import pyomo.environ as pyo


def add_model_timeseries_results_to_df(template_df, models_by_year):
    column_extractor_map = {
        CC.BUY_VOL:  lambda m, t: m.v_BUY_VOL[t],
        CC.SELL_VOL: lambda m, t: m.v_SELL_VOL[t],
        CC.BAT_SOC:         lambda m, t: m.v_BAT_SOC[t],
        CC.PRL_POWER:       lambda m, t: m.e_PRL_POWER[t],
        CC.SRL_POWER_NEG:   lambda m, t: m.e_SRL_POWER_NEG[t],
        CC.SRL_POWER_POS:   lambda m, t: m.e_SRL_POWER_POS[t],
        CC.AGING_COST:      lambda m, t: m.e_AGING_COST[t],
    }

    model_results_timeseries = {}
    for year, model in models_by_year.items():
        for t in model.T:
            model_results_timeseries[t] = {col: pyo.value(fn(model, t)) for col, fn in column_extractor_map.items()}

    results_timeseries_df = pd.DataFrame.from_dict(model_results_timeseries, orient='index')
    combined_df = pd.concat([template_df, results_timeseries_df], axis=1)
    return combined_df


def add_model_atrs_results_to_df(models_by_year):
    attrs = {

        CC.PRL_POWER_SUM: lambda m: pyo.value(m.e_PRL_POWER_SUM),
        CC.SRL_POWER_NEG_SUM: lambda m: pyo.value(m.e_SRL_POWER_NEG_SUM),
        CC.SRL_POWER_POS_SUM: lambda m: pyo.value(m.e_SRL_POWER_POS_SUM),
        CC.AGING_COST_SUM: lambda m: pyo.value(m.e_AGING_COST_SUM),


        CC.REVENUE_MARKET_SUM: lambda m: pyo.value(m.e_REVENUE_MARKET_SUM),
        CC.REVENUE_PRL_SUM: lambda m: pyo.value(m.e_REVENUE_PRL_SUM),
        CC.REVENUE_SRL_SUM: lambda m: pyo.value(m.e_REVENUE_SRL_SUM),
        CC.TOTAL_REVENUE_SUM: lambda m: pyo.value(m.e_TOTAL_REVENUE_SUM),
        CC.TAXES_SUM: lambda m: pyo.value(m.e_TAX),
        CC.OBJ: lambda m: pyo.value(m.OBJ),
        #CC.REVENUE_PRL_SUM:     
        #CC.REVENUE_SRL_SUM:  
        #CC.TOTAL_REVENUE_SUM:
        #CC.TAXES_SUM:        
        #CC.OBJ:              



        #CC.OBJ:                   lambda m: pyo.value(m.OBJ),
        #CC.TOTAL_REVENUE_SUM:     lambda m: pyo.value(m.e_TOTAL_REVENUE_SUM),
    }

    data = {}
    for year, model in models_by_year.items():
        data[year] = {name: fn(model) for name, fn in attrs.items()}

    df_attrs = pd.DataFrame.from_dict(data, orient='index')
    df_attrs.index.name = 'Year'
    
    return df_attrs




