import pyomo.environ as pyo
from model_components import (
    set_data,
    define_variables,
    define_charge_discharge_expr,
    define_aging_cost_expr,
    define_profit_expr,
    define_tax_expression,
    add_constraints,
    define_objective
) 


def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    return solver.solve(model, tee=False)


def setup_model(time_points, da_auc_price_dict, id_price_dict, prl_price_dict, srl_power_price_neg_dict, srl_power_price_pos_dict, srl_work_price_neg_dict, srl_work_price_pos_dict, charge_rate):	
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)

    set_data(model, da_auc_price_dict, id_price_dict, prl_price_dict, srl_power_price_neg_dict, srl_power_price_pos_dict, srl_work_price_neg_dict, srl_work_price_pos_dict)
    define_variables(model, charge_rate)
    define_charge_discharge_expr(model)
    define_aging_cost_expr(model)
    define_profit_expr(model)
    define_tax_expression(model)
    add_constraints(model, time_points)
    define_objective(model)

    return model
