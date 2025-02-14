from price_data import get_interval_minutes


BATTERY_CAPACITY = 1 #MWh
BATTERY_PRICE = 150000 #€
CYCLES = 5000
EFFICIENCY = 0.96 
SPECIFIC_CHARGE_RATE = 1 #MW
CHARGE_RATE = SPECIFIC_CHARGE_RATE * (get_interval_minutes()/60)
