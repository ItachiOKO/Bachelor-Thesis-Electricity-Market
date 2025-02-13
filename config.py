from price_data import get_interval_time

BATTERY_CAPACITY = 2 #MWh
EFFICIENCY = 0.96 
SPECIFIC_CHARGE_RATE = 1 #MW
CHARGE_RATE = SPECIFIC_CHARGE_RATE * (get_interval_time()/60)
