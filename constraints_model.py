import pyomo.environ as pyo
from config import BATTERY_CAPACITY, EFFICIENCY, BATTERY_PRICE, LIFETIME_CYCLES, END_OF_DAY_SOC

def add_electricity_exchange_constraints(model):
    def cumulative_soc_rule(model, t):
        if t == min(model.T):
            return model.battery_soc[t] == model.buy_volume[t]*EFFICIENCY - model.sell_volume[t]/EFFICIENCY
        else:
            prev_t = model.T.prev(t)  
            return model.battery_soc[t] == model.battery_soc[prev_t] + model.buy_volume[t]*EFFICIENCY - model.sell_volume[t]/EFFICIENCY
    model.cumulative_soc_constraint = pyo.Constraint(model.T, rule=cumulative_soc_rule)

    def aging_cost_rule(model, t):
        specific_aging_cost = BATTERY_PRICE / (BATTERY_CAPACITY * LIFETIME_CYCLES) / 2
        return model.aging_cost[t] == specific_aging_cost * (model.buy_volume[t] * EFFICIENCY + model.sell_volume[t]/EFFICIENCY)
    model.aging_cost_constraint = pyo.Constraint(model.T, rule=aging_cost_rule)

    def end_of_day_soc_rule(model, t):
        if END_OF_DAY_SOC == 0:
            return pyo.Constraint.Skip
        current_date = t.date()
        daily_steps = [t_ for t_ in model.T if t_.date() == current_date]
        if t == max(daily_steps):
            return model.battery_soc[t] == 0.5 * BATTERY_CAPACITY
        return pyo.Constraint.Skip
    model.end_of_day_soc_constraint = pyo.Constraint(model.T, rule=end_of_day_soc_rule)

def add_prl_constraints(model):
    def prl_capacity_once_a_day_rule(model, t):
        current_date = t.date()
        daily_steps = [t_ for t_ in model.T if t_.date() == current_date]
        if t != min(daily_steps):
            return model.prl_capacity[t] == 0
        return pyo.Constraint.Skip
    model.prl_capacity_once_a_day_constraint = pyo.Constraint(model.T, rule=prl_capacity_once_a_day_rule)


def add_market_choice_constraint(model, t, charge_rate):
    unique_days = t.date()
    model.D = pyo.Set(initialize=unique_days, ordered=True, within=pyo.Any)
    
    def day_init(model, t):
        return t.date()
    model.day = pyo.Param(model.T, initialize=day_init, within=pyo.Any)
    
    model.mode = pyo.Var(model.D, domain=pyo.Binary)

    M_buy = charge_rate / EFFICIENCY
    M_sell = charge_rate * EFFICIENCY
    M_prl = BATTERY_CAPACITY
    
    def market_mode_buy_rule(model, t):
        d = model.day[t]

        return model.buy_volume[t] <= M_buy * model.mode[d]
    model.market_mode_buy_constraint = pyo.Constraint(model.T, rule=market_mode_buy_rule)
    
    def market_mode_sell_rule(model, t):
        d = model.day[t]
        return model.sell_volume[t] <= M_sell * model.mode[d]
    model.market_mode_sell_constraint = pyo.Constraint(model.T, rule=market_mode_sell_rule)
    
    def prl_mode_rule(model, t):
        d = model.day[t]
        return model.prl_capacity[t] <= M_prl * (1 - model.mode[d])
    model.prl_mode_constraint = pyo.Constraint(model.T, rule=prl_mode_rule)