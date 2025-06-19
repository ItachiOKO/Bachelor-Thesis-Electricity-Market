import pyomo.environ as pyo
from config import (
    SYSTEM_POWER,
    CHARGE_RATE,
)


def define_variables(model):
    # market
    model.v_BUY_VOL  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE))
    model.v_SELL_VOL = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE))

    model.v_BAT_SOC = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))
    # prl and srl
    model.v_PRL_POWER   = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_NEG = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_POS = pyo.Var(model.D4, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))


    model.v_TAX_BASE  = pyo.Var(domain=pyo.NonNegativeReals)
