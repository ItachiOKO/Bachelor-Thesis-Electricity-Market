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

def add_market_choice_constraint(model, time_points):
    unique_days = sorted({t.date() for t in time_points})
    model.D = pyo.Set(initialize=unique_days, ordered=True, within=pyo.Any)
    model.mode = pyo.Var(model.D, domain=pyo.Binary)

    def market_mode_buy_rule(model, t):
        return model.buy_volume[t] <= model.buy_volume[t].ub * model.mode[t.date()]
    model.market_mode_buy_constraint = pyo.Constraint(model.T, rule=market_mode_buy_rule)
    
    def market_mode_sell_rule(model, t):
        return model.sell_volume[t] <= model.sell_volume[t].ub * model.mode[t.date()]
    model.market_mode_sell_constraint = pyo.Constraint(model.T, rule=market_mode_sell_rule)
    
    def prl_mode_rule(model, t):
        return model.prl_capacity[t] <= model.prl_capacity[t].ub * (1 - model.mode[t.date()])
    model.prl_mode_constraint = pyo.Constraint(model.T, rule=prl_mode_rule)










