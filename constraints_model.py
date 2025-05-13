import pyomo.environ as pyo
from config import BATTERY_CAPACITY, EFFICIENCY, SYSTEM_POWER
from cost_calculator import calculate_depreciation_amount


def add_electricity_exchange_constraints(model):

    def cumulative_soc_rule(model, t):
        if t == min(model.T):
            return model.battery_soc[t] == (model.buy_volume[t]*EFFICIENCY - model.sell_volume[t]/EFFICIENCY) / BATTERY_CAPACITY
        else:
            prev_t = model.T.prev(t)  
            return model.battery_soc[t] == model.battery_soc[prev_t] + (model.buy_volume[t]*EFFICIENCY - model.sell_volume[t]/EFFICIENCY) / BATTERY_CAPACITY
    model.cumulative_soc_constraint = pyo.Constraint(model.T, rule=cumulative_soc_rule)

def add_prl_constraints(model):
    return None


def add_market_choice_constraint(model, time_points):
    unique_intervals = sorted({(t.date(), t.hour // 4) for t in time_points})
    model.D4 = pyo.Set(initialize=unique_intervals, ordered=True)
    model.mode = pyo.Var(model.D4, domain=pyo.Binary) # 0 = PRL, 1 = Market

    time_to_interval = {t: (t.date(), t.hour // 4) for t in time_points}

    def market_mode_buy_rule(model, t):
        return model.buy_volume[t] <= model.buy_volume[t].ub * model.mode[time_to_interval[t]]
    model.market_mode_buy_constraint = pyo.Constraint(model.T, rule=market_mode_buy_rule)
    
    def market_mode_sell_rule(model, t):
        return model.sell_volume[t] <= model.sell_volume[t].ub * model.mode[time_to_interval[t]]
    model.market_mode_sell_constraint = pyo.Constraint(model.T, rule=market_mode_sell_rule)
    
    def prl_mode_rule(model, t):
        return model.prl_power[t] <= model.prl_power[t].ub * (1 - model.mode[time_to_interval[t]])
    model.prl_mode_constraint = pyo.Constraint(model.T, rule=prl_mode_rule)
    
   
    M = 0.5 / BATTERY_CAPACITY
    def battery_soc_lower_rule(model, t):
        return model.battery_soc[t] >= SYSTEM_POWER * (0.5/BATTERY_CAPACITY) - M * model.mode[time_to_interval[t]]
    model.battery_soc_lower_constraint = pyo.Constraint(model.T, rule=battery_soc_lower_rule)

    def battery_soc_upper_rule(model, t):
        return model.battery_soc[t] <= 1 - (SYSTEM_POWER * (0.5/BATTERY_CAPACITY)) + M * model.mode[time_to_interval[t]]
    model.battery_soc_upper_constraint = pyo.Constraint(model.T, rule=battery_soc_upper_rule)


def add_tax_constraints(model):
    s = calculate_depreciation_amount()
    revenue = model.total_revenue
    # tax_base = max(0, profit - s)
    model.c1 = pyo.Constraint(expr = model.tax_base >= revenue - s)
    model.c2 = pyo.Constraint(expr = model.tax_base >= 0)



#1. Fall: soc >= 1MW * (0,5/1MWh) - 0,5/1MWh * mode
#         soc >=       0,5 - 0,5*mode


#2. Fall: soc <= 1MW * (0,5/1MWh) - 0,5/1MWh * mode
#         soc <=       0,5 - 0,5*mode




# prl_power = 1-soc * 2C
# prl_power = soc * 2C

# prl_power_helper <= (1-soc) *2C * (1-mode)
# prl_power_helper <= soc * 2C * (1-mode)



