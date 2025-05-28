import pyomo.environ as pyo
from config import (
    BAT_CAPACITY,
    SYSTEM_POWER,
)


def add_prl_constraints(model):
    M = 0.5 / BAT_CAPACITY
    def battery_soc_lower_rule(model, t):
        return model.v_BAT_SOC[t] >= SYSTEM_POWER * (0.5/BAT_CAPACITY) - M * (1 - model.v_MODE_PRL[model.time_to_interval[t]])
    model.c_PRL_BAT_SOC_LOWER = pyo.Constraint(model.T, rule=battery_soc_lower_rule)

    def battery_soc_upper_rule(model, t):
        return model.v_BAT_SOC[t] <= 1 - (SYSTEM_POWER * (0.5/BAT_CAPACITY)) + M * (1 - model.v_MODE_PRL[model.time_to_interval[t]])
    model.c_PRL_BAT_SOC_UPPER = pyo.Constraint(model.T, rule=battery_soc_upper_rule)