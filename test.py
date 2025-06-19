from pyomo.environ import *
from pyomo.gdp import *

model = ConcreteModel()

# Variablen mit Schranken (damit Big-M schätzbar ist)
model.x = Var(bounds=(0, 100))
model.y = Var(within=Binary)

# Disjunktive Teilbedingungen
model.disj = Disjunct()
model.disj.c = Constraint(expr=model.x <= 10)

model.no_disj = Disjunct()
# keine Einschränkung

# Disjunktion: Entweder disj oder no_disj aktiv
model.indicator = Disjunction(expr=[model.disj, model.no_disj])

# Binärverknüpfung (sauberer: nicht direkt auf indicator_var referenzieren)
model.link = Constraint(expr=model.y == model.disj.indicator_var.get_associated_binary())

# GDP zu MIP transformieren (entweder automatisch oder manuell mit M)
TransformationFactory('gdp.bigm').apply_to(model)

# Gurobi lösen
solver = SolverFactory('gurobi')
solver.solve(model, tee=True)
