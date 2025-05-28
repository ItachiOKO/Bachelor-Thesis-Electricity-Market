import pyomo.environ as pyo
from config import (
    SPECIFIC_AGING_COST,
    SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE,
    SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE,
)


def define_aging_cost_expr(model):
    def aging_cost_rule(model, t):
        c_exchange = SPECIFIC_AGING_COST * (model.e_CHARGE[t] + model.e_DISCHARGE[t])
        c_prl = SPECIFIC_AGING_COST * SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE * model.v_PRL_POWER[t]
        c_srl = SPECIFIC_AGING_COST * (SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE * (model.v_SRL_POWER_NEG[t] + model.v_SRL_POWER_POS[t]))
        return c_exchange + c_prl + c_srl

    model.e_AGING_COST     = pyo.Expression(model.T, rule=aging_cost_rule)
    model.e_AGING_COST_SUM = pyo.Expression(expr=sum(model.e_AGING_COST[t] for t in model.T))
