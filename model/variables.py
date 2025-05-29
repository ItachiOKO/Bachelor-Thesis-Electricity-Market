import pyomo.environ as pyo
from config import (
    SYSTEM_POWER
)


def define_variables(model, charge_rate):
    model.v_DA_AUC_BUY_VOL  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate))
    model.v_DA_AUC_SELL_VOL = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate))
    model.v_BAT_SOC = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))
    model.v_PRL_POWER   = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_NEG = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_POS = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))

    model.v_TAX_BASE  = pyo.Var(domain=pyo.NonNegativeReals)
