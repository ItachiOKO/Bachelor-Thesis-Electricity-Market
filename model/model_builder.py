import pyomo.environ as pyo
from model.param import define_params
from model.variables import define_variables
from model.expressions import define_all_expressions
from model.constraints import add_all_constraints
from model.objective import define_objective



def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    solver.options['Threads'] = 12
    solver.options['MIPGap'] = 0.005  # 1% Optimalitätslücke akzeptieren

    solver.options['TimeLimit'] = 10  # Zeitlimit (Sekunden)
    return solver.solve(model, tee=False)



def setup_model(df_data_period):
    time_points = df_data_period.index.tolist()	
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)
    unique_intervals = sorted({(t.date(), t.hour // 4) for t in time_points})
    model.D4 = pyo.Set(initialize=unique_intervals, ordered=True)
    model.time_to_interval = {t: (t.date(), t.hour // 4) for t in time_points}
    
    define_params(model, df_data_period)
    define_variables(model)
    define_all_expressions(model)
    add_all_constraints(model, time_points)
    define_objective(model)

    return model
