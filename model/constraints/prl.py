import pyomo.environ as pyo
from config import (
    BAT_CAPACITY,
    SYSTEM_POWER,
)

def add_prl_mode_constraints(model):
    def prl_ub_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_PRL_POWER[t] <= model.v_PRL_POWER[t].ub * model.v_MODE_PRL[iv]
    model.c_MODE_PRL_POWER_UB = pyo.Constraint(model.T, rule=prl_ub_rule)

    def prl_lb_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_PRL_POWER[t] >= 1 * model.v_MODE_PRL[iv]
    model.c_MODE_PRL_POWER_LB = pyo.Constraint(model.T, rule=prl_lb_rule)

def add_prl_constraints(model):
    def soc_prl_discharge_buffer(model, t):
        return model.v_BAT_SOC[t] * BAT_CAPACITY >= 0.5 * model.v_PRL_POWER[t]

    def soc_prl_charge_buffer(model, t):
        return (1-model.v_BAT_SOC[t]) * BAT_CAPACITY >= 0.5 * model.v_PRL_POWER[t]

    model.soc_prl_discharge_buffer = pyo.Constraint(model.T, rule=soc_prl_discharge_buffer)
    model.soc_prl_charge_buffer    = pyo.Constraint(model.T, rule=soc_prl_charge_buffer)




