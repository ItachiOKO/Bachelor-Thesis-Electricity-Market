# cost_config.py

## Einmalige Investitionskosten (CAPEX)
SPECIFIC_BATTERY_INVEST = 180000  # €/MWh; (2MWh/MW)Quelle Torsten Batterieinfos
SPECIFIC_INVERTER_INVEST = 20000  # €/MW
SPECIFIC_TRANSFORMER_INVEST = 25000  # €/MW
SPECIFIC_CONSTRUCTION_ALLOWANCE_INVEST = 50000  # €/MW, z.B. zwischen 50-100k€; Quelle Torsten Batterieinfos
SPECIFIC_GRID_CONNECTION_INVEST = 5000  # €/MW

## Laufende Betriebskosten (OPEX, jährlich)
# Betriebskosten = 20-40K€ pro MW pro Jahr (alles zusammen); Quelle: Torsten Batteriespeicherinfos
INSURANCE_PERCENTAGE = 0.01  # % der Investitionskosten (abzüglich CONSTRUCTION_ALLOWANCE_INVEST)
SPECIFIC_TECHNICAL_MANAGEMENT_COST = 3000 # €/MW pro Jahr
SPECIFIC_MAINTENANCE_COST = 3000  # €/MW pro Jahr
SPECIFIC_REPAIRS_COST = 3000 # €/MW pro Jahr
SPECIFIC_MEASUREMENTS_COST = 3000 # €/MW pro Jahr
ACCOUNTING_COST = 3000 # € pro Jahr

## Taxes
TAXES = 0.20 #Steuersatz
DEPRECIATION_YEARS = 10 #Abschreibungsdauer in Jahren