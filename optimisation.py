import pyomo.environ as pyo

##Model
model = pyo.ConcreteModel()

##Variablen

##Constraints


##Objective Rule
sell_invest = sell_volume * market_price[t]
buy_invest = buy_volume * market_price[t]

profit = sum(sell_invest) - sum(buy_invest) = sum(profit)

def objective_rule(model):
    return sum(
        profit
    )
model.OBJ = pyo.Objective(rule=objective_rule, sense=pyo.maximize)


