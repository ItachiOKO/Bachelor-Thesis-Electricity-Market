import pyomo.environ as pyo
from config import (
    BAT_CAPACITY,
    SYSTEM_POWER,
)


def add_prl_constraints(model):
    def soc_prl_upper(model, t):
        # Wenn v_PRL_POWER[t] = 1:  v_BAT_SOC[t]*BAT_CAPACITY <= 0.5*BAT_CAPACITY
        # Wenn v_PRL_POWER[t] = 0:  v_BAT_SOC[t]*BAT_CAPACITY <= 0.5*BAT_CAPACITY + 1*BAT_CAPACITY = 1.5*BAT_CAPACITY
        #                                                          ⇒ triviale obere Schranke ≤ 1.5*BAT_CAPACITY, denn SOC<=1 ⇒ SOC*BAT_CAPACITY<=BAT_CAPACITY
        return model.v_BAT_SOC[t] * BAT_CAPACITY <= 0.5 * BAT_CAPACITY \
            + (1 - model.v_PRL_POWER[t]) * BAT_CAPACITY

    def soc_prl_lower(model, t):
        # Wenn v_PRL_POWER[t] = 1:  v_BAT_SOC[t]*BAT_CAPACITY >= 0.5*BAT_CAPACITY
        # Wenn v_PRL_POWER[t] = 0:  v_BAT_SOC[t]*BAT_CAPACITY >= 0.5*BAT_CAPACITY - 1*BAT_CAPACITY = -0.5*BAT_CAPACITY
        #                                                            ⇒ triviale untere Schranke ≥ -0.5*BAT_CAPACITY, denn SOC>=0
        return model.v_BAT_SOC[t] * BAT_CAPACITY >= 0.5 * BAT_CAPACITY \
            - (1 - model.v_PRL_POWER[t]) * BAT_CAPACITY

    model.c_SOC_PRL_UPPER = pyo.Constraint(model.T, rule=soc_prl_upper)
    model.c_SOC_PRL_LOWER = pyo.Constraint(model.T, rule=soc_prl_lower)



