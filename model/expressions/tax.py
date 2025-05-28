import pyomo.environ as pyo
from config_cost import (
    TAX_RATE,
)


def define_tax_expression(model):
    model.e_TAX = pyo.Expression(expr = TAX_RATE * model.v_TAX_BASE)