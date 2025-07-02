import pyomo.environ as pyo
from typing import Mapping, Any
from config_column_names import ColumnNamesClean as CC

def define_params(model: pyo.ConcreteModel, df_data_period) -> None:
    
    #market prices
    higher_market_price_dict = df_data_period[CC.HiGHER_MARKET_PRICE].to_dict()
    lower_market_price_dict = df_data_period[CC.LOWER_MARKET_PRICE].to_dict()
    #PRL and SRL prices
    prl_price_dict = df_data_period[CC.PRL_PRICE].to_dict()
    srl_power_price_neg_dict = df_data_period[CC.SRL_POWER_PRICE_NEG].to_dict()
    srl_power_price_pos_dict = df_data_period[CC.SRL_POWER_PRICE_POS].to_dict()
    srl_work_price_neg_dict = df_data_period[CC.SRL_NEG_WORK_CBMP].to_dict()
    srl_work_price_pos_dict = df_data_period[CC.SRL_POS_WORK_CBMP].to_dict()

    model.p_HIGHER_MARKET_PRICE = pyo.Param(model.T, initialize=higher_market_price_dict)
    model.p_LOWER_MARKET_PRICE = pyo.Param(model.T, initialize=lower_market_price_dict)
    model.p_PRLPRICE    = pyo.Param(model.T, initialize=prl_price_dict)
    model.p_SRL_PRICE_NEG = pyo.Param(model.T, initialize=srl_power_price_neg_dict)
    model.p_SRL_PRICE_POS = pyo.Param(model.T, initialize=srl_power_price_pos_dict)
    model.p_SRL_WORK_PRICE_NEG = pyo.Param(model.T, initialize=srl_work_price_neg_dict)
    model.p_SRL_WORK_PRICE_POS = pyo.Param(model.T, initialize=srl_work_price_pos_dict)