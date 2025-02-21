import pyomo.environ as pyo
from load_marketprice_data import create_dataframe   
from config import BATTERY_CAPACITY, EFFICIENCY, BATTERY_PRICE, LIFETIME_CYCLES, END_OF_DAY_SOC


def solve_model(model):
    solver = pyo.SolverFactory('glpk') 
    result = solver.solve(model)
    return result

def setup_model(time_points, market_price_dict, charge_rate):
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points)
    model.market_price = pyo.Param(model.T, initialize=market_price_dict)
    model.buy_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate/EFFICIENCY)) 
    model.sell_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate*EFFICIENCY))  
    model.battery_soc = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, BATTERY_CAPACITY))
    model.aging_cost = pyo.Var(model.T, within=pyo.NonNegativeReals)

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

    #Objective
    def profit_rule(model):
        return sum(
            model.sell_volume[t] * model.market_price[t] - model.buy_volume[t] * model.market_price[t] - model.aging_cost[t] 
            for t in model.T
        )
    model.OBJ = pyo.Objective(rule=profit_rule, sense=pyo.maximize)

    return model






