import pyomo.environ as pyo
import pandas as pd

from price_data import create_dataframe   
from config import BATTERY_CAPACITY, EFFICIENCY, BATTERY_PRICE, CYCLES, SPECIFIC_CHARGE_RATE, START_DATE, END_DATE
from utils import get_interval_minutes, calculate_period_in_days



df = create_dataframe(START_DATE, END_DATE)
CHARGE_RATE = SPECIFIC_CHARGE_RATE * (get_interval_minutes(df)/60)


time_points = df.index.tolist()
market_price_dict = df['market_price'].to_dict()


model = pyo.ConcreteModel()
model.T = pyo.Set(initialize=time_points)

model.market_price = pyo.Param(model.T, initialize=market_price_dict)
model.buy_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE/EFFICIENCY)) 
model.sell_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, CHARGE_RATE*EFFICIENCY))  
model.battery_soc = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, BATTERY_CAPACITY))
model.aging_cost = pyo.Var(model.T, within=pyo.NonNegativeReals)


def soc_rule(model, t):
    if t == min(model.T):
        return model.battery_soc[t] == model.buy_volume[t]*EFFICIENCY - model.sell_volume[t]/EFFICIENCY
    else:
        prev_t = model.T.prev(t)  
        return model.battery_soc[t] == model.battery_soc[prev_t] + model.buy_volume[t]*EFFICIENCY - model.sell_volume[t]/EFFICIENCY
model.battery_balance_constraint = pyo.Constraint(model.T, rule=soc_rule)


def aging_cost_rule(model, t):
    specific_aging_cost = BATTERY_PRICE / (BATTERY_CAPACITY * CYCLES) / 2
    return model.aging_cost[t] == specific_aging_cost * (model.buy_volume[t] * EFFICIENCY + model.sell_volume[t]/EFFICIENCY)
model.aging_cost_constraint = pyo.Constraint(model.T, rule=aging_cost_rule)


#Objective
def profit_rule(model):
    return sum(
        model.sell_volume[t] * model.market_price[t] - model.buy_volume[t] * model.market_price[t] - model.aging_cost[t] 
        for t in model.T
    )


model.OBJ = pyo.Objective(rule=profit_rule, sense=pyo.maximize)
solver = pyo.SolverFactory('glpk') 
result = solver.solve(model)


df["buy_volume"] = [pyo.value(model.buy_volume[t]) for t in model.T]
df["sell_volume"] = [pyo.value(model.sell_volume[t]) for t in model.T]
df["battery_soc"] = [pyo.value(model.battery_soc[t]) for t in model.T]
df["aging_cost"] = [pyo.value(model.aging_cost[t]) for t in model.T]

df["order_cost"] = -df["buy_volume"] * df["market_price"] + df["sell_volume"] * df["market_price"]
df["profit_calc"] = df["sell_volume"] * df["market_price"] - df["buy_volume"] * df["market_price"] - df["aging_cost"]


df.to_excel("optimisation_result.xlsx")
print(df)

n_cycles = df["buy_volume"].sum()/BATTERY_CAPACITY
total_profit_model = pyo.value(model.OBJ)
total_profit_calc = df["profit_calc"].sum()
profit_per_cycle = total_profit_model/n_cycles
print(f"{n_cycles}: Ladezyklen")
print(f"Order Profit: {df['order_cost'].sum()} €")
print(f"Gesamtprofit_model: {total_profit_model} €")
print(f"Profit pro Zyklus: {profit_per_cycle} €")
print(f"Profit pro Battery: {profit_per_cycle * CYCLES} €")


