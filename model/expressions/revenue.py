import pyomo.environ as pyo
from config import (
    SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE,
)


def define_revenue_expr(model):
    model.e_REVENUE_MARKET = pyo.Expression(
        expr = sum(
            model.v_DA_AUC_SELL_VOL[t] * model.p_HIGHER_MARKET_PRICE[t]
          - model.v_DA_AUC_BUY_VOL[t]  * model.p_LOWER_MARKET_PRICE[t]
          for t in model.T
        )
    )

    model.e_REVENUE_PRL = pyo.Expression(
        expr = sum(
            model.p_PRLPRICE[t] * model.v_PRL_POWER[t]
            for t in model.T
        )
    )

    model.e_REVENUE_SRL = pyo.Expression(
        expr = sum(
            model.v_SRL_POWER_NEG[t] * (model.p_SRL_PRICE_NEG[t] + -1*model.p_SRL_WORK_PRICE_NEG[t] * SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE)
          + model.v_SRL_POWER_POS[t] * (model.p_SRL_PRICE_POS[t] + model.p_SRL_WORK_PRICE_POS[t] * SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE)

            for t in model.T
        )
    )
    
    model.e_TOTAL_REVEVNUE = pyo.Expression(
        expr = model.e_REVENUE_MARKET + model.e_REVENUE_PRL +  model.e_REVENUE_SRL
    )
