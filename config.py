#Data Config
START_DATE = "2023-01-01" #included
END_DATE = "2024-01-01" #excluded
CSV_PATH = "energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2023.csv"
#STEP_INTERVAL = "15min"
SKIPROWS = 2

#Battery Config
BATTERY_CAPACITY = 1 #MWh
BATTERY_PRICE = 200000 * BATTERY_CAPACITY #€
LIFETIME_CYCLES = 5000
EFFICIENCY = 0.85 
SPECIFIC_CHARGE_RATE = 1 #MW

#Export Config
RESULTS_FILE_NAME_EXCEL =  f"results_BC-{BATTERY_CAPACITY}MWH_SCR-{SPECIFIC_CHARGE_RATE}MW_P-{BATTERY_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.xlsx"
RESULTS_FILE_NAME_PICKLE = f"results_BC-{BATTERY_CAPACITY}MWH_SCR-{SPECIFIC_CHARGE_RATE}MW_P-{BATTERY_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}.pkl"


#Table Config
CELL_NAMES = {
    'date': 'Date', #only date as date-obj
    'time': 'Time', #only time as string
    'market_price': 'Market_price', #€/MWh
    'buy_volume': 'Buy Volume', #MWh charging volume = buy_volume * EFFICIENCY
    'sell_volume': 'Sell Volume', #MWh discharging volume = sell_volume / EFFICIENCY
    'battery_soc': 'Battery SOC', #MWh 
    'aging_cost': 'Aging Cost', #€
    'order_cost': 'Order Cost', #€
    'profit_calc': 'Profit Calculation' #€

}