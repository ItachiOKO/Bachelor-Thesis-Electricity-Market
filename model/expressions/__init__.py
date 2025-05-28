from .charge_discharge import define_charge_discharge_expr
from .aging_cost import define_aging_cost_expr
from .revenue import define_revenue_expr
from .tax import define_tax_expression

def define_all_expressions(model):
    define_charge_discharge_expr(model)
    define_aging_cost_expr(model)
    define_revenue_expr(model)
    define_tax_expression(model)
