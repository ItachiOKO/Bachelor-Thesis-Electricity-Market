import pyomo.environ as pyo
from config import BATTERY_CAPACITY, SYSTEM_POWER


def add_market_choice_constraint(model, time_points):
    unique_intervals = sorted({(t.date(), t.hour // 4) for t in time_points})
    model.D4 = pyo.Set(initialize=unique_intervals, ordered=True)

    model.mode_dayahead = pyo.Var(model.D4, domain=pyo.Binary)
    model.mode_prl      = pyo.Var(model.D4, domain=pyo.Binary)
    model.mode_srl      = pyo.Var(model.D4, domain=pyo.Binary)

    def one_mode_per_interval_rule(model, date, interval):
        return (
          model.mode_dayahead[date, interval]
        + model.mode_prl[date, interval]
        + model.mode_srl[date, interval]
        == 1
        )
    model.one_mode = pyo.Constraint(model.D4, rule=one_mode_per_interval_rule)


    model.time_to_interval = {t: (t.date(), t.hour // 4) for t in time_points}

    _add_dayahead_mode_constraints(model)
    _add_prl_mode_constraints(model)
    _add_srl_mode_constraints(model)


def _add_dayahead_mode_constraints(model):
    def buy_rule(model, t):
        iv = model.time_to_interval[t]
        return model.buy_volume[t] <= model.buy_volume[t].ub * model.mode_dayahead[iv]
    model.dayahead_buy = pyo.Constraint(model.T, rule=buy_rule)

    def sell_rule(model, t):
        iv = model.time_to_interval[t]
        return model.sell_volume[t] <= model.sell_volume[t].ub * model.mode_dayahead[iv]
    model.dayahead_sell = pyo.Constraint(model.T, rule=sell_rule)


def _add_prl_mode_constraints(model):
    def prl_rule(model, t):
        iv = model.time_to_interval[t]
        return model.prl_power[t] <= model.prl_power[t].ub * model.mode_prl[iv]
    model.prl_power_constraint = pyo.Constraint(model.T, rule=prl_rule)


def _add_srl_mode_constraints(model):
    def pos_rule(model, t):
        iv = model.time_to_interval[t]
        return model.srl_power_pos[t] <= model.srl_power_pos[t].ub * model.mode_srl[iv]
    model.srl_power_pos_constraint = pyo.Constraint(model.T, rule=pos_rule)

    def neg_rule(model, t):
        iv = model.time_to_interval[t]
        return model.srl_power_neg[t] <= model.srl_power_neg[t].ub * model.mode_srl[iv]
    model.srl_power_neg_constraint = pyo.Constraint(model.T, rule=neg_rule)

