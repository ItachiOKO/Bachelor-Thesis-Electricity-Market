import pyomo.environ as pyo
from config import BAT_CAPACITY, SYSTEM_POWER


def add_srl_constraints(model):

    model.v_SRL_POS_IND = pyo.Var(model.T, domain=pyo.Binary)
    model.v_SRL_NEG_IND = pyo.Var(model.T, domain=pyo.Binary)

    def max_srl_power_rule(m, t):
        return m.v_SRL_POWER_POS[t] + m.v_SRL_POWER_NEG[t] <= SYSTEM_POWER
    model.c_MAX_SRL_POWER = pyo.Constraint(model.T, rule=max_srl_power_rule)


    def soc_pos_rule(m, t):
        return m.v_BAT_SOC[t] * BAT_CAPACITY >= m.v_SRL_POWER_POS[t]
    model.c_SRL_POWER_POS = pyo.Constraint(model.T, rule=soc_pos_rule)

    def soc_neg_rule(m, t):
        return (1 - m.v_BAT_SOC[t]) * BAT_CAPACITY >= m.v_SRL_POWER_NEG[t]
    model.c_SRL_POWER_NEG = pyo.Constraint(model.T, rule=soc_neg_rule)


    def ind_pos_mode_rule(m, t):
        iv = m.time_to_interval[t]
        return m.v_SRL_POS_IND[t] <= m.v_MODE_SRL[iv]
    model.c_IND_POS_MODE = pyo.Constraint(model.T, rule=ind_pos_mode_rule)

    def ind_neg_mode_rule(m, t):
        iv = m.time_to_interval[t]
        return m.v_SRL_NEG_IND[t] <= m.v_MODE_SRL[iv]
    model.c_IND_NEG_MODE = pyo.Constraint(model.T, rule=ind_neg_mode_rule)

    # 5) Fluss = 0 wenn Indikator=0; ≥1 wenn Indikator=1
    def pos_lb_rule(m, t):
        return m.v_SRL_POWER_POS[t] >= 1 * m.v_SRL_POS_IND[t]
    model.c_POS_LB = pyo.Constraint(model.T, rule=pos_lb_rule)

    def pos_ub_rule(m, t):
        return m.v_SRL_POWER_POS[t] <= m.v_SRL_POS_IND[t] * SYSTEM_POWER
    model.c_POS_UB = pyo.Constraint(model.T, rule=pos_ub_rule)

    def neg_lb_rule(m, t):
        return m.v_SRL_POWER_NEG[t] >= 1 * m.v_SRL_NEG_IND[t]
    model.c_NEG_LB = pyo.Constraint(model.T, rule=neg_lb_rule)

    def neg_ub_rule(m, t):
        return m.v_SRL_POWER_NEG[t] <= m.v_SRL_NEG_IND[t] * SYSTEM_POWER
    model.c_NEG_UB = pyo.Constraint(model.T, rule=neg_ub_rule)
