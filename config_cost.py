# cost_config.py

## Einmalige Investitionskosten (CAPEX)
BASE_COST = 0
INVERTER_INVESTMENT = 0  # €/MW
TRANSFORMER_INVESTMENT = 0  # €/MW
CONSTRUCTION_ALLOWANCE = 50000  # €/MW, z.B. zwischen 50-100k€; Quelle Torsten Batterieinfos
GRID_CONNECTION_COST = 0  # €/MW

BATTERY_INVEST = 350000  # €/MWh; Quelle Torsten Batterieinfos


## Laufende Betriebskosten (OPEX, jährlich)
# Betriebskosten = 20-40K€ pro MW pro Jahr (alles zusammen); Quelle: Torsten Batteriespeicherinfos
INSURANCE = 0
TECHNICAL_MANAGEMENT = 0  
MAINTENANCE = 0 
REPAIRS = 0
MEASUREMENTS = 0
ACCOUNTING = 0 

TAXES = 0 # Abschreibungen unklar
