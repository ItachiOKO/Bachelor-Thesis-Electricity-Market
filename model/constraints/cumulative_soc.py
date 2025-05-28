import pyomo.environ as pyo
from config import (
    BAT_CAPACITY,
)


def add_cumulative_soc_constraints(model):
    def cumulative_soc_rule(model, t):
        if t == min(model.T):
            return model.v_BAT_SOC[t] == (model.e_CHARGE[t] - model.e_DISCHARGE[t]) / BAT_CAPACITY
        else:
            prev_t = model.T.prev(t)  
            return model.v_BAT_SOC[t] == model.v_BAT_SOC[prev_t] + (model.e_CHARGE[t] - model.e_DISCHARGE[t]) / BAT_CAPACITY
    model.c_CUMULATIVE_SOC = pyo.Constraint(model.T, rule=cumulative_soc_rule)