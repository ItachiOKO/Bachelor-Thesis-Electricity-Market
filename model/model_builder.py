import pyomo.environ as pyo
from model.param import define_params
from model.variables import define_variables
from model.expressions import define_all_expressions
from model.constraints import add_all_constraints
from model.objective import define_objective



def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    return solver.solve(model, tee=False)


def setup_model(time_points, higher_market_price_dict, lower_market_price_dict, prl_price_dict, srl_power_price_neg_dict, srl_power_price_pos_dict, srl_work_price_neg_dict, srl_work_price_pos_dict, charge_rate):	
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)

    define_params(model, higher_market_price_dict, lower_market_price_dict, prl_price_dict, srl_power_price_neg_dict, srl_power_price_pos_dict, srl_work_price_neg_dict, srl_work_price_pos_dict)
    define_variables(model, charge_rate)
    define_all_expressions(model)
    add_all_constraints(model, time_points)
    define_objective(model)

    return model
