import pyomo.environ as pyo


def prl_mapping_expr(model):
    def prl_power_maping_rule(m, t):
        iv = m.time_to_interval[t]
        return m.v_PRL_POWER[iv]
    model.e_PRL_POWER = pyo.Expression(model.T, rule=prl_power_maping_rule)