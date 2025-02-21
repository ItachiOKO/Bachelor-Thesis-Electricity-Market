import pyomo.environ as pyo
from load_marketprice_data import create_dataframe   
from config import BATTERY_CAPACITY, EFFICIENCY, BATTERY_PRICE, LIFETIME_CYCLES, END_OF_DAY_SOC


def solve_model(model):
    solver = pyo.SolverFactory('glpk') 
    result = solver.solve(model)
    return result

def setup_model(time_points, market_price_dict, prl_price_dict, charge_rate):
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)
    model.market_price = pyo.Param(model.T, initialize=market_price_dict)
    model.prl_price = pyo.Param(model.T, initialize=prl_price_dict)

    model.buy_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate/EFFICIENCY)) 
    model.sell_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate*EFFICIENCY))  
    model.battery_soc = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, BATTERY_CAPACITY))
    model.aging_cost = pyo.Var(model.T, within=pyo.NonNegativeReals)

    model.prl_capacity = pyo.Var(model.T, bounds=(-1, BATTERY_CAPACITY))

    #Constraints
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

    def prl_capacity_once_a_day_rule(model, t):
        current_date = t.date()
        daily_steps = [t_ for t_ in model.T if t_.date() == current_date]
        if t != min(daily_steps):
            return model.prl_capacity[t] == 0
        return pyo.Constraint.Skip
    model.prl_capacity_once_a_day_constraint = pyo.Constraint(model.T, rule=prl_capacity_once_a_day_rule)


    unique_days = sorted({t.date() for t in time_points})
    model.D = pyo.Set(initialize=unique_days, ordered=True)
    
    def day_init(model, t):
        return t.date()
    model.day = pyo.Param(model.T, initialize=day_init)
    
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
    
    def regulation_mode_rule(model, t):
        d = model.day[t]
        return model.prl_capacity[t] <= M_prl * (1 - model.mode[d])
    model.regulation_mode_constraint = pyo.Constraint(model.T, rule=regulation_mode_rule)
    
    #Objective
    def profit_rule(model):
        order_profit_sum = sum(
            model.sell_volume[t] * model.market_price[t] - model.buy_volume[t] * model.market_price[t] - model.aging_cost[t] 
            for t in model.T
        )
        prl_profit_sum = sum(
            model.prl_price[t] * model.prl_capacity[t]
            for t in model.T
        )
        return order_profit_sum + prl_profit_sum
    model.OBJ = pyo.Objective(rule=profit_rule, sense=pyo.maximize)

    return model






