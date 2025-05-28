import pyomo.environ as pyo


def define_objective(model):
    def profit_rule(model):
        return model.e_TOTAL_REVEVNUE - model.e_AGING_COST_SUM - model.e_TAX

    model.OBJ = pyo.Objective(rule=profit_rule, sense=pyo.maximize)




