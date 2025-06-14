import pyomo.environ as pyo

def define_additional_sums_expr(model):
    def prl_power_sum_rule(m):
        return sum(m.e_PRL_POWER[t] for t in m.T)
    model.e_PRL_POWER_SUM = pyo.Expression(rule=prl_power_sum_rule)

    def srl_power_pos_sum_rule(m):
        return sum(m.e_SRL_POWER_POS[t] for t in m.T)

    def srl_power_neg_sum_rule(m):
        return sum(m.e_SRL_POWER_NEG[t] for t in m.T)

    model.e_SRL_POWER_POS_SUM = pyo.Expression(rule=srl_power_pos_sum_rule)
    model.e_SRL_POWER_NEG_SUM = pyo.Expression(rule=srl_power_neg_sum_rule)