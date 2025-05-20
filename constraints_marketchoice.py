import pyomo.environ as pyo


def add_market_choice_constraint(model, time_points):
    unique_intervals = sorted({(t.date(), t.hour // 4) for t in time_points})
    model.D4 = pyo.Set(initialize=unique_intervals, ordered=True)

    model.v_MODE_DA_AUC = pyo.Var(model.D4, domain=pyo.Binary)
    model.v_MODE_PRL      = pyo.Var(model.D4, domain=pyo.Binary)
    model.v_MODE_SRL      = pyo.Var(model.D4, domain=pyo.Binary)

    def one_mode_per_interval_rule(model, date, interval):
        return (
          model.v_MODE_DA_AUC[date, interval]
        + model.v_MODE_PRL[date, interval]
        + model.v_MODE_SRL[date, interval]
        == 1
        )
    model.c_ONE_MODE_ONLY = pyo.Constraint(model.D4, rule=one_mode_per_interval_rule)


    model.time_to_interval = {t: (t.date(), t.hour // 4) for t in time_points}

    _add_dayahead_mode_constraints(model)
    _add_prl_mode_constraints(model)
    _add_srl_mode_constraints(model)


def _add_dayahead_mode_constraints(model):
    def buy_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_DA_AUC_BUY_VOL[t] <= model.v_DA_AUC_BUY_VOL[t].ub * model.v_MODE_DA_AUC[iv]
    model.c_MODE_DA_BUY = pyo.Constraint(model.T, rule=buy_rule)

    def sell_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_DA_AUC_SELL_VOL[t] <= model.v_DA_AUC_SELL_VOL[t].ub * model.v_MODE_DA_AUC[iv]
    model.c_MODE_DA_SELL = pyo.Constraint(model.T, rule=sell_rule)


def _add_prl_mode_constraints(model):
    def prl_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_PRL_POWER[t] <= model.v_PRL_POWER[t].ub * model.v_MODE_PRL[iv]
    model.c_MODE_PRL_POWER = pyo.Constraint(model.T, rule=prl_rule)


def _add_srl_mode_constraints(model):
    def neg_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_SRL_POWER_NEG[t] <= model.v_SRL_POWER_NEG[t].ub * model.v_MODE_SRL[iv]
    model.c_MODE_SRL_POWER_NEG = pyo.Constraint(model.T, rule=neg_rule)

    def pos_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_SRL_POWER_POS[t] <= model.v_SRL_POWER_POS[t].ub * model.v_MODE_SRL[iv]
    model.c_MODE_SRL_POWER_POS = pyo.Constraint(model.T, rule=pos_rule)


