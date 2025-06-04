import pyomo.environ as pyo
from typing import Mapping, Any

def define_params(
    model: pyo.ConcreteModel,
    higer_market_price_dict: Mapping[Any, float],
    lower_market_price_dict: Mapping[Any, float],
    prl_price_dict: Mapping[Any, float],
    srl_price_neg_dict: Mapping[Any, float],
    srl_price_pos_dict: Mapping[Any, float],
    srl_work_price_neg_dict: Mapping[Any, float],
    srl_work_price_pos_dict: Mapping[Any, float],
) -> None:

    model.p_HIGHER_MARKET_PRICE = pyo.Param(model.T, initialize=higer_market_price_dict)
    model.p_LOWER_MARKET_PRICE = pyo.Param(model.T, initialize=lower_market_price_dict)
    model.p_PRLPRICE    = pyo.Param(model.T, initialize=prl_price_dict)
    model.p_SRL_PRICE_NEG = pyo.Param(model.T, initialize=srl_price_neg_dict)
    model.p_SRL_PRICE_POS = pyo.Param(model.T, initialize=srl_price_pos_dict)
    model.p_SRL_WORK_PRICE_NEG = pyo.Param(model.T, initialize=srl_work_price_neg_dict)
    model.p_SRL_WORK_PRICE_POS = pyo.Param(model.T, initialize=srl_work_price_pos_dict)