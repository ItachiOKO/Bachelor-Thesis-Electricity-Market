import pyomo.environ as pyo
from constraints_market_specific import add_electricity_exchange_constraints, add_prl_constraints, add_srl_constraints
from constraints_marketchoice import add_market_choice_constraint
from config import (
    EFFICIENCY,
    SPECIFIC_AGING_COST,
    SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE,
    SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE,
    SYSTEM_POWER
)
from config_cost import TAX_RATE
from cost_calculator import calculate_depreciation_amount


def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    return solver.solve(model, tee=False)


def setup_model(time_points, market_price_dict, prl_price_dict, srl_price_pos_dict, srl_price_neg_dict ,charge_rate):
    model = pyo.ConcreteModel()
    model.T = pyo.Set(initialize=time_points, ordered=True)

    _set_data(model, market_price_dict, prl_price_dict, srl_price_pos_dict, srl_price_neg_dict)
    _define_variables(model, charge_rate)
    _define_aging_costs(model)
    _define_profit_expressions(model)
    _define_tax_expression(model)
    _add_constraints(model, time_points)
    _define_objective(model)

    return model


def _set_data(model, market_price_dict, prl_price_dict, srl_price_pos_dict, srl_price_neg_dict):
    model.market_price = pyo.Param(model.T, initialize=market_price_dict)
    model.prl_price    = pyo.Param(model.T, initialize=prl_price_dict)
    model.srl_price_pos = pyo.Param(model.T, initialize=srl_price_pos_dict)
    model.srl_price_neg = pyo.Param(model.T, initialize=srl_price_neg_dict)


def _define_variables(model, charge_rate):
    model.buy_volume  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate))
    model.sell_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate * EFFICIENCY))
    model.battery_soc = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))
    model.prl_power   = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.srl_power_pos = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.srl_power_neg = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))

    model.tax_base  = pyo.Var(domain=pyo.NonNegativeReals)


def _define_aging_costs(model):
    def _aging_cost_expr(model, t):
        c_exc = SPECIFIC_AGING_COST * (model.buy_volume[t] * EFFICIENCY + model.sell_volume[t] / EFFICIENCY)
        c_prl = SPECIFIC_AGING_COST * SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE * model.prl_power[t]
        c_srl = SPECIFIC_AGING_COST * (SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE * (model.srl_power_pos[t] + model.srl_power_neg[t]))
        return c_exc + c_prl + c_srl

    model.aging_cost     = pyo.Expression(model.T, rule=_aging_cost_expr)
    model.aging_cost_sum = pyo.Expression(expr=sum(model.aging_cost[t] for t in model.T))


def _define_profit_expressions(model):
    model.revenue_day_ahead = pyo.Expression(
        expr = sum(
            model.sell_volume[t] * model.market_price[t]
          - model.buy_volume[t]  * model.market_price[t]
          for t in model.T
        )
    )
    model.revenue_prl = pyo.Expression(
        expr = sum(
            model.prl_price[t] * model.prl_power[t]
            for t in model.T
        )
    )

    model.revenue_srl = pyo.Expression(
        expr = sum(
            model.srl_power_pos[t] * model.srl_price_pos[t]
          + model.srl_power_neg[t] * model.srl_price_neg[t]
            for t in model.T
        )
    )
    
    model.total_revenue = pyo.Expression(
        expr = model.revenue_day_ahead + model.revenue_prl + model.revenue_srl
    )


def _define_tax_expression(model):
    model.Tax = pyo.Expression(expr = TAX_RATE * model.tax_base)


def _define_objective(model):
    def _profit_rule(model):
        return model.total_revenue - model.aging_cost_sum - model.Tax

    model.OBJ = pyo.Objective(rule=_profit_rule, sense=pyo.maximize)


def _add_constraints(model, time_points):
    add_market_choice_constraint(model, time_points)
    add_electricity_exchange_constraints(model)
    add_prl_constraints(model)
    add_srl_constraints(model)
    add_tax_constraints(model)


def add_tax_constraints(model):
    """ tax_base = max(0, profit - s) """
    s = calculate_depreciation_amount()
    revenue = model.total_revenue
    model.c1 = pyo.Constraint(expr = model.tax_base >= revenue - s)
    model.c2 = pyo.Constraint(expr = model.tax_base >= 0)