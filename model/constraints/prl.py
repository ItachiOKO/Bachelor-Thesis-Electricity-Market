import pyomo.environ as pyo
from config import (
    BAT_CAPACITY,
    SYSTEM_POWER,
)

def add_prl_mode_constraints(model):
    def prl_ub_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_PRL_POWER[iv] <= SYSTEM_POWER * m.v_MODE_PRL[iv]
    model.c_PRL_POWER_UB_IV = pyo.Constraint(model.D4, rule=prl_ub_iv)

    def prl_lb_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_PRL_POWER[iv] >= 1 * m.v_MODE_PRL[iv]
    model.c_PRL_POWER_LB_IV = pyo.Constraint(model.D4, rule=prl_lb_iv)


def add_prl_constraints(model):
    def soc_prl_discharge_buffer(model, t):
        return model.v_BAT_SOC[t] * BAT_CAPACITY >= 0.5 * model.e_PRL_POWER[t]

    def soc_prl_charge_buffer(model, t):
        return (1-model.v_BAT_SOC[t]) * BAT_CAPACITY >= 0.5 * model.e_PRL_POWER[t]

    model.soc_prl_discharge_buffer = pyo.Constraint(model.T, rule=soc_prl_discharge_buffer)
    model.soc_prl_charge_buffer    = pyo.Constraint(model.T, rule=soc_prl_charge_buffer)




