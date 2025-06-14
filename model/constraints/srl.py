from config import SYSTEM_POWER, BAT_CAPACITY
import pyomo.environ as pyo

def add_srl_mode_constraints(model):
    model.v_SRL_POS_IND = pyo.Var(model.D4, domain=pyo.Binary)
    model.v_SRL_NEG_IND = pyo.Var(model.D4, domain=pyo.Binary)
    # 1) UB pro Richtung & Intervall
    def neg_ub_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_SRL_POWER_NEG[iv] <= SYSTEM_POWER * m.v_MODE_SRL[iv]
    model.c_SRL_PWR_NEG_UB_IV = pyo.Constraint(model.D4, rule=neg_ub_iv)

    def pos_ub_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_SRL_POWER_POS[iv] <= SYSTEM_POWER * m.v_MODE_SRL[iv]
    model.c_SRL_PWR_POS_UB_IV = pyo.Constraint(model.D4, rule=pos_ub_iv)

    # 2) Indicator-Link auf MODE_SRL
    def neg_ind_mode_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_SRL_NEG_IND[iv] <= m.v_MODE_SRL[iv]
    model.c_SRL_IND_NEG_MODE_IV = pyo.Constraint(model.D4, rule=neg_ind_mode_iv)

    def pos_ind_mode_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_SRL_POS_IND[iv] <= m.v_MODE_SRL[iv]
    model.c_SRL_IND_POS_MODE_IV = pyo.Constraint(model.D4, rule=pos_ind_mode_iv)

def add_srl_constraints(model):
    # 3) LB pro Richtung & Intervall
    def neg_lb_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_SRL_POWER_NEG[iv] >= 1 * m.v_SRL_NEG_IND[iv]
    model.c_SRL_PWR_NEG_LB_IV = pyo.Constraint(model.D4, rule=neg_lb_iv)

    def pos_lb_iv(m, date, quartal):
        iv = (date, quartal)
        return m.v_SRL_POWER_POS[iv] >= 1 * m.v_SRL_POS_IND[iv]
    model.c_SRL_PWR_POS_LB_IV = pyo.Constraint(model.D4, rule=pos_lb_iv)

    # 4) SOC-Puffer bleibt slot-weise
    def soc_pos_rule(m, t):
        return m.v_BAT_SOC[t] * BAT_CAPACITY >= m.e_SRL_POWER_POS[t]
    model.c_SRL_SOC_POS = pyo.Constraint(model.T, rule=soc_pos_rule)

    def soc_neg_rule(m, t):
        return (1 - m.v_BAT_SOC[t]) * BAT_CAPACITY >= m.e_SRL_POWER_NEG[t]
    model.c_SRL_SOC_NEG = pyo.Constraint(model.T, rule=soc_neg_rule)
