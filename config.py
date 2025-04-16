#Data Config
START_DATE = "2023-01-01" #included
END_DATE = "2023-02-01" #excluded
PATH_MARKET_DATA = "data\energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
PATH_PRL_DATA = "data\RESULT_OVERVIEW_CAPACITY_MARKET_FCR_2023-01-01_2023-12-31.xlsx"
SKIPROWS =2

#Battery Config
BATTERY_CAPACITY = 1 #MWh
SPECIFIC_CHARGE_RATE = 1 #MW (1MW = 1MWh/1h)
BATTERY_PRICE = 360000 * BATTERY_CAPACITY #€
LIFETIME_CYCLES = 9000
EFFICIENCY = 0.86 # einseitiger Wirkungsgrad (jeweils Lade- und Entladeverluste)
SPECIFIC_AGING_COST = BATTERY_PRICE / (BATTERY_CAPACITY * LIFETIME_CYCLES * 2) #€/(MWh*Cycle)

#PRL Config
SPECIFIC_PRL_ENERGY_NEED_4H_CYCLE = 1/3 # 1/3 -> MWh/MW


#Simulation Config
ENABLE_EXCHANGE_MARKET = 1 #0=Off, 1=On
ENABLE_PRL_MARKET = 1 #0=Off, 1=On 

#Export Config
RESULTS_FILE_NAME_EXCEL =  f"results_BC-EXCHANGE_MARKET_{ENABLE_EXCHANGE_MARKET}-PRL_MARKET_{ENABLE_PRL_MARKET}-{BATTERY_CAPACITY}MWH_SCR-{SPECIFIC_CHARGE_RATE}MW_P-{BATTERY_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.xlsx"
RESULTS_FILE_NAME_PICKLE = f"results_BC-EXCHANGE_MARKET_{ENABLE_EXCHANGE_MARKET}-PRL_MARKET_{ENABLE_PRL_MARKET}-{BATTERY_CAPACITY}MWH_SCR-{SPECIFIC_CHARGE_RATE}MW_P-{BATTERY_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.pkl"


#Table Config
CELL_NAMES = {
    'date': 'Date', #only date as date-obj
    'market_price': 'Market_price', #€/MWh
    'prl_price': 'GERMANY_SETTLEMENTCAPACITY_PRICE_[EUR/MW]', #€/MWh
    'buy_volume': 'Buy Volume', #MWh charging volume = buy_volume * EFFICIENCY
    'sell_volume': 'Sell Volume', #MWh discharging volume = sell_volume / EFFICIENCY
    'order_cost': 'Net order value', #€
    'battery_soc': 'Battery SOC', #MWh 
    'prl_capacity': 'PRL Power', #€
    'aging_cost': 'Aging Cost', #€
    'profit_calc': 'Profit' #€

}