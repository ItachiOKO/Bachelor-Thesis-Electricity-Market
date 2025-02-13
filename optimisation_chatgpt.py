import pyomo.environ as pyo
import pandas as pd

from price_data import get_market_price_data   
from config import CHARGE_RATE, BATTERY_CAPACITY


df = get_market_price_data()

time_points = df['date'].tolist()
market_price_dict = df.set_index('date')['market_price'].to_dict()

model = pyo.ConcreteModel()
model.T = pyo.Set(initialize=time_points)
model.market_price = pyo.Param(model.T, initialize=market_price_dict, within=pyo.NonNegativeReals)
model.buy_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE)) 
model.sell_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE))  
model.battery_soc = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, BATTERY_CAPACITY))


def battery_balance_rule(model, t):
    if t == min(model.T):
        return model.battery_soc[t] == model.buy_volume[t] - model.sell_volume[t]
    else:
        prev_t = model.T.prev(t)  
        return model.battery_soc[t] == model.battery_soc[prev_t] + model.buy_volume[t] - model.sell_volume[t]
model.battery_balance_constraint = pyo.Constraint(model.T, rule=battery_balance_rule)

def charge_rule(model, t):
    return model.buy_volume[t] <= CHARGE_RATE
model.charge_constraint = pyo.Constraint(model.T, rule=charge_rule)

def profit_rule(model):
    return sum(
        model.sell_volume[t] * model.market_price[t] - model.buy_volume[t] * model.market_price[t]
        for t in model.T
    )
model.OBJ = pyo.Objective(rule=profit_rule, sense=pyo.maximize)
solver = pyo.SolverFactory('glpk') 
result = solver.solve(model)




df["buy_volume"] = [pyo.value(model.buy_volume[t]) for t in model.T]
df["sell_volume"] = [pyo.value(model.sell_volume[t]) for t in model.T]
df["battery_soc"] = [pyo.value(model.battery_soc[t]) for t in model.T]
df["buy_invest"] = df["buy_volume"] * df["market_price"]
df["sell_invest"] = df["sell_volume"] * df["market_price"]
df["profit"] = df["sell_invest"] - df["buy_invest"]

df['date'] = df['date'].dt.tz_localize(None)
df.to_excel("optimisation_result.xlsx")


print(df)
print(f"{df["buy_volume"].sum()/BATTERY_CAPACITY}: Ladezyklen")
print(f"Gesamtprofit: {pyo.value(model.OBJ)} €")
