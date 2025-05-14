import pyomo.environ as pyo
from config import BATTERY_CAPACITY, EFFICIENCY, SYSTEM_POWER


def add_electricity_exchange_constraints(model):

    def cumulative_soc_rule(model, t):
        if t == min(model.T):
            return model.battery_soc[t] == (model.buy_volume[t]*EFFICIENCY - model.sell_volume[t]/EFFICIENCY) / BATTERY_CAPACITY
        else:
            prev_t = model.T.prev(t)  
            return model.battery_soc[t] == model.battery_soc[prev_t] + (model.buy_volume[t]*EFFICIENCY - model.sell_volume[t]/EFFICIENCY) / BATTERY_CAPACITY
    model.cumulative_soc_constraint = pyo.Constraint(model.T, rule=cumulative_soc_rule)


def add_prl_constraints(model):
    M = 0.5 / BATTERY_CAPACITY
    def battery_soc_lower_rule(model, t):
        return model.battery_soc[t] >= SYSTEM_POWER * (0.5/BATTERY_CAPACITY) - M * (1 - model.mode_prl[model.time_to_interval[t]])
    model.prl_battery_soc_lower_constraint = pyo.Constraint(model.T, rule=battery_soc_lower_rule)

    def battery_soc_upper_rule(model, t):
        return model.battery_soc[t] <= 1 - (SYSTEM_POWER * (0.5/BATTERY_CAPACITY)) + M * (1 - model.mode_prl[model.time_to_interval[t]])
    model.prl_battery_soc_upper_constraint = pyo.Constraint(model.T, rule=battery_soc_upper_rule)


def add_srl_constraints(model):	
    def max_srl_power_rule(model, t):	
        return model.srl_power_pos[t] + model.srl_power_neg[t] <= SYSTEM_POWER
    model.max_srl_power_constraint = pyo.Constraint(model.T, rule=max_srl_power_rule)

    M = 0.5 / BATTERY_CAPACITY
    def battery_soc_lower_rule(model, t):
        return model.battery_soc[t] >= SYSTEM_POWER * (0.5/BATTERY_CAPACITY) - M * (1 - model.mode_srl[model.time_to_interval[t]])
    model.srl_battery_soc_lower_constraint = pyo.Constraint(model.T, rule=battery_soc_lower_rule)

    def battery_soc_upper_rule(model, t):
        return model.battery_soc[t] <= 1 - (SYSTEM_POWER * (0.5/BATTERY_CAPACITY)) + M * (1 - model.mode_srl[model.time_to_interval[t]])
    model.srl_battery_soc_upper_constraint = pyo.Constraint(model.T, rule=battery_soc_upper_rule)

