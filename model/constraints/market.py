import pyomo.environ as pyo

def add_market_mode_constraints(model):
    model.v_BUY_IND  = pyo.Var(model.T, domain=pyo.Binary)
    model.v_SELL_IND = pyo.Var(model.T, domain=pyo.Binary)

    def buy_ub_rule(m, t):
        return m.v_BUY_VOL[t]  <= m.v_BUY_VOL[t].ub  * m.v_BUY_IND[t]
    model.c_MODE_DA_BUY_UB  = pyo.Constraint(model.T, rule=buy_ub_rule)

    def sell_ub_rule(m, t):
        return m.v_SELL_VOL[t] <= m.v_SELL_VOL[t].ub * m.v_SELL_IND[t]
    model.c_MODE_DA_SELL_UB = pyo.Constraint(model.T, rule=sell_ub_rule)


    def buysell_excl_rule(m, t):
        return m.v_BUY_IND[t] + m.v_SELL_IND[t] <= model.v_MODE_MARKET[t]
    model.c_BUYSELL_EXCL = pyo.Constraint(model.T, rule=buysell_excl_rule)

    def buy_lb_rule(m, t):
        return m.v_BUY_VOL[t] >= 0.25 * m.v_BUY_IND[t]
    model.c_BUY_VOL_LB = pyo.Constraint(model.T, rule=buy_lb_rule)

    def sell_lb_rule(m, t):
        return m.v_SELL_VOL[t] >= 0.25 * m.v_SELL_IND[t]
    model.c_SELL_VOL_LB = pyo.Constraint(model.T, rule=sell_lb_rule)
