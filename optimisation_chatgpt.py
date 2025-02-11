import pyomo.environ as pyo
import pandas as pd

data = {'date': pd.date_range(start='2023-01-01', periods=24, freq='H'),
        'market_price': [10, 20, 40, 20, 20, 25, 20, 15, 10, 15, 20, 35, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 20, 85]}
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
time_points = df['date'].tolist()


model = pyo.ConcreteModel()
model.T = pyo.Set(initialize=time_points)

market_price_dict = df.set_index('date')['market_price'].to_dict()
model.market_price = pyo.Param(model.T, initialize=market_price_dict, within=pyo.NonNegativeReals)

model.buy_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))  # Kauf max. 1 MWh
model.sell_volume = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))  # Verkauf max. 1 MWh
model.battery_soc = pyo.Var(model.T, within=pyo.NonNegativeReals, bounds=(0, 1))  # Batteriekapazität max. 1 MWh

def initial_battery_rule(model):
    first_t = min(model.T)
    return model.battery_soc[first_t] == 0
model.initial_battery_constraint = pyo.Constraint(rule=initial_battery_rule)

# Ladezustand der Batterie: SoC(t) = SoC(t-1) + buy_volume(t) - sell_volume(t)
def battery_balance_rule(model, t):
    if t == min(model.T):  # Für den ersten Zeitschritt ist die Batterie bereits definiert
        return pyo.Constraint.Skip
    prev_t = model.T.prev(t)  # Vorheriger Zeitschritt
    return model.battery_soc[t] == model.battery_soc[prev_t] + model.buy_volume[t] - model.sell_volume[t]
model.battery_balance_constraint = pyo.Constraint(model.T, rule=battery_balance_rule)


def profit_rule(model):
    return sum(
        model.sell_volume[t] * model.market_price[t] - model.buy_volume[t] * model.market_price[t]
        for t in model.T
    )
model.OBJ = pyo.Objective(rule=profit_rule, sense=pyo.maximize)

solver = pyo.SolverFactory('glpk') 
result = solver.solve(model)

for t in model.T:
    print(f"Zeitpunkt {t}: Gekauft = {pyo.value(model.buy_volume[t])} MWh, "
          f"Verkauft = {pyo.value(model.sell_volume[t])} MWh, "
          f"Preis = {pyo.value(model.market_price[t])} €/MWh")

print(f"Gesamtprofit: {pyo.value(model.OBJ)} €")
