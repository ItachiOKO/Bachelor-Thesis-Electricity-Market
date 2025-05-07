import pyomo.environ as pyo
from constraints_model import add_electricity_exchange_constraints, add_market_choice_constraint, add_tax_constraints
from config import (
    BATTERY_CAPACITY,
    EFFICIENCY,
    SPECIFIC_AGING_COST,
    SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE,
    SYSTEM_POWER
)
from config_cost import TAX_RATE


def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    return solver.solve(model, tee=False)


def setup_model(time_points, market_price_dict, prl_price_dict, charge_rate):
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)

    _set_data(model, market_price_dict, prl_price_dict)
    _define_variables(model, charge_rate)
    _define_aging_costs(model)
    _define_profit_expressions(model)
    _define_tax_expression(model)
    _add_constraints(model, time_points)
    _define_objective(model)

    return model


def _set_data(model, market_price_dict, prl_price_dict):
    model.market_price = pyo.Param(model.T, initialize=market_price_dict)
    model.prl_price    = pyo.Param(model.T, initialize=prl_price_dict)


def _define_variables(model, charge_rate):
    model.buy_volume  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate))
    model.sell_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate * EFFICIENCY))
    model.battery_soc = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))
    model.prl_power   = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))

    model.tax_base  = pyo.Var(domain=pyo.NonNegativeReals)


def _define_aging_costs(model):
    def _aging_cost_expr(m, t):
        c_exc = SPECIFIC_AGING_COST * (m.buy_volume[t] * EFFICIENCY + m.sell_volume[t] / EFFICIENCY)
        c_prl = SPECIFIC_AGING_COST * SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE * m.prl_power[t]
        return c_exc + c_prl

    model.aging_cost     = pyo.Expression(model.T, rule=_aging_cost_expr)
    model.aging_cost_sum = pyo.Expression(expr=sum(model.aging_cost[t] for t in model.T))


def _define_profit_expressions(model):
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

def _define_tax_expression(model):
    model.Tax = pyo.Expression(expr = TAX_RATE * model.tax_base)


def _define_objective(model):
    def _profit_rule(model):
        return model.exchange_profit + model.prl_profit - model.aging_cost_sum - model.Tax

    model.OBJ = pyo.Objective(rule=_profit_rule, sense=pyo.maximize)


def _add_constraints(model, time_points):
    add_electricity_exchange_constraints(model)
    add_market_choice_constraint(model, time_points)
    add_tax_constraints(model)
