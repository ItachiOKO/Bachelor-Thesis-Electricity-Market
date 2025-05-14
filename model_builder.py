import pyomo.environ as pyo
from model_components import (
    set_data,
    define_variables,
    define_aging_costs,
    define_profit_expressions,
    define_tax_expression,
    add_constraints,
    define_objective
) 


def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    return solver.solve(model, tee=False)


def setup_model(time_points, market_price_dict, prl_price_dict, srl_price_pos_dict, srl_price_neg_dict ,charge_rate):
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)

    set_data(model, market_price_dict, prl_price_dict, srl_price_pos_dict, srl_price_neg_dict)
    define_variables(model, charge_rate)
    define_aging_costs(model)
    define_profit_expressions(model)
    define_tax_expression(model)
    add_constraints(model, time_points)
    define_objective(model)

    return model
