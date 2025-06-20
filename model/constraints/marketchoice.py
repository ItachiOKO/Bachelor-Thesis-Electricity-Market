import pyomo.environ as pyo
from model.constraints.market import add_market_mode_constraints
from model.constraints.prl import add_prl_mode_constraints
from model.constraints.srl import add_srl_mode_constraints
from config import MARKET_SWITCH, PRL_SWITCH, SRL_SWITCH

def add_market_choice_constraint(model, time_points):


    
    model.v_MODE_MARKET = pyo.Var(model.T, domain=pyo.Binary) #alle 15 Minuten
    model.v_MODE_PRL      = pyo.Var(model.D4, domain=pyo.Binary) # alle 4 Stunden
    model.v_MODE_SRL      = pyo.Var(model.D4, domain=pyo.Binary) # alle 4 Stunden


    def prl_switch_rule(m, date, quartal):
        iv = (date, quartal)
        return m.v_MODE_PRL[iv] <= PRL_SWITCH
    model.c_PRL_SWITCH = pyo.Constraint(model.D4, rule=prl_switch_rule)

    def srl_switch_rule(m, date, quartal):
        iv = (date, quartal)
        return m.v_MODE_SRL[iv] <= SRL_SWITCH
    model.c_SRL_SWITCH = pyo.Constraint(model.D4, rule=srl_switch_rule)


    def mode_sos_rule(m, t):
        return m.v_MODE_MARKET[t] + m.v_MODE_PRL[m.time_to_interval[t]] + m.v_MODE_SRL[m.time_to_interval[t]] <= 1
    model.c_MODE_SOS = pyo.Constraint(model.T, rule=mode_sos_rule)


    add_market_mode_constraints(model)
    add_prl_mode_constraints(model)
    add_srl_mode_constraints(model)


