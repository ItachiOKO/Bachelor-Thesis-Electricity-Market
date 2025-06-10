import pyomo.environ as pyo
from config import (
    SPECIFIC_AGING_COST,
    SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE,
    SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE,
)


def define_aging_cost_expr(model):
    def aging_cost_rule(model, t):
        return SPECIFIC_AGING_COST * (model.e_TOTAL_CHARGE[t] + model.e_TOTAL_DISCHARGE[t]) 

    model.e_AGING_COST     = pyo.Expression(model.T, rule=aging_cost_rule)
    model.e_AGING_COST_SUM = pyo.Expression(expr=sum(model.e_AGING_COST[t] for t in model.T))
