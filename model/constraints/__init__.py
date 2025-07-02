from .marketchoice import add_market_choice_constraint
from .prl import add_prl_soc_constraints
from .srl import add_srl_soc_constraints
from .cumulative_soc import add_cumulative_soc_constraints
from .tax import add_tax_constraints


def add_all_constraints(model, time_points):
    add_market_choice_constraint(model, time_points)
    add_prl_soc_constraints(model)
    add_srl_soc_constraints(model)
    add_tax_constraints(model)
    add_cumulative_soc_constraints(model)

