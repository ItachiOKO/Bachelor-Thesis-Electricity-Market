import pyomo.environ as pyo
from constraints_model import add_electricity_exchange_constraints, add_market_choice_constraint
from config import (
    BATTERY_CAPACITY, EFFICIENCY, SPECIFIC_AGING_COST,
    SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE, ENABLE_EXCHANGE_MARKET,
    ENABLE_PRL_MARKET, SYSTEM_POWER
)

##### Steuern #####
tau = 0.20
S   = 10000
M   = 1e6


def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    result = solver.solve(model, tee=False)
    return result

def setup_model(time_points, market_price_dict, prl_price_dict, charge_rate):
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)
    # Daten
    model.market_price = pyo.Param(model.T, initialize=market_price_dict)
    model.prl_price    = pyo.Param(model.T, initialize=prl_price_dict)
    # Variablen
    model.buy_volume   = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate))
    model.sell_volume  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate*EFFICIENCY))
    model.battery_soc  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))
    model.prl_power    = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))



    # Aging‑Kosten
    def aging_cost_expr(m, t):
        c_exc = SPECIFIC_AGING_COST * (m.buy_volume[t]  * EFFICIENCY
                                     + m.sell_volume[t] / EFFICIENCY)
        c_prl = SPECIFIC_AGING_COST * SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE * m.prl_power[t]
        return c_exc + c_prl
    model.aging_cost = pyo.Expression(model.T, rule=aging_cost_expr)

    # technische Constraints
    add_electricity_exchange_constraints(model)
    add_market_choice_constraint(model, time_points)


#######Profitberrechnung ######

    # reine Profite
    model.exchange_profit = pyo.Expression(
        expr = sum(
            model.sell_volume[t] * model.market_price[t]
          - model.buy_volume[t]  * model.market_price[t]
          for t in model.T
        )
    )

    model.prl_profit = pyo.Expression(
        expr = sum(
            model.prl_price[t] * model.prl_power[t]
            for t in model.T
        )
    )


    # aging costs (exchange and prl)
    model.aging_cost_sum = pyo.Expression(
        expr = sum(model.aging_cost[t] for t in model.T)
    )

    # Operativer Cashflow C = P - A
    model.operative_cashflow = pyo.Expression(expr = model.exchange_profit + model.prl_profit - model.aging_cost_sum)


    # Steuerbasis Base = max(Profit - S, 0)
    model.Base  = pyo.Var(domain=pyo.NonNegativeReals)
    model.delta = pyo.Var(domain=pyo.Binary)
    model.b1 = pyo.Constraint(expr = model.Base >= model.exchange_profit + model.prl_profit - S)
    model.b2 = pyo.Constraint(expr = model.Base <= model.exchange_profit + model.prl_profit - S + M*(1-model.delta))
    model.b3 = pyo.Constraint(expr = model.Base <= M*model.delta)

    # Steuer Tax = tau * Base
    model.Tax = pyo.Var(domain=pyo.NonNegativeReals)
    model.t1  = pyo.Constraint(expr = model.Tax == tau * model.Base)

    # kombiniertes Objective
    def profit_rule(model):
        exchange_profit = model.exchange_profit
        prl_profit = model.prl_profit
        aging_cost_sum = model.aging_cost_sum
        taxes = model.Tax

        # operativer Gewinn minus Steuer + PRL-Ertrag
        return exchange_profit + prl_profit - aging_cost_sum - taxes

    # nur ein Objective-Objekt
    model.OBJ = pyo.Objective(rule=profit_rule, sense=pyo.maximize)

    return model


