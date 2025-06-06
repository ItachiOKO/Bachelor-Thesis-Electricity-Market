import pyomo.environ as pyo


def add_market_choice_constraint(model, time_points):
    unique_intervals = sorted({(t.date(), t.hour // 4) for t in time_points})
    model.D4 = pyo.Set(initialize=unique_intervals, ordered=True)
    model.time_to_interval = {t: (t.date(), t.hour // 4) for t in time_points}


    model.v_MODE_DA_AUC = pyo.Var(model.T, domain=pyo.Binary) #alle 15 Minuten
    model.v_MODE_ID = pyo.Var(model.T, domain=pyo.Binary) #alle 15 Minuten
    model.v_MODE_PRL      = pyo.Var(model.D4, domain=pyo.Binary) # alle 4 Stunden
    model.v_MODE_SRL      = pyo.Var(model.D4, domain=pyo.Binary) # alle 4 Stunden

    def one_mode_per_t_rule(model, t):
        iv = model.time_to_interval[t]
        return (
            model.v_MODE_DA_AUC[t]
          + model.v_MODE_PRL[iv]
          + model.v_MODE_SRL[iv]
        ) <= 1
    #model.c_ONE_MODE_ONLY = pyo.Constraint(model.T, rule=one_mode_per_t_rule)

    def mode_sos_rule(m, t):
        iv = m.time_to_interval[t]
        return [
            m.v_MODE_DA_AUC[t],
            m.v_MODE_PRL[iv],
            m.v_MODE_SRL[iv],
        ]
    model.SOS_ONE_MODE = pyo.SOSConstraint(model.T,rule=mode_sos_rule,sos=1)


    _add_dayahead_mode_constraints(model)
    _add_prl_mode_constraints(model)
    _add_srl_mode_constraints(model)


def _add_dayahead_mode_constraints(model):
    def buy_ub_rule(m, t):
        return m.v_DA_AUC_BUY_VOL[t]  <= m.v_DA_AUC_BUY_VOL[t].ub  * m.v_MODE_DA_AUC[t]
    model.c_MODE_DA_BUY_UB  = pyo.Constraint(model.T, rule=buy_ub_rule)

    def sell_ub_rule(m, t):
        return m.v_DA_AUC_SELL_VOL[t] <= m.v_DA_AUC_SELL_VOL[t].ub * m.v_MODE_DA_AUC[t]
    model.c_MODE_DA_SELL_UB = pyo.Constraint(model.T, rule=sell_ub_rule)



    def da_sos1_rule(m, t):
        return [
            m.v_DA_AUC_BUY_VOL[t],
            m.v_DA_AUC_SELL_VOL[t],
        ]
    model.SOS_DA_BUY_SELL = pyo.SOSConstraint(
        model.T,
        rule=da_sos1_rule,
        sos=1    # Typ 1 ⇒ max. eine Variable ≠ 0
    )


def _add_prl_mode_constraints(model):
    def prl_ub_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_PRL_POWER[t] == model.v_PRL_POWER[t].ub * model.v_MODE_PRL[iv]
    model.c_MODE_PRL_POWER_UB = pyo.Constraint(model.T, rule=prl_ub_rule)

    def prl_lb_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_PRL_POWER[t] >= 1 * model.v_MODE_PRL[iv]
    #model.c_MODE_PRL_POWER_LB = pyo.Constraint(model.T, rule=prl_lb_rule)


def _add_srl_mode_constraints(model):
    def neg_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_SRL_POWER_NEG[t] <= model.v_SRL_POWER_NEG[t].ub * model.v_MODE_SRL[iv]
    model.c_MODE_SRL_POWER_NEG_UB = pyo.Constraint(model.T, rule=neg_rule)

    def pos_rule(model, t):
        iv = model.time_to_interval[t]
        return model.v_SRL_POWER_POS[t] <= model.v_SRL_POWER_POS[t].ub * model.v_MODE_SRL[iv]
    model.c_MODE_SRL_POWER_POS_UB = pyo.Constraint(model.T, rule=pos_rule)



