import pyomo.environ as pyo
from config import (
    SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE,
)


def define_revenue_expr(model):
    def rev_market_per_t(model, t):
        return model.v_DA_AUC_SELL_VOL[t] * model.p_HIGHER_MARKET_PRICE[t] - model.v_DA_AUC_BUY_VOL[t] * model.p_LOWER_MARKET_PRICE[t]
    model.e_REVENUE_MARKET = pyo.Expression(model.T, rule=rev_market_per_t)
    model.e_REVENUE_MARKET_SUM = pyo.Expression(expr=sum(model.e_REVENUE_MARKET[t] for t in model.T))


    def rev_prl_per_t(model, t):
        return model.p_PRLPRICE[t] * model.v_PRL_POWER[t]
    model.e_REVENUE_PRL = pyo.Expression(model.T, rule=rev_prl_per_t)
    model.e_REVENUE_PRL_SUM = pyo.Expression(expr=sum(model.e_REVENUE_PRL[t] for t in model.T))

    def rev_srl_per_t(model, t):
        return model.v_SRL_POWER_NEG[t] * (model.p_SRL_PRICE_NEG[t] - model.p_SRL_WORK_PRICE_NEG[t] * SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE) + model.v_SRL_POWER_POS[t] * (model.p_SRL_PRICE_POS[t] + model.p_SRL_WORK_PRICE_POS[t] * SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE)
    model.e_REVENUE_SRL = pyo.Expression(model.T, rule=rev_srl_per_t)
    model.e_REVENUE_SRL_SUM = pyo.Expression(expr=sum(model.e_REVENUE_SRL[t] for t in model.T))

    def rev_total_per_t(model, t):
        return 1 * model.e_REVENUE_MARKET[t] + 1* model.e_REVENUE_PRL[t] + 0 *model.e_REVENUE_SRL[t]
    model.e_TOTAL_REVENUE = pyo.Expression(model.T, rule=rev_total_per_t)
    model.e_TOTAL_REVENUE_SUM = pyo.Expression(expr=sum(model.e_TOTAL_REVENUE[t] for t in model.T))


