import pyomo.environ as pyo
from config import BAT_CAPACITY, SYSTEM_POWER


def add_srl_constraints(model):	
    def max_srl_power_rule(model, t):	
        return model.v_SRL_POWER_POS[t] + model.v_SRL_POWER_NEG[t] <= SYSTEM_POWER
    model.c_MAX_SRL_POWER = pyo.Constraint(model.T, rule=max_srl_power_rule)


    def srl_power_pos_rule(model, t):
        return model.v_SRL_POWER_POS[t] <= BAT_CAPACITY * model.v_BAT_SOC[t] * model.v_MODE_SRL[model.time_to_interval[t]]
    model.c_SRL_POWER_POS = pyo.Constraint(model.T, rule=srl_power_pos_rule)

    def srl_power_neg_rule(model, t):
        return model.v_SRL_POWER_NEG[t] <= BAT_CAPACITY *(1 - model.v_BAT_SOC[t]) * model.v_MODE_SRL[model.time_to_interval[t]]
    model.c_SRL_POWER_NEG = pyo.Constraint(model.T, rule=srl_power_neg_rule)
