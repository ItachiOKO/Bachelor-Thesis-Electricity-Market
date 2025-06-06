import pyomo.environ as pyo
from model.param import define_params
from model.variables import define_variables
from model.expressions import define_all_expressions
from model.constraints import add_all_constraints
from model.objective import define_objective



def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    return solver.solve(model, tee=False)


def setup_model(df_data_period):
    time_points = df_data_period.index.tolist()	
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)

    define_params(model, df_data_period)
    define_variables(model)
    define_all_expressions(model)
    add_all_constraints(model, time_points)
    define_objective(model)

    return model
