import pyomo.environ as pyo
from config import BAT_CAPACITY, EFFICIENCY, SYSTEM_POWER


def add_electricity_exchange_constraints(model):

    def cumulative_soc_rule(model, t):
        if t == min(model.T):
            return model.v_BAT_SOC[t] == (model.v_DA_AUC_BUY_VOL[t]*EFFICIENCY - model.v_DA_AUC_SELL_VOL[t]/EFFICIENCY) / BAT_CAPACITY
        else:
            prev_t = model.T.prev(t)  
            return model.v_BAT_SOC[t] == model.v_BAT_SOC[prev_t] + (model.v_DA_AUC_BUY_VOL[t]*EFFICIENCY - model.v_DA_AUC_SELL_VOL[t]/EFFICIENCY) / BAT_CAPACITY
    model.c_CUMULATIVE_SOC = pyo.Constraint(model.T, rule=cumulative_soc_rule)


def add_prl_constraints(model):
    M = 0.5 / BAT_CAPACITY
    def battery_soc_lower_rule(model, t):
        return model.v_BAT_SOC[t] >= SYSTEM_POWER * (0.5/BAT_CAPACITY) - M * (1 - model.v_MODE_PRL[model.time_to_interval[t]])
    model.c_PRL_BAT_SOC_LOWER = pyo.Constraint(model.T, rule=battery_soc_lower_rule)

    def battery_soc_upper_rule(model, t):
        return model.v_BAT_SOC[t] <= 1 - (SYSTEM_POWER * (0.5/BAT_CAPACITY)) + M * (1 - model.v_MODE_PRL[model.time_to_interval[t]])
    model.c_PRL_BAT_SOC_UPPER = pyo.Constraint(model.T, rule=battery_soc_upper_rule)


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
