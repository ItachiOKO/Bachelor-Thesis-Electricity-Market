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


def set_data(model, market_price_dict, prl_price_dict, srl_price_neg_dict, srl_price_pos_dict, srl_work_price_neg_dict, srl_work_price_pos_dict):
    model.p_DA_PRICE = pyo.Param(model.T, initialize=market_price_dict)
    model.p_PRLPRICE    = pyo.Param(model.T, initialize=prl_price_dict)
    model.p_SRL_PRICE_NEG = pyo.Param(model.T, initialize=srl_price_neg_dict)
    model.p_SRL_PRICE_POS = pyo.Param(model.T, initialize=srl_price_pos_dict)
    model.p_SRL_WORK_PRICE_NEG = pyo.Param(model.T, initialize=srl_work_price_neg_dict)
    model.p_SRL_WORK_PRICE_POS = pyo.Param(model.T, initialize=srl_work_price_pos_dict)


def define_variables(model, charge_rate):
    model.v_DA_AUC_BUY_VOL  = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate))
    model.v_DA_AUC_SELL_VOL = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, charge_rate * EFFICIENCY))
    model.v_BAT_SOC = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))
    model.v_PRL_POWER   = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_NEG = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))
    model.v_SRL_POWER_POS = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, SYSTEM_POWER))

    model.v_TAX_BASE  = pyo.Var(domain=pyo.NonNegativeReals)


def define_aging_costs(model):
    def _aging_cost_expr(model, t):
        c_exc = SPECIFIC_AGING_COST * (model.v_DA_AUC_BUY_VOL[t] * EFFICIENCY + model.v_DA_AUC_SELL_VOL[t] / EFFICIENCY)
        c_prl = SPECIFIC_AGING_COST * SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE * model.v_PRL_POWER[t]
        c_srl = SPECIFIC_AGING_COST * (SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE * (model.v_SRL_POWER_NEG[t] + model.v_SRL_POWER_POS[t]))
        return c_exc + c_prl + c_srl

    model.e_AGING_COST     = pyo.Expression(model.T, rule=_aging_cost_expr)
    model.e_AGING_COST_SUM = pyo.Expression(expr=sum(model.e_AGING_COST[t] for t in model.T))


def define_profit_expressions(model):
    model.e_REVENUE_DA_AUC = pyo.Expression(
        expr = sum(
            model.v_DA_AUC_SELL_VOL[t] * model.p_DA_PRICE[t]
          - model.v_DA_AUC_BUY_VOL[t]  * model.p_DA_PRICE[t]
          for t in model.T
        )
    )
    model.e_REVENUE_PRL = pyo.Expression(
        expr = sum(
            model.p_PRLPRICE[t] * model.v_PRL_POWER[t]
            for t in model.T
        )
    )

    model.e_REVENUE_SRL = pyo.Expression(
        expr = sum(
            model.v_SRL_POWER_NEG[t] * (model.p_SRL_PRICE_NEG[t] + -1*model.p_SRL_WORK_PRICE_NEG[t] * SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE)
          + model.v_SRL_POWER_POS[t] * (model.p_SRL_PRICE_POS[t] + model.p_SRL_WORK_PRICE_POS[t] * SPECIFIC_SRL_ENERGY_NEED_4H_CYCLE)

            for t in model.T
        )
    )
    
    model.e_TOTAL_REVEVNUE = pyo.Expression(
        expr = model.e_REVENUE_DA_AUC + model.e_REVENUE_PRL + model.e_REVENUE_SRL
    )


def define_tax_expression(model):
    model.e_TAX = pyo.Expression(expr = TAX_RATE * model.v_TAX_BASE)


def define_objective(model):
    def _profit_rule(model):
        return model.e_TOTAL_REVEVNUE - model.e_AGING_COST_SUM - model.e_TAX

    model.OBJ = pyo.Objective(rule=_profit_rule, sense=pyo.maximize)


def add_constraints(model, time_points):
    add_market_choice_constraint(model, time_points)
    add_electricity_exchange_constraints(model)
    add_prl_constraints(model)
    add_srl_constraints(model)
    add_tax_constraints(model)


def add_tax_constraints(model):
    """ tax_base = max(0, profit - s) """
    s = calculate_depreciation_amount()
    revenue = model.e_TOTAL_REVEVNUE
    model.c_TAX1 = pyo.Constraint(expr = model.v_TAX_BASE >= revenue - s)
    model.c_TAX2 = pyo.Constraint(expr = model.v_TAX_BASE >= 0)