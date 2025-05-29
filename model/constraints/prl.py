import pyomo.environ as pyo
from config import (
    BAT_CAPACITY,
    SYSTEM_POWER,
)


def add_prl_constraints(model):
    def battery_soc_lower_rule(model, t):
        return model.v_BAT_SOC[t] * BAT_CAPACITY >= 0.5 * model.v_PRL_POWER[t] 
    model.c_PRL_BAT_SOC_LOWER = pyo.Constraint(model.T, rule=battery_soc_lower_rule)

    def battery_soc_upper_rule(model, t):
        return (1 - model.v_BAT_SOC[t]) * BAT_CAPACITY >= 0.5 * model.v_PRL_POWER[t] 
    model.c_PRL_BAT_SOC_UPPER = pyo.Constraint(model.T, rule=battery_soc_upper_rule)



