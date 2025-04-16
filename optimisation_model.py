import pyomo.environ as pyo
from constraints_model import add_electricity_exchange_constraints, add_market_choice_constraint
from config import BATTERY_CAPACITY, EFFICIENCY, SPECIFIC_AGING_COST, SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE, ENABLE_EXCHANGE_MARKET, ENABLE_PRL_MARKET, SPECIFIC_CHARGE_RATE


def solve_model(model):
    solver = pyo.SolverFactory('glpk') 
    result = solver.solve(model, tee=False)
    return result

def setup_model(time_points, market_price_dict, prl_price_dict, charge_rate):
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)
    #data
    model.market_price = pyo.Param(model.T, initialize=market_price_dict)
    model.prl_price = pyo.Param(model.T, initialize=prl_price_dict)
    #orders
    model.buy_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate)) #Fehler? übersteigt doch leistung der Batterie bzw Umrichter
    model.sell_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate*EFFICIENCY)) 

    model.battery_soc = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))
    model.prl_power = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SPECIFIC_CHARGE_RATE))


    def aging_cost_expr(model, t):
        aging_cost_exchange = SPECIFIC_AGING_COST * (model.buy_volume[t] * EFFICIENCY + model.sell_volume[t] / EFFICIENCY)
        aging_cost_prl = SPECIFIC_AGING_COST * SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE * model.prl_power[t]
        return aging_cost_exchange + aging_cost_prl
    model.aging_cost = pyo.Expression(model.T, rule=aging_cost_expr)

    add_electricity_exchange_constraints(model) 
    add_market_choice_constraint(model, time_points)

    #Objective
    def profit_rule(model):
        order_profit_sum = sum(
            model.sell_volume[t] * model.market_price[t] - model.buy_volume[t] * model.market_price[t] - model.aging_cost[t] 
            for t in model.T
        )
        prl_profit_sum = sum(
            model.prl_price[t] * model.prl_power[t]
            for t in model.T
        )
        return ENABLE_EXCHANGE_MARKET * order_profit_sum + ENABLE_PRL_MARKET * prl_profit_sum
    model.OBJ = pyo.Objective(rule=profit_rule, sense=pyo.maximize)
    return model






