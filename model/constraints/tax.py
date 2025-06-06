import pyomo.environ as pyo
from cost_calculator import calculate_depreciation_amount

def add_tax_constraints(model):
    """ tax_base = max(0, profit - s) """
    s = calculate_depreciation_amount()
    revenue = model.e_TOTAL_REVENUE_SUM
    model.c_TAX1 = pyo.Constraint(expr = model.v_TAX_BASE >= revenue - s)
    model.c_TAX2 = pyo.Constraint(expr = model.v_TAX_BASE >= 0)