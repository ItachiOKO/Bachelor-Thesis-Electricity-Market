import pyomo.environ as pyo
from config import (
    SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE,
    MARKET_SWITCH,
    PRL_SWITCH, 
    SRL_SWITCH,
)


def define_revenue_expr(model):
    
    def rev_market(model, t):
        return MARKET_SWITCH * (model.v_SELL_VOL[t] * model.p_HIGHER_MARKET_PRICE[t] - model.v_BUY_VOL[t] * model.p_LOWER_MARKET_PRICE[t])
    model.e_REVENUE_MARKET = pyo.Expression(model.T, rule=rev_market)
    model.e_REVENUE_MARKET_SUM = pyo.Expression(expr=sum(model.e_REVENUE_MARKET[t] for t in model.T))


    def rev_prl(model, t):
        return model.p_PRLPRICE[t] * model.e_PRL_POWER[t]
    model.e_REVENUE_PRL = pyo.Expression(model.T, rule=rev_prl)
    model.e_REVENUE_PRL_SUM = pyo.Expression(expr=sum(model.e_REVENUE_PRL[t] for t in model.T))

    def rev_srl(model, t):
        rev_p_neg = model.e_SRL_POWER_NEG[t] * model.p_SRL_PRICE_NEG[t]
        rev_p_pos = model.e_SRL_POWER_POS[t] * model.p_SRL_PRICE_POS[t]
        rev_w_neg = model.e_SRL_POWER_NEG[t] * -model.p_SRL_WORK_PRICE_NEG[t] * 1/4  # mwh/15min # negativer Preis --> Anbieter erhält Geld
        rev_w_pos = model.e_SRL_POWER_POS[t] * model.p_SRL_WORK_PRICE_POS[t] * 1/4   # mwh/15min # positiver Preis --> Anbieter erhält Geld
        return rev_p_neg + rev_p_pos + rev_w_neg + rev_w_pos

    model.e_REVENUE_SRL = pyo.Expression(model.T, rule=rev_srl)
    model.e_REVENUE_SRL_SUM = pyo.Expression(expr=sum(model.e_REVENUE_SRL[t] for t in model.T))


    def rev_total(model, t):
        return  model.e_REVENUE_MARKET[t] + model.e_REVENUE_PRL[t] + model.e_REVENUE_SRL[t]
    model.e_TOTAL_REVENUE = pyo.Expression(model.T, rule=rev_total)
    model.e_TOTAL_REVENUE_SUM = pyo.Expression(expr=sum(model.e_TOTAL_REVENUE[t] for t in model.T))
