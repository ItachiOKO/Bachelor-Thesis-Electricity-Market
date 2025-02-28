#Data Config
START_DATE = "2023-01-01" #included
END_DATE = "2024-01-01" #excluded
PATH_MARKET_DATA = "data\energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
PATH_PRL_DATA = "data\RESULT_OVERVIEW_CAPACITY_MARKET_FCR_2023-01-01_2023-12-31.xlsx"
SKIPROWS = 2

#Battery Config
BATTERY_CAPACITY = 5 #MWh
BATTERY_PRICE = 200000 * BATTERY_CAPACITY #€
LIFETIME_CYCLES = 5000
EFFICIENCY = 0.90 
SPECIFIC_CHARGE_RATE = 2.5 #MW
SPECIFIC_AGING_COST = BATTERY_PRICE / (BATTERY_CAPACITY * LIFETIME_CYCLES) #€/(MWh*Cycle)

#PRL Config
PRL_PRICE = 1000000 #€/MWh
PRL_CYCLES_PER_4h = 1/6

#Export Config
RESULTS_FILE_NAME_EXCEL =  f"results_BC-{BATTERY_CAPACITY}MWH_SCR-{SPECIFIC_CHARGE_RATE}MW_P-{BATTERY_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.xlsx"
RESULTS_FILE_NAME_PICKLE = f"results_BC-{BATTERY_CAPACITY}MWH_SCR-{SPECIFIC_CHARGE_RATE}MW_P-{BATTERY_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.pkl"


#Table Config
CELL_NAMES = {
    'date': 'Date', #only date as date-obj
    'market_price': 'Market_price', #€/MWh
    'prl_price': 'PRL Price', #€/MWh
    'buy_volume': 'Buy Volume', #MWh charging volume = buy_volume * EFFICIENCY
    'sell_volume': 'Sell Volume', #MWh discharging volume = sell_volume / EFFICIENCY
    'order_cost': 'Net order value', #€
    'battery_soc': 'Battery SOC', #MWh 
    'prl_capacity': 'PRL Capacity', #€
    'aging_cost': 'Aging Cost', #€
    'profit_calc': 'Profit' #€

}