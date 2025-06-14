import pyomo.environ as pyo

def srl_mapping_expr(model):
    def pos_map(m, t):
        iv = m.time_to_interval[t]
        return m.v_SRL_POWER_POS[iv]
    def neg_map(m, t):
        iv = m.time_to_interval[t]
        return m.v_SRL_POWER_NEG[iv]
    model.e_SRL_POWER_POS = pyo.Expression(model.T, rule=pos_map)
    model.e_SRL_POWER_NEG = pyo.Expression(model.T, rule=neg_map)
