from .charge_discharge import define_charge_discharge_expr
from .aging_cost import define_aging_cost_expr
from .revenue import define_revenue_expr
from .tax import define_tax_expr
from .additional_sums import define_additional_sums_expr
from .prl_mapping import prl_mapping_expr
from .srl_mapping import srl_mapping_expr

def define_all_expressions(model):
    prl_mapping_expr(model)
    srl_mapping_expr(model)
    define_charge_discharge_expr(model)
    define_aging_cost_expr(model)
    define_revenue_expr(model)
    define_tax_expr(model)
    define_additional_sums_expr(model)
