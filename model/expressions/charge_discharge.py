import pyomo.environ as pyo
from config import (
    EFFICIENCY,
)

def define_charge_discharge_expr(model):
    model.e_DA_AUC_CHARGE = pyo.Expression(
        model.T,
        rule=lambda model, t: model.v_DA_AUC_BUY_VOL[t] * EFFICIENCY
    )

    model.e_DA_AUC_DISCHARGE = pyo.Expression(
        model.T,    
        rule=lambda model, t: model.v_DA_AUC_SELL_VOL[t] / EFFICIENCY
    )

    model.e_ID_CHARGE = pyo.Expression(
        model.T,
        rule=lambda model, t: model.v_ID_BUY_VOL[t] * EFFICIENCY
    )

    model.e_ID_DISCHARGE = pyo.Expression(
        model.T,
        rule=lambda model, t: model.v_ID_SELL_VOL[t] / EFFICIENCY
    )
    
    model.e_CHARGE = pyo.Expression(
        model.T,
        rule=lambda model, t: model.e_DA_AUC_CHARGE[t] + model.e_ID_CHARGE[t]
    )

    model.e_DISCHARGE = pyo.Expression(
        model.T,
        rule=lambda model, t: model.e_DA_AUC_DISCHARGE[t] + model.e_ID_DISCHARGE[t]
    )
